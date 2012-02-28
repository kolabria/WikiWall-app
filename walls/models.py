from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from hashlib import md5

class Wall(models.Model):
    """
    Wall model to represent each unique wall in Kolabria.
    """
    STATUS_CHOICES = (
        (u'Active', u'Active'),
        (u'Private', u'Private'),
        (u'Inactive', u'Inactive'),
    )        
    name = models.CharField(max_length=32)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    owner = models.ForeignKey(User)
    now_hash = md5(datetime.now().isoformat()).hexdigest()
    link = models.CharField(default=now_hash, max_length=32)


    def __unicode__(self):
        """
        Returns the Wall Name as unicode description for admin and shell
        """
        return self.name
