import numpy as np
import pickle
from sklearn.model_selection import train_test_split

def splitdata(data, test_size=0.2, random_state=42):
    train, test = train_test_split(data,
                                   test_size=test_size,
                                   random_state=random_state)
    return train, test

def save_model(model, filepth: str):
    pickle.dump(model, open(filepth, 'wb'))

def load_model(filepth: str):
    return pickle.load(open(filepth, 'rb'))

def predict(model, X: np.ndarray):
    return model.predict(X)
    
def evaluate(model, X: np.ndarray, y_true: np.ndarray, metric_fn: callable):
    y_preds = predict(model, X)
    return metric_fn(y_true, y_preds)