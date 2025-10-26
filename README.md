# 🍛 Indian Food Nutrition Predictor

A professional Linear Regression ML model + interactive web UI for predicting nutritional quality scores and finding similar dishes in the Indian cuisine dataset.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Model Performance](#model-performance)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)

---

## 🎯 Overview

This project combines **machine learning** with a **modern web UI** to predict nutritional quality scores for Indian dishes. Given 4 nutritional inputs (Calories, Protein, Carbohydrates, Sugar), the model predicts a score (0–100) and returns the top 2 most similar dishes from a dataset of **1,014 Indian dishes**.

**Use cases:**
- Predict nutritional quality of a new dish
- Find similar healthy alternatives
- Compare nutritional profiles
- Explore Indian cuisine nutrition

---

## ✨ Features

### Model
- ✅ **Linear Regression** trained on 1,014 Indian dishes
- ✅ **82.5% accuracy** (Test R² = 0.8252)
- ✅ Weighted nutritional scoring formula
- ✅ Model persistence (joblib)

### Web UI
- ✅ **Professional dark theme** with glassmorphism design
- ✅ **Animated meter** showing predicted nutritional score
- ✅ **Top 2 matching dishes** with similarity metrics
- ✅ **Responsive grid layout** (desktop & mobile)
- ✅ **Real-time predictions** via Flask API

### API
- ✅ `POST /api/predict` — Predict score + find matches
- ✅ `GET /api/search` — Search dishes by name
- ✅ CORS enabled for cross-origin requests
- ✅ Single Flask process serves both frontend & API

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3.11+, Flask 3.1+, Flask-CORS |
| **ML** | scikit-learn, pandas, numpy, joblib |
| **Frontend** | HTML5, CSS3, JavaScript (vanilla) |
| **Visualization** | matplotlib, seaborn |
| **Dataset** | CSV (1,014 Indian dishes) |

---

## 📂 Project Structure

```
nutrition_regression_project/
├── Indian_Food_Nutrition_Processed.csv    # Dataset (1,014 dishes)
├── config.py                              # Configuration (paths, features)
├── data_loader.py                         # DataLoader class
├── model_trainer.py                       # ModelTrainer class
├── main.py                                # Training script
├── app.py                                 # CLI prediction app
├── server.py                              # Flask API + frontend server
├── requirements.txt                       # Python dependencies
├── models/                                # Trained artifacts
│   ├── linear_regression_model.joblib
│   ├── scaler.joblib
│   ├── features.joblib
│   └── dishes.joblib
├── frontend/                              # Web UI
│   ├── index.html                         # Main page
│   ├── styles.css                         # Modern styling
│   ├── script.js                          # Frontend logic
│   └── README.md                          # Frontend notes
├── Indian_Food_Nutrition_Prediction.ipynb # Jupyter Notebook (Colab)
└── README.md                              # This file
```

---

## 🔧 Installation

### Prerequisites
- Python 3.11+
- pip or uv package manager
- Git

### Steps

1. **Clone repository**:
   ```bash
   git clone <repo-url>
   cd nutrition_regression_project
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\Activate.ps1
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   # or with uv
   uv pip install -r requirements.txt
   ```

---

## 🚀 Usage

### Option 1: Web UI (Recommended) ⭐

Start the Flask server (serves both API & frontend):

```bash
python server.py
```

Open browser: **http://127.0.0.1:5000**

**Features:**
- Enter Calories, Protein, Carbs, Sugar
- Click "Predict" → instant score + top 2 matches
- Animated meter shows score 0–100
- Match cards show similar dishes

### Option 2: CLI App

Interactive command-line interface:

```bash
python app.py
```

**Menu options:**
1. Enter nutritional values manually
2. Search for dish in dataset
3. Exit

### Option 3: Jupyter Notebook (Google Colab)

Run in Google Colab:

```bash
# File: Indian_Food_Nutrition_Prediction.ipynb
# Upload to Colab and run cells sequentially
```

**Features:**
- Step-by-step EDA & training
- Dataset upload (Colab file picker)
- Model training with visualizations
- Interactive predictions

### Option 4: Training Only

Train a fresh model:

```bash
python main.py
```

**Output:** Trained model files in `models/`

---

## 📊 Model Performance

### Training Results

| Metric | Train | Test |
|--------|-------|------|
| **R² Score** | 0.8099 (80.99%) | 0.8252 (82.52%) ⭐ |
| **RMSE** | 4.9117 | 4.6388 |
| **MAE** | 3.6232 | 3.6323 |
| **Samples** | 811 | 203 |

### Feature Importance (Coefficients)

| Feature | Coefficient | Impact |
|---------|-------------|--------|
| Carbohydrates (g) | +5.7302 | ↑ Positive |
| Protein (g) | +5.6154 | ↑ Positive |
| Free Sugar (g) | -5.7391 | ↓ Negative |
| Calories (kcal) | -7.0194 | ↓ Negative |

### Nutritional Score Categories

| Range | Category | Rating |
|-------|----------|--------|
| 80–100 | Excellent | 🌟 |
| 70–79 | Very Good | ✅ |
| 60–69 | Good | 👍 |
| 50–59 | Fair | ⚖️ |
| 40–49 | Poor | ⚠️ |
| 0–39 | Very Poor | ❌ |

---

## 🎯 Scoring System

The nutritional score is calculated using a **weighted formula**:

- **Protein (35%)**: Higher is better (scale: 0-20g)
- **Calories (25%)**: Lower is better (scale: 0-500 kcal)
- **Carbohydrates (25%)**: Optimal 30-50g range
- **Sugar (15%)**: Lower is better (scale: 0-15g)

**Formula:**
```
score = (protein_score × 0.35) + (calorie_score × 0.25) + 
        (carb_score × 0.25) + (sugar_score × 0.15)
```

---

## 🔌 API Documentation

### Predict Score

**Endpoint:** `POST /api/predict`

**Request:**
```json
{
  "calories": 280,
  "protein": 25,
  "carbs": 30,
  "sugar": 10
}
```

**Response:**
```json
{
  "score": 78.31,
  "category": "Very Good",
  "matches": [
    {
      "Dish Name": "Moong Bean Dosa",
      "Calories (kcal)": 275,
      "Protein (g)": 26,
      "Carbohydrates (g)": 28,
      "Free Sugar (g)": 9,
      "Nutritional_Score": 75.2
    },
    {
      "Dish Name": "Chicken Walnut Sandwich",
      "Calories (kcal)": 285,
      "Protein (g)": 24,
      "Carbohydrates (g)": 32,
      "Free Sugar (g)": 11,
      "Nutritional_Score": 76.8
    }
  ]
}
```

### Search Dishes

**Endpoint:** `GET /api/search?q=dosa`

**Response:**
```json
{
  "results": [
    {
      "Dish Name": "Moong Bean Dosa",
      "Nutritional_Score": 75.2
    },
    {
      "Dish Name": "Masala Dosa",
      "Nutritional_Score": 62.1
    }
  ]
}
```

---

## 🌐 Deployment

### Local Development

```bash
python server.py
# Visit http://127.0.0.1:5000
```

### Production (with Gunicorn)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 server:app
```

### Docker

**Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "server.py"]
```

**Build & run:**
```bash
docker build -t nutrition-predictor .
docker run -p 5000:5000 nutrition-predictor
```

### Cloud Deployment (Heroku, Railway, Render)

1. Push to GitHub
2. Connect repository
3. Set buildpack to Python
4. Deploy

**Procfile:**
```
web: gunicorn -w 1 -t 120 server:app
```

---

## 📚 Documentation Files

- **`FINAL_PROJECT_SUMMARY.md`** — Complete project overview
- **`COMPLETE_GUIDE.md`** — Detailed user guide with examples
- **`frontend/README.md`** — Frontend setup notes
- **`Indian_Food_Nutrition_Prediction.ipynb`** — Jupyter Notebook for Colab

---

## 🎓 Learning Outcomes

This project demonstrates:
- ✅ Data loading & preprocessing (pandas)
- ✅ Feature engineering (weighted scoring formula)
- ✅ Train/test split & scaling (scikit-learn)
- ✅ Model training & evaluation (Linear Regression)
- ✅ Model persistence (joblib)
- ✅ REST API design (Flask)
- ✅ Frontend-backend integration (fetch API)
- ✅ Responsive UI/UX (HTML/CSS/JS)
- ✅ Similarity matching (Euclidean distance)

---

## 📦 Dataset

**Source:** Indian Food Nutrition (1,014 dishes)

**Columns:** 12 nutritional features
- Dish Name
- Calories (kcal)
- Protein (g)
- Carbohydrates (g)
- Fat (g)
- Fiber (g)
- Free Sugar (g)
- Salt (g)
- Saturated Fat (g)
- Trans Fat (g)
- Cholesterol (mg)
- Iron (mg)

---

## 🤝 Contributing

Contributions welcome! Areas to improve:
- [ ] Add more dish categories
- [ ] Implement k-NN for better matching
- [ ] Add user authentication
- [ ] Deploy to cloud
- [ ] Mobile app (React Native)
- [ ] Advanced visualizations

---

## ✅ Checklist

- [x] Data loading & exploration
- [x] Nutritional score calculation
- [x] Linear Regression model training
- [x] Model evaluation & metrics
- [x] Model persistence (joblib)
- [x] CLI prediction app
- [x] REST API (Flask + CORS)
- [x] Professional web UI (HTML/CSS/JS)
- [x] Animated components & responsive design
- [x] Dish matching algorithm (Euclidean distance)
- [x] Jupyter Notebook (Colab-ready)
- [x] Comprehensive documentation
- [x] Git repository

---

**🚀 Ready to predict!** Start with: `python server.py` → http://127.0.0.1:5000
