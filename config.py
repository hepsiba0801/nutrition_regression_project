"""
Configuration File
Centralized settings for the nutrition regression project
"""

from pathlib import Path

# Directories
PROJECT_DIR = Path(__file__).parent
DATA_DIR = PROJECT_DIR
MODELS_DIR = PROJECT_DIR / 'models'
OUTPUTS_DIR = PROJECT_DIR / 'outputs'

# Dataset
DATASET_PATH = DATA_DIR / 'Indian_Food_Nutrition_Processed.csv'

# Model configuration
TEST_SIZE = 0.2
RANDOM_STATE = 42

# Features and target
FEATURE_COLUMNS = ['Calories (kcal)', 'Protein (g)', 'Carbohydrates (g)', 'Free Sugar (g)']
TARGET_COLUMN = 'Nutritional_Score'
DISH_NAME_COLUMN = 'Dish Name'

# Model files
MODEL_FILE = MODELS_DIR / 'linear_regression_model.joblib'
SCALER_FILE = MODELS_DIR / 'scaler.joblib'
FEATURES_FILE = MODELS_DIR / 'features.joblib'
DISHES_FILE = MODELS_DIR / 'dishes.joblib'

# Ensure directories exist
MODELS_DIR.mkdir(exist_ok=True)
OUTPUTS_DIR.mkdir(exist_ok=True)


def print_config():
    """Print configuration summary"""
    print("\n" + "=" * 80)
    print("  CONFIGURATION")
    print("=" * 80)
    print(f"✓ Dataset: {DATASET_PATH.name}")
    print(f"✓ Features: {', '.join(FEATURE_COLUMNS)}")
    print(f"✓ Target: {TARGET_COLUMN}")
    print(f"✓ Models Directory: {MODELS_DIR}")
    print(f"✓ Test Size: {TEST_SIZE * 100:.0f}%")
    print()
