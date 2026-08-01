from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('chat/', views.chat_view, name='chat'),
    path('chat/message/', views.chat_message, name='chat_message'),
    path('chat/history/', views.chat_history, name='chat_history'),
    path('chat/clear-history/', views.clear_history, name='clear_history'),
    path('reports/weekly/', views.weekly_report, name='weekly_report'),
    path('chat/faq_quiz/', views.faq_quiz, name='faq_quiz'),
    path('chat/history/', views.chat_history, name='chat_history'),
    path('chat/history/clear/', views.clear_history, name='clear_history'),
    path('chat/history/delete/<int:message_id>/', views.delete_single_message, name='delete_message'),
    


    # Auth URLs
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),

   
]