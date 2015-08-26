from django.shortcuts import render

# Create your views here.
from apps.hello.models import AppUser


def index(request):
    app_users = AppUser.objects.all()
    context = {'appusers': app_users}
    return render(request, 'hello/main.html', context)
