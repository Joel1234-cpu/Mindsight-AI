import logging
import random

logger = logging.getLogger(__name__)

class RecommendationEngine:
    def __init__(self):
        self.exercises = self._initialize_exercises()
        self.resources = self._initialize_resources()
    
    def _initialize_exercises(self):
        return [
            {
                'id': 1,
                'title': 'Deep Breathing Exercise',
                'description': '5-minute guided breathing to reduce anxiety',
                'type': 'anxiety',
                'duration': 5,
                'content': 'Find a comfortable position. Breathe in slowly through your nose for 4 seconds, hold for 4 seconds, exhale slowly through your mouth for 6 seconds. Repeat 10 times.',
                'difficulty': 'beginner',
                'icon': '🌬️'
            },
            {
                'id': 2,
                'title': 'Gratitude Journaling',
                'description': 'Write down three things you are grateful for',
                'type': 'depression',
                'duration': 10,
                'content': 'Take a moment to reflect on positive aspects of your life. Write down three specific things you feel grateful for today, no matter how small.',
                'difficulty': 'beginner',
                'icon': '📝'
            },
            {
                'id': 3,
                'title': '5-4-3-2-1 Grounding Technique',
                'description': 'Use your senses to stay present',
                'type': 'anxiety',
                'duration': 3,
                'content': 'Name 5 things you can see, 4 things you can touch, 3 things you can hear, 2 things you can smell, and 1 thing you can taste.',
                'difficulty': 'beginner',
                'icon': '🌍'
            },
            {
                'id': 4,
                'title': 'Positive Affirmations',
                'description': 'Repeat positive statements about yourself',
                'type': 'depression',
                'duration': 5,
                'content': 'Repeat these affirmations: "I am worthy of love and happiness," "I am strong and capable," "I am doing my best," "This feeling is temporary."',
                'difficulty': 'beginner',
                'icon': '💫'
            },
            {
                'id': 5,
                'title': 'Body Scan Meditation',
                'description': 'Progressive relaxation through body awareness',
                'type': 'stress',
                'duration': 10,
                'content': 'Close your eyes. Slowly bring attention to each part of your body starting from your toes up to your head. Notice any tension and consciously relax each area.',
                'difficulty': 'intermediate',
                'icon': '🧘'
            }
        ]
    
    def _initialize_resources(self):
        return {
            'high_risk': [
                {'name': 'National Suicide Prevention Lifeline', 'number': '1-800-273-8255', 'available': '24/7'},
                {'name': 'Crisis Text Line', 'number': 'Text HOME to 741741', 'available': '24/7'},
                {'name': 'Emergency Services', 'number': '911', 'available': '24/7'}
            ],
            'general': [
                {'name': 'SAMHSA Helpline', 'number': '1-800-662-4357', 'available': '24/7'},
                {'name': 'NAMI Helpline', 'number': '1-800-950-6264', 'available': 'Mon-Fri 10AM-6PM ET'}
            ]
        }
    
    def get_personalized_recommendations(self, user_text, emotion_data, risk_level, limit=3):
        """Get personalized exercise recommendations based on user state"""
        try:
            # Determine recommendation focus based on risk and emotions
            if risk_level >= 7:  # High risk - focus on immediate calming
                focus_types = ['anxiety', 'stress']
                priority = 'immediate_calm'
            elif risk_level >= 4:  # Medium risk
                focus_types = ['anxiety', 'depression', 'stress']
                priority = 'emotional_regulation'
            else:  # Low risk
                focus_types = ['stress', 'general']
                priority = 'maintenance'
            
            # Filter exercises by type and priority
            filtered_exercises = [
                ex for ex in self.exercises 
                if ex['type'] in focus_types
            ]
            
            # Sort by difficulty (easier first for high risk)
            if priority == 'immediate_calm':
                filtered_exercises.sort(key=lambda x: 0 if x['difficulty'] == 'beginner' else 1)
            
            # Add priority information
            for exercise in filtered_exercises:
                exercise['priority'] = priority
                exercise['recommended_for'] = self._get_recommendation_reason(risk_level, emotion_data)
            
            return filtered_exercises[:limit]
            
        except Exception as e:
            logger.error(f"Recommendation error: {str(e)}")
            return self.get_default_recommendations(risk_level, limit)
    
    def _get_recommendation_reason(self, risk_level, emotion_data):
        if risk_level >= 7:
            return "Immediate calming technique"
        elif risk_level >= 4:
            return "Emotional regulation"
        else:
            return "Mental wellness maintenance"
    
    def get_default_recommendations(self, risk_level, limit=3):
        """Get default recommendations based on risk level"""
        return self.exercises[:limit]
    
    def get_emergency_resources(self, risk_level):
        """Get emergency resources for high-risk situations"""
        if risk_level >= 7:
            return {
                'emergency': True,
                'message': 'Your safety is important. Please contact one of these resources immediately:',
                'resources': self.resources['high_risk'],
                'additional_advice': [
                    'You are not alone',
                    'This feeling will pass',
                    'Reach out to someone you trust'
                ]
            }
        elif risk_level >= 4:
            return {
                'emergency': False,
                'message': 'Consider reaching out for additional support:',
                'resources': self.resources['general']
            }
        return None