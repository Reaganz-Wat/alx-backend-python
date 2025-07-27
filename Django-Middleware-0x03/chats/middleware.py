# chats/middleware.py
import logging
from datetime import datetime
from django.http import HttpResponseForbidden
import time
from collections import defaultdict, deque
from django.http import JsonResponse


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Configure a file logger
        self.logger = logging.getLogger("request_logger")
        handler = logging.FileHandler("requests.log")
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(handler)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Restrict if current hour is NOT between 18 (6PM) and 21 (9PM)
        if not (18 <= current_hour < 21):
            return HttpResponseForbidden("Chat access is restricted at this time.")

        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Store timestamps of requests per IP
        self.ip_requests = defaultdict(lambda: deque())

        # Settings
        self.TIME_WINDOW = 60        # seconds
        self.MAX_REQUESTS = 5        # per time window

    def __call__(self, request):
        if request.method == "POST" and "/messages" in request.path:
            ip = self.get_client_ip(request)
            now = time.time()

            # Clean up old timestamps
            timestamps = self.ip_requests[ip]
            while timestamps and now - timestamps[0] > self.TIME_WINDOW:
                timestamps.popleft()

            # Check rate limit
            if len(timestamps) >= self.MAX_REQUESTS:
                return JsonResponse(
                    {"error": "Rate limit exceeded. Max 5 messages per minute."},
                    status=429
                )

            # Record this request
            timestamps.append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        # Use X-Forwarded-For if behind a proxy
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "")