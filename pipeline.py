from preprocess import splitdata, process
from training import train, save_model, load_model
from inference import predict, evaluate
import numpy as np
import pandas as pd

if __name__ == "__main__":
    data = pd.read_csv('data/us-sales-tax-dataset.csv')
    train_df, val_df = splitdata(data)
    
    # train
    # X_train, y_train = process(train_df)
    # model = train(X_train, y_train)
    # save_model(model, 'ml_models/model.pkl')
    
    # evaluate
    model = load_model('ml_models/model.pkl')
    X_val, y_val = process(val_df, train=False)
    mse = evaluate(X_val, y_val, model)
    print(f"MSE: {mse:5f} | RMSE: {np.sqrt(mse):.5f}")
    
    # dummy predictions
    test_input = pd.DataFrame({"state": ["California", "Louisiana"], "product_type": ["Food", "General"]})
    encoder = load_model('ml_models/encoder.pkl')
    input_arr = encoder.transform(test_input)
    test_pred = predict(input_arr, model)
    print(test_pred)
    
    