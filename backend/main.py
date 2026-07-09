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

# Resolve paths correctly regardless of where uvicorn is run from
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ai_model", "shortage_model.pkl")
VEC_PATH = os.path.join(BASE_DIR, "ai_model", "vectorizer.pkl")
DATA_PATH = os.path.join(BASE_DIR, "data", "training_data.csv")

model = None
vectorizer = None

if os.path.exists(MODEL_PATH) and os.path.exists(VEC_PATH):
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(VEC_PATH, "rb") as f:
        vectorizer = pickle.load(f)
else:
    print(f"Warning: Model files not found at {MODEL_PATH}. Ensure train.py has been run.")

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
    features = vectorizer.transform([reason]).toarray()
    
    prob = model.predict_proba(features)[0][1]
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
    df = df.fillna("Unknown")
    records = df.head(limit).to_dict(orient="records")
    return {"data": records}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
