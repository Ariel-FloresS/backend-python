import numpy as np
import pandas as pd
import os

train_dataframe = pd.read_csv('./data/raw/train.csv')

test_dataframe = pd.read_csv('./data/raw/test.csv')

def fill_missing_with_median(dataframe:pd.DataFrame)->pd.DataFrame:

    for column in dataframe.columns:

        if dataframe[column].isnull().any():

            median_valuue = dataframe[column].median()

            dataframe[column].fillna(value = median_valuue,  inplace = True)

    return dataframe

train_processed_data = fill_missing_with_median(dataframe = train_dataframe)
test_processed_data =  fill_missing_with_median(dataframe = test_dataframe)

data_path = os.path.join('data', 'processed')

os.makedirs(data_path)

train_processed_data.to_csv(os.path.join(data_path,'train_processed.csv'), index = False)
test_processed_data.to_csv(os.path.join(data_path,'test_processed.csv'), index = False)

