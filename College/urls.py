from django.urls import path
from . import views

urlpatterns = [
     path('college_home/', views.college_home, name='college_home'),
     path('college_home/profile/<str:user_id>/', views.user_profile, name='user_profile'),  # Accept string user_id
]
