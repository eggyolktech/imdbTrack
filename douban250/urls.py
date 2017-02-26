from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /douban250/
    url(r'^$', views.index, name='index'),
    # ex: /douban250/1292052/
    url(r'^(?P<douban_id>[0-9]+)/$', views.detail, name='detail'),
	url(r'^filter/(?P<resolution_filter>\w{1,50})/$', views.filter, name='filter'),
	]
