import json
import logging
from django.http.response import HttpResponse
from django.shortcuts import render
from django.utils.dateparse import parse_datetime
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
    date_from = None
    if request.is_ajax():
        date_str = request.GET.get('from')
        if date_str is not None:
            try:
                date_from = parse_datetime(date_str)
            except ValueError:
                pass
    if date_from is None:
        requests = RequestLog.objects.order_by(
            '-date')[:REQUESTLOG_NUM_REQUESTS]
    else:
        requests = RequestLog.objects.order_by('-date').filter(
            date__gt=date_from)[:REQUESTLOG_NUM_REQUESTS]
    context = {'requests': requests}
    logger.debug('requestlog')
    if request.is_ajax():
        json_data = {"requests": []}
        for req in requests:
            json_data['requests'] += [{
                "date": req.date.strftime('%Y-%m-%d %H:%M:%S'),
                "method": req.method,
                "path": req.path
            }]
        return HttpResponse(
            json.dumps(json_data),
            content_type="application/json")
    else:
        return render(request, 'hello/requestlog.html', context)
