from django.urls import path
from . import views


urlpatterns = [
     path('college_home/',views.college_home,name='college_home'),
]