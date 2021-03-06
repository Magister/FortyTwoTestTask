import json
import logging
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect, \
    HttpResponseBadRequest
from django.shortcuts import render
from django.utils import timezone
from apps.hello import tools
from apps.hello.forms import EditForm
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
    id_from = None
    if request.is_ajax():
        id_str = request.GET.get('idfrom')
        if id_str is not None:
            try:
                id_from = int(id_str)
            except ValueError:
                pass
    requests = RequestLog.objects.order_by('-priority', '-date')
    if id_from is not None:
        requests = requests.filter(id__gt=id_from)
    requests = requests[:REQUESTLOG_NUM_REQUESTS]
    last_id = 0
    for req in requests:
        last_id = max(last_id, req.id)
    context = {
        'requests': requests,
        'last_update': timezone.now(),
        'requests_count': REQUESTLOG_NUM_REQUESTS,
        'last_id': last_id
    }
    logger.debug('requestlog')
    if request.is_ajax():
        json_data = {
            'last_update': context['last_update'].isoformat(),
            'requests': [],
            'requests_count': context['requests_count']
        }
        for req in context['requests']:
            json_data['requests'] += [{
                'id': req.id,
                'date': req.date.strftime('%Y-%m-%d %H:%M:%S'),
                'method': req.method,
                'path': req.path,
                'priority': req.priority,
            }]
        return HttpResponse(
            json.dumps(json_data),
            content_type="application/json")
    else:
        return render(request, 'hello/requestlog.html', context)


def edit_request(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()
    try:
        req_id = int(request.POST.get('id'))
        priority = int(request.POST.get('priority'))
    except ValueError:
        return HttpResponseBadRequest()
    req = RequestLog.objects.get(id=req_id)
    if req.priority != priority:
        req.priority = priority
        req.save()
    return HttpResponseRedirect(reverse('requestlog'))


@login_required
def edit(request):
    appuser = AppUser.objects.get(pk=AppUser.INITIAL_APP_USER_PK)
    if request.method == 'POST':
        if request.is_ajax():
            data = json.loads(request.body)
            if 'photo' in data:
                (content, content_type) = tools.decode_data_uri(data['photo'])
                file_dict = {
                    'content': content,
                    'filename': data.get('photo_filename'),
                    'content-type': content_type
                }
                img_file = SimpleUploadedFile.from_dict(file_dict)
                request.FILES['photo'] = img_file
        else:
            data = request.POST
        form = EditForm(data, request.FILES, instance=appuser)
        if form.is_valid():
            img_data = form.cleaned_data.get('photo')
            if img_data is not None:
                tools.resize_photo(img_data, AppUser.PHOTO_WIDTH,
                                   AppUser.PHOTO_HEIGHT)
            form.save()
            if not request.is_ajax():
                return HttpResponseRedirect(reverse('index'))
        response = tools.convert_to_json(form)
        return HttpResponse(response, content_type='application/json')
    else:
        form = EditForm(instance=appuser)
    return render(request, 'hello/edit.html', {'form': form})
