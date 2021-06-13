from django.urls import path,include
from accounting.viewsets.AccountingManagement import AccountingTotalAPI
from .routers import router

app_name = 'accounting'

urlpatterns = [
	path('', include(router.urls)),
    path('calculate-total/', AccountingTotalAPI.as_view(),name='calculate-total'),
    # path('highest-selling-courses/',DashboardHighestSellingCousesAPI.as_view(),name='highest-selling-courses'),
]


