from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from hashlib import md5

def set_link():
    """
    Unique link from float derived from datetime hash.
    """
    raw_string = datetime.now().isoformat()
    link = md5(raw_string).hexdigest()
    return link


class Link(models.Model):
    """ 
    Used to mimic many-to-many relationship linking users and walls as two 
    one-to-many relationships.
    """
    link = models.CharField(default=set_link, max_length=32)

    def __unicode__(self):
        return self.link


class Wall(models.Model):
    """
    Wall model to represent each unique wall in Kolabria.
    """
    STATUS_CHOICES = (
        (u'Active', u'Active'),
        (u'Private', u'Private'),
        (u'Inactive', u'Inactive'),
    )        
    name = models.CharField(max_length=30)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    owner = models.ForeignKey(User)
#    link = models.ForeignKey(Link)
    
#    created_on = models.DateTimeField(blank=True, null=True) # timestamp of wall creation 
#    last_modified = models.DateTimeField(blank=True, null=True) # last change made by any user
#    last_viewed = models.DateTimeField(blank=True, null=True) # last time this user opened this wall

    def __unicode__(self):
        """
        Returns the Wall Name as unicode description for admin and shell
        """
        return self.name
