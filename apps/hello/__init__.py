from django.dispatch.dispatcher import receiver
from south.signals import post_migrate
from django.contrib.auth.models import User


@receiver(post_migrate)
def my_callback(sender, **kwargs):
    try:
        User.objects.get_by_natural_key('admin')
    except User.DoesNotExist:
        User.objects.create_superuser('admin', '', 'admin')
        print('Created superuser "admin" with password "admin"')
