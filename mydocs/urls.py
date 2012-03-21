from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('mydocs',
	url(r'^', include('edit.urls')),
	url(r'^openid/', include('django_openid_auth.urls')),
)
