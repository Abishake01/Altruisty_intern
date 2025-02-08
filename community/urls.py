from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



app_name='community'

urlpatterns=[
    path('community_info/<str:pk>',views.community_info,name='community_info'),
    path('involvedcommunity_info/<str:pk>',views.invlvedcommunity_info,name='involvedcommunity_info'),
    path('exitcommunity/',views.delete_member,name='exit_community'),
    path('user_info/<str:pk>',views.userinfo,name='user_info'),
    path('following_info/<str:pk>',views.following_info,name='following_info'),
   path('community_index/<str:pk>',views.community_index,name='community'),
   path('change_community/',views.community_content_change,name='community_change'),
    path('join_community/<str:pk>',views.joincomm,name='join_community'),
    path('community_list/',views.community_list,name='community_list'),
    path('community_data/<str:pk>',views.community_data,name='community_data'),
    path('mediapost/<str:uid>/<str:comid>',views.mediaform,name='mediaform'),
    path('mediapostupload/',views.mediapostupload,name='mediapostupload'),
    path('community_chat/',views.chat_community,name='chat_community'),
     path('edit_chat/<str:pk>/<str:cd>',views.edit_chat,name='chat_edit'),
     path('view_media/<str:pk>/<str:cd>',views.view_media,name="view_media"),
     path('edit_content/',views.edit_content,name='content_edit'),
     path('join_community/',views.join_community,name='join_community'),
     path('search_community/<str:pk>/<str:query>',views.search_community,name='search_community'),
     path('add_member/',views.add_member,name="add_member"),
     path('follow_user/',views.follow_member,name="follow_user"),
     path('unfollow_user/',views.unfollow_member,name="unfollow_user"),
      path('createcommunity/',views.create_communityini,name="create_community"),
     path('community_home/',views.community_home,name="community_home"),
     path('community_myfeed/<str:pk>',views.community_myfeed,name="community_myfeed"),
      path('generalpostupload/',views.generalpostupload,name='generalpostupload'),
      path('find_user/<str:pk>',views.search_info,name='find_user'),
      path('editprofile/',views.editprofile,name='editprofile'),
      path('calender_check/',views.calender,name='calender_check')
     
    ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)