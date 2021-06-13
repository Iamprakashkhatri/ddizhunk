from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .models import *
from .helpers import *

class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class BasicUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('pk','first_name','last_name','profile_image','email','gender')


class LoginSerializers(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class DizHunkaAuthTokenSerializer(AuthTokenSerializer):
    username = serializers.CharField(
        label=_("Username"),
        write_only=True,
        required=False
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True,
        required=False
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )
    access_token = serializers.CharField(
        label=_("Access Token"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True,
        required=False,
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        access_token = attrs.get('access_token')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        elif access_token:
            user = validate_access_token(access_token)
            if user is None:
                msg = _('Not a valid firebase token')
                raise serializers.ValidationError(msg, code='authorization')
            else:
                user_logged_in.send(sender=user.__class__, request=self.context.get('request'), user=user)
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class DizHunkaPhoneAuthTokenSerializer(AuthTokenSerializer):
    username = serializers.CharField(
        label=_("Username"),
        write_only=True,
        required=False
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True,
        required=False
    )
    access_token = serializers.CharField(
        label=_("Access Token"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True,
        required=False,
    )

    def validate(self, attrs):
        access_token = attrs.get('access_token')

        if access_token:
            user = validate_phone_access_token(access_token)
            if user is None:
                msg = _('Not a valid firebase token')
                raise serializers.ValidationError(msg, code='authorization')
            else:
                user_logged_in.send(sender=user.__class__, request=self.context.get('request'), user=user)
        else:
            msg = _('Not a valid firebase token')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class SubscriberSerializer(serializers.ModelSerializer):
    conf_code = serializers.IntegerField(required=False)

    class Meta:
        model = Subscriber
        fields = '__all__'

class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'

class ReferralUserSerializer(serializers.ModelSerializer):
    referred = BasicUserSerializer()

    class Meta:
        model = Referrals
        fields = '__all__'
        

class BasicOwnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','first_name','last_name')