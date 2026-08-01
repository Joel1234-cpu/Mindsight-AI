import nltk
from textblob import TextBlob
import logging

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self):
        logger.info("Sentiment analyzer initialized")
    
    def analyze_emotions(self, text):
        """Enhanced emotion analysis using TextBlob and NLTK"""
        if not text or len(text.strip()) < 3:
            return {"neutral": 1.0}
        
        try:
            analysis = TextBlob(text)
            polarity = analysis.sentiment.polarity
            subjectivity = analysis.sentiment.subjectivity
            
            # Enhanced emotion mapping based on sentiment analysis
            if polarity > 0.3:
                return {"joy": 0.8, "optimism": 0.6, "neutral": 0.2}
            elif polarity > 0.1:
                return {"joy": 0.5, "neutral": 0.5}
            elif polarity < -0.3:
                return {"sadness": 0.8, "fear": 0.5, "anger": 0.3}
            elif polarity < -0.1:
                return {"sadness": 0.6, "neutral": 0.4}
            else:
                if subjectivity > 0.5:
                    return {"curiosity": 0.6, "neutral": 0.4}
                else:
                    return {"neutral": 0.9, "calm": 0.1}
                
        except Exception as e:
            logger.error(f"Emotion analysis error: {str(e)}")
            return {"neutral": 1.0}
    
    def analyze_sentiment_intensity(self, text):
        """Get sentiment score (-1 to 1)"""
        try:
            analysis = TextBlob(text)
            return analysis.sentiment.polarity
        except:
            return 0.0
    
    def get_dominant_emotion(self, text):
        emotions = self.analyze_emotions(text)
        return max(emotions.items(), key=lambda x: x[1])