# -*- coding: utf-8 -*-
"""
Created on Mon Aug 11 23:19:57 2025

@author: DELL
"""

import numpy as np
import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

model = tf.keras.models.load_model('xor_model.keras')
    
print("Model loaded successfully.\n")

user_input = input("\nEnter your three inputs: ").strip()

input_values = [int(val) for val in user_input.split()]
if len(input_values) != 3 or not all(v in [0,1] for v in input_values):
    raise ValueError

input_array = np.array([input_values])
prediction = model.predict(input_array, verbose=0)
result = (prediction > 0.5).astype(int)[0][0]
        
print(f"Model prediction for {input_values} is: {result}")

