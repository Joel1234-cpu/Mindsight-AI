import re
import logging

logger = logging.getLogger(__name__)

class RiskAssessor:
    def __init__(self):
        self.keyword_weights = {
            'suicide': 10, 'kill myself': 9, 'want to die': 9, 'end it all': 8,
            'depressed': 6, 'hopeless': 7, 'worthless': 6, 'anxious': 4,
            'panic': 5, 'cant cope': 6, 'overwhelmed': 5, 'help me': 4,
            'alone': 3, 'scared': 4, 'terrified': 5, 'crying': 3
        }
    
    def assess_risk_level(self, text, user_history=None):
        """Assess mental health risk level (0-10 scale)"""
        try:
            # Keyword analysis
            keyword_score = self._keyword_analysis(text)
            
            # Sentiment analysis
            from .sentiment_analyzer import sentiment_analyzer
            sentiment_score = sentiment_analyzer.analyze_sentiment_intensity(text)
            sentiment_risk = abs(sentiment_score) * 3 if sentiment_score < -0.2 else 0
            
            # Urgency analysis
            urgency_score = self._urgency_analysis(text)
            
            # Text characteristics
            text_score = self._text_characteristics_analysis(text)
            
            # Combined risk score
            total_risk = (
                keyword_score * 0.4 +
                sentiment_risk * 0.3 +
                urgency_score * 0.2 +
                text_score * 0.1
            )
            
            risk_level = min(10, total_risk)
            
            return {
                'risk_level': round(risk_level, 2),
                'risk_category': self._get_risk_category(risk_level),
                'factors': {
                    'keywords_found': self._get_found_keywords(text),
                    'sentiment_intensity': round(sentiment_score, 2),
                    'urgency_indicators': urgency_score > 0
                }
            }
            
        except Exception as e:
            logger.error(f"Risk assessment error: {str(e)}")
            return {'risk_level': 0, 'risk_category': 'low', 'factors': {}}
    
    def _keyword_analysis(self, text):
        text_lower = text.lower()
        score = 0
        for keyword, weight in self.keyword_weights.items():
            if keyword in text_lower:
                count = text_lower.count(keyword)
                score += weight * min(count, 3)  # Cap repeated keywords
        return min(10, score)
    
    def _urgency_analysis(self, text):
        urgency_patterns = [
            (r'\b(help|emergency|urgent|now|immediately)\b', 3),
            (r'!{2,}', 2),  # Multiple exclamation marks
            (r'\b(cant|cannot).*cope\b', 4),
            (r'\b(please).*help\b', 3),
            (r'\b(need).*help\b', 3)
        ]
        
        score = 0
        text_lower = text.lower()
        for pattern, weight in urgency_patterns:
            matches = re.findall(pattern, text_lower)
            score += len(matches) * weight
        
        return min(5, score)
    
    def _text_characteristics_analysis(self, text):
        """Analyze text characteristics that might indicate distress"""
        score = 0
        # Very short or very long messages might indicate distress
        words = text.split()
        if len(words) < 3:
            score += 2
        elif len(words) > 100:  # Very long message
            score += 1
            
        # Multiple question marks or exclamation marks
        if text.count('?') > 3 or text.count('!') > 3:
            score += 2
            
        return min(3, score)
    
    def _get_found_keywords(self, text):
        text_lower = text.lower()
        found = []
        for keyword in self.keyword_weights.keys():
            if keyword in text_lower:
                found.append(keyword)
        return found
    
    def _get_risk_category(self, risk_level):
        if risk_level >= 7:
            return 'high'
        elif risk_level >= 4:
            return 'medium'
        else:
            return 'low'