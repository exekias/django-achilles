from django.conf.urls import patterns, url, include
from .views import Home

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^achilles$', include('achilles.urls')),
)
