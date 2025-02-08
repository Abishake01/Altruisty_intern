from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
app_name = 'internship'

urlpatterns = [
   
   path('applyrtime/',views.realtimeintern_apply,name='realtimeinternship'),
    path('appintern/<str:dom>',views.appintern,name='apply_internship'),
    
    path('uploaddq/',views.uploaddq,name="upload_dq"),
    path('showdaily_challenges/',views.showdq,name='show_daily_challenges'),
     path('getdq/<str:pk>',views.getdq,name='get_daily_challenges'),
    path('checkanswerd/',views.check_answer,name='checkanswer'),
     
     path('uploadwq/',views.uploadwq,name="upload_wq"),
    path('showweekly_challenges/',views.showwq,name='show_weekly_challenges'),
     path('getwq/<str:pk>',views.getwq,name='get_weekly_challenges'),
    path('checkanswerw/',views.check_answerw,name='checkanswerw'),
    
   path('uploadcq/',views.uploadcq,name="upload_cq"),
    path('showcommon_challenges/',views.showcq,name='show_common_challenges'),
     path('getcq/<str:pk>',views.getcq,name='get_common_challenges'),
    path('checkanswerc/',views.check_answerc,name='checkanswerc'),

    path('progress/',views.progress,name='progress'),
    path('request_teammate/', views.request_teammate, name='request_teammate'),
    path('connect_user/<str:user_id>/', views.connect_user, name='connect_user'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




















