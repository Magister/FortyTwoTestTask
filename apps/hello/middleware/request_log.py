from django.core.urlresolvers import reverse
from apps.hello.models import RequestLog


class RequestLogMiddleware(object):

    ignore_path = [reverse('requestlog'), ]

    def process_request(self, request):
        if not (request.path in self.ignore_path and request.is_ajax()):
            req_log = RequestLog()
            req_log.method = request.META['REQUEST_METHOD']
            req_log.path = request.path
            req_log.save()
        return None
