from django.db import DatabaseError
from django.db.models.signals import post_save, post_delete
from django.dispatch.dispatcher import receiver
from apps.hello.models import ObjectEvents


@receiver(post_save, dispatch_uid="hello.object_events.post_save")
def post_save_handler(sender, instance, created, raw,
                      using, update_fields, **kwargs):
    # skip event log add events
    if (instance._meta.model_name == ObjectEvents._meta.model_name) \
            and created:
        return
    event = ObjectEvents()
    event.event = ObjectEvents.CREATE if created else ObjectEvents.EDIT
    event.object_model = instance._meta.model_name
    event.object_repr = str(instance)
    try:
        event.save()
    except DatabaseError:
        # we are probably in syncdb
        pass


@receiver(post_delete, dispatch_uid="hello.object_events.post_delete")
def post_delete_handler(sender, instance, using, **kwargs):
    event = ObjectEvents()
    event.event = ObjectEvents.DELETE
    event.object_model = instance._meta.model_name
    event.object_repr = str(instance)
    try:
        event.save()
    except DatabaseError:
        # we are probably in syncdb
        pass
