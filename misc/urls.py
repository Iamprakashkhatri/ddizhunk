from django.urls import path, include

from .routers import router

app_name = 'misc'

urlpatterns = [
    path('', include(router.urls)),

]
