from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('mydocs.edit.views',
	url(r'^$', 'index'),
	url(r'^add$', 'add'),
	url(r'^([a-f0-9]+)$', 'edit'),
	url(r'^permissions/([a-f0-9]+)$', 'change_permissions'),
	url(r'^delete/([a-f0-9]+)$', 'delete'),
)
