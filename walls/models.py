from django.db import models
from django.contrib.auth.models import User

class Wall(models.Model):
    STATUS_CHOICES = (
        (u'Active', u'Active'),
        (u'Private', u'Private'),
        (u'Inactive', u'Inactive'),
    )        
    name = models.CharField(max_length=30)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    owner = models.ForeignKey(User)
    created_on = models.DateField(blank=True,default=True,auto_now_add=True) # the date this wall was first created
#    last_viewed = models.DateField() # last time this user opened this wall
    last_modified = models.DateField(blank=True,default=True,auto_now=True) # last time a change was made by any user
