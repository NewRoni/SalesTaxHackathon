import xgboost as xg
import pickle

def save_model(model, filepth: str):
    pickle.dump(model, open(filepth, 'wb'))

def load_model(filepth: str):
    return pickle.load(open(filepth, 'rb'))

def train(X, y):
    xgb_model = xg.XGBRegressor()
    xgb_model.fit(X, y)
    return xgb_model