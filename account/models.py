from mongoengine import connect, Document
from mongoengine import ReferenceField, StringField, EmailField
from mongoengine import DateTimeField, ListField
from mongoengine.django.auth import User

from mongoengine_extras.fields import SlugField, AutoSlugField
from mongoengine_extras.utils import slugify
from datetime import datetime

class Account(Document):
    """
    Corporate Account model in MongoDB to represent Company objects
    """
    STATUS_CHOICES = (
        (u'Active', u'Active'),
        (u'Inactive', u'Inactive'),
    )
   
    admin = ReferenceField(User)
    name = StringField(max_length=32)
#    slug = SlugField(default=slugify(name))
    phone = StringField(max_length=30)
    address1 = StringField(max_length=80)
    address2 = StringField(max_length=80)
    city = StringField(max_length=64)
    state_or_province = StringField(max_length=64)
    postal_zip = StringField(max_length=6)
    country = StringField(max_length=30)
    status = StringField(default='Active', 
                         max_length=8, 
                         choices=STATUS_CHOICES,
                         required=True)
    created = DateTimeField(default=datetime.now())
    modified = DateTimeField(default=datetime.now(), required=True)

    users = ListField(EmailField())

    def __unicode__(self):
        """
        Returns the Wall Name as unicode description for admin and shell
        """
        return self.name
