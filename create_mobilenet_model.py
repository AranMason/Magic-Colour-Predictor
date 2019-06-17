import numpy as np
import keras
from keras import backend as K
from keras.models import Model
from keras.layers import Activation,GlobalAveragePooling2D
from keras.layers.core import Dense
from keras.optimizers import Adam
from keras.metrics import categorical_crossentropy
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from keras.layers.normalization import BatchNormalization
from keras.applications.mobilenet import preprocess_input
import json
from sklearn.metrics import confusion_matrix
import itertools

import datetime

now = datetime.datetime.now()
LOG_DIR = './logs/mobile_net/%d' % now.strftime("%Y-%m-%d %H:%M")

epochs = 60

train_path = 'mtg/test'

IDG = ImageDataGenerator(validation_split=0.2, preprocessing_function=preprocess_input)

train_batches = IDG.flow_from_directory(train_path,
										target_size=(224,224),
										color_mode='rgb',
										batch_size=32,
										class_mode='categorical',
										shuffle=True)

valid_batches = IDG.flow_from_directory(train_path,
										target_size=(224, 224),
										batch_size=32,
										subset='validation')

print("Classes: ", train_batches.class_indices)

file_classes = train_batches.class_indices
#
# Based off: https://towardsdatascience.com/transfer-learning-using-mobilenet-and-keras-c75daf7ff299
#
base_model = keras.applications.mobilenet.MobileNet(weights='imagenet', include_top=False)

#Convert to a Sequential Model Type, remove the top layer

x=base_model.output
x=GlobalAveragePooling2D()(x)
x=Dense(1024,activation='relu')(x) #we add dense layers so that the model can learn more complex functions and classify for better results.
x=Dense(1024,activation='relu')(x) #dense layer 2
x=Dense(512,activation='relu')(x) #dense layer 3
preds=Dense(len(file_classes),activation='softmax')(x) #final layer with softmax activation

model = Model(inputs=base_model.input, outputs=preds)

for layer in model.layers:
    layer.trainable=False

for layer in model.layers[-4:]:
    layer.trainable=True

model.summary()

model.compile(Adam(lr=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

step_size_train = train_batches.n//train_batches.batch_size

model.fit_generator(train_batches,
					steps_per_epoch=step_size_train,
					validation_data=valid_batches,
					epochs=epochs,
					callbacks=[keras.callbacks.TensorBoard(log_dir=LOG_DIR, histogram_freq=0, write_images=True)])


json_model = model.to_json()
with open('models/model.json', 'w') as json_file:
	json_file.write(json_model)

model.save_weights('models/model_weights.h5')

model.save('models/model_complete.h5')
print("Saved Model")

# Saving Classes for reference later

with open('models/classes.json', 'w') as outfile:
	print(type(file_classes))
	json.dump(file_classes, outfile)

