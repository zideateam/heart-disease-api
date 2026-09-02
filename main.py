
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException

from schemas import HeartDiseaseInput


# -------------------------------------------------
# Model configuration
# -------------------------------------------------

MODEL_PATH = Path("model/heart_model.joblib")

FEATURES = [
    "age",
    "sex",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalach",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal",
]

model = None


# -------------------------------------------------
# Load the model when the API starts
# -------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model

    if not MODEL_PATH.exists():
        raise RuntimeError(
            f"Model file was not found at: {MODEL_PATH}"
        )

    model = joblib.load(MODEL_PATH)
    print("Heart-disease model loaded successfully.")

    yield

    model = None


# -------------------------------------------------
# Create FastAPI application
# -------------------------------------------------

app = FastAPI(
    title="Heart Disease Prediction API",
    description=(
        "A FastAPI application that predicts the presence "
        "of heart disease using a trained machine-learning model."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


# -------------------------------------------------
# GET /health
# -------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }


# -------------------------------------------------
# GET /info
# -------------------------------------------------

@app.get("/info")
def info():
    return {
        "application": "Heart Disease Prediction API",
        "model_type": type(model).__name__ if model else "Not loaded",
        "prediction_classes": {
            "0": "No heart disease",
            "1": "Heart disease"
        },
        "feature_count": len(FEATURES),
        "features": FEATURES
    }


# -------------------------------------------------
# POST /predict
# -------------------------------------------------

@app.post("/predict")
def predict(patient: HeartDiseaseInput):
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="The prediction model is not available."
        )

    try:
        patient_data = patient.model_dump()

        input_dataframe = pd.DataFrame(
            [[patient_data[feature] for feature in FEATURES]],
            columns=FEATURES
        )

        prediction = int(model.predict(input_dataframe)[0])

        return {
            "heart_disease": bool(prediction)
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(error)}"
        )
