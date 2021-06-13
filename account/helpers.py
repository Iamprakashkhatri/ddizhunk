from django.conf import settings
import firebase_admin
from firebase_admin import credentials,auth
from firebase_admin.auth import verify_id_token

from rest_framework.authtoken.models import Token

import random

from account.models import User

cred = credentials.Certificate(str(settings.FIREBASE_KEY_PATH))
default_app = firebase_admin.initialize_app(cred)


def validate_access_token(access_token):
    decoded = verify_id_token(access_token)
    uuid = decoded.get('uid')
    email = decoded.get('email')

    if uuid and email:
        user, created = User.objects.get_or_create(email=email)
        if created:
            # need to save other fields too
            user.firebase_uuid = uuid
            user.save()
    else:
        user = None
    return user

def validate_phone_access_token(access_token):
    decoded = verify_id_token(access_token)
    uuid = decoded.get('uid')
    phone = decoded.get('phone')

    # email = "padkhu@gmail.com"
    # phone = "+9779860837166"
    # user1 = auth.get_user_by_phone_number(phone)
    # uuid=user1.uid
    # print('uuid',uuid)

    # user = auth.create_user(email = 'padkhu@gmail.com',password='123456',phone_number='+9779860837166')


    if uuid:
        try:
            user = User.objects.get(mobile=phone)
        except User.DoesNotExist:
            user = User.objects.create(mobile=phone)
        user.firebase_uuid=uuid
        user.save()
    else:
        user = None
    return user


def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)
