from rest_framework.routers import DefaultRouter

from accounting.viewsets.AccountingManagement import SalesReportAPI,AccountRetailersReportAPI,TeachersReportAPI

router = DefaultRouter()
router.register('sales-report', SalesReportAPI,basename='sales-report'),
router.register('retailers-report',AccountRetailersReportAPI,basename='retailers-report'),
router.register('teachers-report',TeachersReportAPI,basename='teacher-report')
