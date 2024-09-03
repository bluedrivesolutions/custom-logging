# backends.py

import logging

from django.contrib.auth.backends import ModelBackend
from ipware import get_client_ip

logger = logging.getLogger(__name__)


class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(
            request, username=username, password=password, **kwargs
        )

        if request is not None:
            ip, _ = get_client_ip(request)

            if user is not None:
                logger.info(
                    f"User {user.username} with IP {ip} has successfully "
                    f"authenticated"
                )
            else:
                logger.warning(
                    f"User {username} with IP {ip} has failed to " f"authenticate"
                )
        return user
