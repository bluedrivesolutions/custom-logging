import logging

try:
    from django.contrib.auth.signals import (
        user_logged_in,
        user_logged_out,
        user_login_failed,
    )
    from django.dispatch import receiver
except ImportError:
    raise ImportError("Django is required to use this module")

from .utils import get_ip_from_request

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = get_ip_from_request(request)
    if user:
        logger.info(
            f"User {user.username} with IP {ip} has successfully "
            f"authenticated from Django Admin"
        )


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    ip = get_ip_from_request(request)
    if user:
        logger.info(
            f"User {user.username} with IP {ip} has successfully "
            f"logged out from Django Admin"
        )


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    ip = get_ip_from_request(request)
    logger.warning(
        f"User {credentials['username']} with IP {ip} has failed to "
        f"authenticate from Django Admin"
    )
