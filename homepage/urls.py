from django.conf.urls import url
from . import views
  
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search-movie/', views.get_movie, name='get_movie'),
]

