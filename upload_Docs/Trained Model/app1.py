import pickle
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained model, label encoder, and scaler
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('label_encoder.pkl', 'rb') as le_file:
    label_encoder = pickle.load(le_file)

with open('scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)


class InputData(BaseModel):
    bloodGlucose: float = 0
    HBA1C: float = 0
    systolicBp: float = 0
    DiastolicBP: float = 0
    LDL: float = 0
    HDL: float = 0
    Triglycerides: float = 0
    Haemoglobin: float = 0
    MuscularCorpusValue: float = 0

@app.post("/predict")
async def predict(data: InputData):
    features = [
        data.bloodGlucose, data.HBA1C, data.systolicBp, data.DiastolicBP,
        data.LDL, data.HDL, data.Triglycerides, data.Haemoglobin, data.MuscularCorpusValue
    ]
    
    features = np.array(features).reshape(1, -1)
    

    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)

    predicted_label = label_encoder.inverse_transform(prediction)
    
    return {"prediction": predicted_label.tolist()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


# uvicorn app1:app --reload --host 0.0.0.0 --port 8000 
# Manual Entry