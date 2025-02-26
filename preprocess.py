import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

def splitdata(data):
    X, y = train_test_split(data, test_size=0.2, random_state=42)
    return X, y

def process(data: pd.DataFrame, train=True):
    cat_data = data[['state', 'product_type']]
    y = data.iloc[:, -1].to_numpy()
    if train:
        encoder = OneHotEncoder(sparse_output=False)
        X = encoder.fit_transform(cat_data)
        pickle.dump(encoder, open('ml_models/encoder.pkl', 'wb'))
        return X, y
    else:
        encoder = pickle.load(open('ml_models/encoder.pkl', 'rb'))
        X = encoder.transform(cat_data)
        return X, y