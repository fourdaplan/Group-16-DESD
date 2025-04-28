# /audio_model/train.py

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv1D, MaxPooling1D
from sklearn.model_selection import train_test_split

# Define paths
data_dir = './audio_dataset'  # Expected to have 'features.npy' and 'labels.npy'
model_save_path = './audio_model.h5'

# Load data
features = np.load(os.path.join(data_dir, 'features.npy'))  # Shape: (n_samples, time_steps, 1)
labels = np.load(os.path.join(data_dir, 'labels.npy'))

# Split the data
X_train, X_val, y_train, y_val = train_test_split(features, labels, test_size=0.2, random_state=42)

# Model architecture
model = Sequential([
    Conv1D(16, kernel_size=3, activation='relu', input_shape=(features.shape[1], 1)),
    MaxPooling1D(pool_size=2),
    Dropout(0.3),
    Conv1D(32, kernel_size=3, activation='relu'),
    MaxPooling1D(pool_size=2),
    Dropout(0.3),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(len(np.unique(labels)), activation='softmax')
])

# Compile model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train model
model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=10, batch_size=32)

# Save model
model.save(model_save_path)
print(f'Model saved to {model_save_path}')
