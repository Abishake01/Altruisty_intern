from django.urls import path
from . import views  # Import views from the chatbot app

urlpatterns = [
    path('download/', views.download, name='download'),  # Map the `download` function
     path('', views.chatbot, name='chatbot'),
     path('chat/', views.chat_view, name='chat'),
     path('documentdbsave/', views.documentdbsave, name='document'),
]
