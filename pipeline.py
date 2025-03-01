from preprocess import process
from training import train
from sklearn.metrics import mean_squared_error
import ml_utilities as ml
import numpy as np
import pandas as pd

if __name__ == "__main__":
    data = pd.read_csv('data/us-sales-tax-dataset.csv')
    train_df, val_df = ml.splitdata(data)
    
    # train
    X_train, y_train = process(train_df)
    model = train(X_train, y_train, hp_tuning=True)
    ml.save_model(model, 'tax_models/model4.pkl')
    
    # evaluate
    model = ml.load_model('tax_models/model4.pkl')
    X_val, y_val = process(val_df, train=False)
    mse = ml.evaluate(model, X_val, y_val, mean_squared_error)
    print(f"MSE: {mse:.5f} | RMSE: {np.sqrt(mse):.5f}")
    
    # dummy predictions
    test_input = pd.DataFrame({"state": ["California", "Louisiana", "Connecticut", "Delaware"], "product_type": ["Food", "General", "Digital", "General"]})
    encoder = ml.load_model('tax_models/encoder.pkl')
    input_arr = encoder.transform(test_input)
    test_pred = ml.predict(model, input_arr)
    print(f"Predictions: {test_pred}")
    
    