from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

from user_panel.models import CustomUser


class UserTypeCheckMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated and request.path == '/API/':
            return JsonResponse({'message': 'User is not authenticated.'}, status=401)
        try:
            user = CustomUser.objects.get(username=request.user)
            if not user.is_authenticated:
                return

            if user.user_type == 'customer':
                if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
                    return JsonResponse({'message': 'Customer user is not allowed for this operation.'}, status=403)
            print(user.user_type)
        except CustomUser.DoesNotExist:
            pass


