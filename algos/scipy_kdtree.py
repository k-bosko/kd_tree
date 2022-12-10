from scipy.spatial import KDTree

from .converter import BaseConverter


class ScipyKDTreeConverter(BaseConverter):
    def convert(self):
        # leafsize controls when to switch to brute-force
        # by default leafsize=10
        # here adjusted to mimic custom KDTree implementation
        kd_tree = KDTree(self.colors, leafsize=1)
        for x in range(len(self.input_image)):
            row = []
            for img_color in self.input_image[x]:
                _, idx = kd_tree.query(img_color)
                row.append(self.colors[idx])
            self.new_image.append(row)
