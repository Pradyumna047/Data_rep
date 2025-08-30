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
import itertools

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

def generate_and_gate_data(num_inputs):
    
    X = np.array(list(itertools.product([0, 1], repeat=num_inputs)))
    y = np.all(X, axis=1).astype(int)
    return X, y

def create_padded_dataset(max_inputs, padding_value=0):
    
    all_X = []
    all_y = []

    for n in range(2, max_inputs + 1):
        X, y = generate_and_gate_data(n)
        
        pad_width = ((0, 0), (0, max_inputs - n))
        X_padded = np.pad(X, pad_width=pad_width, mode='constant', constant_values=padding_value)
        
        all_X.append(X_padded)
        all_y.append(y)

    X_train = np.vstack(all_X)
    y_train = np.hstack(all_y)
    
    return X_train, y_train

n_max = 12
X_train, y_train = create_padded_dataset(n_max)

permutation = np.random.permutation(len(X_train))
X_train = X_train[permutation]
y_train = y_train[permutation]



model = Sequential([
    Input(shape=(n_max,)),
    Dense(16, activation='relu'),
    Dense(8, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.summary()

history = model.fit(X_train, y_train, epochs=1000, batch_size=8, verbose=0)
final_accuracy = history.history['accuracy'][-1]
print(f"Final training accuracy: {final_accuracy:.4f}")

if final_accuracy > 0.95:
    print("Saving training model")
    model.save('and_model_n_inputs.keras')
else:
    print("Run training again")
