import sys
import os
import pandas as pd
import numpy as np
import json
import re

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder

current_dir = os.path.dirname(os.path.abspath(__file__))
ml_utilities_path = os.path.join(current_dir, '../ml_utilities.py')
sys.path.append(os.path.dirname(ml_utilities_path))
import ml_utilities as ml

with open("config.json", "rb") as f:
    config = json.load(f)
    vectorizer_pth = f"{config['text_model_dir']}/text_vectorizer.pkl"
    lb_encoder_pth = f"{config['text_model_dir']}/label_encoder.pkl"


def gen_corpus(data: pd.DataFrame):
    lm = WordNetLemmatizer()
    corpus = []
    
    for sentence in data["product_name"]:
        sentence = re.sub('[^a-zA-Z]',' ', str(sentence))
        tokens = sentence.lower().split()
        tokens = [lm.lemmatize(word) for word in tokens if word 
                  not in set(stopwords.words('english'))]
        corpus.append(' '.join(tokens))
    return corpus

def preprocess(data: pd.DataFrame, mode="train"):
    corpus = gen_corpus(data)
    if mode == "train":
        vectorizer = CountVectorizer()
        label_encoder = LabelEncoder()
        X = vectorizer.fit_transform(corpus)
        y = label_encoder.fit_transform(data['product_type'])
        ml.save_model(vectorizer, vectorizer_pth)
        ml.save_model(label_encoder, lb_encoder_pth)
        return X, y
    else:
        vectorizer = ml.load_model(vectorizer_pth)
        X = vectorizer.transform(corpus)
        if mode == "inference":
            return X
        
        label_encoder = ml.load_model(lb_encoder_pth)
        y = label_encoder.transform(data['product_type'])
        return X, y