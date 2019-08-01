
from django.shortcuts import redirect,render

from . import views
from .forms import DataForm
import pandas as pd
from .training import train,transform,predict_values,predict_transform
import requests
from django.core.cache import cache

def process(request):
    data=upload(request)
    response = get_data(data)
    x_train,y_train=transform(pd.DataFrame(response))
    print("x_train done")
    logreg=train_model(x_train,y_train)
    print("model trained")
    get_predicted_array = predict(logreg,data)

    print(get_predicted_array)
    return get_predicted_array


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
    predicted_results=[]
    waiting_dates=dict()
    for wait_days in range(int(data['maxdays'])+1):
        considered_date=pd.Series(pd.to_datetime(data['date'])+pd.DateOffset(wait_days))
        transfored_data = predict_transform(considered_date)

        for days in ['Monday','Tuesday','Wednesday','Thursday','Friday']:
            if days not in transfored_data.columns:
                transfored_data[days]=0
        conversion=predict_values(logreg, transfored_data)
        if conversion== -1:
            continue
        waiting_dates[str(considered_date[0])]=predict_values(logreg, transfored_data)

        # predicted_results.append(predict_values(logreg, transfored_data))

    return waiting_dates



