from django.urls import path
from . import views

urlpatterns = [
    # Main unified interface
    path('', views.unified_assistant, name='unified_assistant'),
    
    # Core functionality
    path('chat/', views.chat_with_ai, name='chat_with_ai'),
    path('languages/', views.get_supported_languages, name='supported_languages'),
    path('voice/input/', views.process_voice_input, name='voice_input'),
    path('voice/response/', views.get_voice_response, name='voice_response'),
    path('status/', views.get_assistant_status, name='assistant_status'),
    path('commands/', views.get_quick_commands, name='quick_commands'),
    
    # Legacy routes for backward compatibility
    path('assistant/', views.voice_assistant, name='voice_assistant'),
    path('chatbot/', views.chatbot, name='chatbot'),
]
