from django.urls import path
from . import views

urlpatterns = [
     path('college_home/', views.college_home, name='college_home'),
     path('college_home/profile/<str:user_id>/', views.progress, name='progress'),
     path('upload_image/', views.upload_image, name='upload_image'),

]
