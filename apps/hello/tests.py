import json
from django.core.urlresolvers import reverse
from django.template import defaultfilters
from django.test import TestCase, Client

# Create your tests here.
from django.utils.html import escape
import time
from apps.hello.models import AppUser, RequestLog
from apps.hello.views import REQUESTLOG_NUM_REQUESTS


class TestAppUser(TestCase):
    def test_model_has_one_user(self):
        """Tests that model for storing user data exists and
        and has initial data loaded from fixture
        There should be exactly one user with pk=INITIAL_APP_USER_PK"""
        self.assertEqual(AppUser.objects.count(), 1)
        self.assertEqual(
            AppUser.objects.first().pk,
            AppUser.INITIAL_APP_USER_PK)


class TestMainView(TestCase):
    c = Client()

    def test_page_has_data(self):
        """Tests that main page has data from db"""
        user = AppUser.objects.get(pk=AppUser.INITIAL_APP_USER_PK)
        response = self.c.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, escape(user.first_name))
        self.assertContains(response, escape(user.last_name))
        self.assertContains(
            response,
            defaultfilters.linebreaksbr(escape(user.bio)))
        self.assertContains(
            response,
            defaultfilters.date(user.date_of_birth))
        self.assertContains(response, escape(user.email))
        self.assertContains(response, escape(user.skype))
        self.assertContains(response, escape(user.jabber))
        self.assertContains(
            response,
            defaultfilters.linebreaksbr(escape(user.other_contacts)))

    def test_using_correct_template(self):
        """Tests that we used a correct template"""
        response = self.c.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hello/main.html')

    def test_context_has_data(self):
        """Tests that context has all needed data"""
        response = self.c.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['appuser'])
        self.assertEqual(
            response.context['appuser'].pk,
            AppUser.INITIAL_APP_USER_PK)


class TestRequestLog(TestCase):
    c = Client()

    def test_requests_storing(self):
        """Tests that requests are stored in db"""
        # there should be no requests at the beginning
        self.assertEqual(RequestLog.objects.count(), 0)
        # make a request and check it's stored
        self.c.get(reverse('index'))
        self.assertEqual(RequestLog.objects.count(), 1)
        stored_request = RequestLog.objects.last()
        self.assertEqual(stored_request.method, 'GET')
        self.assertEqual(stored_request.path, '/')
        # make POST request
        self.c.post('/blah')
        self.assertEqual(RequestLog.objects.count(), 2)
        stored_request = RequestLog.objects.last()
        self.assertEqual(stored_request.method, 'POST')
        self.assertEqual(stored_request.path, '/blah')

    def test_page_has_data(self):
        """Tests that requestlog page has all data"""
        # make some requests to fill db
        self.c.get(reverse('index'))
        self.c.get('/blah')
        self.c.put('/some_put/here')
        self.c.post('/and_some_post')
        self.c.get('/some/get?with&params')
        response = self.c.get(reverse('requestlog'))
        self.assertEqual(response.status_code, 200)
        requests = RequestLog.objects.all()
        for request in requests:
            self.assertContains(response, escape(request.path))
            self.assertContains(
                response,
                defaultfilters.date(request.date, "Y-m-d H:i:s"))
            self.assertContains(response, escape(request.method))

    def test_using_correct_template(self):
        """Tests that we used a correct template"""
        response = self.c.get(reverse('requestlog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hello/requestlog.html')

    def test_context_has_data(self):
        """Tests that request log is rendered correctly"""
        response = self.c.get(reverse('requestlog'))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['requests'])
        self.assertEqual(
            len(response.context['requests']),
            min(RequestLog.objects.count(), REQUESTLOG_NUM_REQUESTS))
        self.assertIsNotNone(response.context['last_update'])
        self.assertEqual(response.context['requests_count'],
                         REQUESTLOG_NUM_REQUESTS)

    def test_context_has_correct_requests(self):
        """Tests that context has last 10 requests"""
        # first make a lot of requests
        for i in xrange(1, REQUESTLOG_NUM_REQUESTS * 2):
            self.c.get('/request/' + str(i))
        # now check context has correct number of requests
        response = self.c.get(reverse('requestlog'))
        requests = \
            RequestLog.objects.order_by('-date')[:REQUESTLOG_NUM_REQUESTS]
        self.assertEqual(len(response.context['requests']),
                         REQUESTLOG_NUM_REQUESTS)
        for request in requests:
            self.assertIn(request, requests)

    def test_async_requests_not_stored(self):
        """Tests that async update requests are not stored
        in the database"""
        self.c.get(reverse('requestlog'),
                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(RequestLog.objects.count(), 0)

    def test_async_update_interface(self):
        """Tests that backend can respond with JSON when requested"""
        # first make a request to have some data
        self.c.get('/blah')
        # now make ajax call
        response = self.c.get(reverse('requestlog'),
                              HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['requests']), 1)
        self.assertIsNotNone(data['last_update'])
        self.assertEqual(data['requests_count'], REQUESTLOG_NUM_REQUESTS)

    def test_async_update_filtering(self):
        """Tests that we can filter async requests by date"""
        # make two requests with some delay
        self.c.get(reverse('index'))
        time.sleep(0.5)
        self.c.get(reverse('requestlog'))
        # ensure we have two items if filter is not requested
        response = self.c.get(reverse('requestlog'),
                              HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data = json.loads(response.content)
        self.assertEqual(len(data['requests']), 2)
        # now use filter to get only second request
        from_date = RequestLog.objects.first().date.isoformat()
        response = self.c.get(reverse('requestlog'),
                              {"from": from_date},
                              HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data = json.loads(response.content)
        self.assertEqual(len(data['requests']), 1)
        self.assertEqual(data['requests'][0]['path'], reverse('requestlog'))
        second_request_date = RequestLog.objects.order_by("-date").\
            first().date.strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(data['requests'][0]['date'], second_request_date)
