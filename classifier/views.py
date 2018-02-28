import os
import base64
import json

from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View
from django.http import HttpResponse
from .networks.keras.keras import KerasNetwork


class FrontendAppView(View):
    @staticmethod
    @ensure_csrf_cookie
    def get(request):
        return render(request, 'classifier/index.html')

    @staticmethod
    def post(request):
        if request.POST:
            img = base64.b64decode(request.read())
            with open('image.png', 'wb') as f:
                f.write(img)

            network = KerasNetwork('image.png')

            predict = network.predict()

            predict_result = map(lambda lst: [{
                'digit': digit,
                'probability': f'{round(probability * 100, 3)}%'
            } for probability, digit in lst], predict)

            if predict[0][0][0] > (predict[1][0][0] + 0.2):
                result_digit = predict[0][0][1]
            else:
                result_digit = predict[1][0][1]

            json_result = json.dumps({
                "number": result_digit,
                "info": [{
                    "type": name,
                    "answer": result
                } for result, name in zip(predict_result, ['Keras FNN', 'Keras CNN'])]
            })

            os.remove('image.png')

            return HttpResponse(json_result, content_type='application/json')
        else:
            return render(request, 'classifier/index.html')
