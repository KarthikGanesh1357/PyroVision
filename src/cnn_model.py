import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from PIL import Image, ImageFile
import os

# Enable handling of truncated images
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Function to verify and clean corrupted images
def verify_images(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                with Image.open(filepath) as img:
                    img.verify()  # Verify the image integrity
            except (IOError, SyntaxError):
                print(f"Removing corrupted file: {filepath}")
                os.remove(filepath)

# Clean the dataset directories (train, valid, test)
verify_images(r'C:\pyrovision\data\processed\train')
verify_images(r'C:\pyrovision\data\processed\valid')
verify_images(r'C:\pyrovision\data\processed\test')

train = r'C:\pyrovision\data\processed\train'
valid = r'C:\pyrovision\data\processed\valid'
test =  r'C:\pyrovision\data\processed\test'

# Define image size and batch size
IMG_HEIGHT, IMG_WIDTH = 150, 150
BATCH_SIZE = 16

# Create ImageDataGenerators
train_datagen = ImageDataGenerator(
    rescale=1.0/255,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

valid_datagen = ImageDataGenerator(rescale=1.0/255)
test_datagen = ImageDataGenerator(rescale=1.0/255)

# Load data
train_data = train_datagen.flow_from_directory(
    train,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='binary'
)

valid_data = valid_datagen.flow_from_directory(
    valid,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='binary'
)

test_data = test_datagen.flow_from_directory(
    test,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='binary'
)

# Define the CNN model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
    MaxPooling2D(pool_size=(2, 2)),
    
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')  # Output layer for binary classification
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(
    train_data,
    validation_data=valid_data,
    epochs=1,  # Adjust based on needs
    steps_per_epoch=len(train_data),
    validation_steps=len(valid_data)
)

# Evaluate the model
loss, accuracy = model.evaluate(test_data)
print(f"Test Accuracy: {accuracy * 100:.2f}%")

# Save the model
model.save('wildfire_detection_model.h5')

# Predict function
def predict_image(image_path):
    from tensorflow.keras.preprocessing import image
    import numpy as np

    img = image.load_img(image_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    if prediction[0][0] > 0.5:
        return "Wildfire"
    else:
        return "No Wildfire"