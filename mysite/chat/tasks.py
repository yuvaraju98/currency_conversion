
from django.shortcuts import redirect,render

from . import views
from .forms import DataForm
import pandas as pd
from .training import train,transform,predict_values
import requests
from .charts import LineChart

def process(request):
    data=upload(request)
    response = get_data(data)
    x_train,y_train=transform(pd.DataFrame(response))
    print(x_train)
    logreg=train_model(x_train,y_train)
    get_predicted_array = predict(logreg,data)

    return list(get_predicted_array[0])


def upload(request):
    data=dict()
    data['base'] = request.POST.get('base')
    data['target'] = request.POST.get('target')
    data['date'] = request.POST.get('date')
    data['maxdays'] = request.POST.get('maxdays')
    data['amount'] = request.POST.get('amount')
    return data




def get_data(data):

    url='https://api.exchangeratesapi.io/history?start_at={}&end_at=2019-04-01&base={}&' \
        'symbols={},{}'.format(data['date'],data['base'],data['base'],data['target'])
    response=requests.get(url).json()
    return response


def train_model(dependent,independent):
    return train(dependent,independent)


def predict(logreg,data):
    print(pd.Series(data['date']).item())
    transfored_data=transform(pd.Series(data['date']))
    for x in ['Monday','Tuesday','Wednesday','Thursday','Friday']:
        if x not in transfored_data.columns:
            transfored_data[x]=0
    print(transfored_data)


    return predict_values(logreg,transfored_data)



