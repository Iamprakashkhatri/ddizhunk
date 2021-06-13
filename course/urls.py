from django.urls import path,include
from course.views import *
from .routers import router

urlpatterns = [
	path('', include(router.urls)),
	path('create/', CourseCreateView.as_view()),
	path('pay-and-enroll/', CourseEnrollView.as_view()),
]