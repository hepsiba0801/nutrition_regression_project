"""
Data Loading Module
Load and process the nutrition dataset
"""

import pandas as pd
import numpy as np
from config import DATASET_PATH, FEATURE_COLUMNS, TARGET_COLUMN, DISH_NAME_COLUMN


class DataLoader:
    """Load and prepare nutrition dataset"""
    
    def __init__(self):
        self.df = None
    
    def load(self):
        """Load dataset from CSV"""
        if not DATASET_PATH.exists():
            raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}")
        
        self.df = pd.read_csv(DATASET_PATH)
        return self.df
    
    def calculate_score(self, row):
        """Calculate nutritional score for a dish
        
        Scoring formula:
        - Protein (35%): Higher is better (0-20g scale)
        - Calories (25%): Lower is better (0-500 kcal scale)
        - Carbs (25%): Optimal 30-50g range
        - Sugar (15%): Lower is better (0-15g scale)
        """
        score = 0
        
        # Protein score (35%) - higher is better
        protein = min(row.get('Protein (g)', 0), 20)
        protein_score = (protein / 20) * 100
        score += protein_score * 0.35
        
        # Calorie score (25%) - lower is better
        calories = min(row.get('Calories (kcal)', 0), 500)
        calorie_score = (1 - (calories / 500)) * 100
        score += calorie_score * 0.25
        
        # Carb score (25%) - optimal 30-50g
        carbs = row.get('Carbohydrates (g)', 0)
        if 30 <= carbs <= 50:
            carb_score = 100
        elif carbs < 30:
            carb_score = (carbs / 30) * 100
        else:  # carbs > 50
            carb_score = max(0, 100 - ((carbs - 50) / 30) * 100)
        score += carb_score * 0.25
        
        # Sugar score (15%) - lower is better
        sugar = min(row.get('Free Sugar (g)', 0), 15)
        sugar_score = (1 - (sugar / 15)) * 100
        score += sugar_score * 0.15
        
        return min(100, max(0, score))
    
    def prepare_data(self):
        """Load and prepare data with target variable"""
        if self.df is None:
            self.load()
        
        # Calculate nutritional scores
        self.df[TARGET_COLUMN] = self.df.apply(self.calculate_score, axis=1)
        
        # Extract features and target
        X = self.df[FEATURE_COLUMNS].copy()
        y = self.df[TARGET_COLUMN].copy()
        dishes = self.df[DISH_NAME_COLUMN].copy()
        
        return X, y, dishes
    
    def get_summary(self):
        """Get dataset summary"""
        if self.df is None:
            self.load()
        
        return {
            'total_records': len(self.df),
            'total_columns': len(self.df.columns),
            'shape': self.df.shape
        }
