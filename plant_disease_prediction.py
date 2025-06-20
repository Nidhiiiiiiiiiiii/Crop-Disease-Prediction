# -*- coding: utf-8 -*-
"""plant-disease-prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1UX9JltHl_orNkUSz9Q4coMQEHcYntKhO
"""

import random
random.seed(0)

import numpy as np
np.random.seed(0)

import tensorflow as tf
tf.random.set_seed(0)

import os
import json
from zipfile import ZipFile
from PIL import Image

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers,models

!pip install kaggle

kaggle_credentials=json.load(open("kaggle.json"))



os.environ['KAGGLE_USERNAME']=kaggle_credentials["username"]
os.environ['Kaggle_key']=kaggle_credentials["key"]

import kagglehub

path = kagglehub.dataset_download("abdallahalidev/plantvillage-dataset")

print("Path to dataset files:", path)

dataset_root = os.path.join(path, "plantvillage dataset")
print(dataset_root)
print("Subfolders in dataset:", os.listdir(dataset_root))

subfolders = os.listdir(dataset_root)

base_dir='plantvillage dataset/color'

data_gen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

img_size = 224
batch_size = 32

color_dir = os.path.join(dataset_root, "color")
classes = os.listdir(color_dir)
num_classes=len(classes)
print(f"Number of classes in 'color': {len(classes)}")
print("First 5 classes:", classes[:5])

import random

sample_class = random.choice(classes)
sample_class_path = os.path.join(color_dir, sample_class)

# List images
image_files = os.listdir(sample_class_path)
print(f"Number of images in class '{sample_class}': {len(image_files)}")
print("First 5 images:", image_files[:5])

import random

sample_class = random.choice(classes)
sample_class_path = os.path.join(color_dir, sample_class)

image_files = os.listdir(sample_class_path)
print(f"Number of images in class '{sample_class}': {len(image_files)}")
print("First 5 images:", image_files[:5])

train_gen = data_gen.flow_from_directory(
    color_dir,
    target_size=(img_size,img_size),
    batch_size=batch_size,
    class_mode='categorical',
    subset='training',
    shuffle=True,
    seed=42
)
val_gen = data_gen.flow_from_directory(
    color_dir,
    target_size=(img_size,img_size),
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation',
    shuffle=True,
    seed=42
)

from tensorflow.keras import layers,models
model=models.Sequential([
    layers.Conv2D(32,(3,3),activation='relu',input_shape=(img_size,img_size,3)),
    layers.MaxPooling2D((2,2)),

    layers.Conv2D(64,(3,3),activation='relu'),
    layers.MaxPooling2D((2,2)),

    layers.Conv2D(128,(3,3),activation='relu'),
    layers.MaxPooling2D((2,2)),

    layers.Flatten(),
    layers.Dense(128,activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(num_classes,activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
model.summary()

history=model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=3
)

import numpy as np
from tensorflow.keras.preprocessing import image

img_path = '/content/Screenshot 2025-05-19 223833.png'

img = image.load_img(img_path, target_size=(224, 224))
img_array = image.img_to_array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0) 

pred = model.predict(img_array)
predicted_class = np.argmax(pred)

class_names = list(train_gen.class_indices.keys())
predicted_class_name = class_names[predicted_class]

print(f"Predicted Class Index: {predicted_class}")
print(f"Predicted Class Name: {predicted_class_name}")
