from mongoengine import connect, Document
from mongoengine import ReferenceField, StringField, DateTimeField
from mongoengine.django.auth import User

from datetime import datetime
from hashlib import md5
from random import random

connect('mongo-tut')

def hash_link():
    now_hash = md5(datetime.now().isoformat()).hexdigest()
    noise = str(random())
    hash_link = md5(now_hash + noise).hexdigest()
    return hash_link 

def slug_link(text):
    #TODO add slugify text logic 
    return text 

class Wall(Document):
    """
    Wall model in MongoDB to represent Wall objects
    """
    STATUS_CHOICES = (
        (u'Active', u'Active'),
        (u'Private', u'Private'),
        (u'Inactive', u'Inactive'),
    )        

    owner = ReferenceField(User)
    name = StringField(max_length=32, required=True)
    description = StringField(max_length=256, required=False)
    status = StringField(default='Active', 
                         max_length=8, 
                         choices=STATUS_CHOICES,
                         required=True)
    hash_link = StringField(default=hash_link(),
                            max_length=32,
                            required=True)
    created = DateTimeField(default=datetime.now(), required=True)
    modified = DateTimeField(default=datetime.now(), required=True)
