from django.db import models

# Primary key of AppUser loaded from fixture


class AppUser(models.Model):
    INITIAL_APP_USER_PK = 1
    PHOTO_WIDTH = 200
    PHOTO_HEIGHT = 200

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    bio = models.TextField()
    email = models.EmailField()
    jabber = models.EmailField()
    skype = models.CharField(max_length=255)
    other_contacts = models.TextField()
    photo = models.ImageField(upload_to='appuser', blank=True, null=True)


class RequestLog(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    # well-known methods defined at
    # http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html
    # have max. length = 7
    method = models.CharField(max_length=7)
    # set some reasonable field length
    # http://stackoverflow.com/questions/417142/what-is-the-maximum-length-of-a-url-in-different-browsers
    path = models.CharField(max_length=2048)
    priority = models.IntegerField(default=0)


class ObjectEvents(models.Model):
    CREATE = 'C'
    EDIT = 'E'
    DELETE = 'D'

    EVENT_CHOICES = (
        (CREATE, 'Create'),
        (EDIT, 'Edit'),
        (DELETE, 'Delete')
    )

    date = models.DateTimeField(auto_now_add=True)
    event = models.CharField(max_length=1, choices=EVENT_CHOICES, null=True)
    object_model = models.CharField(max_length=255)
    object_repr = models.CharField(max_length=255)

    def __unicode__(self):
        return u'{0}: event={1} model={2} - {4}'.\
            format(self.date.isoformat(),
                   self.get_event_display(),
                   self.object_model,
                   self.object_repr)
