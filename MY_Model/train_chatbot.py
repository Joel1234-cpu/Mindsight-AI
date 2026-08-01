import json
import pickle
import random
import numpy as np
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Simple tokenizer that doesn't require NLTK data
tokenizer = RegexpTokenizer(r'\w+')

def simple_preprocess(text):
    """Tokenize and convert to lowercase without lemmatization"""
    return ' '.join(tokenizer.tokenize(text.lower()))

# --- 1. Load and Preprocess Data ---
print("Loading and preprocessing data...")

with open('intents.json', 'r') as file:
    intents = json.load(file)

patterns = []
tags = []

for intent in intents['intents']:
    for pattern in intent['patterns']:
        # Simplified preprocessing
        processed_pattern = simple_preprocess(pattern)
        patterns.append(processed_pattern)
        tags.append(intent['tag'])

print(f"Processed {len(patterns)} patterns.")

# After loading intents, add validation
if not intents.get('intents'):
    raise ValueError("Invalid intents.json format: 'intents' key not found")

if len(patterns) == 0:
    raise ValueError("No patterns found in intents.json")

# --- 2. Feature Extraction and Encoding ---
print("Performing feature extraction and encoding...")

# Convert text patterns into numerical features using TF-IDF
vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
X = vectorizer.fit_transform(patterns)

# Convert categorical tags into numerical labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(tags)

# After vectorization, add dimensionality info
print(f"Vocabulary size: {len(vectorizer.vocabulary_)}")
print(f"Feature matrix shape: {X.shape}")

# --- 3. Split Data and Train the Model ---
print("Splitting data and training the model...")

# For small datasets, use a larger training portion
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.1, random_state=42
)

# Before training, add data split info
print(f"Training samples: {X_train.shape[0]}")
print(f"Testing samples: {X_test.shape[0]}")

# Use Support Vector Classifier with adjusted parameters for small datasets
model = SVC(kernel='linear', probability=True, C=1.0, class_weight='balanced')
model.fit(X_train, y_train)

print("Model training complete.")

# --- 4. Evaluate the Model ---
print("\n--- Model Evaluation ---")
y_pred = model.predict(X_test)

# Calculate and print accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

# Get unique labels that appear in the test set
unique_labels = np.unique(y_test)
target_names = [label_encoder.classes_[i] for i in unique_labels]

# Print a detailed classification report
print("\nClassification Report:")
report = classification_report(y_test, y_pred, target_names=target_names)
print(report)

# Test with sample inputs from each intent
print("\nTesting model with sample inputs:")
test_texts = []
for intent in intents['intents']:
    if intent['patterns']:
        test_texts.append(intent['patterns'][0])  # Take first pattern from each intent

print("\nTesting all intents:")
for text in test_texts:
    processed = simple_preprocess(text)
    X_test_sample = vectorizer.transform([processed])
    pred_idx = model.predict(X_test_sample)[0]
    pred_tag = label_encoder.inverse_transform([pred_idx])[0]
    confidence = np.max(model.predict_proba(X_test_sample)[0])
    print(f"Input: '{text}' -> Tag: '{pred_tag}' (confidence: {confidence:.4f})")

# --- 5. Save the Model and Other Necessary Objects ---
print("Saving model and associated objects...")

# Save the trained model, vectorizer, and label encoder to a single pickle file
# This makes it easy to load everything needed for prediction in another script
chatbot_data = {
    "model": model,
    "vectorizer": vectorizer,
    "label_encoder": label_encoder,
}

with open('chatbot_model.pkl', 'wb') as file:
    pickle.dump(chatbot_data, file)

print("\nTraining process finished. 'chatbot_model.pkl' saved successfully!")
