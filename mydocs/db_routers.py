class DocumentRouter(object):

	def db_for_read(self, model, **hints):
		if model._meta.object_name == 'Document':
			return 'documents'
		else:
			return None

	def db_for_write(self, model, **hints):
		return self.db_for_read(model, **hints)
