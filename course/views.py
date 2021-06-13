from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.db.models import Count, Avg
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework.parsers import FileUploadParser
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework import filters, status
from rest_framework.filters import SearchFilter
import requests
from account.models import Referrals,User
from account.tasks import send_email
from course.serializers import *
from course.models import *
from .permissions import IsTeacher,IsEnrolled
from payments.models import *

class CourseEnrollView(APIView):
    """
    For Khalti
    {"token": "khalti_transaction_token",
    "amount": "courseamount",
    "paymentMethod": "Khalti",
    "courseID": "id_of_course_to_be_enrolled"
    }
    For Esewa
    {"amount": 'courseamount',
    "refId": 'reference_id',
    "paymentMethod": 'Esewa',
    "courseID": 'id_of_course_to_be_enrolled'
    }
    For Free
    {
    "courseID":14
    }
    """
    permission_classes = [IsAuthenticated, ]

    def post(self, request, format=None):
        if request.data.get('token'):
            token = request.data['token']
        if request.data.get('amount'):
            amount = request.data['amount']
        if request.data.get('paymentMethod'):
            method = request.data['paymentMethod']
        if request.data.get('courseID'):
            pk = request.data['courseID']
        if request.data.get('refId'):
            refId=request.data['refId']

        course = None
        try:
            course = Course.objects.get(id=pk)
        except Course.DoesNotExist:
            return Response({'enrolled': False, 'detail': 'Course not found'})
        if course.sale_price == 0:
            course.students.add(request.user)
            return Response({'enrolled': True})

        else:
            if method == 'Khalti':
                if token and amount:
                    verified = verifypayment(token, amount)
                    print('verified',verified)
                    if verified:
                        course.students.add(request.user)
                        payment = Payment.objects.create(
                            done_by=request.user, method='Khalti',
                            amount=float(amount) / 100,
                            paid_for=course, status='Completed'
                        )
                        payment.save()
                        subject = 'Thank you for trusting PadhaiSewa'
                        message = f'Thank your for ordering Course {course.title}'
                        to_mail = [request.user.email, ]
                        html_content = render_to_string('invoice.html',
                                                        {'payment': payment,
                                                         'user': request.user,
                                                         'course':course,
                                                         'subject':subject,
                                                         'message':message}
                                                        )
                        send_email(
                            subject=subject, message=message,
                            html_content=html_content, to_mail=to_mail,
                        )
                        try:
                            referral = Referrals.objects.get(
                                referred=request.user)
                            print('referral',referral)
                            referral.referred_by.total_earning += 100
                            print('--',referral.referred_by.total_earning)
                            print('reference_id',referral.referred_by)
                            referral.referred_by.save()
                        except Exception:
                            pass
                        return Response({'enrolled': True,
                                         'detail': 'Payment Successfull,order completed.'})
                    else:
                        payment = Payment.objects.create(
                            done_by=request.user, method='Khalti',
                            amount=float(amount) / 100,
                            paid_for=course, status='To be verified'
                        )
                        payment.save()
                        """subject = 'Thank you for trusting PadhaiSewa'
                        message = f'Thank your for ordering Course {course.title}'
                        to_mail = [request.user.email, ]
                        html_content = render_to_string('invoice.html',
                                                        {'payment': payment,
                                                         'user': request.user})
                        send_email.delay(
                            subject=subject, message=message,
                            html_content=html_content, to_mail=to_mail,
                        )"""
                        return Response({'enrolled': False,
                                         'detail': 'Couldnt verify payment please contact support.'})
                else:
                    payment = Payment.objects.create(
                        done_by=request.user, method='Khalti',
                        amount=float(amount) / 100,
                        paid_for=course, status='Payment Failed'
                    )
                    payment.save()
                    """subject = 'Thank you for trusting PadhaiSewa'
                    message = f'Thank your for ordering Course {course.title}'
                    to_mail = [request.user.email, ]
                    html_content = render_to_string('invoice.html',
                                                    {'payment': payment,
                                                     'user': request.user})
                    send_email.delay(
                        subject=subject, message=message,
                        html_content=html_content, to_mail=to_mail,
                    )"""
                    return Response({'enrolled': False,
                                     'detail': 'Payment Failed,Connection Issue.'})
            elif method == 'Esewa':
                if refId and amount:
                    verified = esewaverifypayment(refId, amount,pk)
                    if verified:
                        course.students.add(request.user)
                        print('course',course.title)
                        payment = Payment.objects.create(
                            done_by=request.user, method='Esewa',
                            amount=amount,
                            paid_for=course, status='Completed'
                        )
                        payment.save()
                        subject = 'Thank you for trusting PadhaiSewa'
                        message = f'Thank your for ordering Course {course.title}'
                        to_mail = [request.user.email, ]
                        html_content = render_to_string('invoice.html',
                                                        {'payment': payment,
                                                         'user': request.user,
                                                         'course':course,
                                                         'subject':subject,
                                                         'message':message}
                                                        )
                        send_email(
                            subject=subject, message=message,
                            html_content=html_content, to_mail=to_mail,
                        )
                        try:
                            referral = Referrals.objects.get(
                                referred=request.user)
                            referral.referred_by.total_earning += 100
                            referral.referred_by.save()
                        except Exception:
                            pass
                        return Response({'enrolled': True,
                                         'detail': 'Payment Successfull,order completed.'})
                    else:
                        payment = Payment.objects.create(
                            done_by=request.user, method='Esewa',
                            amount=amount,
                            paid_for=course, status='To be verified'
                        )
                        payment.save()
                        """subject = 'Thank you for trusting PadhaiSewa'
                        message = f'Couldnt verify payment for ordering Course {course.title}'
                        to_mail = [request.user.email, ]
                        html_content = render_to_string('invoice.html',
                                                        {'payment': payment,
                                                         'user': request.user,
                                                         'course':course,
                                                         'subject':subject,
                                                         'message':message})
                        send_email(
                            subject=subject, message=message,
                            html_content=html_content, to_mail=to_mail,
                        )"""
                        return Response({'enrolled': False,
                                         'detail': 'Couldnt verify payment please contact support.'})
                else:
                    payment = Payment.objects.create(
                        done_by=request.user, method='Esewa',
                        amount=amount,
                        paid_for=course, status='Payment Failed'
                    )
                    payment.save()
                    """subject = 'Thank you for trusting PadhaiSewa'
                    message = f'Thank your for ordering Course {course.title}'
                    to_mail = [request.user.email, ]
                    html_content = render_to_string('invoice.html',
                                                    {'payment': payment,
                                                     'user': request.user,
                                                     'course':course,
                                                     'subject':subject,
                                                     'message':message})
                    send_email(
                        subject=subject, message=message,
                        html_content=html_content, to_mail=to_mail,
                    )"""
                    return Response({'enrolled': False,
                                     'detail': 'Payment Failed,Connection Issue.'})
            elif method == 'Bank Transfer Offline':
                payment = Payment.objects.create(
                    done_by=request.user, method='Bank Transfer Offline',
                    amount=amount / 100,
                    paid_for=course, status='To be verified'
                )
                payment.save()
                """subject = 'Thank you for trusting PadhaiSewa'
                message = f'Thank your for ordering Course {course.title}'
                to_mail = [request.user.email, ]
                html_content = render_to_string('invoice.html',
                                                {'payment': payment,
                                                 'user': request.user,
                                                 'course':course,
                                                 'subject':subject,
                                                 'message':message})
                send_email.delay(
                    subject=subject, message=message,
                    html_content=html_content, to_mail=to_mail,
                )"""
                return Response({'enrolled': False,
                                 'detail': 'Contact support to verify your payment'})
            else:
                return Response({
                    'enrolled': False,
                    'detail': 'Please choose a valid payment option'
                })


def verifypayment(token, amount):
    payload = {
        "token": token,
        "amount": amount,
    }
    headers = {
        "Authorization": "Key {}".format(settings.KHALTI_SECRET_KEY)
    }
    try:
        response = requests.post(settings.KHALTI_VERIFY_URL, payload,
                                 headers=headers)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.HTTPError as e:
        return False

def esewaverifypayment(refId, amount,pk):
    import xml.etree.ElementTree as ET
    url ="https://uat.esewa.com.np/epay/transrec"
    d = {
    'amt': amount,
    'scd': 'epay_payment',
    'rid': refId,
    'pid':pk,
    }
    resp = requests.post(url, d)
    root = ET.fromstring(resp.content)
    status = root[0].text.strip()
    print('status',status)
    if status =="Success":
        return True
    else:
        return False

class CourseAPIView(generics.ListAPIView):
    # queryset = Course.objects.all()
    serializer_class = CourseSerializer
    def get_queryset(self):
        return Course.objects.all()

class EnrolledCourseView(viewsets.ModelViewSet):
    serializer_class = CourseContentSerializer
    queryset = Course.objects.all()
    http_method_names = ['get',]
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """ Manage Course
    ## View Detail through slug:
        http://localhost:8000/course/course-11/
    """
    permission_classes=[IsAuthenticated,IsEnrolled]
    queryset = Course.objects.all()
    serializer_class = CourseContentSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['category__id', 'title']

    def get_queryset(self):
        return Course.objects.filter(visibility=True).annotate(
            no_of_topics=Count('modules__lessons'),
            no_of_lessons=Count('modules__lessons__contents'),
            no_of_enroll=Count('students__id', distinct=True),
            rating=Avg('ratings__rating')
        )

    @action(detail=True,
            methods=['get'],
            serializer_class=CourseContentSerializer,
            permission_classes=[IsAuthenticated,IsEnrolled])
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class CourseCreateView(APIView):
    '''
    Required Data Format
    {
            "sub_category": 1,
            "title": "youtube preview-second",
            "overview": "overview",
            "created": "2021-05-26T13:31:35.922712Z",
            "owner": [
                1
            ],
            "modules": [
                {
                    "lessons": [
                        {
                            "order": 0,
                            "title": "title-1",
                            "description": "this is lesson first",
                            "video":null,
                            "contents": [],
                            "time": "4"
                        }
                    ],
                    "title": "module 2",
                    "description": "module 2",
                    "order": 0,
                    "course": 45
                }
            ],
            "price": 200,
            "description": "<p>description\t</p>",
            "thumbnail": null,
            "preview_video": null,
            "sale_price":20,
            "syllabus": "syllabus",
            "notes": "notes",
        }
    '''
    permission_classes = [IsAuthenticated,IsTeacher]
    serializer_class = CourseCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = CourseCreateSerializer(data=request.data, context={
            'request': self.request})
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

# class CourseCreateView(viewsets.ModelViewSet):
#     permission_classes = [IsTeacher, ]
#     serializer_class = CourseCreateSerializer
#     http_method_names = ['post', ]


class CategoryViewset(viewsets.ModelViewSet):
    """ Manage Category
    ## Filtering:
        Filter by status  http://localhost:8000/categories/?status=active
    ## Search:
        Search by status http://localhost:8000/categories/?search=active
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAdminUser, ]
    filter_backends = [DjangoFilterBackend,SearchFilter, ]
    search_fields = ['status']
    filterset_fields = ['status']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permission() for permission in (AllowAny,)]
        return super(CategoryViewset, self).get_permissions()

class SubCategoryViewset(viewsets.ModelViewSet):
    """ Manage SubCategory
    ## Filtering:
        Filter by status name, category id and title  http://localhost:8000/categories/?status=active
    ## Search:
        Search by status,title, and category id http://localhost:8000/categories/?search=active
    """
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()
    permission_classes = [IsAdminUser, ]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter,DjangoFilterBackend]
    search_fields = ['category__id', 'title','status','id','slug']
    filterset_fields = ['category__id','title','status','id','slug']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permission() for permission in (AllowAny,)]
        return super(SubCategoryViewset, self).get_permissions()


class CourseGetView(viewsets.ModelViewSet):
    serializer_class = CourseGetSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAdminUser, ]
    lookup_field = 'slug'

class RatingView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = RatingSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('course__id',)
    queryset = Rating.objects.all()


class CourseUpdateAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    serializer_class = UpdateCourseSerializer
    queryset = Course.objects.all()
    http_method_names = ['patch', 'delete', ]

class ModuleUpdateAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    serializer_class = UpdateModuleSerializer
    queryset = Module.objects.all()
    http_method_names = ['patch', 'delete', 'post', ]


class LessonUpdateAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    serializer_class = UpdateLessonSerializer
    queryset = Lesson.objects.all()
    http_method_names = ['patch', 'delete', 'post', ]


class ContentUpdateAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    serializer_class = UpdateContentSerializer
    queryset = Content.objects.all()
    http_method_names = ['patch', 'delete', 'post', ]


class FileCreateView(APIView):
    permission_classes = [IsAuthenticated, ]

    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=self.request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)