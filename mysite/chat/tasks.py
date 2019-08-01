
from django.shortcuts import redirect,render

from . import views
from .forms import DataForm
import pandas as pd
from .training import train,transform,predict_values,predict_transform
import requests
# from django.core.cache import cache
from django_redis import get_redis_connection
cache= get_redis_connection("default")
def process(request):
    data=upload(request)
    response = get_data(data)
    print(response)
    # x_train,y_train=transform(pd.DataFrame(response))
    # print("x_train done")
    # logreg=train_model(x_train,y_train)
    # print("model trained")
    # get_predicted_array = predict(logreg,data)
    #
    # print(get_predicted_array)
    # return get_predicted_array
    return {'label':0}


def upload(request):
    data=dict()
    data['base'] = request.POST.get('base')
    data['target'] = request.POST.get('target')
    data['date'] = request.POST.get('date')
    data['maxdays'] = request.POST.get('maxdays')
    data['amount'] = request.POST.get('amount')
    return data




def get_data(data):

    start_date=data['date']
    prev_2M_date=pd.to_datetime(start_date)+pd.DateOffset(months=-2)
    df_dict={'base':[],'target':[]}
    retrieve_start_date=prev_2M_date
    retrieve_end_date=start_date

    print("min",cache.get('min_date1'))
    print("man",cache.get('max_date1'))


    if not cache.get('min_date1'):
        cache.set('min_date1',str(prev_2M_date.date()))
    if not cache.get('max_date1'):
        cache.set('max_date1',str(start_date))
    print(prev_2M_date,cache.get('max_date1'))
    if pd.to_datetime(prev_2M_date)> pd.to_datetime(str(cache.get('max_date1'))):
        retrieve_start_date=str(prev_2M_date.date())
        retrieve_end_date=start_date
        cache.set('min_date1',str(prev_2M_date.date()))
        cache.set('max_date1',start_date)

    elif pd.to_datetime(start_date) < pd.to_datetime(cache.get('min_date1')):
        retrieve_start_date = start_date
        retrieve_end_date = str(prev_2M_date.date())
        cache.set('min_date1', str(prev_2M_date.date()))
        cache.set('max_date1', start_date)

    elif pd.to_datetime(prev_2M_date)> pd.to_datetime(cache.get('min_date1')):
        retrieve_start_date=cache.get('max_date1')
        retrieve_end_date=str(start_date)
        cache.set('max_date1',start_date)
    elif pd.to_datetime(prev_2M_date) < pd.to_datetime(cache.get('min_date1')):
        retrieve_start_date=str(prev_2M_date.date())
        retrieve_end_date=cache.get('min_date1')
        cache.set('min_date1',str(prev_2M_date.date()))
    else:
        while prev_2M_date != pd.to_datetime(start_date):
            df_dict['base'].append(cache.hget(prev_2M_date,data['base']))
            df_dict['target'].append(cache.hget(prev_2M_date,data['target']))
            prev_2M_date=prev_2M_date+pd.DateOffset(1)
        print(df_dict)

    url='https://api.exchangeratesapi.io/history?start_at={}&end_at={}'.format(str(retrieve_start_date),str(retrieve_end_date))
    response=requests.get(url).json()
    for key,value in response.items():
        cache.hmset(key,value)
        cache.lpush('dates',key)
    print("endmin", cache.get('min_date1'))
    print("endman", cache.get('max_date1'))
    return response


def train_model(dependent,independent):
    return train(dependent,independent)


def predict(logreg,data):
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


    return waiting_dates



