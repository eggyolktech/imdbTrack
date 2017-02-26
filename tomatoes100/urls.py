from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /tomatoes100/
    url(r'^$', views.index, name='index'),
	url(r'^filter/(?P<resolution_filter>\w{1,50})/$', views.filter, name='filter'),
	]
