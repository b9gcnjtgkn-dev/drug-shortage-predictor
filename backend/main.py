from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import pickle
import os

app = FastAPI(title="Drug Shortage Predictor API")

# Allow CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Models
MODEL_PATH = "ai_model/shortage_model.pkl"
VEC_PATH = "ai_model/vectorizer.pkl"
DATA_PATH = "data/training_data.csv"

model = None
vectorizer = None

if os.path.exists(MODEL_PATH) and os.path.exists(VEC_PATH):
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(VEC_PATH, "rb") as f:
        vectorizer = pickle.load(f)
else:
    print("Warning: Model files not found. Ensure train.py has been run.")

class PredictionRequest(BaseModel):
    termination_reason: str

@app.get("/")
def read_root():
    return {"message": "Drug Shortage Predictor API is running."}

@app.post("/api/predict")
def predict_shortage(request: PredictionRequest):
    if not model or not vectorizer:
        raise HTTPException(status_code=500, detail="Model not loaded.")
        
    reason = request.termination_reason
    # Transform text to features
    features = vectorizer.transform([reason]).toarray()
    
    # Predict
    prob = model.predict_proba(features)[0][1] # Probability of shortage (class 1)
    prediction = int(model.predict(features)[0])
    
    return {
        "termination_reason": reason,
        "shortage_risk_probability": round(prob, 2),
        "high_risk": bool(prediction)
    }

@app.get("/api/historical")
def get_historical_data(limit: int = 50):
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=404, detail="Data not found.")
        
    df = pd.read_csv(DATA_PATH)
    # Convert NaN to string to avoid JSON errors
    df = df.fillna("Unknown")
    
    # Sort or format if needed. Returning raw dict for now.
    records = df.head(limit).to_dict(orient="records")
    return {"data": records}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
