# -*- coding: utf-8 -*-
"""
Created on Sat Aug 16 17:21:12 2025

@author: DELL
"""

import numpy as np
import tensorflow as tf
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

and_model = tf.keras.models.load_model('and_model.keras')
or_model = tf.keras.models.load_model('or_model.keras')
not_model = tf.keras.models.load_model('not_model.keras')

def predict(model, inputs):
    return np.round(model.predict(inputs, verbose=0)).astype(int)

def mux_2_to_1(i0, i1, s):
    not_s = predict(not_model, np.array([[s]]))

    # (I0 AND (NOT S))
    term1_input = np.array([[i0, not_s[0][0], 1]])
    term1 = predict(and_model, term1_input)

    # (I1 AND S)
    term2_input = np.array([[i1, s, 1]])
    term2 = predict(and_model, term2_input)

    # (Term1 OR Term2)
    final_or_input = np.array([[term1[0][0], term2[0][0], 0]])
    output = predict(or_model, final_or_input)

    return output[0][0]

i0 = int(input("Enter input I0 (0 or 1): "))
i1 = int(input("Enter input I1 (0 or 1): "))
s = int(input("Enter select line S (0 or 1): "))
    
result = mux_2_to_1(i0, i1, s)
print(f"Output of 2-to-1 MUX: {result}")