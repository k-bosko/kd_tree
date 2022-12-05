from PIL import Image
import numpy as np

class BaseConverter:
    def __init__(self, filename, colors):
        self.colors = np.asarray(colors)
        self.new_image = []

        with Image.open(filename) as img:
            img.load()
        self.input_image = np.asarray(img)

    def convert(self):
        raise NotImplementedError()

    def save_file(self, output):
        np_new_image = np.asarray(self.new_image, dtype=np.uint8)
        img = Image.fromarray(np_new_image, mode='RGB')
        img.save(output)
