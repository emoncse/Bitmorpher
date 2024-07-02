import datetime
from django.utils.deprecation import MiddlewareMixin
from log_space.models import APILog


class LogRequestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            log = APILog(username=request.user.username, date_time=datetime.datetime.now())
            log.save()

