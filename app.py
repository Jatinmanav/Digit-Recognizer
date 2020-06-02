from flask import Flask, request
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np


app = Flask(__name__)


MODEL_PATH = 'mnist'

model = load_model(MODEL_PATH)


def model_predict(path, model):
    img = image.load_img(path, color_mode='grayscale', target_size=(28, 28))
    X = image.img_to_array(img)
    X = abs(X/255)
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
    return str(result)


if __name__ == "__main__":
    app.run(debug=True)
