from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.generics import GenericAPIView,ListAPIView
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from account.models import User
from .serializers import *
from course.models import Course
from course.serializers import CourseContentSerializer
from .tasks import send_subscription_email




@method_decorator(name='post', decorator=swagger_auto_schema(tags=['User']))
class UserRegisterAPIView(GenericAPIView):
    serializer_class = UserSerializers
    def post(self, request, *args, **kwargs):
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(password = make_password(serializer.validated_data['password']))
            token,created = Token.objects.get_or_create(user_id=serializer.data['id'])
            return JsonResponse({'message': 'success', 'details': serializer.data, 'Token': token.key},status=201)
        return JsonResponse({'message': 'failure', 'details': serializer.errors},status=400)


@method_decorator(name='post', decorator=swagger_auto_schema(tags=['User']))
class UserLoginAPIView(GenericAPIView):
    serializer_class = LoginSerializers
    def post(self, request, *args, format=None):
        serializer = LoginSerializers(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            user = authenticate(
                username=email,
                password=password
                )
            if user:
                serializer = UserSerializers(user)
                token,created = Token.objects.get_or_create(user_id=serializer.data['id'])
                return JsonResponse(
                    {'message': 'success',
                     'details': serializer.data,
                     'Token': token.key},
                    status=201
                    )
            return JsonResponse({'message': 'failure', 'details': 'Invalid Credentials'},status=400)
        return JsonResponse({'message': 'failure', 'details': serializer.errors},status=400)


@method_decorator(name='post', decorator=swagger_auto_schema(tags=['User']))
class LogOutAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self, request, *args, **kwargs):
        print(request.user)
        token = Token.objects.filter(user=request.user).delete()
        return Response({'Logged Out'})


class ObtainAuthTokenView(ObtainAuthToken):
    """
    Data Format
    #if usename and password
    {
        "username":"",
        "password":""
    }
    #or access_token
    {
        "access_token":"",
    }

    """
    serializer_class = DizHunkaAuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        print('user',user)
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        #else:
            #return Response({'error': 'Already logged in'}, status=status.HTTP_400_BAD_REQUEST)
        user_serializer = UserSerializers(user)
        return Response({'token': token.key, 'user': user_serializer.data})


class phoneAuthTokenView(ObtainAuthToken):
    """
    Data Format
    {
        "access_token":"",
    }
    """
    serializer_class = DizHunkaPhoneAuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        print('user',user)
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        #else:
            #return Response({'error': 'Already logged in'}, status=status.HTTP_400_BAD_REQUEST)
        user_serializer = UserSerializers(user)
        return Response({'token': token.key, 'user': user_serializer.data})


class CreateReferralView(APIView):
    """
    Data Format
    {
        "referral_code":"",
        "firebase_uuid":""
    }
    """

    def post(self, request, *args, **kwargs):
        try:
            referral_code = request.data['referral_code']
            firebase_uuid = request.data['firebase_uuid']
        except MultiValueDictKeyError:
            referral_code = False
            firebase_uuid = False
        if referral_code and firebase_uuid:
            try:
                referred_by = User.objects.get(referral_code=referral_code)
                referred = User.objects.get(firebase_uuid=firebase_uuid)
                Referrals.objects.create(referred_by=referred_by, referred=referred)
                referred_by.users_referred.add(referred)
                print('referred',referred_by)
                referred_by.save()
                return Response({'status': True, 'detail': 'Referral Successfull'})
            except User.DoesNotExist:
                return Response({'status': False, 'detail': 'Referring user doesnt exist'})
        else:
            return Response({'status': False, 'detail': 'Invalid Data Format'})

class ReferredUser(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ReferralUserSerializer

    def get_queryset(self):
        return Referrals.objects.filter(referred_by=self.request.user)


class VerifyTeacherView(APIView):
    """
    api for teacher verify
    :param
    id
    http://127.0.0.1:8000/api/account/verify-user/?id=1
    """
    permission_classes = [IsAdminUser, ]

    def get(self, request, *args, **kwargs):
        user = self.request.query_params.get('id', None)
        user = User.objects.get(id=user)
        user.is_teacher = True
        user.save()
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Teacher Successfully Verified'
        })

class TeacherListView(ListAPIView):
    serializer_class = BasicUserSerializer
    # filter_backends = [filters.SearchFilter,DjangoFilterBackend]
    # search_fields = ['is_teacher',]
    # filterset_fields = ['is_teacher',]

    def get_queryset(self):
        return User.objects.filter(is_teacher=True)


class TeacherCourseView(viewsets.ModelViewSet):
    serializer_class = CourseContentSerializer
    queryset = Course.objects.all()
    http_method_names = ['get', ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner__in=[self.request.user])

class SubscriberView(APIView):
    '''
    Post Data format:
    {
    "conf_code": "123",
    "email": "khatri799prakash@gmail.com"
    }
    '''
    serializer_class = SubscriberSerializer

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data.update({'conf_code':random_digits()})
        serializer = SubscriberSerializer(data=data)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class UnsubscribeView(APIView):
    """
    api for unsubscribing user
    :param
    email
    code
    http://127.0.0.1:8000/api/accounts/unsubscribe/?email=testing100quantum@gmail.com&conf_code=431263080105
    """
    def get(self,request,*args,**kwargs):
        email = self.request.query_params.get('email')
        print('email',email)
        conf_code = self.request.query_params.get('conf_code')
        try:
            sub = Subscriber.objects.get(email=email)
            if sub.conf_code == conf_code:
                sub.delete()
                return Response({
                    'status': True,
                    'detail': 'Unsubscribed Successfully',
                })
            return Response({
                'status': False,
                'detail': 'Email and Code not matched.',
            })
        except Subscriber.DoesNotExist:
            return Response({
                'status':False,
                'detail':'Email does not exist.',
            })


class NewsletterViewset(viewsets.ModelViewSet):
    '''
    Search through Subject
    http://127.0.0.1:8000/api/accounts/newsletter/?search=this is subject-1
    '''
    permission_classes = (IsAdminUser,)
    serializer_class = NewsletterSerializer
    queryset = Newsletter.objects.all()
    filter_backends = [SearchFilter, ]
    search_fields = ['subject']

    def create(self, request):
        serializer = NewsletterSerializer(data=request.data)
        if serializer.is_valid():
            ns=serializer.save()
            return Response({'message': 'Successfully Added New Campaign', 'data': serializer.data}, status=201)
        else:
            return Response(serializer.errors, status=400)

    def update(self, request, *args, **kwargs):
        ns = self.get_object()
        serializer = NewsletterSerializer(ns, data=request.data)
        if serializer.is_valid():
            ns=serializer.save()
            return Response({'message': 'Successfully Edited Campaign', 'data': serializer.data}, status=201)
        else:
            return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            return Response({'message': 'No Such Campaign'}, status=404)

        return Response({'message': f'{instance.subject} Deleted Successfully'}, status=200)


class SendSubsriptionMailAPI(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request, id):
        subscribers = Subscriber.objects.all()
        if not subscribers.exists():
            return Response({'message': 'Failed there are no subscribers'})
        try:
            newsletter = Newsletter.objects.get(id=id)
        except Newsletter.DoesNotExist:
            return Response({'message': 'Invalid newsletter'})
        subscribers = SubscriberSerializer(subscribers, many=True).data
        newsletter = NewsletterSerializer(newsletter).data

        send_subscription_email(subscribers, newsletter)
        return Response({'message': 'Mail is being sent'})
