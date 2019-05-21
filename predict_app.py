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
from keras.utils.generic_utils import CustomObjectScope
from flask import request
from flask import jsonify
from flask import Flask

K.clear_session()

graph = tf.get_default_graph()

model_file = '/home/ubuntu/Magic-Colour-Predictor/models/model_complete.h5'

app = Flask(__name__)

if __name__ == '__main__':
	app.run(host="0.0.0.0")

class ReverseProxied(object):
    '''Wrap the application in this middleware and configure the
    front-end server to add these headers, to let you quietly bind
    this to a URL other than / and to an HTTP scheme that is
    different than what is used locally.

    In nginx:
    location /myprefix {
        proxy_pass http://192.168.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /myprefix;
        }

    :param app: the WSGI application
    '''
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)

app.wsgi_app = ReverseProxied(app.wsgi_app)

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
	with CustomObjectScope({'relu6': keras.applications.mobilenet.relu6,'DepthwiseConv2D': keras.applications.mobilenet.DepthwiseConv2D}):
		model = load_model(model_file)
	# model._make_predict_function()

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

@app.route('/api/predict', methods=["POST"])
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
