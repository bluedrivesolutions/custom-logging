try:
    from ipware import get_client_ip
except ImportError:
    raise ImportError(
        "Django-IPware is required to use this module "
        "Run 'pip install django-ipware' to install it"
    )


def get_ip_from_request(request):
    client_ip, _ = get_client_ip(request)
    return client_ip


def convert_string_to_numeric(value):
    try:
        return float(value)
    except Exception:
        return value
