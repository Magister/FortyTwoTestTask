import json
import logging
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect
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


REQUESTLOG_SORT_FIELDS = {
    'date': 'Priority',
    'method': 'Method',
    'path': 'Path'
}
REQUESTLOG_DEFAULT_SORT = 'date'
REQUESTLOG_SORT_DIRECTIONS = {
    '': 'Ascending',
    '-': 'Descending'
}
REQUESTLOG_DEFAULT_DIRECTION = '-'


def requestlog(request):
    id_from = None
    order = request.GET.get('order')
    direction = request.GET.get('direction')
    if order not in REQUESTLOG_SORT_FIELDS.keys():
        order = REQUESTLOG_DEFAULT_SORT
    if direction not in REQUESTLOG_SORT_DIRECTIONS.keys():
        direction = REQUESTLOG_DEFAULT_DIRECTION
    if request.is_ajax():
        id_str = request.GET.get('idfrom')
        if id_str is not None:
            try:
                id_from = int(id_str)
            except ValueError:
                pass
    query = RequestLog.objects.order_by(direction + order, '-date')
    if id_from is not None and order == 'date' and direction == '-':
        # special case - id grows with date, so we can filter by id here
        query = query.filter(id__gt=id_from)
    query = query[:REQUESTLOG_NUM_REQUESTS]
    last_id = 0
    requests = []
    for req in query:
        last_id = max(last_id, req.id)
    if id_from is None or last_id > id_from:
        # first page load or something changed
        requests = query
    context = {
        'requests': requests,
        'last_update': timezone.now(),
        'requests_count': REQUESTLOG_NUM_REQUESTS,
        'direction': direction,
        'order': order,
        'available_order': REQUESTLOG_SORT_FIELDS,
        'available_direction': REQUESTLOG_SORT_DIRECTIONS,
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
            }]
        return HttpResponse(
            json.dumps(json_data),
            content_type="application/json")
    else:
        return render(request, 'hello/requestlog.html', context)


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
