import base64
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from functools import wraps


def basic_auth_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if settings.DEBUG:
            return view(request, *args, **kwargs)
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Basic '):
            try:
                decoded = base64.b64decode(auth_header[6:]).decode('utf-8')
                username, password = decoded.split(':', 1)
                if username == settings.SUBMISSIONS_USER and password == settings.SUBMISSIONS_PASSWORD:
                    return view(request, *args, **kwargs)
            except Exception:
                pass
        response = HttpResponse(render_to_string('401.html'), status=401)
        response['WWW-Authenticate'] = 'Basic realm="Submissions"'
        return response
    return wrapper
