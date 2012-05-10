# Documents belong to the mongodb,
# other stuff to the SQL database for compability
class DocumentRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.object_name in ('Document', 'UserPermission'):
            return 'documents'
        else:
            return None

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)

    def allow_syncdb(self, db, model):
        if model._meta.object_name in ('Document', 'UserPermission'):
            return db == 'documents'
        return True
