from django.conf.urls import patterns, url
from .views import endpoint


urlpatterns = patterns(
    '',
    url(r'^$', endpoint, name='endpoint'),
)
