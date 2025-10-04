import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import numpy as np
import os
import cv2
import joblib

def load_data(data_path, img_size=(64, 64)):
    """
    Load images and labels from the dataset directory.

    Args:
    - data_path (str): Path to the dataset directory.
    - img_size (tuple): Target image size (width, height).

    Returns:
    - Tuple (np.array, np.array): Images and labels as numpy arrays.
    """
    images, labels = [], []
    for label, class_dir in enumerate(['Non-Autistic', 'Autistic']):
        class_path = os.path.join(data_path, class_dir)
        if not os.path.exists(class_path):
            raise FileNotFoundError(f"Directory not found: {class_path}")
        for img_name in os.listdir(class_path):
            img_path = os.path.join(class_path, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_COLOR)
            if img is None:
                print(f"Warning: Unable to read image: {img_path}")
                continue
            img = cv2.resize(img, img_size)
            images.append(img)
            labels.append(label)
    return np.array(images), np.array(labels)

# Path to the dataset
data_path = r"C:\Users\patel\Downloads\autism_detection_mainCopy\dataset"

try:
    # Load and preprocess the data
    IMG_SIZE = (64, 64)
    X, y = load_data(data_path, img_size=IMG_SIZE)
    X = X / 255.0
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # ----- CNN Model -----
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3)),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    print("Training CNN model...")
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=3, batch_size=32, verbose=1)

    os.makedirs("models", exist_ok=True)
    model.save('models/trained_model.h5')
    print("✅ CNN model saved as 'models/trained_model.h5'.")

    # ----- SVM Model -----
    print("Preparing balanced data for SVM...")

    max_samples_per_class = 150  # Adjust based on dataset size & performance

    class0_idx = np.where(y == 0)[0]
    class1_idx = np.where(y == 1)[0]

    np.random.seed(42)
    sampled_class0_idx = np.random.choice(class0_idx, size=min(max_samples_per_class, len(class0_idx)), replace=False)
    sampled_class1_idx = np.random.choice(class1_idx, size=min(max_samples_per_class, len(class1_idx)), replace=False)

    sampled_indices = np.concatenate([sampled_class0_idx, sampled_class1_idx])

    X_svm = X.reshape(X.shape[0], -1)[sampled_indices]
    y_svm = y[sampled_indices]

    X_train_svm, X_test_svm, y_train_svm, y_test_svm = train_test_split(
        X_svm, y_svm, test_size=0.2, random_state=42, stratify=y_svm
    )

    print("Training SVM model...")
    svm_model = SVC(kernel='linear', probability=True)
    svm_model.fit(X_train_svm, y_train_svm)
    print("✅ Finished SVM training.")

    y_pred_svm = svm_model.predict(X_test_svm)
    svm_accuracy = accuracy_score(y_test_svm, y_pred_svm)

    print(f"✅ SVM Accuracy: {svm_accuracy * 100:.2f}%")
    print("Classification Report (SVM):")
    print(classification_report(y_test_svm, y_pred_svm))

    joblib.dump(svm_model, 'models/svm_model.pkl')
    print("✅ SVM model saved as 'models/svm_model.pkl'.")

except FileNotFoundError as e:
    print(f"❌ Error: {e}")
except Exception as e:
    print(f"❌ An unexpected error occurred: {e}")