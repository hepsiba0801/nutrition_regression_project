"""
Model Training Module
Train and save Linear Regression model
"""

import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from config import TEST_SIZE, RANDOM_STATE, MODEL_FILE, SCALER_FILE, FEATURES_FILE, DISHES_FILE, FEATURE_COLUMNS


class ModelTrainer:
    """Train and manage Linear Regression model"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.features = None
        self.dishes_train = None
        self.dishes_test = None
        self.results = {}
    
    def prepare_data(self, X, y, dishes):
        """Split and scale data"""
        self.features = X.columns.tolist()
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test, self.dishes_train, self.dishes_test = train_test_split(
            X, y, dishes,
            test_size=TEST_SIZE,
            random_state=RANDOM_STATE
        )
        
        # Scale features
        self.scaler = StandardScaler()
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        print(f"✓ Data prepared:")
        print(f"  ├─ Training samples: {len(self.X_train)}")
        print(f"  ├─ Testing samples: {len(self.X_test)}")
        print(f"  └─ Features scaled: {len(self.features)} features")
    
    def train(self):
        """Train Linear Regression model"""
        print(f"\n🔄 Training Linear Regression model...")
        
        self.model = LinearRegression()
        self.model.fit(self.X_train_scaled, self.y_train)
        
        print(f"✓ Model trained successfully")
        
        # Make predictions
        y_pred_train = self.model.predict(self.X_train_scaled)
        y_pred_test = self.model.predict(self.X_test_scaled)
        
        # Calculate metrics
        self.results = {
            'train_r2': r2_score(self.y_train, y_pred_train),
            'test_r2': r2_score(self.y_test, y_pred_test),
            'train_rmse': np.sqrt(mean_squared_error(self.y_train, y_pred_train)),
            'test_rmse': np.sqrt(mean_squared_error(self.y_test, y_pred_test)),
            'train_mae': mean_absolute_error(self.y_train, y_pred_train),
            'test_mae': mean_absolute_error(self.y_test, y_pred_test),
        }
        
        return self.results
    
    def display_results(self):
        """Display training results"""
        print(f"\n📊 Model Performance:")
        print(f"  ├─ Train R² Score: {self.results['train_r2']:.4f} ({self.results['train_r2']*100:.2f}%)")
        print(f"  ├─ Test R² Score:  {self.results['test_r2']:.4f} ({self.results['test_r2']*100:.2f}%)")
        print(f"  ├─ Train RMSE:     {self.results['train_rmse']:.4f}")
        print(f"  ├─ Test RMSE:      {self.results['test_rmse']:.4f}")
        print(f"  ├─ Train MAE:      {self.results['train_mae']:.4f}")
        print(f"  └─ Test MAE:       {self.results['test_mae']:.4f}")
        
        print(f"\n📝 Model Coefficients:")
        for feature, coef in zip(self.features, self.model.coef_):
            print(f"  ├─ {feature:<25} {coef:>10.4f}")
        print(f"  └─ Intercept: {self.model.intercept_:>10.4f}")
    
    def save_model(self):
        """Save model, scaler, and metadata"""
        print(f"\n💾 Saving model files...")
        
        joblib.dump(self.model, str(MODEL_FILE))
        print(f"  ├─ Model saved: {MODEL_FILE.name}")
        
        joblib.dump(self.scaler, str(SCALER_FILE))
        print(f"  ├─ Scaler saved: {SCALER_FILE.name}")
        
        joblib.dump(self.features, str(FEATURES_FILE))
        print(f"  ├─ Features saved: {FEATURES_FILE.name}")
        
        joblib.dump(self.dishes_train.reset_index(drop=True), str(DISHES_FILE))
        print(f"  └─ Dishes saved: {DISHES_FILE.name}")
