from rest_framework import serializers
from account.models import User
from course.models import Course
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _

class EditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk','first_name','last_name','profile_image','email','gender','mobile')

# class ChangePasswordSerializer(serializers.Serializer):
#     """
#     Serializer for password change endpoint.
#     """
#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)

#     def validate_new_password(self, value):
#         validate_password(value)
#         return value

class AnotherChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password1 = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password2 = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                _('Your old password was entered incorrectly. Please enter it again.')
            )
        return value

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({'new_password2': _("The two password fields didn't match.")})
        password_validation.validate_password(data['new_password1'], self.context['request'].user)
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password1']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user

class TeacherSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(required=False, allow_null=True)
    no_of_enroll = serializers.CharField(required=False, allow_null=True)
    class Meta:
        model = Course
        fields = ['id','title','teacher_name','no_of_enroll']
