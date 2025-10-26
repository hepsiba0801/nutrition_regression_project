"""
Flask server exposing simple prediction API for the frontend.
Run: python server.py
Requires: flask, flask_cors, joblib, pandas, numpy
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import os

# serve static frontend from frontend/ folder
app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)

# locate model files (assumes they are in working dir, models/, or outputs/models/)
MODEL_PATHS = [
    'linear_regression_model.joblib',
    os.path.join('models', 'linear_regression_model.joblib'),
    os.path.join('outputs', 'models', 'linear_regression_model.joblib')
]
SCALER_PATHS = [
    'scaler.joblib',
    os.path.join('models', 'scaler.joblib'),
    os.path.join('outputs', 'models', 'scaler.joblib')
]
FEATURES_PATHS = [
    'features.joblib',
    os.path.join('models', 'features.joblib'),
    os.path.join('outputs', 'models', 'features.joblib')
]
DATASET_PATHS = [
    'Indian_Food_Nutrition_Processed.csv',
    'Indian_Food_Nutrition_Predicted.csv',
    os.path.join('nutrition_regression_project', 'Indian_Food_Nutrition_Processed.csv')
]

# load model, scaler, features, dataset
model = None
scaler = None
FEATURES = None
DF = None


def _locate(paths):
    for p in paths:
        if os.path.exists(p):
            return p
    return None

# load artifacts
model_file = _locate(MODEL_PATHS)
scaler_file = _locate(SCALER_PATHS)
features_file = _locate(FEATURES_PATHS)

if model_file and scaler_file and features_file:
    model = joblib.load(model_file)
    scaler = joblib.load(scaler_file)
    FEATURES = joblib.load(features_file)
else:
    # attempt to load from current project outputs
    print('Warning: Model/scaler/features not found in expected locations. Please run training (main.py) first and ensure model files are saved.')

# load dataset
dataset_file = _locate(DATASET_PATHS)
if dataset_file:
    DF = pd.read_csv(dataset_file)
else:
    print('Warning: Dataset CSV not found. Some API endpoints will be limited.')


def calculate_nutritional_score_row(row):
    # fallback score from data if available
    return float(row.get('Nutritional_Score', 0))


def interpret_score(score):
    if score >= 80:
        return 'Excellent'
    elif score >= 70:
        return 'Very Good'
    elif score >= 60:
        return 'Good'
    elif score >= 50:
        return 'Fair'
    elif score >= 40:
        return 'Poor'
    else:
        return 'Very Poor'


@app.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.get_json(force=True)
    try:
        calories = float(data.get('calories', 0))
        protein = float(data.get('protein', 0))
        carbs = float(data.get('carbs', 0))
        sugar = float(data.get('sugar', 0))
    except Exception as e:
        return jsonify({'error': 'invalid input', 'detail': str(e)}), 400

    if model is None or scaler is None:
        return jsonify({'error': 'model not loaded. Run training and place model files in project root or outputs/models.'}), 500

    X_input = np.array([[calories, protein, carbs, sugar]])
    X_scaled = scaler.transform(X_input)
    score = float(model.predict(X_scaled)[0])
    score = max(0.0, min(100.0, score))
    category = interpret_score(score)

    # find top 2 matches using Euclidean distance on raw features
    matches = []
    if DF is not None:
        input_vals = np.array([calories, protein, carbs, sugar])
        features = DF[FEATURES].values
        dists = np.sqrt(((features - input_vals) ** 2).sum(axis=1))
        idx = np.argsort(dists)[:2]
        for i in idx:
            row = DF.iloc[int(i)].to_dict()
            row_out = {
                'Dish Name': row.get('Dish Name', ''),
                'Calories (kcal)': float(row.get('Calories (kcal)', 0)),
                'Protein (g)': float(row.get('Protein (g)', 0)),
                'Carbohydrates (g)': float(row.get('Carbohydrates (g)', 0)),
                'Free Sugar (g)': float(row.get('Free Sugar (g)', 0)),
                'Nutritional_Score': float(row.get('Nutritional_Score', 0)),
                'distance': float(dists[int(i)])
            }
            matches.append(row_out)

    return jsonify({'score': round(score, 4), 'category': category, 'matches': matches})


@app.route('/api/search', methods=['GET'])
def api_search():
    q = request.args.get('q', '').strip().lower()
    if DF is None:
        return jsonify({'error': 'dataset not loaded'}), 500
    if not q:
        return jsonify({'results': []})
    res = DF[DF['Dish Name'].str.lower().str.contains(q, na=False)][['Dish Name', 'Nutritional_Score']].head(10)
    return jsonify({'results': res.to_dict(orient='records')})


# Serve static frontend
@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')


@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('frontend', path)


if __name__ == '__main__':
    print('Starting server on http://127.0.0.1:5000')
    print('Open http://127.0.0.1:5000 in your browser')
    app.run(host='0.0.0.0', port=5000, debug=True)
