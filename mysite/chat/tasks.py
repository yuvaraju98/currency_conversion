
from django.shortcuts import redirect,render

from . import views
from .forms import DataForm
import pandas as pd
from .training import train,transform
import requests


def upload(request):
    data=dict()
    data['base'] = request.POST.get('base')
    data['target'] = request.POST.get('target')
    data['date'] = request.POST.get('date')
    data['maxdays'] = request.POST.get('maxdays')
    data['amount'] = request.POST.get('amount')
    print(data)

    # print(base,target,date,maxdays)
    jsn=get_data(data)

    return 0


def get_data(data):

    url='https://api.exchangeratesapi.io/history?start_at={}&end_at=2019-04-01&base={}&' \
        'symbols={},{}'.format(data['date'],data['base'],data['base'],data['target'])
    response=requests.get(url).json()
    print(response)
    x_train,y_train=transform(pd.DataFrame(response))
    train_model(x_train,y_train)






def train_model(dependent,independent):





