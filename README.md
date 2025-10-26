# Nutrition Regression Model

A Linear Regression model to predict nutritional quality scores for dishes based on their nutritional values.

## 📊 Overview

This project trains a Linear Regression model using:
- **Dataset**: Indian Food Nutrition (1,014 dishes)
- **Features**: Calories, Protein, Carbohydrates, Sugar
- **Target**: Nutritional Quality Score (0-100)

## 🎯 Scoring System

The nutritional score is calculated based on:
- **Protein (35%)**: Higher is better (scale: 0-20g)
- **Calories (25%)**: Lower is better (scale: 0-500 kcal)
- **Carbohydrates (25%)**: Optimal 30-50g range
- **Sugar (15%)**: Lower is better (scale: 0-15g)

Score ranges:
- **80-100**: Excellent 🌟
- **70-79**: Very Good ✅
- **60-69**: Good 👍
- **50-59**: Fair ⚖️
- **40-49**: Poor ⚠️
- **0-39**: Very Poor ❌

## 🚀 Quick Start

### 1. Train the Model

```bash
python main.py
```

This will:
- Load the dataset
- Calculate nutritional scores for all dishes
- Train a Linear Regression model
- Save model, scaler, and features

### 2. Use the Prediction App

```bash
python app.py
```

The app provides:
- Manual entry of nutritional values
- Search for similar dishes in dataset
- Real-time score prediction and interpretation

## 📁 Project Structure

```
nutrition_regression_project/
├── Indian_Food_Nutrition_Processed.csv   # Dataset (1,014 dishes)
├── config.py                             # Configuration settings
├── data_loader.py                        # Data loading and scoring
├── model_trainer.py                      # Model training
├── main.py                               # Training script
├── app.py                                # Interactive prediction app
├── requirements.txt                      # Dependencies
├── models/                               # Trained models (auto-created)
│   ├── linear_regression_model.joblib   # Trained model
│   ├── scaler.joblib                    # Feature scaler
│   ├── features.joblib                  # Feature names
│   └── dishes.joblib                    # Training dishes
└── outputs/                              # Generated files (auto-created)
```

## 💻 Usage Examples

### Example 1: Manually enter values
```
Enter nutritional values for the dish:

Calories (kcal): 200
Protein (g): 15
Carbohydrates (g): 25
Free Sugar (g): 5

🎯 Predicted Score: 67.80/100
📈 Rating: Good 👍
```

### Example 2: Search for similar dishes
```
Search for a similar dish in dataset:
Enter dish name to search: chicken

📋 Found 3 similar dish(es):
  • Chicken sandwich
  • Lemon chicken
  • Chicken tikka
```

## 📊 Model Performance

Typical model performance:
- **Train R² Score**: ~0.84 (84% variance explained)
- **Test R² Score**: ~0.85 (85% variance explained)
- **Test RMSE**: ~4.28 (average prediction error)
- **Test MAE**: ~3.36 (mean absolute error)

## 🔧 Requirements

- Python 3.8+
- pandas
- numpy
- scikit-learn
- joblib

Install with:
```bash
pip install -r requirements.txt
```

## 📝 Files Description

### config.py
Centralized configuration including:
- Directory paths
- Feature columns
- Model file locations

### data_loader.py
- `DataLoader` class
- Load CSV dataset
- Calculate nutritional scores
- Prepare features and target

### model_trainer.py
- `ModelTrainer` class
- Split and scale data
- Train Linear Regression
- Calculate metrics
- Save trained model

### main.py
- Training orchestration script
- Loads data
- Trains model
- Saves artifacts

### app.py
- Interactive prediction app
- User input handling
- Real-time predictions
- Dish searching

## 🎓 Course Project Integration

This project is designed for:
- Machine Learning course projects
- Data science demonstrations
- Regression model practice
- Model deployment examples

## 📈 Future Enhancements

Potential improvements:
- Multiple regression models comparison
- Hyperparameter tuning
- Cross-validation
- Feature importance analysis
- Web API deployment
- Batch predictions
- Database integration

## 🤝 Contributing

To extend this project:
1. Modify `data_loader.py` for different scoring systems
2. Update `model_trainer.py` for different models
3. Enhance `app.py` with new features
4. Add visualization capabilities

## 📄 License

This project is for educational purposes.

---

**Created**: October 2025
**Last Updated**: October 26, 2025
