from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /top250/
    url(r'^$', views.index, name='index'),
    # ex: /top250/0107048/
    url(r'^(?P<imdb_id>[0-9]+)/$', views.detail, name='detail'),
	url(r'^filter/(?P<resolution_filter>\w{1,50})/$', views.filter, name='filter'),
	]
