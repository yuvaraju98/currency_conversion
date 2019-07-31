
from django.shortcuts import redirect,render

from . import views
from .forms import DataForm
import pandas as pd
from .training import train


def upload(request):
    base = request.POST.get('base')
    target = request.POST.get('target')
    date = request.POST.get('date')
    maxdays = request.POST.get('maxdays')
    amount = request.POST.get('amount')

    print(base,target,date,maxdays)

    return request,base,target,date,maxdays,amount

def train_model(data):
    get_data()
    train(data)
    predict(date,maxdays)




