import json
import logging

logger = logging.getLogger("api.middleware")


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.content_type and "application/json" not in request.content_type and request.method == "POST":
            return self._json_response(
                415,
                "Content-Type must be application/json",
            )

        response = self.get_response(request)

        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        response["Cache-Control"] = "no-store"

        return response

    @staticmethod
    def _json_response(status, detail):
        from django.http import JsonResponse

        return JsonResponse({"detail": detail}, status=status)


class ExceptionHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except Exception:
            logger.exception("Unexpected error processing request")
            from django.http import JsonResponse

            return JsonResponse(
                {"detail": "Internal server error"},
                status=500,
            )
