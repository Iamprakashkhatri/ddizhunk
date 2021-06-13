from django.urls import path,include
from dashboard.viewsets.DashboardManagement import *
from .routers import router

app_name = 'dashboard'

urlpatterns = [
	path('', include(router.urls)),
    path('calculate-total/', DashboardTotalAPI.as_view(),name='calculate-total'),
    path('recent-report/',DashboardRecentReportAPI.as_view(),name='recent-report'),
    path('highest-selling-course/',DashboardHighestSellingCousesAPI.as_view(),name='highest-selling-course')
]


