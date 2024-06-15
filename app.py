import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import requests
from io import BytesIO
import json

# Load class indices
with open('class_indices.json') as f:
    class_indices = json.load(f)

# Invert the class indices dictionary for easy lookup
class_names = {v: k for k, v in class_indices.items()}

# Load the model
def load_model():
    model = tf.keras.models.load_model('plant_disease_prediction_model.h5')
    return model

model = load_model()

# Preprocess the image
def preprocess_image(image, target_size=(224, 224)):
    # Resize the image
    img = image.resize(target_size)
    # Convert img to numpy array
    img_array = np.array(img)
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    # Scale the image values to [0, 1]
    img_array = img_array.astype('float32') / 255.
    return img_array

# Predict the class of the image
def predict_image_class(model, image, class_indices):
    preprocessed_img = preprocess_image(image)
    predictions = model.predict(preprocessed_img)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    predicted_class_name = class_indices[str(predicted_class_index)]
    return predicted_class_name

# Streamlit app
st.title("Plant Disease Detection")
st.write("Upload an image of a plant leaf to detect its disease.")

# Image upload section
uploaded_file = st.file_uploader("Choose an image from your computer...", type="jpg")

# URL input section
url = st.text_input("Or enter an image URL:")

image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
elif url:
    try:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
    except Exception as e:
        st.write("Invalid URL or image could not be loaded.")

if image is not None:
    st.image(image, caption='Uploaded Image', use_column_width=True)
    st.write("Classifying...")
    label = predict_image_class(model, image, class_indices)
    st.write(f"Prediction: {label}")
