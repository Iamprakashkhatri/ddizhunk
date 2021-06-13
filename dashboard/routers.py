from rest_framework.routers import DefaultRouter

from dashboard.viewsets.DashboardManagement import *

router = DefaultRouter()
# router.register('highest-selling-course', DashboardHighestSellingCouseAPI,basename='highest-selling-course'),
router.register('new-users',DashboardNewUsersAPI,basename='new-users'),
router.register('recent-payment-order',RecentPaymentOrderAPI,basename='recent-payment')