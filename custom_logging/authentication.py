import logging

from django.contrib.auth import authenticate, get_user_model
from ipware import get_client_ip
from rest_framework import authentication, exceptions

logger = logging.getLogger(__name__)


User = get_user_model()


class CustomLoggingAuthentication(authentication.BaseAuthentication):
    """For logging user authentication ip using Django Rest Framework"""

    def authenticate(self, request):
        user = authenticate(request=request)
        ip, _ = get_client_ip(request)

        if user:
            username = getattr(user, User.USERNAME_FIELD)
            logger.info(f"User {username} with IP {ip} has successfully authenticated")
        else:
            logger.warning(f"User {username} with IP {ip} has failed to authenticate")
            raise exceptions.AuthenticationFailed("Authentication failed")

        return user, None
