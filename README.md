# Diabetes Prediction App

A production-ready web application for diabetes prediction using machine learning.

## Features
- Interactive UI with real-time predictions
- Model accuracy: ~86.6%
- Feature importance visualization
- Confusion matrix and performance metrics
- Cross-platform support (Windows/macOS/Linux)
- Containerized with Docker

## Prerequisites
- Python 3.8+ (for pip installation)
- pip (Python package manager)
- Git (for cloning the repository)
- Docker (for containerized deployment)

## Deployment Options

### Option 1: Streamlit Cloud (Recommended)

1. **Fork** this repository to your GitHub account
2. Go to [Streamlit Cloud](https://share.streamlit.io/)
3. Click "New app" and select your forked repository
4. Set the branch to `main`
5. Set the main file path to `app.py`
6. Click "Deploy!"

### Option 2: Local Installation

### Method 1: Using pip (macOS/Linux/Windows)

#### 1. Clone the Repository
```bash
git clone https://github.com/saketh-005/diabetes-prediction.git
cd diabetes-prediction
```

#### 2. Set Up Virtual Environment

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
.\venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
# Install pip-tools first
pip install pip-tools

# Install all dependencies
pip-sync
```

#### 4. Run the Application
```bash
streamlit run app.py
```
The application will be available at: http://localhost:8501

#### 5. Stopping the Application

**macOS/Linux/Windows (in the terminal where it's running):**
1. Press `Ctrl + C` to stop the Streamlit server
2. Deactivate the virtual environment (if needed):
   ```bash
   deactivate
   ```

### Method 2: Using Docker

#### 1. Clone the Repository
```bash
git clone https://github.com/saketh-005/diabetes-prediction.git
cd diabetes-prediction
```

#### 2. Build the Docker Image
```bash
docker build -t diabetes-prediction .
```

#### 3. Run the Container
```bash
docker run -p 8501:8501 diabetes-prediction
```
The application will be available at: http://localhost:8501

#### 4. Stopping the Container
1. Find the container ID:
   ```bash
   docker ps
   ```
2. Stop the container:
   ```bash
   docker stop <container_id>
   ```
3. (Optional) Remove the container:
   ```bash
   docker rm <container_id>
   ```

## Project Structure
```
diabetes-prediction/
├── .dockerignore
├── .env.example       # Example environment variables
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

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for full details.

Copyright (c) 2025 Saketh Jangala
