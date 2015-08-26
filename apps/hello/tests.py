from django.test import TestCase

# Create your tests here.
from apps.hello.models import AppUser


class TestModel(TestCase):
    def test_model_has_data(self):
        "Tests that model for storing user data exists"
        assert(AppUser.objects.count() == 1)
