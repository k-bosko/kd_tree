# Implementation code from:
# https://scipy-cookbook.readthedocs.io/items/KDTree_example.html

import numpy as np

from .converter import BaseConverter

class KDTree:
    def __init__(self):
        self.kdtree = None

    def build_kdtree(self, data):
        self.kdtree = self._build_kdtree(data)

    def _build_kdtree(self, data, leafsize=2048):
        ndim = data.shape[0]
        ndata = data.shape[1]

        hrect = np.zeros((2, data.shape[0]))
        hrect[0,:] = data.min(axis=1)
        hrect[1,:] = data.max(axis=1)

        # create root of kd-tree
        idx = np.argsort(data[0,:], kind='mergesort')
        data[:,:] = data[:,idx]
        splitval = data[0,ndata//2]

        left_hrect = hrect.copy()
        right_hrect = hrect.copy()
        left_hrect[1, 0] = splitval
        right_hrect[0, 0] = splitval

        self.kd_tree = [(None, None, left_hrect, right_hrect, None, None)]

        stack = [(data[:,:ndata//2], idx[:ndata//2], 1, 0, True),
                (data[:,ndata//2:], idx[ndata//2:], 1, 0, False)]

        while stack:
            # pop data off stack
            data, didx, depth, parent, leftbranch = stack.pop()
            ndata = data.shape[1]
            nodeptr = len(self.kd_tree)

            # update parent node

            _didx, _data, _left_hrect, _right_hrect, left, right = self.kd_tree[parent]

            self.kd_tree[parent] = (_didx, _data, _left_hrect, _right_hrect, nodeptr, right) if leftbranch \
                else (_didx, _data, _left_hrect, _right_hrect, left, nodeptr)

            # insert node in kd-tree

            # leaf node?
            if ndata <= leafsize:
                _didx = didx.copy()
                _data = data.copy()
                leaf = (_didx, _data, None, None, 0, 0)
                self.kd_tree.append(leaf)

            # not a leaf, split the data in two
            else:
                splitdim = depth % ndim
                idx = np.argsort(data[splitdim,:], kind='mergesort')
                data[:,:] = data[:,idx]
                didx = didx[idx]
                nodeptr = len(self.kd_tree)
                stack.append((data[:,:ndata//2], didx[:ndata//2], depth+1, nodeptr, True))
                stack.append((data[:,ndata//2:], didx[ndata//2:], depth+1, nodeptr, False))
                splitval = data[splitdim,ndata//2]
                if leftbranch:
                    left_hrect = _left_hrect.copy()
                    right_hrect = _left_hrect.copy()
                else:
                    left_hrect = _right_hrect.copy()
                    right_hrect = _right_hrect.copy()
                left_hrect[1, splitdim] = splitval
                right_hrect[0, splitdim] = splitval
                # append node to tree
                self.kd_tree.append((None, None, left_hrect, right_hrect, None, None))

    def intersect(self, hrect, r2, centroid):
        """
        checks if the hyperrectangle hrect intersects with the
        hypersphere defined by centroid and r2
        """
        maxval = hrect[1,:]
        minval = hrect[0,:]
        p = centroid.copy()
        idx = p < minval
        p[idx] = minval[idx]
        idx = p > maxval
        p[idx] = maxval[idx]
        return ((p-centroid)**2).sum() < r2

    def quadratic_knn_search(self, data, lidx, ldata, K):
        """ find K nearest neighbours of data among ldata """
        ndata = ldata.shape[1]
        K = K if K < ndata else ndata
        sqd = ((ldata - data[:,:ndata])**2).sum(axis=0)
        idx = np.argsort(sqd, kind='mergesort')
        idx = idx[:K]
        return list(zip(sqd[idx], lidx[idx]))

    def search_kdtree(self, datapoint, K=1):
        """ find the k nearest neighbours of datapoint in a kdtree """
        stack = [self.kd_tree[0]]
        knn = [(np.inf, None)]*K
        _datapt = datapoint[:,0]
        while stack:

            leaf_idx, leaf_data, left_hrect, \
                    right_hrect, left, right = stack.pop()

            # leaf
            if leaf_idx is not None:
                _knn = self.quadratic_knn_search(datapoint, leaf_idx, leaf_data, K)
                if _knn[0][0] < knn[-1][0]:
                    knn = sorted(knn + _knn)[:K]

            # not a leaf
            else:

                # check left branch
                if self.intersect(left_hrect, knn[-1][0], _datapt):
                    stack.append(self.kd_tree[left])

                # chech right branch
                if self.intersect(right_hrect, knn[-1][0], _datapt):
                    stack.append(self.kd_tree[right])
        return knn

class CustomKDTreeConverter(BaseConverter):

    def convert(self):
        kd_tree = KDTree()
        # Make a copy because build_kdtree rewrites input data
        # but we need original colors because of indexes
        copy_colors = np.transpose(np.copy(self.colors))
        kd_tree.build_kdtree(copy_colors)


        for x in range(len(self.input_image)):
            row = []
            for img_color in self.input_image[x]:
                data = kd_tree.search_kdtree(img_color.reshape((3, 1)))
                # for K=1, data = [(123,12)]
                # where 123 - squared-distance, 12 - color index in color palette
                row.append(self.colors[data[0][1]])
            self.new_image.append(row)
