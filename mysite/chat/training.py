
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
    print("values",values)
    for x, y in values.T.iteritems():
        x_train['day'].append(pd.to_datetime(x).day)
        x_train['month'].append(pd.to_datetime(x).month)
        x_train['dayname'].append(pd.to_datetime(x).day_name())
        x_result.append(y['rates']['INR'])
    df = pd.DataFrame(pd.get_dummies(x_train['dayname']))
    df['day'] = x_train['day']
    df['month'] = x_train['month']
    # df['base']=values['base']

    return df,x_result


def predict_transform(values):
    x_predict = {'day': [], 'month': [], 'dayname': []}
    # x_predict['day'].append()
    # x_predict['month'].append()
    # x_predict['dayname'].append()
    df = pd.DataFrame(pd.get_dummies(pd.to_datetime(values[0]).day_name()))
    df['day'] = pd.to_datetime(values[0]).day
    df['month'] = pd.to_datetime(values[0]).month
    # df['base']=values['base']

    return df


def predict_values(logreg,p):

    print(p.columns)
    if 'Saturday' not in p.columns and 'Sunday' not in p.columns:
        res=logreg.predict(p)
        return res[0]
    else:
        return -1
