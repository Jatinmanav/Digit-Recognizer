from flask import Flask, request
from flask_cors import CORS
import os
import sys
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import cv2
import numpy as np
import base64


app = Flask(__name__)
CORS(app)


MODEL_PATH = 'mnist'

model = load_model(MODEL_PATH)


def model_predict(path, model):
    X = cv2.resize(cv2.imread(path, 0), (28, 28))
    X = X/255
    X = np.expand_dims(X, axis=0)
    temp = model.predict(X)
    return temp


@app.route('/', methods=['GET'])
def home():
    return '<h1> Home Page </h1>'


@app.route('/predict', methods=['POST'])
def predict():
    print('Here')
    f = request.files['file']
    basepath = os.path.dirname(__file__)
    filepath = os.path.join(basepath, 'uploads', f.filename)
    f.save(filepath)
    preds = model_predict(filepath, model)
    result = np.argmax(preds)
    print(str(result), file=sys.stderr)
    return str(result)


if __name__ == "__main__":
    app.run()
