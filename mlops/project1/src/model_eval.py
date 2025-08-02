import numpy as np
import pandas as pd
import os
import pickle
import json

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

test_data = pd.read_csv('./data/processed/test_processed.csv')

X_test = test_data.iloc[:,0:-1].values
y_test = test_data.iloc[:,-1].values

model = pickle.load(open('model.pkl','rb'))

y_pred = model.predict(X_test)

acc = accuracy_score(y_true=y_test, y_pred =y_pred)
predcs = precision_score(y_true=y_test, y_pred=y_pred)
re = recall_score(y_true=y_test, y_pred=y_pred)
f1 = f1_score(y_true=y_test, y_pred=y_pred)

metrics_dic = {
    'acc':acc,
    'precision':predcs,
    'recall':re,
    'f1_score':f1
}

with open('metrics.json','w') as file:
    json.dump(metrics_dic,file,indent=4)