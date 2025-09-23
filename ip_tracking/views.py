from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit  

@ratelimit(key="ip", rate="10/m", method="GET", block=True)
@ratelimit(key="ip", rate="5/m", method="POST", block=True)
def login_view(request):
    if request.method == "POST":
        return JsonResponse({"message": "Login attempt recorded"})
    return JsonResponse({"message": "Please POST to login"})
