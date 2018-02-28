import numpy as np
from skimage.transform import resize
from skimage.io import imread, imshow


class Image:
    def __init__(self, img):
        self.img = imread(img, as_grey=True)

    def transform(self):
        self.crop()
        self.resize()
        self.negate()
        self.get()

    def get(self):
        return self.img

    def crop(self):
        self.img = self.filter(self.filter(self.img))

    @staticmethod
    def filter(lst):
        return np.array([row for row in lst if np.mean(row) != 1]).T

    def resize(self):
        new_height, new_width = self.rescale()

        img = resize(self.img, (new_height, new_width), mode="reflect")

        height, width = map(lambda x: (28 - x) // 2, [new_height, new_width])

        self.img = np.ones((28, 28))
        self.img[height:height + new_height, width:width + new_width] = img

    def rescale(self):
        height, width = self.img.shape
        if height > width:
            return [20, (width * 20) // height]
        else:
            return [(height * 20) // width, 20]

    def negate(self):
        self.img = 1 - self.img

    def show(self):
        imshow(self.img)
