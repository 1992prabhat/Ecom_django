from django.shortcuts import redirect
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/admin/"):
            if request.user.is_authenticated and not request.user.is_staff:
                # Option 1: Redirect to home page
                return redirect("/")
            return self.get_response(request)
        return self.get_response(request)