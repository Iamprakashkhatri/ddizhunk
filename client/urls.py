from django.urls import path,include
from client.viewsets.ClientManagement import UserProfile,UserProfileCourse,ChangePasswordView,TeacherAPI
from .views import *
from .routers import router

app_name = 'client'

urlpatterns = [
	path('', include(router.urls)),
    path('user-profile/',UserProfile.as_view(),name='user-profile'),
    path('user-profile-course/',UserProfileCourse.as_view(),name='user-profile-course'),
    # path('update-password/',UpdatePassword.as_view(),name='update-password'),
    path('change-password/',ChangePasswordView.as_view(),name='change-password'),
    path('teachers/',TeacherAPI.as_view(),name='teacher'),
    path('esewa-request/<int:id>/',esewarequest,name='esewa-request'),
    path('khalti-request/<int:id>/',khaltirequest,name='khalti-request')
 #    path('recent-report/',DashboardRecentReportAPI.as_view(),name='recent-report')
]


