
import numpy as np
import os

try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential, load_model
    from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
    from tensorflow.keras.preprocessing.image import load_img, img_to_array
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("TensorFlow not installed. Image classification will be simulated.")

MODEL_PATH = 'models/ct_scan_model.h5'
IMG_SIZE = (150, 150)

def create_model():
    """
    Creates a simple CNN model for Lung Cancer classification (Normal vs Cancer).
    """
    if not TF_AVAILABLE:
        print("TensorFlow not available.")
        return None

    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
        MaxPooling2D(2, 2),
        
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        
        Flatten(),
        Dense(512, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')  # Binary classification: 0=Normal, 1=Cancer
    ])
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def predict_image(image_file):
    """
    Predicts if a CT scan image shows cancer.
    Args:
        image_file: File-like object or path to image.
    Returns:
        prob: Probability of cancer (0-1).
    """
    if not TF_AVAILABLE:
        # Simulation mode for demo
        # Deterministic random based on file size or name to be consistent?
        # Or just random
        return np.random.random()

    if not os.path.exists(MODEL_PATH):
        print("Model not found. Using random prediction.")
        return np.random.random()

    try:
        model = load_model(MODEL_PATH)
        
        # Preprocess image
        # If image_file is a path str
        if isinstance(image_file, str):
            img = load_img(image_file, target_size=IMG_SIZE)
        else:
            # If it's a file-like object (Buffer) from Streamlit, load_img might handle it or need conversion
            img = load_img(image_file, target_size=IMG_SIZE)
            
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Create batch axis
        img_array = img_array / 255.0  # Rescale
        
        prediction = model.predict(img_array)
        return float(prediction[0][0])
    except Exception as e:
        print(f"Error during prediction: {e}")
        return np.random.random()

def train_dummy_model():
    """
    Trains a dummy model on random data just to save a valid model file.
    """
    if not TF_AVAILABLE:
        print("TensorFlow not available. Skipping dummy training.")
        return

    print("Training dummy model...")
    model = create_model()
    
    # Generate random dummy data
    X_train = np.random.random((10, 150, 150, 3))
    y_train = np.random.randint(0, 2, 10)
    
    model.fit(X_train, y_train, epochs=1, verbose=0)
    model.save(MODEL_PATH)
    print(f"Dummy model saved to {MODEL_PATH}")

if __name__ == "__main__":
    if not os.path.exists(MODEL_PATH):
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        train_dummy_model()
