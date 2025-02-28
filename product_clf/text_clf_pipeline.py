from preprocess import gen_corpus, preprocess
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay, roc_curve, auc
import matplotlib.pyplot as plt
import ml_utilities as ml
from training import train
import pandas as pd
import numpy as np
import json
import os

with open('config.json', 'r') as f:
    config = json.load(f)
    model_pth = os.path.join(config['text_model_dir'], 'product_clf.pkl')
    result_dir = config['text_results_dir']



if __name__ == "__main__":
    data = pd.read_csv('data/product-types-dataset.csv')
    train_df, val_df = ml.splitdata(data)
    
    # train
    X_train, y_train = preprocess(train_df)
    # model = train(X_train, y_train)
    # ml.save_model(model_pth)

    # evaluate
    model = ml.load_model(model_pth)
    X_val, y_val = preprocess(val_df, mode="val")
    accuracy = ml.evaluate(model, X_val, y_val, accuracy_score)
    print(f'Accuracy: {accuracy}')
    
    y_pred = model.predict(X_val)
    report = classification_report(y_val, y_pred)
    print(report)
    with open(f"{result_dir}/clf_report.txt", "w") as f:
        f.write(report)
    
    le = ml.load_model(f"{config['text_model_dir']}/label_encoder.pkl")
    class_names = le.classes_
    
    disp = ConfusionMatrixDisplay.from_estimator(
        model,
        X_val,
        y_val,
        display_labels=class_names,
        cmap=plt.cm.Blues,
    )
    plt.xticks(fontsize=6)
    plt.yticks(fontsize=6)
    disp.ax_.set_title("Confusion Matrix of Product name classification")
    plt.savefig(f"{result_dir}/conf_mat.png")

    
    # dummy predictions
    input_df = pd.DataFrame({"product_name": ["Manuka honey", "Vegetable oil", "Nike sneakers", "Boots handcream", "Sony headphones", "ibuprofen"]})
    input_arr = preprocess(input_df, mode="inference")
    preds = model.predict(input_arr)
    for i, pred in enumerate(preds):
        print(f"{input_df.iloc[i]['product_name']} -> {class_names[pred]}")
    
    
    
    