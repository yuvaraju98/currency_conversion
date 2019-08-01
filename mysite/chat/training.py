
import pandas as pd
import pandas as pd
from sklearn.linear_model import LinearRegression
import json

def train(x,y):
    logreg = LinearRegression()
    logreg.fit(x, y)

    return logreg

def transform(values):
    x_train = {'day': [], 'month': [], 'dayname': []}
    x_result = list()
    purpose='train'
    for x, y in values.T.iteritems():
        x_train['day'].append(pd.to_datetime(x).day)
        x_train['month'].append(pd.to_datetime(x).month)
        x_train['dayname'].append(pd.to_datetime(x).day_name())
        try:
            x_result.append(y['rates']['INR'])
        except:
            purpose='predict'
    df = pd.DataFrame(pd.get_dummies(x_train['dayname']))
    df['day'] = x_train['day']
    df['month'] = x_train['month']

    if(purpose=='predict'):
        return df
    else:
        return df,x_result


def predict_values(logreg,p):
    res=[]
    res.append(logreg.predict(p))
    print("res is ",res)
    return res
