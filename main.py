from typing import Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import pickle
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

with open('tokenizer.pkl', 'rb') as tokenizer_file:
    tokenizer = pickle.load(tokenizer_file)

with open('label_encoder.pkl', 'rb') as encoder_file:
    label_encoder = pickle.load(encoder_file)

# Define the maximum sequence length (same as used during training)
max_length = 500 


app = FastAPI()

# Load the saved model, tokenizer, and label encoder
model = load_model('spam_detector_model.keras')


class EmailText(BaseModel): 
    email_text: str

def predict_spam(email_text):
    # Clean and tokenize the input email text
    email_seq = tokenizer.texts_to_sequences([email_text])
    email_padded = pad_sequences(email_seq, maxlen=max_length, padding='post')
    
    # Predict using the loaded model
    prediction = model.predict(email_padded)[0][0]
    print(prediction)
    return 'Spam' if prediction > 0.5 else 'Not Spam'

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/predict")
async def predict(email_text: EmailText):
    try:
        result = predict_spam(email_text.email_text)
        return {"prediction": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))