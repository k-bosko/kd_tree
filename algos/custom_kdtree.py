from .converter import BaseConverter
import numpy as np
from heapq import heappush, heappop
from collections import Counter
from statistics import median

class AlternateMedian:
  '''
  Alternate through dimension and always use the median value to split.
  '''
  def __init__(self, dimension = -1, stopping_criteria = lambda x: len(x)<=1):
    self.dim = dimension
    self._should_stop_split = stopping_criteria
    self.same_dim_values_count = 0

  def get_split_dimension_value(self, data=None):
    self.dim = (self.dim+1)%len(data[0])

    dim_values = [example[self.dim] for example in data]
    dim_values_counter = Counter(dim_values)

    if len(dim_values_counter)==1:                    # All having the same values
      self.same_dim_values_count+=1
      if self.same_dim_values_count == len(data[0]):  # Gone through all dimension is still the same
        median_val = dim_values[0]
        # print("Exactly same values")
        self._should_stop_split = lambda x: True
        return self.dim, median_val
      else:                                           # try the next dimension
        return self.get_split_dimension_value(data)
    elif len(dim_values_counter) ==2:
      median_val = min(list(dim_values_counter.keys()))
      return self.dim, median_val
    else:
      return self.dim, median(dim_values)

  def should_stop_split(self, data=None):
    return self._should_stop_split(data)

  def clone(self):
    return self.__class__(self.dim, self._should_stop_split)

  def __str__(self):
    return "AlternateMedian"

class Node:
  '''
  A Tree node within the KDTree
  '''
  def __init__(self, data = None, split_value=None, split_dimension=None, left=None, right=None):
    self.data = data
    self.split_value, self.split_dimension = split_value, split_dimension
    self.left, self.right = left, right

  def __str__(self, offset = 0):
    offsetTabs = "\t"*offset
    desc = ""
    desc= desc+ offsetTabs + "split_value: "+ str(self.split_value)+", split_dimension: "+ str(self.split_dimension)+"\n"
    if self.data: desc= desc+ offsetTabs + "data: "+ str(self.data)+"\n"
    if self.left: desc+= self.left.__str__(offset+1)
    if self.right: desc+= self.right.__str__(offset+1)
    return desc

class KDTree:
  '''
  Two main methods:
  1. build_kdtree
  2. search_knn --- given a query data, look for the top k nearest neighbor (NN)
  '''
  def __init__(self):
    self.kdtree = None

  def build_kdtree(self, data, KDStrategy):
    self.kdtree = self._build_kdtree(data, KDStrategy)

  def search_knn(self, query, k, dist_func=None, alpha=1):
    if not self.kdtree: return None
    if not dist_func: dist_func = self.euclidean
    results = []  # max heap of size k; [(-dist, point)]
    self._search(self.kdtree, results, query, dist_func, k, alpha)
    # if len(results) > k: print("More than k nearest neigbor is found - ", len(results), "neighbors found")
    return [res[1] for res in results][::-1] # reverse the list

  def _build_kdtree(self, data, KDStrategy):
    if not data: return None
    if KDStrategy.should_stop_split(data): return Node(data=data)

    dimension, value = KDStrategy.get_split_dimension_value(data)
    partition_left, partition_right = self._partition_by_dim_value(data, dimension, value)

    return Node (
        split_value = value,
        split_dimension = dimension,
        left = self._build_kdtree(partition_left, KDStrategy.clone()),
        right = self._build_kdtree(partition_right, KDStrategy.clone())
    )

  def _search(self, node, results, query, dist_func, k, alpha = 1):
    if not node: return
    if node.data:
      dist_vec = dist_func(node.data, query)
      for i in range(len(node.data)):
        dist = dist_vec[i]
        example = node.data[i]
        if len(results) < k or dist == -results[0][0]: heappush(results, (-dist, example))
        elif dist < -results[0][0]:
          heappush(results, (-dist, example))
          heappop(results)
      return
    else:
      dim, value = node.split_dimension, node.split_value
      val_diff = query[dim] - value

      searchFirst, searchNext = node.left, node.right
      if val_diff >0: searchFirst, searchNext = searchNext, searchFirst

      self._search(searchFirst, results, query, dist_func, k, alpha)
      # Pruning
      if len(results)<k or dist_func(query[dim],value) < (-results[0][0]/alpha):
        self._search(searchNext, results, query, dist_func, k, alpha)
      return

  def _partition_by_dim_value(self, data, dim, value):
    partition_left, partition_right = [], []
    for example in data:
      if example[dim]<=value: partition_left.append(example)
      else: partition_right.append(example)
    return partition_left, partition_right

  def euclidean (self, x, y):
    if hasattr(x, '__len__') and hasattr(x[0], '__len__'):return np.linalg.norm(np.subtract(x, y), axis=1)
    if hasattr(y, '__len__') and hasattr(y[0], '__len__'): return np.linalg.norm(np.subtract(x, y), axis=1)
    # No axis 1 is found on either x or y
    return np.linalg.norm(np.subtract(x, y), axis=None)

class CustomKDTreeConverter(BaseConverter):
  LEAF_SIZE = 2048

  def convert(self):
    kd_tree = KDTree()
    # Make a copy because build_kdtree rewrites input data
    # but we need original colors because of indexes
    copy_colors = self.colors.tolist()
    kd_tree.build_kdtree(copy_colors, AlternateMedian(stopping_criteria= lambda x: len(x)<=self.LEAF_SIZE))

    for x in range(len(self.input_image)):
      row = []
      for img_color in self.input_image[x]:
        data = kd_tree.search_knn(img_color.tolist(), k = 1)[0]  # take the first in case many same dist neighbors found
        row.append(data)
      self.new_image.append(row)
