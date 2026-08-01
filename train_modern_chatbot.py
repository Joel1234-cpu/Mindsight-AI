import json
import numpy as np
import pandas as pd
from transformers import pipeline
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib

class ModernMentalHealthAI:
    def __init__(self):
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        self.emotion_classifier = pipeline("text-classification", 
                                          model="j-hartmann/emotion-english-distilroberta-base")
        self.crisis_keywords = {
            'immediate_crisis': [
                'kill myself', 'suicide', 'end my life', 'want to die now',
                'going to jump', 'going to overdose', 'cutting myself',
                'planning suicide', 'suicide method', 'ready to die'
            ],
            'high_risk': [
                'hopeless', 'no reason to live', 'burden to everyone',
                'can\'t take anymore', 'unbearable pain', 'no way out',
                'better off dead', 'world without me', 'give up completely'
            ]
        }
    
    def analyze_modern_risk(self, text):
        """Modern risk analysis using multiple approaches"""
        text_lower = text.lower()
        
        # 1. Keyword-based scoring
        crisis_score = self._keyword_analysis(text_lower)
        
        # 2. Sentiment analysis
        sentiment_result = self.sentiment_analyzer(text)[0]
        sentiment_risk = self._sentiment_to_risk(sentiment_result)
        
        # 3. Emotion analysis
        emotion_result = self.emotion_classifier(text)[0]
        emotion_risk = self._emotion_to_risk(emotion_result)
        
        # Combined risk score
        total_risk = crisis_score * 0.6 + sentiment_risk * 0.2 + emotion_risk * 0.2
        
        return {
            'risk_level': min(10, total_risk),
            'risk_category': self._categorize_risk(total_risk),
            'sentiment': sentiment_result,
            'emotion': emotion_result,
            'crisis_indicators': self._extract_crisis_indicators(text_lower)
        }
    
    def _keyword_analysis(self, text):
        score = 0
        for keyword in self.crisis_keywords['immediate_crisis']:
            if keyword in text:
                score += 3
        for keyword in self.crisis_keywords['high_risk']:
            if keyword in text:
                score += 2
        return min(10, score)

# Usage example:
ai = ModernMentalHealthAI()
result = ai.analyze_modern_risk("I want to kill myself because everything is hopeless")
print(result)