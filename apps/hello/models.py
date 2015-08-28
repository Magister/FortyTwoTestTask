from django.db import models

# Primary key of AppUser loaded from fixture


class AppUser(models.Model):
    INITIAL_APP_USER_PK = 1
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    bio = models.TextField()
    email = models.EmailField()
    jabber = models.EmailField()
    skype = models.CharField(max_length=255)
    other_contacts = models.TextField()


class RequestLog(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    # well-known methods defined at
    # http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html
    # have max. length = 7
    method = models.CharField(max_length=7)
    # set some reasonable field length
    # http://stackoverflow.com/questions/417142/what-is-the-maximum-length-of-a-url-in-different-browsers
    path = models.CharField(max_length=2048)
