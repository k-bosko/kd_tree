import numpy as np
import math
from .converter import BaseConverter

'''
Example:
palette_color: [0 0 0]
img_color [194 191 186]
min_distance 329.71654492912546
'''

class NaiveConverter(BaseConverter):
    def find_closest(self, img_color):
        min_distance = math.inf
        for palette_color in self.colors:
            diffs = [x - y for x,y in zip(palette_color, img_color)]
            squared_dist = sum([d**2 for d in diffs])
            if squared_dist < min_distance:
                min_distance = squared_dist
                closest_color = palette_color
        return list(closest_color)

    def convert(self):
        for x in range(len(self.input_image)):
            row = []
            for img_color in self.input_image[x]:
                closest_color = self.find_closest(img_color)
                row.append(closest_color)
            self.new_image.append(row)
