from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from hashlib import md5

class Wall(models.Model):
    STATUS_CHOICES = (
        (u'Active', u'Active'),
        (u'Private', u'Private'),
        (u'Inactive', u'Inactive'),
    )        
    name = models.CharField(max_length=30)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    owner = models.ForeignKey(User)
    link = models.CharField(default='dummylink', max_length=32)
    
#    created_on = models.DateTimeField(blank=True, null=True) # timestamp of wall creation 
#    last_modified = models.DateTimeField(blank=True, null=True) # last change made by any user
#    last_viewed = models.DateTimeField(blank=True, null=True) # last time this user opened this wall

    def __unicode__(self):
        """
        Returns the Wall Name as unicode description for admin and shell
        """
        return self.name

    def set_link(self, **kwargs):
        raw_string = self.owner.email + str(self.id)
        link = md5(raw_string).hexdigest()
        self.link = link


    def save(self, *args, **kwargs):
        if not self.pk:
            self.set_link() # create unique link from hash of email + id
#            now = datetime.now()
#            self.created_on = now
#            self.last_modified = now
#            self.last_viewed = now
        super(Wall, self).save(*args, **kwargs)
