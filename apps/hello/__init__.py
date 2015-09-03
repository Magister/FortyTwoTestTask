from django.core.management import call_command
from django.dispatch.dispatcher import receiver
from south.signals import post_migrate
from django.contrib.auth.models import User
from apps.hello.models import AppUser
import signals  # nopep8 - it's actually used to trigger signals registration


@receiver(post_migrate)
def my_callback(sender, **kwargs):
    try:
        AppUser.objects.get(pk=AppUser.INITIAL_APP_USER_PK)
    except AppUser.DoesNotExist:
        call_command('loaddata', 'app_user.json')
    try:
        User.objects.get_by_natural_key('admin')
    except User.DoesNotExist:
        User.objects.create_superuser('admin', '', 'admin')
        print('Created superuser "admin" with password "admin"')
