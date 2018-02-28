from ..model import ModelsCompiler
from ..models_config import models_list
from ..image import Image


class KerasNetwork:
    def __init__(self, img):
        self.models = ModelsCompiler.inst(models_list)
        self.img = Image(img)

    def predict(self):
        self.img.transform()
        predict = self.models.predict(self.img.get())
        return [self.prepare_result(data) for data in predict]

    @staticmethod
    def prepare_result(data):
        numerated_list = [(item, digit) for digit, item in enumerate(data[0])]
        numerated_list.sort(reverse=True)
        return numerated_list[:3]

