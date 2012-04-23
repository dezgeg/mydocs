from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django_openid_auth.exceptions import IdentityAlreadyClaimed
from djangotoolbox.fields import ListField, DictField, EmbeddedModelField
from django_mongodb_engine.contrib import MongoDBManager
from django import forms

# A form field for ListField: https://gist.github.com/1200165
class StringListField(forms.CharField):
    def prepare_value(self, value):
        return ', '.join(value)

    def to_python(self, value):
        if not value:
            return []
        return [item.strip() for item in value.split(',')]

ListField.formfield = lambda self, **kwargs: models.Field.formfield(self, StringListField, **kwargs)

PERMISSIONS = (
    (1, 'Access'),
    (2, 'Modify'),
    (3, 'Change permissions')
)

class UserPermission(models.Model):
    email = models.CharField(max_length=64)
    permission = models.IntegerField(choices=PERMISSIONS)

class Document(models.Model):
    objects = MongoDBManager()

    name = models.CharField(max_length=64)
    content = models.TextField()
    tags = ListField(models.CharField(max_length=16, blank=True))
    permissions = ListField(EmbeddedModelField(UserPermission))
    owner = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name

    @staticmethod
    def find_accessible_by(user):
        if not user.is_authenticated():
            return Document.objects.none()

        query = { '$or': [
            { 'owner': user.email },
            { 'permissions': {
                '$elemMatch': {
                    'email': user.email }}}]}
        return Document.objects.raw_query(query)

@receiver(pre_save, sender=User)
def require_unique_email(sender, instance, **kwargs):
    if User.objects.filter(email=instance.email).exclude(pk=instance.pk).count() >= 1:
        raise IdentityAlreadyClaimed("Someone has already registered with this e-mail.")
