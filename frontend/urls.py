from django.urls import path
from . import views


urlpatterns = [
    path('overview/',views.overview,name="overview"),
    path('api/questions/', views.get_questions, name='get_questions'),
    path('save-swot-analysis/', views.save_swot_analysis, name='save_swot_analysis'),
    path('improvement/',views.improvement,name="improvement"),
    path('create-swot/',views.createswot,name='create-swot'),
    path('strength/',views.strength,name="strength"),
    path('list/',views.list,name="list"),
    path('points/<str:data>',views.points,name="points"),
    path('swot/',views.swot,name="swot"),
    path('',views.login,name="index"),
    path('startup-home/',views.index,name="startup-home"),
    path('swotStartNow/', views.swotStartNow, name="swot-start-now"),  # Correct URL
    path('delete-report/<int:report_id>/', views.delete_report, name="delete-report"),
    path('report-detail/<int:id>/', views.report_detail, name='report-detail'),
    path('view-improvement/<int:id>/', views.viewImprovement, name='view-improvement'),
    path('save-improvements/', views.save_improvements, name='save_improvements'),
    path('verification_check/<str:udata>',views.verificationlogin,name='loginverify'),
    path('login/',views.login,name='login'),
    path('calender/',views.calender,name='calender'),
    path('course-video/',views.course_video,name='course-video'),
    path('internship_home/',views.internship_home,name='internship_home'),
    path('internship_home/my_learning.html',views.my_learning,name='my_learning'),
    path('add-member/',views.add_member,name="add_member"),
    path('members/', views.member_list, name='member_list'),
    path('costcategory/',views.costcategory,name="costcategory"),
    path('costover/',views.costover,name="costover"),
    path('costquestions/<str:category>',views.costquestions,name="costquestions"),
    path('startup_dashboard/',views.startup_dashboard,name="startup_dashboard"),
    path('api/updatescorecost/', views.gamescoreupdatecostcutting, name="update_score_cost_cutting"),
    path('logout/',views.logout,name="logout"),
]