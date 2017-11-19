from keras.models import model_from_json
from skimage import img_as_float
from skimage.io import imread
from skimage.transform import resize
from skimage.color import rgb2gray


img = imread('two.png')
img = img_as_float(img)
img = rgb2gray(img)
img = resize(img, (28, 28), mode="reflect")
img = img.reshape((1, 784))

with open('keras_model.json', 'r') as f:
    model_json = f.read()
    model = model_from_json(model_json)

model.load_weights('keras_model.h5')

result = model.predict(img)

classifier = []
for digit, item in enumerate(result[0]):
    classifier.append((item, digit))

classifier.sort(reverse=True)

print(*result)
print(f"Я думаю, это цифра {classifier[0][1]}")
