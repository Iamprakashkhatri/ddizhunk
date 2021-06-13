from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAdminUser
from rest_framework import viewsets,mixins
from rest_framework import filters,status
from rest_framework.filters import SearchFilter
from django.core.exceptions import ObjectDoesNotExist
from account.models import User
from account.serializers import BasicUserSerializer
from payments.models import Payment
from course.models import Course,SubCategory,Category
from accounting.serializers import SubcategorySerializer,AccountCategorySerializer,AccountTeacherSerializer
from django.db.models import Count, Avg,Sum,Exists,Q,F


import datetime


class AccountingTotalAPI(APIView):
	permission_classes = (IsAdminUser,)
	def get(self, request):
		try:
			today_sales = Payment.objects.filter(created_at__date=datetime.date.today()).count()
			total_sales = Payment.objects.filter(status='Completed').count()
			sales = Payment.objects.filter(status='Completed')
			cal_total_revenue = 0
			for revenue in sales:
				cal_total_revenue = cal_total_revenue + float(revenue.amount)
			enroll = Course.objects.filter(visibility=True).annotate(no_of_enroll=Count('students__id', distinct=True)).count()
			print('enroll',enroll)
			context=[
				{
    			"today_sales":today_sales,
    			"total_sales":total_sales,
    			"total_balance":cal_total_revenue,
    			"total_enroll":enroll
    			}
    		]
		except ObjectDoesNotExist:
			return Response({'message': 'There is no list'})
		return Response({'context': context}, status=200)


class SalesReportAPI(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    permission_classes = (IsAdminUser,)
    queryset = SubCategory.objects.all()
    serializer_class = SubcategorySerializer
    
    def get_queryset(self):
    	subquery=SubCategory.objects.filter(rel_sub_category__payment__status='Completed')
    	print('subquery',subquery)
    	print('queryset',SubCategory.objects.all().annotate(no_of_enroll=Count('rel_sub_category__students__id', distinct=True)))
    	return SubCategory.objects.all().annotate(
            # total_sales=Exists(SubCategory.objects.filter(courses__payment__status='Completed')),
            total_sales=Count('rel_sub_category__payment__id',filter=Q(rel_sub_category__payment__status='Completed'), distinct=True),
            no_of_enroll=Count('rel_sub_category__students__id', distinct=True),
            rating=Avg('rel_sub_category__ratings__rating')
        )

class AccountRetailersReportAPI(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    permission_classes = (IsAdminUser,)
    queryset = Course.objects.all()
    serializer_class = AccountCategorySerializer
    filter_backends = [SearchFilter, ]
    search_fields = ['sub_category__id','title']

    def get_queryset(self):
    	return Course.objects.all().annotate(
            total_sales=Count('payment__id',filter=Q(payment__status='Completed'), distinct=True),
            no_of_enroll=Count('students__id', distinct=True),
            payment_mode=F('payment__method'),
            rating=Avg('ratings__rating')
            )

class TeachersReportAPI(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = AccountTeacherSerializer
    filter_backends = [SearchFilter, ]
    search_fields = ['first_name']

    def get_queryset(self):
    	return User.objects.filter(is_teacher=True).annotate(
            course_name=F('teacher__title')
            # viewers=F('teacher__viewed_course')
            )
    