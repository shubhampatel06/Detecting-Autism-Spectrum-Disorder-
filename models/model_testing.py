# models/model_testing.py
import tensorflow as tf
import numpy as np
import cv2
import joblib
import os

def preprocess_image(image_path):
    """
    Preprocess the image for both CNN and SVM models.
    Returns:
        - img_cnn: preprocessed image with shape (1, 128, 128, 3)
        - img_svm: flattened image with shape (1, 49152)
    """
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError(f"Failed to read image at: {image_path}")
    
    img = cv2.resize(img, (128, 128))
    img_normalized = img / 255.0

    img_cnn = np.expand_dims(img_normalized, axis=0)  # For CNN (batch, 128, 128, 3)
    img_svm = img_normalized.reshape(1, -1)           # For SVM (batch, 49152)

    return img_cnn, img_svm

def predict_image(image_path, model_type='cnn'):
    """
    Predict the class of an image using either CNN or SVM model.

    Args:
    - image_path (str): Path to the input image.
    - model_type (str): 'cnn' or 'svm'

    Returns:
    - str: Predicted class label
    """
    img_cnn, img_svm = preprocess_image(image_path)

    if model_type == 'cnn':
        model_path = 'models/trained_model.h5'
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"CNN model not found at: {model_path}")
        model = tf.keras.models.load_model(model_path)
        prediction = model.predict(img_cnn)
        result = 'Autistic' if prediction[0][0] > 0.5 else 'Non-Autistic'

    elif model_type == 'svm':
        model_path = 'models/svm_model.pkl'
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"SVM model not found at: {model_path}")
        svm_model = joblib.load(model_path)
        prediction = svm_model.predict(img_svm)
        result = 'Autistic' if prediction[0] == 1 else 'Non-Autistic'

    else:
        raise ValueError("Invalid model_type. Use 'cnn' or 'svm'.")

    return result