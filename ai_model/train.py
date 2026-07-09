import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import pickle
import os

# Ensure models directory exists
os.makedirs('ai_model', exist_ok=True)

def train_model():
    print("Loading training data...")
    try:
        df = pd.read_csv('data/training_data.csv')
    except FileNotFoundError:
        print("Error: training_data.csv not found. Run data_pipeline/fetch_data.py first.")
        return

    # Filter out rows without a termination reason
    df = df.dropna(subset=['termination_reason'])
    
    print(f"Dataset size: {len(df)} records.")
    
    # Feature extraction: Using TF-IDF on the 'termination_reason' text
    vectorizer = TfidfVectorizer(stop_words='english', max_features=100)
    X = vectorizer.fit_transform(df['termination_reason']).toarray()
    
    # Target variable: Did a shortage occur?
    y = df['shortage_occurred']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\nModel Accuracy: {acc:.2f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save the model and vectorizer
    print("Saving model to ai_model/shortage_model.pkl...")
    with open('ai_model/shortage_model.pkl', 'wb') as f:
        pickle.dump(model, f)
        
    with open('ai_model/vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
        
    print("AI Model Training Completed Successfully!")

if __name__ == "__main__":
    train_model()
