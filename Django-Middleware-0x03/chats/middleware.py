import logging
from datetime import datetime
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logging.basicConfig(
            filename="chats/requests.log",
            level=logging.INFO,
        )

    def __call__(self, request):
        if request.user.is_authenticated:
            user = request.user.username
        else:
            user = "Anonymous"

        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)

        response = self.get_response(request)

        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        current_time = datetime.now().hour

        if "messages" in request.path and current_time < 18 or current_time >= 21:
            return HttpResponseForbidden("Can't access this site now")

        response = self.get_response(request)
        return response
