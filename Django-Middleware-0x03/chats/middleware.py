import logging
from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logging.basicConfig(
            filename="request.logs",
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
