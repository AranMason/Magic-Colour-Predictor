import numpy as np
import keras
from keras import backend as K
from keras.models import Sequential
from keras.layers import Activation
from keras.layers.core import Dense, Flatten
from keras.optimizers import Adam
from keras.metrics import categorical_crossentropy
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from keras.layers.normalization import BatchNormalization
import json
from sklearn.metrics import confusion_matrix
import itertools



epochs = 10

train_path = 'mtg/test'
# valid_path = 'mtg/validate'
# test_path = 'data/test'

IDG = ImageDataGenerator(validation_split=0.2)

train_batches = IDG.flow_from_directory(train_path,
										target_size=(224,224),
										batch_size=10)

valid_batches = IDG.flow_from_directory(train_path,
										target_size=(224, 224),
										batch_size=10,
										subset='validation')

print("Classes: ", train_batches.class_indices)

file_classes = train_batches.class_indices

vgg16_model = keras.applications.vgg16.VGG16()


#Convert to a Sequential Model Type, remove the top layer
model = Sequential()
for layer in vgg16_model.layers[:-1]:
    model.add(layer)

for layer in model.layers:
    layer.trainable = False


model.add(Dense(len(file_classes), activation='softmax', name='predictions'))

model.summary()

model.compile(Adam(lr=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

model.fit_generator(train_batches,
					# steps_per_epoch=4,
					validation_data=valid_batches,
					epochs=epochs,
					shuffle=True,
					verbose=2)


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

