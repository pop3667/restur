from django.urls import reverse
from django.shortcuts import redirect
from django.http import JsonResponse
class  CheckUserAuthenticated:
    def __init__(self,get_response):
        self.get_response = get_response
    def __call__(self, request):
        if request.path.startswith("/home/") or request.path == "/" or request.path.startswith(reverse("accounts:login")) or request.path.startswith(reverse("accounts:signup")) or  request.user.is_authenticated:
            return self.get_response(request)
        if request.headers.get("Content-Type") == "application/json" :
            return JsonResponse({
                "url":reverse("accounts:login")
            })
        else:
            return redirect(reverse("accounts:login"))
    
