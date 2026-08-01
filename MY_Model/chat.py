import json
import pickle
import random
import numpy as np
from nltk.tokenize import RegexpTokenizer
import os

# Simple tokenizer that doesn't require NLTK data
tokenizer = RegexpTokenizer(r'\w+')

def simple_preprocess(text):
    """Tokenize and convert to lowercase without lemmatization"""
    return ' '.join(tokenizer.tokenize(text.lower()))

# --- 1. Load Saved Model and Data ---
print("Starting chatbot initialization...")

# Check if required files exist
required_files = ['intents.json', 'chatbot_model.pkl']
for file in required_files:
    if not os.path.exists(file):
        print(f"Error: Required file '{file}' not found!")
        print("\nPlease ensure you:")
        print("1. Are in the correct directory")
        print("2. Have run train_chatbot.py first")
        print(f"3. Have both {', '.join(required_files)} in the same directory")
        exit(1)

# Load the intents file
with open('intents.json', 'r') as file:
    intents = json.load(file)

# Load the pickled model and associated objects
try:
    with open('chatbot_model.pkl', 'rb') as file:
        data = pickle.load(file)
        model = data['model']
        vectorizer = data['vectorizer']
        label_encoder = data['label_encoder']
except Exception as e:
    print(f"Error loading the model: {str(e)}")
    print("Ensure that the 'chatbot_model.pkl' file exists and is a valid pickle file.")
    exit(1)

print("Chatbot is ready! Type 'quit' to exit.")

# --- 2. Helper Functions ---

def predict_intent(sentence):
    """Predicts the intent of a sentence using the trained model."""
    CONFIDENCE_THRESHOLD = 0.3  # Lowered threshold for better matching
    
    try:
        processed_sentence = simple_preprocess(sentence)
        # Transform the sentence into its TF-IDF vector representation
        X_test = vectorizer.transform([processed_sentence])

        # Get prediction probabilities
        probabilities = model.predict_proba(X_test)[0]
        max_prob = np.max(probabilities)

        print(f"\nDebug - Confidence scores:")
        for idx, prob in enumerate(probabilities):
            tag = label_encoder.inverse_transform([idx])[0]
            print(f"{tag}: {prob:.4f}")

        if max_prob > CONFIDENCE_THRESHOLD:
            # Get the index of the highest probability
            prediction_index = np.argmax(probabilities)
            # Convert numerical prediction back to string tag
            predicted_tag = label_encoder.inverse_transform([prediction_index])[0]
            return predicted_tag
        else:
            print(f"Debug - Below confidence threshold ({max_prob:.4f} < {CONFIDENCE_THRESHOLD})")
            return "no_match"
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        return "error"

def get_response(tag):
    """Fetches a random response for a given intent tag."""
    if tag == "error":
        return "I encountered an error processing your request. Please try again."
    # Handle the case where the intent is not matched
    if tag == "no_match":
        return "I'm sorry, I don't understand. Can you rephrase?"

    # Find the matching intent and return a random response
    for intent in intents['intents']:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])
    # This should not be reached if tags are consistent
    return "Something went wrong!"

# --- 3. Main Chat Loop ---

if __name__ == "__main__":
    try:
        print("\nInitial setup:")
        print("1. Testing model prediction...")
        test_input = "hello"
        test_tag = predict_intent(test_input)
        print(f"   - Prediction test: {test_tag}")
        
        print("\nAll systems ready! You can start chatting.")
        print("Type 'quit' to exit the chat.")
        print("-" * 50)

        while True:
            user_input = input("You: ")
            if user_input.lower() == 'quit':
                print("Bot: Goodbye!")
                break

            # Get the predicted intent
            intent_tag = predict_intent(user_input)
            # Get a suitable response
            response = get_response(intent_tag)

            print(f"Bot: {response}")
            
    except KeyboardInterrupt:
        print("\nBot: Goodbye! (interrupted by user)")
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Delete chatbot_model.pkl and retrain")
        print("2. Check if intents.json is valid JSON")
        print("3. Ensure all required packages are installed:")
        print("   pip install nltk scikit-learn numpy")
        test_input = "hello"
        test_tag = predict_intent(test_input)
        print(f"   - Prediction test: {test_tag}")
        
        print("\nAll systems ready! You can start chatting.")
        print("Type 'quit' to exit the chat.")
        print("-" * 50)

        while True:
            user_input = input("You: ")
            if user_input.lower() == 'quit':
                print("Bot: Goodbye!")
                break

            # Get the predicted intent
            intent_tag = predict_intent(user_input)
            # Get a suitable response
            response = get_response(intent_tag)

            print(f"Bot: {response}")
            
    except KeyboardInterrupt:
        print("\nBot: Goodbye! (interrupted by user)")
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Delete chatbot_model.pkl and retrain")
        print("2. Check if intents.json is valid JSON")
        print("3. Ensure all required packages are installed:")
        print("   pip install nltk scikit-learn numpy")
