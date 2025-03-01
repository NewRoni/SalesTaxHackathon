from sklearn.model_selection import GridSearchCV
import xgboost as xg
import pickle
import json

with open('config.json', 'r') as f:
    config = json.load(f)

def save_model(model, filepth: str):
    pickle.dump(model, open(filepth, 'wb'))

def load_model(filepth: str):
    return pickle.load(open(filepth, 'rb'))

def train(X, y, hp_tuning=False):
    if hp_tuning:
        parameters = config['hp_tuning_dict2']
        grid_search = GridSearchCV(xg.XGBRegressor(), parameters, return_train_score=True)
        grid_search.fit(X,y)
        
        best_params = grid_search.best_params_
        print(best_params)
        
        model = xg.XGBRegressor(learning_rate=best_params['learning_rate'],
                                n_estimators=best_params['n_estimators'],
                                max_depth=best_params['max_depth'],
                                subsample=best_params['subsample'],
                                colsample_bytree=best_params['colsample_bytree'])
    else:
        model = xg.XGBRegressor()
    
    model.fit(X,y)
    return model