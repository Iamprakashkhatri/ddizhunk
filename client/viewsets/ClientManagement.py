from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from rest_framework import permissions, status
from rest_framework import viewsets,mixins
from rest_framework.filters import SearchFilter
from client.permissions import IsAdminUserOrReadOnly
from client.serializers import EditUserSerializer,AnotherChangePasswordSerializer,TeacherSerializer
from account.models import User
from account.serializers import UserSerializers
from course.models import Course
from course.serializers import CourseSerializer
from payments.models import *
from payments.serializers import PaymentSerializer
# from accounting.serializers import AccountTeacherSerializer
from django.db.models import Count, Avg,Sum,Exists,Q,F


class UserProfile(APIView):
    """
    POST Format:
    {
        "first_name":"",
        "last_name":"",
        "email":email@gmail.com,
        "gender":"male",
        "mobile":987763522
    }
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = EditUserSerializer

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        user = UserSerializers(user)
        return Response(user.data, status=200)

    def post(self, request, format=None):
        try:
            user = User.objects.get(id=request.user.id)
            serializer = EditUserSerializer(data=request.data, instance=user)
        except ObjectDoesNotExist:
            return Response({'message': 'User does not exists'})
        if serializer.is_valid():
            user = serializer.save()
            user.save()
            return Response({'message':'Successfully Edited','data':UserSerializers(user).data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileCourse(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CourseSerializer

    def get(self, request):
        course = Course.objects.filter(owner__id=request.user.id)
        course = CourseSerializer(course, many=True, context={'request': request}).data
        return Response(course, status=200)


# class UpdatePassword(APIView):
#     """
#     An endpoint for changing password.
#     """
#     permission_classes = (IsAuthenticated, )

#     def get_object(self, queryset=None):
#         return self.request.user

#     def put(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         serializer = ChangePasswordSerializer(data=request.data)

#         if serializer.is_valid():
#             # Check old password
#             old_password = serializer.data.get("old_password")
#             if not self.object.check_password(old_password):
#                 return Response({"old_password": ["Wrong password."]}, 
#                                 status=status.HTTP_400_BAD_REQUEST)
#             # set_password also hashes the password that the user will get
#             self.object.set_password(serializer.data.get("new_password"))
#             self.object.save()
#             return Response({'message':'Password Successfully Updated'},status=status.HTTP_204_NO_CONTENT)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.generics import UpdateAPIView
from rest_framework.authtoken.models import Token

class ChangePasswordView(UpdateAPIView):
    '''
    {
        "old_password":"1234",
        "new_password1":"django@799",
        "new_password2":"django@799"
    }
    '''
    serializer_class = AnotherChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # if using drf authtoken, create a new token 
        # if hasattr(user, 'auth_token'):
        #     user.auth_token.delete()
        # token, created = Token.objects.get_or_create(user=user)
        # return new token
        return Response({'message':'Password Successfully Updated'}, status=status.HTTP_200_OK)


# class TeachersAPI(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
#     permission_classes = (IsAdminUser,)
#     queryset = Course.objects.all()
#     serializer_class = TeacherSerializer
#     filter_backends = [SearchFilter, ]
#     search_fields = ['first_name']

#     def get_queryset(self):
#         return Course.objects.filter(owner__is_teacher=True).annotate(
#             teacher_name=F('owner__first_name'),
#             no_of_enroll=Count('students__id', distinct=True)
#             )

class TeacherAPI(APIView):
    """
    POST Format:
    {
    "date_start":"2020-10-12",
    "end_date":"2021-12-21"
}
    """ 
    permission_classes = (IsAdminUser,)
    def get(self, request):
        course = Course.objects.filter(owner__is_teacher=True).annotate(teacher_name=F('owner__first_name'),
            no_of_enroll=Count('students__id', distinct=True)
            )
        data = TeacherSerializer(course, many=True, context={'request': request}).data
        return Response(data, status=200)

    def post(self, request, format=None):
        try:
            date_start=request.data['date_start']
            date_end=request.data['end_date']
            user = Course.objects.filter(students__date_joined__date__range=[date_start,date_end]).count()
            print('user',user)
            context=[
            {"user":user}
            ]
        except ObjectDoesNotExist:
            return Response({'message': 'User does not exists'})
        return Response({'context': context}, status=200)


class ClientMyChoiceAPI(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self,*args, **kwargs):
        qs = super(ClientMyChoiceAPI, self).get_queryset(*args, **kwargs)
        data=self.request.user
        qs = qs.filter(Q(done_by=data) & Q(status='Completed'))
        return qs
        
    

