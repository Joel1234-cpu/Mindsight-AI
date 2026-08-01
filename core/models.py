from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom user model that extends Django's built-in User model
    """
    # Additional fields for the user profile
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    
    # Mental health related fields
    emergency_contact = models.CharField(max_length=100, blank=True, null=True)
    therapy_preferences = models.TextField(blank=True, null=True)
    consent_for_analysis = models.BooleanField(default=True)
    
    # Mental wellness tracking
    mood_trend = models.JSONField(default=dict, blank=True)
    risk_history = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username

class ChatMessage(models.Model):
    """
    Model to store chat interactions between user and chatbot
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_message = models.TextField()
    bot_response = models.TextField()
    sentiment_score = models.FloatField(default=0.0)  # -1 to 1 scale
    risk_level = models.IntegerField(default=0)  # 0-10 scale
    emotions = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Chat messages'

    def __str__(self):
        return f"{self.user.username}: {self.user_message[:50]}"
    
    def get_sentiment_label(self):
        """Convert sentiment score to human-readable label"""
        if self.sentiment_score > 0.3:
            return "Positive"
        elif self.sentiment_score < -0.3:
            return "Negative"
        else:
            return "Neutral"
    
    def get_risk_category(self):
        """Convert risk level to category"""
        if self.risk_level >= 7:
            return "High"
        elif self.risk_level >= 4:
            return "Medium"
        else:
            return "Low"

class WeeklyReport(models.Model):
    """
    Model to store weekly mental health reports
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week_start = models.DateField()
    week_end = models.DateField()
    total_chats = models.IntegerField(default=0)
    average_sentiment = models.FloatField(default=0.0)
    average_risk = models.FloatField(default=0.0)
    dominant_emotion = models.CharField(max_length=50, default='neutral')
    insights = models.JSONField(default=list, blank=True)
    recommendations = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'week_start']
        ordering = ['-week_start']
    
    def __str__(self):
        return f"Weekly Report for {self.user.username} - {self.week_start}"

class TextAnalysisSession(models.Model):
    """
    Model to store text analysis sessions and their results
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_input = models.TextField()
    predicted_sentiment = models.CharField(max_length=50)
    confidence_score = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"

class ImageReflectionTest(models.Model):
    """
    Model to store image reflection test results
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_shown = models.CharField(max_length=255)
    user_text = models.TextField()
    detected_emotions = models.JSONField()
    text_sentiment = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"