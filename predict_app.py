print(" * Starting Web App")

# import os; os.environ['KERAS_BACKEND'] = 'theano'

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

from flask import request
from flask import jsonify
from flask import Flask

K.clear_session()

graph = tf.get_default_graph()

model_file = 'models/model_complete.h5'

app = Flask(__name__)

def get_classes():
	global classes
	with open('models/classes.json', 'r') as f:
		classes = json.load(f)
	print(" * Loaded Model Classes")
	print(" * Found: ", classes)

def get_model():
	print(" * Loading Keras Model...")
	# K.clear_session()


	# # Read JSON Model
	# json_file = open('model.json', 'r')
	# loaded_model_json = json_file.read()
	# json_file.close()
	# loaded_model = model_from_json(loaded_model_json)

	# # Get model weights
	# loaded_model.load_weights('model_weights.h5')

	# loaded_model.compile(Adam(lr=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

	global model
	model = load_model(model_file)
	# model._make_predict_function()

	print(model.predict_classes)
	print(' * Model Loaded!')
	model.summary()

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
		print("Handling Prediction Request")

		message = request.get_json(force=True)

		encoded = message["image"]
		print("Retrieved encoded message")
		decoded = base64.b64decode(encoded)

		print("Decoded message")

		image = Image.open(io.BytesIO(decoded))

		print("Coverted to image file")

		processed_image = preprocess_image(image, target_size=(224, 224))

		print("Processed image")
		prediction = model.predict(processed_image)

		print(prediction)

		response = {

		}

		for key in classes.keys():
			response[key] = str(prediction[0][classes[key]])

		return jsonify(response)

@app.route('/test')
def test():
	global graph
	with graph.as_default():

		print("Running Test Route")
		img = load_img('data/60772895_2139110652808772_1139490257108992000_n.jpg', target_size=(224, 224))

		img = img_to_array(img)

		img = np.expand_dims(img, axis=0)

		predict = model.predict(img)

		print(predict)

		return predict