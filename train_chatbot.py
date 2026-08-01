import json
import numpy as np
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import os
from datetime import datetime

class MentalHealthChatbotTrainer:
    def __init__(self):
        self.vectorizer = None
        self.classifier = None
        self.label_encoder = None
        self.intents = self._load_comprehensive_intents()
        
    def _load_comprehensive_intents(self):
        """Load comprehensive mental health intents with realistic conversational patterns"""
        return {
            "greeting": {
                "patterns": [
                    "hello", "hi", "hey", "good morning", "good afternoon", 
                    "good evening", "howdy", "what's up", "hello there",
                    "hi there", "hey there", "how are you", "what's going on",
                    "greetings", "good day", "morning", "afternoon", "evening",
                    "hello friend", "hi chat", "hey bot", "hello ai", "yo",
                    "hey there", "hiya", "how's it going", "what's happening",
                    "long time no see", "hey how are you", "hi how you doing"
                ],
                "responses": [
                    "Hello! I'm MindSight AI. How are you feeling today?",
                    "Hi there! I'm here to listen and support you. How can I help?",
                    "Hello! Thank you for reaching out. How are you doing today?",
                    "Hey! I'm glad you're here. How is everything going?",
                    "Hi! I'm here to talk whenever you're ready. What's on your mind?"
                ]
            },
            "feeling_sad": {
                "patterns": [
                    "i feel sad", "i'm depressed", "i'm unhappy", "feeling down",
                    "i'm so sad", "i feel miserable", "i'm feeling low",
                    "nothing makes me happy", "i can't stop crying", "so depressed",
                    "extremely sad", "very unhappy", "feeling blue", "down in the dumps",
                    "i feel hopeless", "life is sad", "everything is sad", "constant sadness",
                    "deep sadness", "overwhelming sadness", "can't be happy", "always sad",
                    "tearful", "crying spells", "emotional pain", "heart hurts",
                    "i've been feeling down lately", "nothing brings me joy anymore",
                    "why do i feel so sad all the time", "how do i stop feeling this way",
                    "what should i do when i feel sad", "i can't shake this sadness",
                    "everything feels heavy", "i just want to cry", "the sadness won't go away",
                    "i feel empty inside", "what's wrong with me", "why am i always sad"
                ],
                "responses": [
                    "I'm really sorry you're feeling this way. It takes courage to acknowledge these feelings. Would you like to talk about what's been on your mind?",
                    "Thank you for sharing this with me. Feeling sad can be really difficult. Let's explore what might be contributing to these feelings.",
                    "I hear you. Sadness can feel overwhelming sometimes. Remember that you're not alone in this.",
                    "I'm here with you. It's okay to feel sad. Would you like to talk about what's making you feel this way?",
                    "That sounds really hard. Sometimes just putting these feelings into words can help. What's been going on that might be contributing to this sadness?"
                ]
            },
            "feeling_anxious": {
                "patterns": [
                    "i feel anxious", "i'm nervous", "i'm worried", "feeling anxious",
                    "i'm having anxiety", "i feel panicked", "i'm stressed out",
                    "my heart is racing", "i can't calm down", "having panic",
                    "feeling nervous", "so anxious", "very worried", "anxiety attack",
                    "constant worry", "can't relax", "on edge", "feeling tense",
                    "restless", "apprehensive", "fearful", "panic symptoms",
                    "anxious thoughts", "worried mind", "nervous wreck", "anxiety rising",
                    "how can i calm my anxiety", "what helps with anxiety",
                    "i keep overthinking everything", "my mind won't stop racing",
                    "how do i stop worrying so much", "i feel like something bad will happen",
                    "can you help me relax", "what should i do when i feel anxious",
                    "my anxiety is out of control", "i need to calm down but i can't",
                    "everything makes me anxious", "how to deal with panic attacks"
                ],
                "responses": [
                    "Anxiety can feel overwhelming. Let's explore what might be causing these feelings together. Remember to breathe deeply.",
                    "I understand that anxiety can be really challenging. Would you like to try some grounding techniques together?",
                    "Thank you for sharing this. Anxiety is tough, but there are ways to manage it. Let's talk about what might help.",
                    "I hear how anxious you're feeling. Let's take a moment to breathe together. Inhale slowly... and exhale...",
                    "When anxiety feels overwhelming, it can help to focus on the present moment. What's one thing you can see, hear, or feel right now?"
                ]
            },
            "crisis": {
                "patterns": [
                    "i want to kill myself", "suicide", "end my life", "want to die",
                    "i can't go on", "better off dead", "no reason to live",
                    "harm myself", "thinking about suicide", "kill myself",
                    "ending it all", "don't want to live", "tired of living",
                    "life not worth living", "suicidal thoughts", "ending my life",
                    "no point in living", "give up on life", "suicide plan",
                    "want to disappear", "can't take it anymore", "end the pain",
                    "i don't want to be here anymore", "everyone would be better without me",
                    "the pain is too much to bear", "i see no way out", "nothing matters anymore",
                    "i have nothing to live for", "the world would be better without me",
                    "i'm planning to end it all", "i can't do this anymore", "i give up on life"
                ],
                "responses": [
                    "I'm really concerned about what you're sharing. If you're in crisis, please contact emergency services or a crisis helpline immediately. You can call 988 for mental health support. You are not alone, and there are people who want to help.",
                    "This sounds very serious. Your safety is the most important thing right now. Please reach out to a crisis helpline at 988 or go to your nearest emergency room. I'm here with you while you take these steps.",
                    "I hear how much pain you're in. Please know that there is help available right now. Call the National Suicide Prevention Lifeline at 1-800-273-8255 or text HOME to 741741. You don't have to go through this alone.",
                    "Your life matters. Please reach out for immediate help. You can call 988 anytime, day or night. They have trained professionals who can support you right now."
                ]
            },
            "gratitude": {
                "patterns": [
                    "thank you", "thanks", "i appreciate", "you're helpful",
                    "you helped me", "good advice", "that's helpful", "thank you so much",
                    "thanks a lot", "i appreciate it", "you're amazing", "very helpful",
                    "grateful", "appreciation", "thankful", "you're the best",
                    "helpful chat", "good support", "useful advice", "thanks friend",
                    "you really helped me today", "i feel better after talking to you",
                    "thank you for listening", "you're a good listener", "this helped a lot",
                    "i appreciate your help", "thanks for being here", "you made me feel better"
                ],
                "responses": [
                    "You're welcome! I'm here to support you on your mental wellness journey.",
                    "I'm glad I could help. Remember, taking care of your mental health is a sign of strength.",
                    "Thank you for the kind words. I'm here whenever you need to talk.",
                    "You're very welcome. I'm honored to be part of your support system.",
                    "I'm really glad I could help. How are you feeling now compared to when we started talking?"
                ]
            },
            "stress": {
                "patterns": [
                    "i'm stressed", "i'm overwhelmed", "too much pressure",
                    "i can't handle this", "i'm under stress", "work is stressful",
                    "life is stressful", "so stressed", "overwhelmed", "burned out",
                    "stressed out", "too much to do", "can't cope", "pressure building",
                    "stressful situation", "work stress", "life pressure", "stressful life",
                    "constant stress", "stress management", "dealing with stress",
                    "how to manage stress", "what should i do about stress",
                    "i'm too stressed to function", "everything is too much",
                    "how can i reduce stress", "stress is killing me",
                    "i need to relax but i can't", "my stress levels are too high",
                    "how do people handle stress", "what are good ways to deal with stress"
                ],
                "responses": [
                    "Stress can be challenging. Let's break down what's causing this feeling and explore some coping strategies.",
                    "I understand that stress can feel overwhelming. Would you like to talk about specific stressors and how to manage them?",
                    "Thank you for sharing this. Stress affects us all differently. Let's explore some relaxation techniques together.",
                    "I hear how stressed you're feeling. Let's identify what's within your control and work on manageable steps.",
                    "When stress feels overwhelming, it can help to prioritize. What's one small thing you could tackle right now?"
                ]
            },
            "loneliness": {
                "patterns": [
                    "i feel lonely", "i'm alone", "i feel isolated", "no one understands me",
                    "i have no friends", "i feel disconnected", "nobody cares about me",
                    "so lonely", "very isolated", "all alone", "no one to talk to",
                    "feeling abandoned", "social isolation", "lonely heart", "empty inside",
                    "no connections", "friendless", "alone in crowd", "emotional isolation",
                    "how to make friends", "why do i feel so lonely",
                    "what should i do when i feel lonely", "i have nobody in my life",
                    "how to connect with people", "i feel invisible to others",
                    "why am i always alone", "how to stop feeling lonely",
                    "i want friends but don't know how", "everyone else has friends but me"
                ],
                "responses": [
                    "Feeling lonely can be really difficult. Remember that reaching out is a sign of strength. Would you like to explore ways to build connections?",
                    "I hear how isolated you're feeling. Loneliness can be painful, but you've taken a brave step by reaching out.",
                    "Thank you for sharing this. Feeling disconnected from others is hard. Let's talk about ways to build meaningful connections.",
                    "I'm here with you. Loneliness is tough, but you're not alone in feeling this way. Let's work through this together.",
                    "Loneliness can make us feel invisible, but I see you and I'm listening. What kind of connections are you hoping to build?"
                ]
            },
            "anger": {
                "patterns": [
                    "i'm angry", "i'm mad", "i'm furious", "feeling angry",
                    "i'm so frustrated", "i'm irritated", "i can't control my anger",
                    "so angry", "very mad", "frustrated", "pissed off", "losing my temper",
                    "rage", "outraged", "infuriated", "annoyed", "bitter", "resentful",
                    "angry outburst", "temper issues", "frustration building", "angry feelings",
                    "how to control anger", "what should i do when i'm angry",
                    "why am i always so angry", "how to calm down when mad",
                    "i don't want to be angry anymore", "my anger is ruining relationships",
                    "how to express anger in healthy ways", "what causes anger issues",
                    "i need help with my temper", "how to manage angry feelings"
                ],
                "responses": [
                    "Anger is a natural emotion. Let's explore what's triggering these feelings and find healthy ways to express them.",
                    "I hear your frustration. Anger can be overwhelming. Would you like to talk about what's causing these feelings?",
                    "It's okay to feel angry. Let's work on understanding these emotions and finding constructive ways to handle them.",
                    "I understand you're feeling angry. Let's explore what's behind these feelings and how we can address them.",
                    "Anger often comes from unmet needs or boundaries. What do you think might be underneath this anger for you?"
                ]
            },
            "positive_feelings": {
                "patterns": [
                    "i feel good", "i'm happy", "feeling great", "i'm okay",
                    "doing well", "feeling better", "good mood", "happy today",
                    "feeling positive", "much better", "improved mood", "feeling optimistic",
                    "good day", "positive outlook", "content", "satisfied", "peaceful",
                    "joyful", "excited", "hopeful", "grateful today", "blessed",
                    "things are looking up", "i'm in a good place right now",
                    "life is good today", "i feel hopeful about the future",
                    "finally feeling better", "my mood has improved",
                    "i'm proud of myself today", "i accomplished something good",
                    "today was a good day", "i feel light and happy"
                ],
                "responses": [
                    "That's wonderful to hear! Celebrating positive moments is important. What's been going well for you?",
                    "I'm so glad you're feeling good today! Positive emotions help build resilience.",
                    "That's great! It's important to acknowledge and enjoy these positive feelings.",
                    "I'm happy to hear that! Would you like to explore what's contributing to these good feelings?",
                    "That's fantastic! Recognizing these good moments helps build emotional strength. What's been working well for you lately?"
                ]
            },
            "sleep_issues": {
                "patterns": [
                    "can't sleep", "insomnia", "sleep problems", "trouble sleeping",
                    "waking up", "restless sleep", "bad dreams", "nightmares",
                    "sleep deprivation", "exhausted but can't sleep", "sleep anxiety",
                    "sleep schedule", "sleep quality", "sleep disorders",
                    "how to sleep better", "what should i do when i can't sleep",
                    "why can't i fall asleep", "i'm always tired from poor sleep",
                    "how to fix my sleep schedule", "what helps with insomnia",
                    "i wake up multiple times at night", "my mind races when i try to sleep",
                    "how to stop nightmares", "sleep tips for anxiety",
                    "i need better sleep but don't know how"
                ],
                "responses": [
                    "Sleep issues can be really challenging and affect your overall wellbeing. Let's talk about what might be disrupting your sleep.",
                    "I understand that sleep problems can be frustrating. Good sleep is essential for mental health.",
                    "Sleep difficulties are common with stress and anxiety. Would you like to explore some relaxation techniques for better sleep?",
                    "Trouble sleeping can make everything feel harder. What have you tried so far to improve your sleep?",
                    "Sleep and mental health are deeply connected. Let's explore what might help you get more restful sleep."
                ]
            },
            "motivational_support": {
                "patterns": [
                    "i feel stuck", "i can't move forward", "i'm not making progress",
                    "nothing is working", "i feel trapped", "don't know what to do",
                    "what should i do", "i need direction", "feeling lost",
                    "don't know how to continue", "what's the point", "i feel hopeless",
                    "can't see a way out", "don't know my purpose", "feeling directionless",
                    "what do i do now", "need guidance", "feeling confused about life",
                    "i have no motivation", "can't get motivated", "don't feel like doing anything",
                    "no energy to try", "too tired to care", "lost my drive",
                    "what's the use", "why even try", "nothing matters",
                    "can't find motivation", "too depressed to try", "no willpower",
                    "how can i feel better", "what can i do", "need advice",
                    "how to get motivated", "ways to feel better", "how to improve",
                    "how to be happy", "how to stop feeling this way", "how to move forward",
                    "tips for motivation", "how to get unstuck", "how to find purpose",
                    "i'm not good enough", "i keep failing", "nothing goes right",
                    "why can't i succeed", "always failing", "not making progress",
                    "things never work out", "i'm a failure", "can't achieve anything",
                    "what if i fail", "afraid to try", "scared to move forward",
                    "worried about future", "can't see future", "what's next for me",
                    "how do i find my passion", "what am i supposed to do with my life",
                    "i feel so unmotivated all the time", "how to get my life together"
                ],
                "responses": [
                    "It sounds like you're feeling stuck right now. That's completely normal. Sometimes the first step is just acknowledging how you feel. What's one small thing you could do today that might help you feel slightly better?",
                    "Motivation can be really hard to find sometimes, especially when you're struggling. Remember that action often comes before motivation, not the other way around. What's one tiny step you could take right now?",
                    "When everything feels overwhelming, it helps to break things down. Let's focus on just the next hour rather than the rest of your life. What's one thing that usually brings you even a moment of peace?",
                    "Progress isn't always linear, and it's okay to have difficult days. The fact that you're reaching out shows incredible strength. What's one thing you've overcome in the past that seemed impossible at the time?",
                    "Sometimes the bravest thing we can do is just get through today. Would it help to talk about some small, manageable steps you could take? Even something as simple as drinking water or stepping outside for a minute counts."
                ]
            },
            "goodbye": {
                "patterns": [
                    "bye", "goodbye", "see you", "see ya", "farewell",
                    "i have to go", "i need to go", "talk to you later",
                    "catch you later", "until next time", "i'm leaving",
                    "take care", "peace out", "later", "bye bye",
                    "good night", "gn", "cya", "adios", "au revoir",
                    "i should get going", "time to go", "signing off",
                    "that's all for now", "thanks for your help, goodbye",
                    "thank you, bye", "appreciate your time, goodbye",
                    # ENHANCED PATTERNS FOR BETTER CONFIDENCE
                    "gotta go now", "need to leave", "time for me to go",
                    "thanks for chatting", "appreciate the talk", "thanks for listening",
                    "talk soon", "see you next time", "until we chat again",
                    "take care of yourself", "be well", "all the best",
                    "thanks for your support", "appreciate your help",
                    "signing off now", "logging off", "closing chat",
                    "that's all i needed", "thanks that's all", "done for now",
                    "finished chatting", "ending our conversation", "wrapping up",
                    "thanks for everything", "appreciate your time", "thanks for being there",
                    "have a good day", "have a great day", "have a nice day",
                    "see you tomorrow", "until tomorrow", "catch you tomorrow",
                    "i'm done for today", "that's all for today", "ending for today"
                ],
                "responses": [
                    "Goodbye! Remember I'm here whenever you need to talk. Take care of yourself!",
                    "Take care! I'm always here if you need support. Be kind to yourself today.",
                    "Goodbye! Thank you for reaching out. Remember to practice self-care.",
                    "See you later! Don't hesitate to come back if you need someone to talk to.",
                    "Take care of yourself! I'm here 24/7 whenever you need support.",
                    "Goodbye! Remember your mental health matters. Come back anytime you need to talk.",
                    "Farewell! I'm proud of you for taking this step for your wellbeing.",
                    "Until next time! Remember you're not alone in this journey.",
                    "Take care and be gentle with yourself today. Goodbye!",
                    "Goodbye! I'm always here when you need a listening ear."
                ]
            },
            "seeking_advice": {
                "patterns": [
                    "what should i do", "what can i do", "give me advice",
                    "tell me what to do", "how should i handle this", "what would you do",
                    "need your advice", "can you suggest something", "what do you recommend",
                    "any suggestions", "what's your suggestion", "how to deal with this",
                    "how to feel better", "ways to be happy", "how to stop being sad",
                    "how to reduce anxiety", "ways to relax", "how to manage stress",
                    "how to make friends", "how to be less lonely", "how to sleep better",
                    "how to control anger", "how to be motivated",
                    "what now", "what next", "where do i go from here",
                    "how do i start", "how to begin", "first steps",
                    "how to change", "how to improve", "how to get better",
                    "can you help me figure this out", "i need some guidance",
                    "what would you suggest i try", "how do people usually handle this",
                    "what are my options here", "i don't know what step to take next"
                ],
                "responses": [
                    "That's a really important question. While I can't tell you exactly what to do, I can help you explore options. What have you tried so far?",
                    "I understand you're looking for guidance. Let's think about what might work for you specifically. What sounds manageable to you right now?",
                    "That's a thoughtful question. Different things work for different people. What aspects of this feel most challenging to you?",
                    "I appreciate you asking for input. Let's break this down together. What's one small change you could imagine making?",
                    "That's a great question to ask. Let's explore what's worked for you in the past and what hasn't. What usually helps you when you're facing challenges?"
                ]
            },
            "general_support": {
                "patterns": [
                    "i need someone to talk to", "can we chat", "are you there",
                    "i need to talk", "can you listen", "i need support",
                    "i'm struggling", "having a hard time", "going through a tough time",
                    "life is hard right now", "things are difficult", "i'm having a rough day",
                    "can you help me", "i need help", "could use some support",
                    "not doing well", "having a bad day", "today was tough",
                    "i feel overwhelmed", "everything is too much", "can't handle things",
                    "just need to vent", "need to get this off my chest",
                    "do you have a moment to talk", "are you available to chat"
                ],
                "responses": [
                    "I'm here for you. Take your time and share what's on your mind. I'm listening.",
                    "Thank you for reaching out. I'm here to support you. What would you like to talk about?",
                    "I'm glad you're here. Whatever you're going through, you don't have to face it alone. What's been on your mind?",
                    "I'm here and ready to listen. There's no rush - share what feels comfortable for you.",
                    "You've come to the right place. I'm here to support you. What would be helpful to talk about right now?"
                ]
            }
        }
    
    def load_training_data(self):
        """Load training data from intents"""
        texts = []
        labels = []
        
        # Load from intents
        for intent_name, intent_data in self.intents.items():
            for pattern in intent_data['patterns']:
                texts.append(pattern)
                labels.append(intent_name)
        
        print(f"✅ Loaded {len(texts)} samples from intents")
        return texts, labels
    
    def train_model(self):
        """Enhanced training with better parameters for higher confidence"""
        print("Loading training data...")
        texts, labels = self.load_training_data()
        
        if not texts:
            print("No training data available!")
            return False
        
        print(f"Training on {len(texts)} samples...")
        
        # ENHANCED VECTORIZER FOR BETTER FEATURE EXTRACTION
        self.vectorizer = TfidfVectorizer(
            max_features=3000,  # Increased features
            stop_words='english',
            ngram_range=(1, 4),  # Increased to capture more context
            min_df=2,  # Require at least 2 occurrences
            max_df=0.85,  # Exclude very common words
            sublinear_tf=True,  # Use sublinear TF scaling
            norm='l2',  # L2 normalization
            use_idf=True  # Use IDF
        )
        
        X = self.vectorizer.fit_transform(texts)
        
        # Encode labels
        self.label_encoder = LabelEncoder()
        y = self.label_encoder.fit_transform(labels)
        
        # ENHANCED CLASSIFIER FOR HIGHER CONFIDENCE
        self.classifier = RandomForestClassifier(
            n_estimators=300,  # More trees
            random_state=42,
            max_depth=25,  # Deeper trees
            min_samples_split=5,  # More samples to split
            min_samples_leaf=2,  # More samples per leaf
            max_features='sqrt',  # Better feature selection
            bootstrap=True,
            class_weight='balanced'  # Handle class imbalance
        )
        
        self.classifier.fit(X, y)
        
        # Calculate accuracy
        train_accuracy = self.classifier.score(X, y)
        print(f"Training completed! Accuracy: {train_accuracy:.2f}")
        
        # CONFIDENCE ANALYSIS
        self.analyze_confidence(X, texts, labels, y)
        
        return True
    
    def analyze_confidence(self, X, texts, labels, y):
        """Analyze confidence scores for different intents"""
        print("\n🔍 Confidence Analysis:")
        
        # Get predictions and probabilities
        y_pred = self.classifier.predict(X)
        y_proba = self.classifier.predict_proba(X)
        
        # Analyze by intent
        confidence_report = {}
        for intent_name in self.intents.keys():
            if intent_name in self.label_encoder.classes_:
                intent_idx = np.where(self.label_encoder.classes_ == intent_name)[0][0]
                intent_mask = (y == intent_idx)
                
                if np.sum(intent_mask) > 0:
                    intent_confidences = y_proba[intent_mask, intent_idx]
                    avg_confidence = np.mean(intent_confidences)
                    min_confidence = np.min(intent_confidences)
                    max_confidence = np.max(intent_confidences)
                    
                    confidence_report[intent_name] = {
                        'avg': avg_confidence,
                        'min': min_confidence,
                        'max': max_confidence,
                        'samples': np.sum(intent_mask)
                    }
                    
                    print(f"   {intent_name}:")
                    print(f"      Avg confidence: {avg_confidence:.3f}")
                    print(f"      Min confidence: {min_confidence:.3f}")
                    print(f"      Max confidence: {max_confidence:.3f}")
                    print(f"      Samples: {np.sum(intent_mask)}")
        
        # Print overall statistics
        all_confidences = np.max(y_proba, axis=1)
        print(f"\n📊 Overall Confidence Statistics:")
        print(f"   Average confidence: {np.mean(all_confidences):.3f}")
        print(f"   Minimum confidence: {np.min(all_confidences):.3f}")
        print(f"   Maximum confidence: {np.max(all_confidences):.3f}")
        
        return confidence_report
    
    def save_model(self, model_path='chatbot_model'):
        """Save the trained model"""
        try:
            # Create directory if it doesn't exist
            if not os.path.exists(model_path):
                os.makedirs(model_path)
                print(f"✅ Created directory: {model_path}")
            
            model_data = {
                'vectorizer': self.vectorizer,
                'classifier': self.classifier,
                'label_encoder': self.label_encoder,
                'intents': self.intents
            }
            
            model_file_path = os.path.join(model_path, 'mental_health_chatbot.joblib')
            joblib.dump(model_data, model_file_path)
            
            print(f"✅ Model saved to: {model_file_path}")
            
            # Verify the file was created
            if os.path.exists(model_file_path):
                file_size = os.path.getsize(model_file_path)
                print(f"✅ File verified: {model_file_path} ({file_size} bytes)")
            else:
                print(f"❌ ERROR: File not created at {model_file_path}")
                
            return True
            
        except Exception as e:
            print(f"❌ Error saving model: {e}")
            return False

def main():
    """Main training function"""
    print("🚀 Starting Enhanced Mental Health Chatbot Training...")
    
    # Initialize trainer
    trainer = MentalHealthChatbotTrainer()
    
    # Train the model
    success = trainer.train_model()
    
    if success:
        # Test the model with more realistic conversations
        test_messages = [
            "hello",
            "I feel really sad today and don't know what to do",
            "I'm so anxious about everything, how can I calm down?",
            "I want to kill myself, the pain is too much",
            "thank you for helping me, you're amazing",
            "I'm feeling overwhelmed with work stress",
            "I can't sleep at night, my mind won't stop racing",
            "I'm so angry right now and don't know how to control it",
            "what should I do when I feel this way?",
            "I need some advice about my situation",
            "I feel so lonely and don't know how to make friends",
            "how do I get motivated when I feel stuck?",
            "goodbye", "bye", "see you later", "take care"
        ]
        
        print("\n🧪 Testing the trained model:")
        for message in test_messages:
            # Simple prediction for testing
            X_input = trainer.vectorizer.transform([message.lower()])
            prediction = trainer.classifier.predict(X_input)[0]
            confidence = np.max(trainer.classifier.predict_proba(X_input))
            intent_name = trainer.label_encoder.inverse_transform([prediction])[0]
            
            responses = trainer.intents[intent_name]['responses']
            response = np.random.choice(responses)
            
            print(f"💬 Input: {message}")
            print(f"🤖 Response: {response}")
            print(f"🎯 Intent: {intent_name} (Confidence: {confidence:.3f})")
            print("-" * 60)
        
        # Save the model
        print("\n💾 Saving model...")
        if trainer.save_model():
            print("✅ Model saved successfully!")
        else:
            print("❌ Failed to save model!")
            
    else:
        print("❌ Training failed!")

if __name__ == "__main__":
    main()