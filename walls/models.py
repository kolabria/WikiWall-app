from django.db import models
from django.contrib.auth.models import User
#from datetime import datetime

class Wall(models.Model):
    STATUS_CHOICES = (
        (u'Active', u'Active'),
        (u'Private', u'Private'),
        (u'Inactive', u'Inactive'),
    )        
    name = models.CharField(max_length=30)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    owner = models.ForeignKey(User)
#    created_on = models.DateField(default=datetime.now) # the date this wall was first created
#    last_modified = models.DateField(default=datetime.now) # last time a change was made by any user
#    last_viewed = models.DateField() # last time this user opened this wall
#
    def __unicode__(self):
        """
        Returns the Wall Name as unicode description for admin and shell
        """
        return self.name
