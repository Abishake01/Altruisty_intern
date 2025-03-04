from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
    path('', include('video_call.urls')),
    path('', include('AI_tools.urls')),
    path('chatbot/', include('chatbot.urls')),
     path('', include('IdeaSubmission.urls')),
     path('', include('Ticketing.urls')),
     path('', include('internship.urls')),
     path('', include('courses.urls')),
     path('', include('community.urls')),
     path('', include('College.urls')),
     path('', include('Mentor.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
