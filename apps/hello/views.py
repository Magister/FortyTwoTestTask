import logging
from django.shortcuts import render
from apps.hello.models import AppUser, RequestLog

# Instantiate logger
logger = logging.getLogger('hello.view')

# number of requests to show on requests log page
REQUESTLOG_NUM_REQUESTS = 10


def index(request):
    app_user = AppUser.objects.get(pk=AppUser.INITIAL_APP_USER_PK)
    context = {'appuser': app_user}
    logger.debug('index: appuser %d' % (app_user.pk,))
    return render(request, 'hello/main.html', context)


def requestlog(request):
    return None
