from django.urls import path
from . import views


urlpatterns = [
    path('course-list/',views.courseListPage,name="course-list"),
    path('course/<str:course_id>/', views.course_details, name='course_details'),
]

