from rest_framework.views import APIView
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Avg
from django.db.models import Q
from account.models import User
from payments.models import Payment
from payments.serializers import PaymentSerializer
from course.models import Course
from course.serializers import CourseContentSerializer
from account.serializers import UserSerializers
import datetime
from datetime import date, timedelta


class DashboardTotalAPI(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        try:
            total_user = User.objects.all().count()
            total_sales = Payment.objects.filter(status='Completed').count()
            sales = Payment.objects.filter(status='Completed')
            cal_total_revenue = 0
            for revenue in sales:
                cal_total_revenue = cal_total_revenue + float(revenue.amount)
            enroll = Course.objects.filter(visibility=True).annotate(
                no_of_enroll=Count('students__id', distinct=True)).count()
            print('enroll', enroll)
            context = [
                {
                    "total_user": total_user,
                    "total_sales": total_sales,
                    "total_balance": cal_total_revenue,
                    "total_enroll": enroll
                }
            ]
        except ObjectDoesNotExist:
            return Response({'message': 'There is no list'})
        return Response({'context': context}, status=200)


class DashboardHighestSellingCousesAPI(APIView):
	permission_classes = (IsAdminUser,)
	def get(self, request):
		enroll = Course.objects.filter(visibility=True).annotate(no_of_enroll=Count('students__id'))
		enroll1=enroll[::-1]
		top_six_selling_courses = []
		course_count =Course.objects.count()
		top_six_selling_courses_count = len(top_six_selling_courses)
		for course in enroll1:
			cour = course.id
			print('cour',cour)
			if cour not in top_six_selling_courses:
				top_six_selling_courses.append(cour)
				top_six_selling_courses_count += 1
			if top_six_selling_courses_count == 6 or top_six_selling_courses_count == course_count:
				break
		print('top_six_selling_courses',top_six_selling_courses)
		courses = Course.objects.filter(id__in=top_six_selling_courses)
		print('courses',courses)
		data = CourseSerializer(courses, many=True, context={'request': request}).data
		return Response(data, status=200)


# class DashboardHighestSellingCouseAPI(viewsets.GenericViewSet,
#                                       mixins.ListModelMixin,
#                                       mixins.RetrieveModelMixin,
#                                       mixins.UpdateModelMixin,
#                                       mixins.DestroyModelMixin):
#     permission_classes = (IsAdminUser,)
#     enroll = Course.objects.filter(visibility=True).annotate(
#         no_of_enroll=Count('students__id'))
#     enroll1 = enroll[::-1]
#     queryset = enroll1
#     serializer_class = CourseContentSerializer

#     def get_queryset(self):
#         try:
#             enroll = Course.objects.filter(visibility=True).annotate(
#                 no_of_enroll=Count('students__id'))
#             enroll1 = enroll[::-1]
#             top_six_selling_courses = []
#             course_count = Course.objects.count()
#             top_six_selling_courses_count = len(top_six_selling_courses)
#             for course in enroll1:
#                 cour = course.id
#                 print('cour', cour)
#                 if cour not in top_six_selling_courses:
#                     top_six_selling_courses.append(cour)
#                     top_six_selling_courses_count += 1
#                 if top_six_selling_courses_count == 6 or top_six_selling_courses_count == course_count:
#                     break
#             print('top_six_selling_courses', top_six_selling_courses)
#             queryset = Course.objects.filter(id__in=top_six_selling_courses)
#             return queryset
#         except ObjectDoesNotExist:
#             # raise Http404("You do not have not order history")
#             return Response({"message": "You do not have not course history"},
#                             status=200)


class DashboardNewUsersAPI(viewsets.GenericViewSet, mixins.ListModelMixin,
                           mixins.RetrieveModelMixin):
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def paginate_queryset(self, queryset):
        if self.paginator and self.request.query_params.get(
                self.paginator.page_query_param, None) is None:
            return None
        return super().paginate_queryset(queryset)

    def get_queryset(self):
        try:
            current_week = (datetime.date.today())
            current_week_max = (datetime.date.today() + timedelta(days=7))
            queryset = User.objects.filter(date_joined__gte=current_week,
                                           date_joined__lte=current_week_max).order_by(
                'date_joined')
            return queryset
        except ObjectDoesNotExist:
            # raise Http404("You do not have not order history")
            return Response({"message": "You do not have not user history"},
                            status=200)


class DashboardRecentReportAPI(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        try:
            total_sales = Payment.objects.filter(status='Completed').count()
            jan = Payment.objects.filter(
                Q(created_at__month="01") &
                Q(status='Completed')).count()
            feb = Payment.objects.filter(
                Q(created_at__month="02") &
                Q(status='Completed')).count()
            march = Payment.objects.filter(
                Q(created_at__month="03") &
                Q(status='Completed')).count()
            apr = Payment.objects.filter(
                Q(created_at__month="04") &
                Q(status='Completed')).count()
            may = Payment.objects.filter(
                Q(created_at__month="05") &
                Q(status='Completed')).count()
            jun = Payment.objects.filter(
                Q(created_at__month="06") &
                Q(status='Completed')).count()
            jul = Payment.objects.filter(
                Q(created_at__month="07") &
                Q(status='Completed')).count()
            aug = Payment.objects.filter(
                Q(created_at__month="08") &
                Q(status='Completed')).count()
            sep = Payment.objects.filter(
                Q(created_at__month="09") &
                Q(status='Completed')).count()
            octe = Payment.objects.filter(
                Q(created_at__month="10") &
                Q(status='Completed')).count()
            nov = Payment.objects.filter(
                Q(created_at__month="11") &
                Q(status='Completed')).count()
            dec = Payment.objects.filter(
                Q(created_at__month="12") &
                Q(status='Completed')).count()

            context = [
                {
                    "month": "Jan",
                    "total_sell": jan
                },
                {
                    "month": "Feb",
                    "total_sell": feb
                },
                {
                    "month": "Mar",
                    "total_sell": march
                },
                {
                    "month": "Apr",
                    "total_sell": apr
                },
                {
                    "month": "May",
                    "total_sell": may
                },
                {
                    "month": "Jun",
                    "total_sell": jun
                },
                {
                    "month": "July",
                    "total_sell": jul
                },
                {
                    "month": "Aug",
                    "total_sell": aug
                },
                {
                    "month": "Sep",
                    "total_sell": sep
                },
                {
                    "month": "Oct",
                    "total_sell": octe
                },
                {
                    "month": "Nov",
                    "total_sell": nov
                },
                {
                    "month": "Dec",
                    "total_sell": dec
                },

            ]

        except ObjectDoesNotExist:
            return Response({'message': 'No Items in your List'})
        return Response({'total_sales': total_sales, 'context': context},
                        status=200)


class RecentPaymentOrderAPI(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    permission_classes = (IsAdminUser,)
    queryset = Payment.objects.order_by('-id')[:10]
    serializer_class = PaymentSerializer
