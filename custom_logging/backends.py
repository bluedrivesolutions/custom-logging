import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from ipware import get_client_ip

logger = logging.getLogger(__name__)

User = get_user_model()


class CustomLoggingAuthBackend(ModelBackend):
    """For logging user authentication ip using Django's ModelBackend"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(
            request, username=username, password=password, **kwargs
        )

        if request is not None:
            ip, _ = get_client_ip(request)

            if user is not None:
                username = getattr(user, User.USERNAME_FIELD)
                logger.info(
                    f"User {username} with IP {ip} has successfully authenticated"
                )
            else:
                logger.warning(
                    f"User {username} with IP {ip} has failed to authenticate"
                )
        return user
