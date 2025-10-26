"""
Interactive Prediction App
Get nutritional score predictions for dishes based on their nutritional values
"""

import joblib
import numpy as np
from config import MODEL_FILE, SCALER_FILE, FEATURES_FILE, DISH_NAME_COLUMN
from data_loader import DataLoader


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)


def print_section(text):
    """Print formatted section"""
    print(f"\n{'─' * 80}")
    print(f"  {text}")
    print(f"{'─' * 80}\n")


def load_model():
    """Load trained model and scaler"""
    try:
        model = joblib.load(str(MODEL_FILE))
        scaler = joblib.load(str(SCALER_FILE))
        features = joblib.load(str(FEATURES_FILE))
        return model, scaler, features
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print(f"   Please run 'python main.py' first to train the model")
        return None, None, None


def get_user_input(features):
    """Get nutritional values from user"""
    print("Enter nutritional values for the dish:\n")
    
    try:
        values = {}
        for feature in features:
            while True:
                try:
                    val = float(input(f"  {feature}: "))
                    if val < 0:
                        print("     ❌ Please enter a positive number")
                        continue
                    values[feature] = val
                    break
                except ValueError:
                    print("     ❌ Please enter a valid number")
        
        return np.array([list(values.values())])
    
    except KeyboardInterrupt:
        return None


def predict_score(model, scaler, X_input):
    """Predict nutritional score"""
    X_scaled = scaler.transform(X_input)
    score = model.predict(X_scaled)[0]
    return max(0, min(100, score))  # Clamp between 0-100


def interpret_score(score):
    """Interpret score as category"""
    if score >= 80:
        return "Excellent 🌟", "Outstanding nutritional quality!"
    elif score >= 70:
        return "Very Good ✅", "Very good nutritional value"
    elif score >= 60:
        return "Good 👍", "Good nutritional quality"
    elif score >= 50:
        return "Fair ⚖️", "Moderate nutritional quality"
    elif score >= 40:
        return "Poor ⚠️", "Low nutritional quality"
    else:
        return "Very Poor ❌", "Very low nutritional quality"


def search_similar_dishes(dish_name, loader):
    """Search for similar dishes in dataset"""
    df = loader.df
    if df is None:
        loader.load()
        loader.calculate_scores()
        df = loader.df
    
    matching = df[df[DISH_NAME_COLUMN].str.contains(dish_name, case=False, na=False)]
    
    if len(matching) == 0:
        return None
    
    return matching.head(5)


def find_matching_dishes(X_input, features, loader, top_n=5):
    """Find dishes from dataset with closest nutritional values"""
    df = loader.df
    if df is None:
        loader.load()
        loader.calculate_scores()
        df = loader.df
    
    # Extract feature values from input
    input_values = X_input[0]
    
    # Calculate Euclidean distance for each dish
    distances = []
    for idx, row in df.iterrows():
        dish_values = [row[feature] for feature in features]
        # Euclidean distance
        distance = np.sqrt(np.sum((np.array(input_values) - np.array(dish_values)) ** 2))
        distances.append(distance)
    
    # Add distances to dataframe
    df_with_dist = df.copy()
    df_with_dist['distance'] = distances
    
    # Sort by distance and return top matches
    matching_dishes = df_with_dist.nsmallest(top_n, 'distance')
    
    return matching_dishes


def main():
    """Main app loop"""
    print_header("NUTRITIONAL SCORE PREDICTION APP")
    
    # Load model
    print("🔄 Loading model...")
    model, scaler, features = load_model()
    
    if model is None:
        return
    
    print("✓ Model loaded successfully!")
    
    # Load dataset for reference
    loader = DataLoader()
    loader.load()
    loader.prepare_data()
    
    print_section("HOW TO USE")
    print("This app predicts nutritional quality scores (0-100) for dishes.")
    print("Enter the nutritional values for a dish:\n")
    print(f"Features: {', '.join(features)}\n")
    print("Higher scores = Better nutritional quality\n")
    
    # Main loop
    while True:
        print_section("PREDICTION")
        
        # Option to search similar dishes
        print("Options:")
        print("  1. Enter nutritional values manually")
        print("  2. Search for a similar dish in dataset")
        print("  3. Exit\n")
        
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == '3':
            print("\n" + "=" * 80)
            print("  Thank you for using the Nutrition Prediction App!")
            print("=" * 80 + "\n")
            break
        
        elif choice == '2':
            dish_query = input("Enter dish name to search: ").strip()
            similar = search_similar_dishes(dish_query, loader)
            
            if similar is not None:
                print(f"\n📋 Found {len(similar)} similar dish(es):\n")
                for idx, row in similar.iterrows():
                    print(f"  • {row['Dish Name']}")
                    for feature in features:
                        print(f"    ├─ {feature}: {row[feature]:.2f}")
                    print()
            else:
                print(f"\n❌ No dishes found matching '{dish_query}'")
            
            continue
        
        elif choice == '1':
            X_input = get_user_input(features)
            
            if X_input is None:
                break
            
            # Predict
            score = predict_score(model, scaler, X_input)
            category, message = interpret_score(score)
            
            # Display results
            print("\n" + "─" * 80)
            print("📊 PREDICTION RESULT")
            print("─" * 80)
            
            values = X_input[0]
            print(f"\n📋 Input Nutritional Values:")
            for feature, value in zip(features, values):
                print(f"  ├─ {feature}: {value:.2f}")
            
            print(f"\n🎯 Predicted Score: {score:.2f}/100")
            print(f"📈 Rating: {category}")
            print(f"💬 {message}")
            
            # Detailed interpretation
            if score >= 70:
                print(f"\n✨ Key strengths:")
                print(f"   • Good balance of nutrients")
                print(f"   • Recommended for healthy diet")
            elif score >= 50:
                print(f"\n⚖️  Moderate nutrition:")
                print(f"   • Contains some beneficial nutrients")
                print(f"   • Could be improved")
            else:
                print(f"\n⚠️  Nutritional concerns:")
                print(f"   • Consider healthier alternatives")
                print(f"   • Focus on increasing nutrients")
            
            # Find matching dishes from dataset
            print(f"\n{'─' * 80}")
            print("🍽️  MATCHING DISHES FROM DATASET")
            print(f"{'─' * 80}\n")
            
            matching_dishes = find_matching_dishes(X_input, features, loader, top_n=2)
            
            if matching_dishes is not None and len(matching_dishes) > 0:
                print(f"📋 Top 2 dishes with similar nutritional values:\n")
                
                for rank, (idx, row) in enumerate(matching_dishes.iterrows(), 1):
                    similarity_pct = max(0, 100 - (row['distance'] * 2))  # Rough similarity percentage
                    
                    print(f"  {rank}. {row['Dish Name']}")
                    print(f"     🎯 Similarity: {similarity_pct:.1f}%")
                    for feature in features:
                        print(f"     ├─ {feature}: {row[feature]:.2f}")
                    print()
            else:
                print("❌ No matching dishes found in dataset")
        
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n" + "=" * 80)
        print("  App closed by user")
        print("=" * 80 + "\n")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
