from apps.hello.models import RequestLog


class RequestLogMiddleware(object):

    def process_request(self, request):
        req_log = RequestLog()
        req_log.method = request.META['REQUEST_METHOD']
        req_log.path = request.path
        req_log.save()
        return None
