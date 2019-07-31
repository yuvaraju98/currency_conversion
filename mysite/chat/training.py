
import pandas as pd
import pandas as pd
from sklearn.linear_model import LinearRegression
import json

def train(f):
    contents = f.read()
    logreg = LinearRegression()

    logreg.fit(pd.DataFrame(x_train), x_result)

    return logreg




def transform(values):
    x_train = {'day': [], 'month': [], 'dayname': []}
    x_result = list()
    for x, y in values.T.iteritems():
        x_train['day'].append(pd.to_datetime(x).day)
        x_train['month'].append(pd.to_datetime(x).month)
        x_train['dayname'].append(pd.to_datetime(x).day_name())
        x_result.append(y['rates']['INR'])
    pp=pd.get_dummies(x_train['dayname']).iloc[:0]


def predict(logreg):
    res=[]
    for x in range(0, 5):
        p = pd.DataFrame({1: [x], 2: [1]})
        res.append(logreg.predict(p))
