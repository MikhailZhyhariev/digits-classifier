import numpy as np
from keras.models import model_from_json
from keras.preprocessing import image


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
        self.img = image.load_img(img, target_size=(28, 28), grayscale=True)

    def transform(self, fnn=True):
        img = image.img_to_array(self.img)
        img = 255 - img
        img /= 255
        if fnn:
            img = img.reshape((1, 784))
        else:
            img = np.expand_dims(img, axis=0)
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
