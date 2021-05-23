import jwt

from django.db.models import Q

from django.contrib.auth import get_user_model
from django.contrib.auth import get_user

from django.conf import settings

from rest_framework import authentication, exceptions

from .models import User

# MyUser = get_user_model()

class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            return None

        elif len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            return None

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):

        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except:
            msg = 'Invalid authentication. Could not decode token.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)

class UsernameOrEmailBackend(object):

    def get_user(self, request):
        my_user_model = get_user_model()
        try:
            return my_user_model.objects.get(pk=request)
        except my_user_model.DoesNotExist:
            return None

    def authenticate(self, request, username=None, password=None, **kwargs):
        my_user = get_user_model()

        try:
            user = my_user.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("Не правильно указан email или пароль")