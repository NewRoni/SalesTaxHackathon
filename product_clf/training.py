import pickle
import xgboost as xg
from sklearn.model_selection import GridSearchCV
import json

with open('config.json', 'r') as f:
    config = json.load(f)

def train(X, y):
    parameters = config['hp_tuning_dict']
    grid_search = GridSearchCV(xg.XGBClassifier(), parameters, return_train_score=True)
    grid_search.fit(X,y)
    
    best_params = grid_search.best_params_
    print(best_params)
    
    model = xg.XGBClassifier(learning_rate=best_params['learning_rate'],
                             n_estimators=best_params['n_estimators'],
                             max_depth=best_params['max_depth'],
                             subsample=best_params['subsample'],
                             colsample_bytree=best_params['colsample_bytree'])
    model.fit(X,y)
    return model