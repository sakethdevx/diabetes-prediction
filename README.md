# Diabetes Prediction App

A production-ready web application for diabetes prediction using machine learning.

## Features
- Gradient Boosting model with optimized hyperparameters
- Interactive web interface with Streamlit
- Comprehensive data preprocessing
- Model performance metrics and visualizations
- Containerized with Docker
- Environment management with pip-tools

## Prerequisites
- Python 3.8+
- Docker (optional, for containerized deployment)

## Installation

### Option 1: Using pip
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Using Docker
```bash
docker build -t diabetes-prediction .
docker run -p 8501:8501 diabetes-prediction
```

## Running the Application
```bash
streamlit run app.py
```

The application will be available at http://localhost:8501

## Project Structure
```
diabetes_prediction/
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
├── app.py
├── diabetes.csv
├── models/
│   └── model.joblib
├── requirements.in
├── requirements.txt
└── setup.sh
```

## License
MIT
