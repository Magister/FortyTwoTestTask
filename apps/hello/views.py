from django.shortcuts import render

# Create your views here.
from apps.hello.models import AppUser


def index(request):
    app_user = AppUser.objects.get(pk=1)
    context = {'appuser': app_user}
    return render(request, 'hello/main.html', context)
