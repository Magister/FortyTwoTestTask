import logging
from django.shortcuts import render
from apps.hello.models import AppUser

# Instantiate logger
logger = logging.getLogger('hello.view')


def index(request):
    app_user = AppUser.objects.get(pk=1)
    context = {'appuser': app_user}
    logger.debug('index: appuser %d' % (app_user.pk,))
    return render(request, 'hello/main.html', context)
