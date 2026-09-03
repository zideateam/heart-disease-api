# Heart Disease Prediction API

A Dockerized FastAPI application that predicts the possible presence of heart disease from 13 patient health features. The project uses a trained scikit-learn Logistic Regression model and is deployed on Render.

**Live API documentation:** https://heart-disease-detector-logistic.onrender.com/docs

> **Disclaimer:** This is an academic machine-learning project. It is not medical advice and must not be used for diagnosis, treatment, or clinical decisions.

## Features

* `GET /health` — checks whether the API and model are available.
* `GET /info` — shows the model type and required input features.
* `POST /predict` — returns `heart_disease: true` or `false`.
* Pydantic validation for API input.
* Swagger UI documentation at `/docs`.
* Docker and Docker Compose support for local use.

## Project Structure

```text
.
├── model/
│   └── heart_model.joblib
├── main.py
├── schemas.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .dockerignore
```

## Run Locally with Docker

### Prerequisites

* Docker Desktop installed and running
* Hardware virtualization enabled

### Build and start

```bash
docker compose up --build
```

Open the local Swagger UI:

```text
http://localhost:8000/docs
```

Stop the service:

```bash
docker compose down
```

## API Endpoints

| Method | Endpoint   | Description                   |
| ------ | ---------- | ----------------------------- |
| `GET`  | `/health`  | API and model readiness check |
| `GET`  | `/info`    | Model and feature information |
| `POST` | `/predict` | Heart-disease prediction      |

## Prediction Example

Send a `POST` request to `/predict` with JSON data:

```json
{
  "age": 63,
  "sex": 1,
  "cp": 3,
  "trestbps": 145,
  "chol": 233,
  "fbs": 1,
  "restecg": 0,
  "thalach": 150,
  "exang": 0,
  "oldpeak": 2.3,
  "slope": 0,
  "ca": 0,
  "thal": 1
}
```

Example response:

```json
{
  "heart_disease": true
}
```

## Test the Deployed API

```powershell
Invoke-RestMethod `
  -Uri "https://heart-disease-detector-logistic.onrender.com/health" `
  -Method Get
```

For an interactive test interface, open:

```text
https://heart-disease-detector-logistic.onrender.com/docs
```

## Technology Stack

* Python
* FastAPI
* Pydantic
* scikit-learn
* Joblib
* Docker and Docker Compose
* Render

## Author

Created as a FastAPI, Docker, and cloud-deployment learning project.
