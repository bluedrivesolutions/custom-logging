import logging

from django.contrib.auth import get_user_model
from ipware import get_client_ip
from rest_framework import authentication

logger = logging.getLogger(__name__)


User = get_user_model()


class CustomLoggingAuthentication(authentication.BaseAuthentication):
    """For logging user authentication ip using Django Rest Framework"""

    def authenticate(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        ip, _ = get_client_ip(request)

        if not username or not password:
            return None

        try:
            user = User.objects.get(username=username)
            username = getattr(user, User.USERNAME_FIELD)
        except User.DoesNotExist:
            return None

        password_check = user.check_password(password)

        if password_check:
            logger.info(f"User {username} with IP {ip} has successfully authenticated")
        else:
            logger.warning(f"User {username} with IP {ip} has failed to authenticate")

        return None  # Return None to prevent login
