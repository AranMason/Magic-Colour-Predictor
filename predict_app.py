print(" * Starting Web App")

import base64
import numpy as np
import io
from PIL import Image
import json

import keras
from keras import backend as K
from keras.models import Sequential
from keras.models import load_model, model_from_json
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from keras.optimizers import Adam

import tensorflow as tf
from keras.utils.generic_utils import CustomObjectScope
from flask import request
from flask import jsonify
from flask import Flask

K.clear_session()

graph = tf.get_default_graph()

model_file = 'models/model_complete.h5'

app = Flask(__name__)

if __name__ == '__main__':
	app.run(host="0.0.0.0")

def get_classes():
	global classes
	with open('models/classes.json', 'r') as f:
		classes = json.load(f)
	print(" * Loaded Model Classes")
	print(" * Found: ", classes)

def get_model():
	print(" * Loading Keras Model...")
	global model
	with CustomObjectScope({'relu6': keras.applications.mobilenet.relu6,'DepthwiseConv2D': keras.applications.mobilenet.DepthwiseConv2D}):
		model = load_model(model_file)
	# model._make_predict_function()

	print(' * Model Loaded!')
	# model.summary()

def preprocess_image(image, target_size):
	if image.mode != 'RGB':
		image = image.convert('RGB')

	image = image.resize(target_size)
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)

	return image

print("Using Keras Version: ", keras.__version__)

get_model()
get_classes()

@app.route('/predict', methods=["POST"])
def predict():
	global graph
	with graph.as_default():
		message = request.get_json(force=True)

		encoded = message["image"]
		decoded = base64.b64decode(encoded)

		image = Image.open(io.BytesIO(decoded))
		processed_image = preprocess_image(image, target_size=(224, 224))

		prediction = model.predict(processed_image)

		response = {}

		for key in classes.keys():
			response[key] = str(prediction[0][classes[key]])

		return jsonify(response)

@app.route('/test')
def test():

	return "Web Server is Running"
