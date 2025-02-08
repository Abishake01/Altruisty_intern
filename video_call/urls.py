from django.urls import path
from . import views

urlpatterns = [
    path('lobby/', views.lobby, name='lobby'),
    path('lobby2/', views.lobby2, name='lobby2'),
    path('room/', views.room, name='room'),
    path('get_token/', views.getToken, name='get_token'),
    path('create_member/', views.createMember, name='create_member'),
    path('get_member/', views.getMember, name='get_member'),
    path('delete_member/', views.deleteMember, name='delete_member'),
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
    path('check_meeting_creator/', views.check_meeting_creator, name='check_meeting_creator'),
    path('get_user_details/', views.get_user_details, name='get_user_details'),
]