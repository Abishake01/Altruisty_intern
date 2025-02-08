from django.urls import path
from . import views


urlpatterns = [
    path('mentor-home/',views.mentorHome,name='mentor_home')
]

