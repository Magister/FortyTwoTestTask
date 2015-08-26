from django.core.urlresolvers import reverse
from django.template import defaultfilters
from django.test import TestCase, Client

# Create your tests here.
from django.utils.html import escape
from apps.hello.models import AppUser


class TestAppUser(TestCase):
    def test_model_has_data(self):
        """Tests that model for storing user data exists and
        and has initial data loaded from fixture"""
        self.assertEqual(AppUser.objects.count(), 1)


class TestMainView(TestCase):
    c = Client()

    def test_page_has_data(self):
        """Tests that main page has data from db"""
        users = AppUser.objects.all()
        response = self.c.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        for user in users:
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
