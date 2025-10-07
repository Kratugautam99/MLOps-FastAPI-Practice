---

# MLOps-Dagshub

A streamlined MLOps pipeline integrating version control, model tracking, and reproducibility using **DagsHub**. Ideal for collaborative machine learning workflows and efficient experiment tracking.

## 📚 Table of Contents

- [🚀 Features](#-features)
- [🔧 Tech Stack](#-tech-stack)
- [🏃 Getting Started](#-getting-started)
- [🔗 Quick Access to Dagshub Account](#-quick-access-to-dagshub-account)
- [⚓ Custom API Developments](#-custom-api-developments)
- [🧩 Final Thoughts](#-final-thoughts)


## 🚀 Features

- 📦 Data and model versioning with DVC and Git  
- 🧪 Experiment tracking and reproducibility  
- 📊 Visual insights into model performance  
- 🤝 Seamless collaboration via DagsHub’s web UI  
- 🛠️ CI/CD integration for model deployment (optional extension)  

## 🔧 Tech Stack

- **Python**  
  The core programming language for building and orchestrating all components of your ML workflow—data processing, training scripts, API endpoints, and glue code for tools like DVC and MLflow.

- **DVC (Data Version Control)**  
  A Git-like system for versioning datasets, models, and pipeline stages. It helps you reproduce experiments and collaborate without storing large files in the Git repo, and enables pipeline orchestration.

- **Git**  
  Version control for code and lightweight files. Works in tandem with DVC to manage the code+data+model ecosystem in sync, allowing branching, reverting, and change tracking.

- **DagsHub**  
  A GitHub-integrated platform that brings Git, DVC, and experiment tracking together. Provides a UI to visualize experiments, compare runs, and store datasets and models—think of it as a collaborative MLOps dashboard.

- **MLflow**  
  An experiment tracking tool to log metrics, parameters, artifacts, and models. Lets you compare runs, register models, and optionally serve them via its model registry.

- **FastAPI**  
  A lightweight, high-performance Python web framework. Use it to serve trained models through RESTful API endpoints for real-time or batch predictions.

## 🏃 Getting Started

Clone the repo and enter the directory:

```bash
git clone https://github.com/your_username/MLOps-Dagshub.git
cd MLOps-Dagshub
```

---

## 🔗 Quick Access to Dagshub Account

- 🔍 [View Files](https://dagshub.com/kratugautam99/MLOps-Dagshub)  
- 📂 [Explore Datasets](https://dagshub.com/kratugautam99/MLOps-Dagshub/datasets)  
- 🧪 [Experiment Runs](https://dagshub.com/kratugautam99/MLOps-Dagshub/experiments)  
- 📦 [Registered Models](https://dagshub.com/kratugautam99/MLOps-Dagshub/models)  

---

## ⚓ Custom API Developments

A suite of modular FastAPI services designed for real-world deployment, agentic orchestration, and seamless integration.



### 🩺 **DoctorAPI** — Comprehensive Patient Data Management  
**Purpose:** Full-featured REST API for managing patient records in healthcare systems.

#### 🔧 Key Features
- **CRUD Operations:** Add, edit, delete, and retrieve patient records  
- **Computed Fields:** Auto-calculates BMI and health verdict (Underweight, Normal, Overweight, Obese)  
- **Sorting & Filtering:** Sort by age, height, weight, or BMI  
- **Schema Validation:** Robust Pydantic models ensure data integrity  
- **Persistence:** Lightweight storage via `patients.json`

#### 🧠 Use Cases
- Hospital dashboards  
- Telemedicine platforms  
- Health analytics and reporting



### 👋 **HelloAPI** — Minimal Greeting Service  
**Purpose:** A simple starter API for testing FastAPI setup and deployment.

#### 🔧 Key Features
- **Endpoint:** `/hello/{name}` returns a personalized greeting

#### 🧠 Use Case
- CI/CD pipeline validation  
- FastAPI onboarding for new developers



### 🛡️ **InsuranceAPI** — ML-Powered Risk Prediction  
**Purpose:** Predicts insurance risk or premium category using structured health and lifestyle data.

#### 🔧 Key Features
- **ML Integration:** Uses trained model via `predict_from_model()`  
- **Computed Inputs:** BMI, city tier, lifestyle risk, age group  
- **Endpoints:**  
  - `/predict`: Accepts `UserData`, returns `PredictedResponse` (test via `/docs`)  
  - `/health`: Model health check  
  - `/`: Welcome message

#### 🧠 Use Cases
- Insurance quoting engines  
- Risk segmentation dashboards  
- Agentic decision support systems

#### 🔗 Access Links
- ⚓ [Docker Repository for Initialization](https://hub.docker.com/r/kratuzen/insurance-prediction-api)
- Run Docker Commands first then click below
- ⭕ [API Dashboard](http://localhost:8000/docs)  
- ✔️ [Streamlit GUI](http://localhost:8501/)

---

## 🧩 Final Thoughts

This repository brings together modular, production-ready FastAPI services—DoctorAPI, HelloAPI, and InsuranceAPI—each tailored for real-world use cases in healthcare, testing, and insurance risk modeling. With clean schema validation, computed logic, and ML integration, these APIs are designed for extensibility, agentic orchestration, and seamless deployment.
