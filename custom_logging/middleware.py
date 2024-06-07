from threading import local

from django.utils.deprecation import MiddlewareMixin

try:
    from rest_framework.authentication import (
        BasicAuthentication,
        SessionAuthentication,
        TokenAuthentication,
    )
except ImportError:
    raise ImportError("Django Rest Framework is required to use this module")

_thread_locals = local()


def get_current_user():
    return getattr(_thread_locals, "user", None)


class CustomLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        _thread_locals.user = None

        if request.user.is_authenticated:
            _thread_locals.user = request.user
        else:
            user = None
            for auth_class in [
                BasicAuthentication,
                SessionAuthentication,
                TokenAuthentication,
            ]:
                auth_instance = auth_class()
                try:
                    user_auth_tuple = auth_instance.authenticate(request)
                    if user_auth_tuple is not None:
                        user, _ = user_auth_tuple
                        break
                except Exception:
                    pass

            _thread_locals.user = user

    def process_response(self, request, response):
        return response
