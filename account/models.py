from mongoengine import connect, Document
from mongoengine import ReferenceField, StringField, DateTimeField
from mongoengine.django.auth import User
from datetime import datetime

class Account(Document):
    """
    Corporate Account model in MongoDB to represent Company objects
    """
    STATUS_CHOICES = (
        (u'Active', u'Active'),
        (u'Inactive', u'Inactive'),
    )

    owner = ReferenceField(User)
    company= StringField(max_length=32)
    address1 = StringField(max_length=256)
    city = StringField(max_length=64) 
    status = StringField(default='Active', 
                         max_length=8, 
                         choices=STATUS_CHOICES,
                         required=True)
    created = DateTimeField(default=datetime.now())
    modified = DateTimeField(default=datetime.now(), required=True)

    def __unicode__(self):
        """
        Returns the Wall Name as unicode description for admin and shell
        """
        return self.company
