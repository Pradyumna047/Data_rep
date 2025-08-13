# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 11:54:35 2025

@author: DELL
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

X_input = np.array([[0], [1]])
y_input = np.array([1, 0])

X_train = np.vstack([X_input])
y_train = np.hstack([y_input])

model = Sequential([
    Input(shape=(1,)),
    Dense(16, activation='relu'),  
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

print("Training the model...")
history = model.fit(X_train, y_train, epochs=3000, verbose=0)
print("Model training complete.")

final_accuracy = history.history['accuracy'][-1]
print(f"Final training accuracy: {final_accuracy:.2f}")

if final_accuracy == 1.0:
    print("Saving training model")
    model.save('not_model.keras')
else:
    print("Run again.")