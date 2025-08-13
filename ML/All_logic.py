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

xor_model = tf.keras.models.load_model('xor_model.keras')
xnor_model = tf.keras.models.load_model('xnor_model.keras')
and_model = tf.keras.models.load_model('and_model.keras')
or_model = tf.keras.models.load_model('or_model.keras')
not_model = tf.keras.models.load_model('not_model.keras')
    
print("Model loaded successfully.\n")

user_input = input("\nEnter your inputs: ").strip()

input_values = [int(val) for val in user_input.split()]
and_input = input_values.copy()
if len(input_values) not in [2, 3] or not all(v in [0, 1] for v in input_values):
    print("--> Invalid input.")
    exit()  

if len(input_values) == 2:
    print("(Padding 2-input to 3-input for the model)")
    input_values.append(0)


input_array = np.array([input_values])
xor_prediction = xor_model.predict(input_array, verbose=0)
xnor_prediction = xnor_model.predict(input_array, verbose=0)
or_prediction = or_model.predict(input_array, verbose=0)


if len(and_input) == 2:
    print("(Padding 2-input to 3-input for the AND model)")
    and_input.append(1)
and_array = np.array([and_input])    
and_prediction = and_model.predict(and_array, verbose=0)

xor_result = (xor_prediction > 0.5).astype(int)[0][0]
xnor_result = (xnor_prediction > 0.5).astype(int)[0][0]
and_result = (and_prediction > 0.5).astype(int)[0][0]
or_result = (or_prediction > 0.5).astype(int)[0][0]

nand_input = and_result
nand_prediction = not_model.predict(nand_input.reshape(-1, 1), verbose=0)
nand_result = (nand_prediction > 0.5).astype(int)[0][0]

nor_input = or_result
nor_prediction = not_model.predict(nor_input.reshape(-1, 1), verbose=0)
nor_result = (nor_prediction > 0.5).astype(int)[0][0]
        
print(f"XOR Model prediction for {user_input} is: {xor_result}")
print(f"XNOR Model prediction for {user_input} is: {xnor_result}")
print(f"AND Model prediction for {user_input} is: {and_result}")
print(f"NAND Model prediction for {user_input} is: {nand_result}")
print(f"OR Model prediction for {user_input} is: {or_result}")
print(f"NOR Model prediction for {user_input} is: {nor_result}")