from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django_openid_auth.exceptions import IdentityAlreadyClaimed

class Document(models.Model):
	name = models.CharField(max_length=64)
	content = models.TextField()

	def __unicode__(self):
		return self.name

@receiver(pre_save, sender=User)
def require_unique_email(sender, instance, **kwargs):
	if User.objects.filter(email=instance.email).exclude(pk=instance.pk).count() >= 1:
		raise IdentityAlreadyClaimed("Someone has already registered with this e-mail.")
