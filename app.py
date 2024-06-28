import streamlit as st
import pickle
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load the saved model, tokenizer, and label encoder
model = load_model('spam_detector_model.keras', compile=False)

with open('tokenizer.pkl', 'rb') as tokenizer_file:
    tokenizer = pickle.load(tokenizer_file)

with open('label_encoder.pkl', 'rb') as encoder_file:
    label_encoder = pickle.load(encoder_file)

# Define the maximum sequence length (same as used during training)
max_length = 500  # Update this if max_length was set differently

# Function to preprocess and predict spam
def predict_spam(email_text):
    # Clean and tokenize the input email text
    email_seq = tokenizer.texts_to_sequences([email_text])
    email_padded = pad_sequences(email_seq, maxlen=max_length, padding='post')
    
    # Predict using the loaded model
    prediction = model.predict(email_padded)[0][0]
    return 'Spam' if prediction > 0.5 else 'Not Spam'

# Streamlit app
st.title('Email Spam Detector')

# Input email text
email_text = st.text_area("Enter the email text:")

# Predict button
if st.button('Predict'):
    result = predict_spam(email_text)
    st.write(f'The email is: {result}')
