from training import load_model
from sklearn.metrics import mean_squared_error
import numpy as np


def predict(X: np.ndarray, model):
    return model.predict(X)
    
def evaluate(X: np.ndarray, y_true, model):
    y_preds = predict(X, model)
    return mean_squared_error(y_true, y_preds)