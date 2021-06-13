"""dizhunk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from account.views import (
    TeacherCourseView
    )
from course.views import (
    CourseViewSet,
    CategoryViewset,
    SubCategoryViewset,
    EnrolledCourseView,
    CourseGetView,
    CourseUpdateAPI,
    ContentUpdateAPI,
    LessonUpdateAPI,
    ModuleUpdateAPI,
    RatingView,
    FileCreateView
    )
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view
from rest_framework.documentation import include_docs_urls

schema_view = get_swagger_view(title='Pastebin API')

router = DefaultRouter()

router.register('courses', CourseViewSet)
router.register('categories', CategoryViewset)
router.register('subcategories', SubCategoryViewset)
router.register('enrolledcourses', EnrolledCourseView)
router.register('getcourse', CourseGetView)
router.register('teacher-courses', TeacherCourseView)
router.register('update-course', CourseUpdateAPI)
router.register('update-content', ContentUpdateAPI)
router.register('update-lesson', LessonUpdateAPI)
router.register('update-module', ModuleUpdateAPI)
router.register('ratings', RatingView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('swagger-docs/', schema_view),
    path('docs/sw-api/', include_docs_urls(title='Pastebin API', public=False)),
    path('api/accounts/', include('account.urls')),
    path('api/courses/', include('course.urls')),
    path('api/client/',include('client.urls')),
    path('api/dashboard/',include('dashboard.urls')),
    path('api/accounting/',include('accounting.urls')),
    path('api/misc/',include('misc.urls')),
    path('api/fileupload/', FileCreateView.as_view()),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)