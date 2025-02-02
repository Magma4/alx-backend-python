import logging
from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logging.basicConfig(
            filename="chats/requests.logs",
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

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to store messages sent by IP and their timestamps
        self.message_tracker = defaultdict(list)

    def __call__(self, request):
        # Check if the request method is POST and if it's related to sending messages
        if request.method == 'POST' and '/api/conversations/' in request.path and '/messages/' in request.path:
            ip_address = self.get_client_ip(request)
            current_time = time.time()

            # Clean up message tracker by removing timestamps older than 1 minute
            self.message_tracker[ip_address] = [timestamp for timestamp in self.message_tracker[ip_address] if current_time - timestamp < 60]

            # Check if the user has exceeded the limit of 5 messages per minute
            if len(self.message_tracker[ip_address]) >= 5:
                return HttpResponseForbidden("You have exceeded the message limit (5 messages per minute). Please try again later.")

            # Log the current message by adding the timestamp
            self.message_tracker[ip_address].append(current_time)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Helper function to retrieve the client's IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define restricted routes where only admins should have access
        restricted_paths = [
            '/api/admin-action/',
            '/api/manage-users/',
        ]

        # Check if the request path is restricted
        if any(request.path.startswith(path) for path in restricted_paths):
            # Ensure the user is authenticated
            if not request.user.is_authenticated:
                return HttpResponseForbidden("You must be logged in as an admin or moderator to access this resource.")

            # Check the user's role (assuming role is stored in the User model)
            if request.user.role not in ['admin']:
                return HttpResponseForbidden("You do not have permission to access this resource.")

        response = self.get_response(request)
        return response
