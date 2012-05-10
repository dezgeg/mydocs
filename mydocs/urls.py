from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import logout_then_login
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('mydocs',
    url(r'^', include('edit.urls')),
    url(r'^openid/', include('django_openid_auth.urls')),
    url(r'^logout$', logout_then_login, name='logout'),
)
urlpatterns += staticfiles_urlpatterns()
