import numpy as np
from keras.models import model_from_json
from skimage.color import rgb2gray
from skimage import img_as_float
from skimage.transform import resize
from skimage.io import imread


def crop_image(img):
    height, width = img.shape

    crop_dict = {}

    for row in range(height):
        row_value = np.mean(img[row, :])
        if row_value != 1 and crop_dict.get('top') is None:
            crop_dict['top'] = row
        elif row_value == 1 and crop_dict.get('top') is not None:
            crop_dict['bottom'] = row - 1
            break

    for column in range(width):
        column_value = np.mean(img[:, column])
        if column_value != 1 and crop_dict.get('left') is None:
            crop_dict['left'] = column
        elif column_value == 1 and crop_dict.get('left') is not None:
            crop_dict['right'] = column - 1
            break

    return img[crop_dict['top']:crop_dict['bottom'], crop_dict['left']:crop_dict['right']]


def resize_image(img):
    height, width = img.shape

    if height > width:
        scale = round(height / width)
        img = resize(img, (20, round(20 / scale)))
    else:
        scale = round(width / height)
        img = resize(img, (round(20 / scale), 20))

    height, width = img.shape

    result = np.ones((28, 28))
    result[4:24, 14 - round(width / 2):14 - round(width / 2) + width] = img

    return result


class ModelFNN:
    __instance = None

    @staticmethod
    def inst():
        if ModelFNN.__instance is None:
            ModelFNN.__instance = ModelFNN()
        return ModelFNN.__instance

    def __init__(self):
        with open('classifier/networks/keras/fnn/keras_model_fnn.json', 'r') as f:
            self.model = model_from_json(f.read())

        self.model.load_weights('classifier/networks/keras/fnn/keras_model_fnn.h5')
        self.model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

    def predict(self, img):
        return self.model.predict(img)


class ModelCNN:
    __instance = None

    @staticmethod
    def inst():
        if ModelCNN.__instance is None:
            ModelCNN.__instance = ModelCNN()
        return ModelCNN.__instance

    def __init__(self):
        with open('classifier/networks/keras/cnn/keras_model_cnn.json', 'r') as f:
            self.model = model_from_json(f.read())

        self.model.load_weights('classifier/networks/keras/cnn/keras_model_cnn.h5')
        self.model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

    def predict(self, img):
        return self.model.predict(img)


class KerasNetwork:
    def __init__(self, img):
        self.img = imread(img)

    def transform(self, fnn=True):
        img = rgb2gray(self.img)
        img = img_as_float(img)
        img = crop_image(img)
        img = resize_image(img)
        img = 1 - img
        if fnn:
            img = img.reshape((1, 784))
        else:
            img = img.reshape((1, 28, 28, 1))
        return img

    def predict(self):
        img_fnn = self.transform()
        img_cnn = self.transform(fnn=False)

        predict_fnn = ModelFNN.inst().predict(img_fnn)
        predict_cnn = ModelCNN.inst().predict(img_cnn)

        classifier_fnn = []
        for digit, item in enumerate(predict_fnn[0]):
            classifier_fnn.append((item, digit))
        classifier_fnn.sort(reverse=True)

        classifier_cnn = []
        for digit, item in enumerate(predict_cnn[0]):
            classifier_cnn.append((item, digit))
        classifier_cnn.sort(reverse=True)

        return (classifier_fnn[:3], classifier_cnn[:3])
