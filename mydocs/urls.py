from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import logout_then_login

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('mydocs',
	url(r'^', include('edit.urls')),
	url(r'^openid/', include('django_openid_auth.urls')),
	url(r'^logout$', logout_then_login),
)
