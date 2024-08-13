from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
 
with open('tokenizer.pkl', 'rb') as tokenizer_file:
    tokenizer = pickle.load(tokenizer_file)

with open('label_encoder.pkl', 'rb') as encoder_file:
    label_encoder = pickle.load(encoder_file)

# Define the maximum sequence length (same as used during training)
max_length = 500 


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to your needs (e.g., specific domains instead of "*")
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

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

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('frontend/index.html')

@app.post("/predict")
async def predict(email_text: EmailText):
    try:
        result = predict_spam(email_text.email_text)
        return {"prediction": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))