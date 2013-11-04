from django.conf.urls import patterns, url
from achilles.views import endpoint


urlpatterns = patterns(
    '',
    url(r'^$', endpoint, name='endpoint'),
)
