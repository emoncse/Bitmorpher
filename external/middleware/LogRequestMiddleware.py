import datetime
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from user_panel.models import CustomUser
from log_space.models import APILog


class LogRequestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            log = APILog(username=request.user.username, date_time=datetime.datetime.now())
            log.save()


class CheckUserTypeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/admin/') or request.path.startswith('/v1/'):
            return None

        if request.method == 'GET' and request.path == '/API/users/':
            return None

        auth_token = request.data.get('authentication_token') if request.method == 'POST' else request.GET.get(
            'authentication_token')

        if auth_token:
            try:
                user = CustomUser.objects.get(authentication_token=auth_token)
                request.user = user
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'Invalid token'}, status=401)
        else:
            request.user = None
            return JsonResponse({'error': 'Authentication token required'}, status=401)

        if request.user.is_superuser:
            return None
