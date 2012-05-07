from django.conf.urls.defaults import patterns, include, url

# a helper to automatically associate names to urls
def named_url(regex, view):
    return url(regex, view, name=view)

urlpatterns = patterns('mydocs.edit.views',
    named_url(r'^$', 'index'),
    named_url(r'^add$', 'add'),
    named_url(r'^([a-f0-9]+)$', 'edit'),
    named_url(r'^permissions/([a-f0-9]+)$', 'change_permissions'),
    named_url(r'^delete/([a-f0-9]+)$', 'delete'),
)
