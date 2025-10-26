"""
Main Training Script
Train Linear Regression model and save it
"""

from data_loader import DataLoader
from model_trainer import ModelTrainer
from config import print_config


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)


def main():
    """Main execution"""
    print_header("LINEAR REGRESSION MODEL TRAINING")
    
    print_config()
    
    # Load data
    print_header("STEP 1: LOADING DATA")
    loader = DataLoader()
    summary = loader.get_summary()
    print(f"✓ Dataset loaded: {summary['total_records']} dishes, {summary['total_columns']} features")
    
    # Prepare data with scores
    print_header("STEP 2: PREPARING DATA")
    X, y, dishes = loader.prepare_data()
    print(f"✓ Nutritional scores calculated")
    print(f"  ├─ Score range: {y.min():.2f} - {y.max():.2f}")
    print(f"  ├─ Mean score: {y.mean():.2f}")
    print(f"  └─ Std dev: {y.std():.2f}")
    
    # Train model
    print_header("STEP 3: TRAINING MODEL")
    trainer = ModelTrainer()
    trainer.prepare_data(X, y, dishes)
    trainer.train()
    trainer.display_results()
    
    # Save model
    print_header("STEP 4: SAVING MODEL")
    trainer.save_model()
    
    # Summary
    print_header("TRAINING COMPLETE ✅")
    print(f"\n✓ Model ready for predictions!")
    print(f"✓ Run 'python app.py' to start making predictions")
    print()


if __name__ == "__main__":
    main()
