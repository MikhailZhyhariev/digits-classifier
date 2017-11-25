import os
import base64
import json

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
from .networks.keras import keras


class FrontendAppView(View):
    @staticmethod
    def get(request):
        return render(request, os.path.join(settings.TEMPLATE_PATH, 'index.html'))

    @staticmethod
    def post(request):
        if request.POST:
            img = base64.b64decode(request.read())
            with open('image.png', 'wb') as f:
                f.write(img)

            network = keras.KerasNetwork('image.png')

            predict_fnn, predict_cnn = network.predict()

            ret_fnn = [
                {
                    'digit': digit,
                    'probability': f'{round(probability * 100, 3)}%'
                } for probability, digit in predict_fnn
            ]
            ret_cnn = [
                {
                    'digit': digit,
                    'probability': f'{round(probability * 100, 3)}%'
                } for probability, digit in predict_cnn
            ]
            digit = predict_cnn[0][1] if predict_cnn[0][0] + 15 > predict_fnn[0][0] else predict_fnn[0][1]

            result = json.dumps({
                "number": digit,
                "info": [
                {
                    "type": "Keras FNN",
                    "answer": ret_fnn
                },
                {
                    "type": "Keras CNN",
                    "answer": ret_cnn
                }
            ]})

            os.remove('image.png')

            return HttpResponse(result, content_type='application/json')
        else:
            with open(os.path.join(settings.REACT_APP_DIR, 'build', 'index.html')) as f:
                return HttpResponse(f.read())
