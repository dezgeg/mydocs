from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('mydocs.edit.views',
	url(r'^$', 'index'),
	url(r'^add$', 'add'),
	url(r'^(\d+)', 'edit'),
	url(r'^delete/(\d+)', 'delete'),
)
