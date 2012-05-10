from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django_openid_auth.exceptions import IdentityAlreadyClaimed
from djangotoolbox.fields import ListField, DictField, EmbeddedModelField
from django_mongodb_engine.contrib import MongoDBManager

class Permission:
    NoAccess = 0
    Read = 1
    Modify = 2
    ChangePerms = 3
    Owner = 4

# These are the permissions selectable from the listboxes
PERMISSIONS = (
    (Permission.Read, 'Access'),
    (Permission.Modify, 'Modify'),
    (Permission.ChangePerms, 'Change permissions')
)
# These permissions can be set for anonymous users
ANON_PERMISSIONS = (
    (Permission.NoAccess, 'None'),
    (Permission.Read, 'Access'),
    (Permission.Modify, 'Modify'),
)

class UserPermission(models.Model):
    email = models.EmailField(max_length=64)
    permission = models.IntegerField(choices=PERMISSIONS)

class Document(models.Model):
    objects = MongoDBManager()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=64)
    content = models.TextField(blank=True)
    permissions = ListField(EmbeddedModelField(UserPermission))
    anon_permissions = models.IntegerField("Anonymous user permissions",
                choices=ANON_PERMISSIONS, default=Permission.NoAccess)
    owner = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name

    def get_permission_for(self, user):
        if not user.is_authenticated():
            return self.anon_permissions
        elif user.email == self.owner:
            return Permission.Owner
        for perm in self.permissions:
            if perm.email == user.email:
                return max(perm.permission, self.anon_permissions)

        return self.anon_permissions

    def permitted_user_emails(self):
        lst = []
        if self.anon_permissions:
            lst += ['Anonymous users']
        lst += [self.owner] + map(lambda p: p.email, self.permissions)
        return lst

    @staticmethod
    def find_accessible_by(user):
        if not user.is_authenticated():
            return Document.objects.none()

        query = {
            'permissions': {
                '$elemMatch': {
                    'email': user.email }}}
        return Document.objects.raw_query(query)

    @staticmethod
    def find_own(user):
        if not user.is_authenticated():
            return Document.objects.none()
        return Document.objects.filter(owner=user.email)

@receiver(pre_save, sender=User)
def require_unique_email(sender, instance, **kwargs):
    if User.objects.filter(email=instance.email).exclude(pk=instance.pk).count() >= 1:
        raise IdentityAlreadyClaimed("Someone has already registered with this e-mail.")
