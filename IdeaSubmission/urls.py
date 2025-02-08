from django.urls import path
from . import views


urlpatterns = [
     path('idea-submission/',views.idea_submission_form,name='idea_submission'),
     path('api/uploadidea/',views.submitidea)
]

