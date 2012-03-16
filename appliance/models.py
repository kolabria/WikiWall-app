from mongoengine import connect, Document
from mongoengine import ReferenceField, StringField, DateTimeField
from mongoengine.django.auth import User
from datetime import datetime
from kolabria.account.models import Account
from kolabria.walls.models import Wall

class Box(Document):
    """
    Box represents a unique WikiWall appliance
    """
    STATUS_CHOICES = (
        (u'Active', u'Active'),
        (u'New', u'Not Registered'),
        (u'Offline', u'Offline'),
        (u'Disabled', u'Disabled'),
    )

    company = ReferenceField(Account)
    owner = ReferenceField(User)
    name = StringField(default='New Appliance', max_length=32, required=True)
    location = StringField(max_length=100, required=False)
    status = StringField(default='Active',
                         max_length=16,
                         choices=STATUS_CHOICES,
                         required=True)
    walls = ListField(Wall(unique=True))
    activated = DateTimeField(default=datetime.now(), required=True)
    modified = DateTimeField(default=datetime.now(), required=True)

    def __unicode__(self):
        return self.name
