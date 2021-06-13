from django.urls import path,include
from .views import *
from .routers import router



urlpatterns = [
    path('register/',UserRegisterAPIView.as_view()),
    path('login/',UserLoginAPIView.as_view()),
    path('logout/',LogOutAPIView.as_view()),
    path('auth-token/', ObtainAuthTokenView.as_view()),
    path('phone-auth-token/',phoneAuthTokenView.as_view()),
    path('create-referral/', CreateReferralView.as_view()),
    path('referred-users/', ReferredUser.as_view()),
    path('verify-user/', VerifyTeacherView.as_view()),
    path('teachers/', TeacherListView.as_view()),
    path('subscribe/',SubscriberView.as_view()),
    path('unsubscribe/',UnsubscribeView.as_view()),
    path('send-subscription-mail/<int:id>/', SendSubsriptionMailAPI.as_view()),
    path('', include(router.urls)),
]