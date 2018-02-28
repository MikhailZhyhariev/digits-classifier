from keras.models import model_from_json


class Model:
    def __init__(self, model_tuple):
        self.model_structure, self.model_weights, self.transform = model_tuple

        with open(self.model_structure, 'r') as f:
            self.model = model_from_json(f.read())

        self.model.load_weights(self.model_weights)
        self.model.compile(
            loss='categorical_crossentropy',
            optimizer='adam',
            metrics=['accuracy']
        )

    def predict(self, img):
        img = img.reshape(self.transform)
        return self.model.predict(img)


class ModelsCompiler:
    __instance = None

    @staticmethod
    def inst(models_list):
        if ModelsCompiler.__instance is None:
            ModelsCompiler.__instance = ModelsCompiler(models_list)
        return ModelsCompiler.__instance

    def __init__(self, models_list):
        self.models = [Model(model_tuple) for model_tuple in models_list]

    def get(self):
        return self.models

    def predict(self, img):
        return [model.predict(img) for model in self.models]
