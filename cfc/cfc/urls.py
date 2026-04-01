import logging

from api.views import router
from django.http import JsonResponse
from django.urls import path
from ninja import NinjaAPI
from ninja.errors import HttpError, ValidationError

logger = logging.getLogger("api.views")

api = NinjaAPI(
    title="Company Lookup API",
)

api.add_router("/", router)


@api.exception_handler(ValidationError)
def validation_error_handler(request, exc):
    details = []
    for error in exc.errors:
        field = " -> ".join(str(loc) for loc in error.get("loc", []))
        msg = error.get("msg", "Invalid value")
        details.append({"field": field, "message": msg})
    logger.warning("Invalid input: %s", details)
    return JsonResponse({"detail": details}, status=422)


@api.exception_handler(Exception)
def generic_exception_handler(request, exc):
    logger.exception("Unexpected error processing request")
    return JsonResponse({"detail": "Internal server error"}, status=500)


@api.exception_handler(HttpError)
def http_error_handler(request, exc):
    return JsonResponse({"detail": str(exc)}, status=exc.status_code)


urlpatterns = [
    path("api/", api.urls),
]
