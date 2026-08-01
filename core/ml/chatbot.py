import random
import os

class ChatbotInterface:
    def __init__(self, model_path=None):
        self.responses = {
            'greeting': [
                "Hello! How are you feeling today?",
                "Hi there! How can I help you?",
                "Hello! Would you like to talk about something?"
            ],
            'goodbye': [
                "Goodbye! Take care!",
                "Have a great day!",
                "See you next time!"
            ],
            'thanks': [
                "You're welcome!",
                "Happy to help!",
                "Anytime!"
            ],
            'feeling_good': [
                "That's wonderful to hear!",
                "I'm glad you're feeling good!",
                "Great to know you're doing well!"
            ],
            'feeling_bad': [
                "I'm sorry you're feeling this way. Would you like to talk about it?",
                "It's okay to feel down sometimes. Want to share what's bothering you?",
                "I'm here to listen if you want to talk about what's troubling you."
            ],
            'anxiety': [
                "Take a deep breath. Can you tell me what's making you feel anxious?",
                "Anxiety can be overwhelming. Would you like to talk about what's causing it?",
                "I'm here to help you work through your anxiety. What's on your mind?"
            ],
            'default': [
                "I'm here to listen. Could you tell me more about that?",
                "Please feel free to share more.",
                "I'm listening. Would you like to elaborate?"
            ]
        }
        self.patterns = {
            'greeting': ['hi', 'hello', 'hey', 'good morning', 'good evening'],
            'goodbye': ['bye', 'goodbye', 'see you', 'take care'],
            'thanks': ['thanks', 'thank you', 'appreciate'],
            'feeling_good': ['good', 'great', 'happy', 'wonderful', 'awesome'],
            'feeling_bad': ['sad', 'down', 'depressed', 'unhappy', 'upset'],
            'anxiety': ['anxious', 'nervous', 'worried', 'stressed', 'anxiety']
        }
    
    def predict_intent(self, message):
        message = message.lower()
        words = message.split()
        
        # Check each intent's patterns
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                if pattern in message or pattern in words:
                    return intent
        
        return 'default'

    def get_response(self, message):
        intent = self.predict_intent(message)
        import random
        return random.choice(self.responses[intent])

    def chat(self, message):
        try:
            return self.get_response(message)
        except Exception as e:
            print(f"Chat error: {str(e)}")
            return "I'm here to listen. Could you tell me more about that?"

# Initialize the chatbot
chatbot = None

def initialize_chatbot():
    global chatbot
    try:
        chatbot = ChatbotInterface()
        print("Chatbot initialized successfully!")
    except Exception as e:
        print(f"Error initializing chatbot: {e}")
        chatbot = None

def get_chatbot_response(message):
    if chatbot is None:
        try:
            initialize_chatbot()
        except Exception as e:
            print(f"Error initializing chatbot: {e}")
            return "Sorry, I'm having trouble initializing. Please try again later."
    
    if chatbot:
        try:
            response = chatbot.chat(message)
            print(f"User: {message}")
            print(f"Bot: {response}")
            return response
        except Exception as e:
            print(f"Error getting response: {e}")
            return "I apologize, but I'm having trouble processing your message."
    return "I'm currently unavailable. Please try again later."