import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import OneHotEncoder

def process(data: pd.DataFrame, train=True):
    cat_data = data[['state', 'product_type']]
    y = data.iloc[:, -1].to_numpy()
    if train:
        encoder = OneHotEncoder(sparse_output=False)
        X = encoder.fit_transform(cat_data)
        pickle.dump(encoder, open('tax_models/encoder.pkl', 'wb'))
        return X, y
    else:
        encoder = pickle.load(open('tax_models/encoder.pkl', 'rb'))
        X = encoder.transform(cat_data)
        return X, y