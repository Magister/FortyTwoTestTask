from django.core.urlresolvers import reverse
from django.template import defaultfilters
from django.test import TestCase, Client

# Create your tests here.
from django.utils.html import escape
from apps.hello.models import AppUser


class TestAppUser(TestCase):
    def test_model_has_one_user(self):
        """Tests that model for storing user data exists and
        and has initial data loaded from fixture
        There should be exactly one user with pk=INITIAL_APP_USER_PK"""
        self.assertEqual(AppUser.objects.count(), 1)
        self.assertEqual(AppUser.objects.first().pk, AppUser.INITIAL_APP_USER_PK)


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
        self.assertEqual(response.context['appuser'].pk, AppUser.INITIAL_APP_USER_PK)
