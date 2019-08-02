
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
    x_train,y_train=transform(response)
    # print("x_train done")
    logreg=train_model(x_train,y_train)
    print("model trained")
    get_predicted_array = predict(logreg,data)

    print(get_predicted_array)
    return get_predicted_array
    # return {'label':0}

def merge_dataframe(df_1,df_2):
    print(df_1)
    print(df_2)


def upload(request):
    data=dict()
    data['base'] = request.POST.get('base')
    data['target'] = request.POST.get('target')
    data['date'] = request.POST.get('date')
    data['maxdays'] = request.POST.get('maxdays')
    data['amount'] = request.POST.get('amount')
    return data




def get_data(data):

    start_date=str(data['date'])
    prev_2M_date=pd.to_datetime(start_date)+pd.DateOffset(months=-2)
    df_dict={'base':[],'date':[],'target':[]}
    response={}
    retrieve_start_date=prev_2M_date.date()
    retrieve_end_date=start_date
    flag=0
    print("--------------------------------------------------------")

    print("min",cache.get('min_date1'))
    print("man",cache.get('max_date1'))
    print("2m",prev_2M_date)
    print("current",start_date)

    if not cache.get('min_date1'):
        cache.set('min_date1',str(prev_2M_date.date()))
    if not cache.get('max_date1'):
        cache.set('max_date1',str(start_date))

    x=str(prev_2M_date.date())
    y=start_date

    if pd.to_datetime(prev_2M_date)> pd.to_datetime(str(cache.get('max_date1'), 'utf-8')):
        print("condition 1-- to much")
        retrieve_start_date=str(prev_2M_date.date())
        retrieve_end_date=start_date
        cache.set('min_date1',str(prev_2M_date.date()))
        cache.set('max_date1',start_date)
        flag=1
        # print(retrieve_end_date,retrieve_start_date)

    elif pd.to_datetime(start_date) < pd.to_datetime(str(cache.get('min_date1'), 'utf-8')):
        print("condition 2 -- too less")

        retrieve_start_date = start_date
        retrieve_end_date = str(prev_2M_date.date())
        cache.set('min_date1', str(prev_2M_date.date()))
        cache.set('max_date1', start_date)
        # print(retrieve_end_date,retrieve_start_date)
        flag=1

    elif (pd.to_datetime(prev_2M_date)> pd.to_datetime(str(cache.get('min_date1'), 'utf-8'))) and not (pd.to_datetime(start_date) < pd.to_datetime(str(cache.get('max_date1'), 'utf-8'))):
        print("condition 3 min over current min "  )
        x=str(pd.to_datetime(prev_2M_date).date())
        y=cache.get('max_date1')
        retrieve_start_date=cache.get('max_date1')
        retrieve_end_date=start_date
        cache.set('max_date1',start_date)
        flag=1
        # print(retrieve_end_date,retrieve_start_date)

    elif pd.to_datetime(prev_2M_date) < pd.to_datetime(str(cache.get('min_date1'), 'utf-8')) :
        print("condition 4 min less than current min")
        x=cache.get('min_date1')
        y=start_date
        retrieve_start_date=str(prev_2M_date.date())
        retrieve_end_date=cache.get('min_date1')
        cache.set('min_date1',str(prev_2M_date.date()))
        flag=1
        # print(retrieve_end_date,retrieve_start_date)

    else:
        print("condition 5")
    x = str(x, 'utf-8') if isinstance(x, bytes) else x
    y = str(y, 'utf-8') if isinstance(y, bytes) else y

    print("startx",x,"y",y,type(x))
    while pd.to_datetime(x)!= pd.to_datetime(y):
        # print("current date -",x,type(x),pd.to_datetime(x).day_name())
        print("data =",x,cache.hget(x,'INR'))
        if pd.to_datetime(x).day_name() not in ['Saturday','Sunday']:
            if (cache.hgetall(x)):
                print("indise")
                df_dict['base'].append(float(cache.hget(x,data['base'])))
                df_dict['target'].append(float(cache.hget(x,data['target'])))

                df_dict['date'].append(x)
                x=pd.to_datetime(x).date()+pd.DateOffset(1)
                x=str(x.date())
                # print("next date",x,type(x))
                x = str(x, 'utf-8') if isinstance(x, bytes) else str(x)
                y = str(y, 'utf-8') if isinstance(y, bytes) else str(y)
                # print("end x,y-",x,y)

            else:
                flag=1
                break
        else:
            x = pd.to_datetime(x).date() + pd.DateOffset(1)
            x = str(x.date())

    retrieve_start_date=str(retrieve_start_date,'utf-8') if isinstance(retrieve_start_date,bytes) else retrieve_start_date
    retrieve_end_date=str(retrieve_end_date,'utf-8') if isinstance(retrieve_end_date,bytes) else retrieve_end_date
    cache.set('min_date1',str(cache.get('min_date1'),'utf-8')) if isinstance(cache.get('min_date1'),bytes) else 0
    cache.set('max_date1',str(cache.get('max_date1'),'utf-8')) if isinstance(cache.get('max_date1'),bytes) else 0

    if flag:
        print("retrieveig")
        url='https://api.exchangeratesapi.io/history?start_at={}&end_at={}'.format(retrieve_start_date,retrieve_end_date)
        print(url)
        response=requests.get(url).json()['rates']
        for key,value in response.items():
            print('key',key)
            cache.hmset(str(key),value)
            cache.lpush('dates',key)
            df_dict['date'].append(str(key))
            df_dict['base'].append(value[data['base']])
            df_dict['target'].append(value[data['target']])

    else:
        print(pd.DataFrame(df_dict))
    df_dict=pd.DataFrame(df_dict)

    print("endmin", cache.get('min_date1'))
    print("endman", cache.get('max_date1'))
    print(pd.DataFrame(df_dict))
    return df_dict


def train_model(dependent,independent):
    return train(dependent,independent)


def predict(logreg,data):
    waiting_dates=dict()
    forcast_dict=dict()
    for wait_days in range(int(data['maxdays'])+1):
        considered_date=pd.Series(pd.to_datetime(data['date'])+pd.DateOffset(wait_days))
        forcast_dict['date']=considered_date.values
        forcast_dict['base']=1
        transfored_data = predict_transform(forcast_dict)

        for days in ['Monday','Tuesday','Wednesday','Thursday','Friday']:
            if days not in transfored_data.columns:
                transfored_data[days]=0
        conversion=predict_values(logreg, transfored_data)

        if conversion== -1:
            print("Saturday")
            continue
        waiting_dates[str(considered_date[0])]=predict_values(logreg, transfored_data)


    return waiting_dates



