from django.db import models

class Document(models.Model):
	name = models.CharField(max_length=64)
	content = models.TextField()

	def __unicode__(self):
		return self.name
