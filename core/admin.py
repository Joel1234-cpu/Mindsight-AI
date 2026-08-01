from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, TextAnalysisSession, ImageReflectionTest, ChatMessage

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_message_short', 'sentiment_score', 'risk_level', 'timestamp')
    list_filter = ('timestamp', 'user')
    search_fields = ('user_message', 'bot_response')
    
    def user_message_short(self, obj):
        return obj.user_message[:50] + '...' if len(obj.user_message) > 50 else obj.user_message
    user_message_short.short_description = 'Message'

@admin.register(TextAnalysisSession)
class TextAnalysisSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'predicted_sentiment', 'confidence_score', 'timestamp')
    list_filter = ('timestamp', 'user')

@admin.register(ImageReflectionTest)
class ImageReflectionTestAdmin(admin.ModelAdmin):
    list_display = ('user', 'text_sentiment', 'timestamp')
    list_filter = ('timestamp', 'user')