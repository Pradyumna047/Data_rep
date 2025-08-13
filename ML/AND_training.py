# -*- coding: utf-8 -*-
"""
Created on Mon Aug 11 23:15:49 2025

@author: DELL
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

X_3_inputs = np.array([[0,0,0],[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0],[1,1,1]])
y_3_inputs = np.array([0, 0, 0, 0, 0, 0, 0, 1])


X_2_inputs = np.array([[0,0], [0,1], [1,0], [1,1]])
y_2_inputs = np.array([0, 0, 0, 1])
X_2_inputs_padded = np.pad(X_2_inputs, pad_width=((0,0), (0,1)), mode='constant', constant_values=1)

X_train = np.vstack([X_3_inputs, X_2_inputs_padded])
y_train = np.hstack([y_3_inputs, y_2_inputs])

model = Sequential([
    Input(shape=(3,)),
    Dense(16, activation='relu'), 
    Dense(8, activation='relu'),
    Dense(1, activation='sigmoid')
])


model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

print("Training the model...")
history = model.fit(X_train, y_train, epochs=3000, batch_size=4, verbose=0)
print("Model training complete.")

final_accuracy = history.history['accuracy'][-1]
print(f"Final training accuracy: {final_accuracy:.2f}")

if final_accuracy == 1.0:
    print("Saving training model")
    model.save('and_model.keras')
else:
    print("Run again.")