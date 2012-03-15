from mongoengine import connect, Document
from mongoengine import ReferenceField, StringField, DateTimeField
from mongoengine.django.auth import User
from datetime import datetime
from kolabria.account.models import Account

class Wall(Document):
    """
    Wall model in MongoDB to represent Wall objects
    """
    STATUS_CHOICES = (
        (u'Active', u'Active'),
        (u'Private', u'Private'),
        (u'Inactive', u'Inactive'),
    )        
    company = ReferenceField(Account, 
                             default=Account.objects.get(company='Kolabria'))
    owner = ReferenceField(User)
    name = StringField(max_length=32, required=True)
    description = StringField(max_length=256, required=False)
    status = StringField(default='Active', 
                         max_length=8, 
                         choices=STATUS_CHOICES,
                         required=True)
    created = DateTimeField(default=datetime.now(), required=True)
    modified = DateTimeField(default=datetime.now(), required=True)

    def __unicode__(self):
        """
        Returns the Wall Name as unicode description for admin and shell
        """
        return self.name
