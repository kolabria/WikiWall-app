from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from hashlib import md5
from random import random

def hash_link():
    now_hash = md5(datetime.now().isoformat()).hexdigest()
    noise = str(random())
    hash_link = md5(now_hash + noise).hexdigest()
    return hash_link 

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
    created = models.DateTimeField(null=True, auto_now_add=True)
    modified = models.DateTimeField(null=True, auto_now=True)
    link = models.CharField(null=True, default=hash_link, max_length=32, unique=True)


    def __unicode__(self):
        """
        Returns the Wall Name as unicode description for admin and shell
        """
        return self.name
