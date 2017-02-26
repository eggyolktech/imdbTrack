import urllib.request, json
from django.shortcuts import get_object_or_404, render

from .models import Movie

def detail(request, imdb_id):
	# get json from omdbapi
    url = "http://www.omdbapi.com/?plot=full&r=json&i=tt"
    response = urllib.request.urlopen(url + imdb_id)
    data = response.read()
    encoding = response.info().get_content_charset('utf-8')
    movie_json = json.loads(data.decode(encoding))
	
	# get json from doubanapi
    url = "https://api.douban.com/v2/movie/imdb/tt"
    response = urllib.request.urlopen(url + imdb_id)
    data = response.read()
    encoding = response.info().get_content_charset('utf-8')
    douban_json = json.loads(data.decode(encoding))
    douban_json['mobile_link'] = douban_json['mobile_link'].replace('m.','www.')
	
    return render(request, 'top250/detail.html', {'movie_data': movie_json, 'douban_data': douban_json})

def index(request):
    top_250_list = Movie.objects.order_by('rank')
    context = {'top_250_list': top_250_list}    
    return render(request, 'top250/index.html', context)
	
def filter(request, resolution_filter=None):
    if resolution_filter == "None":
        resolution_filter = None
    top_250_list = Movie.objects.filter(resolution=resolution_filter)
    top_250_list = top_250_list.order_by('rank')
    context = {'top_250_list': top_250_list}    
    return render(request, 'top250/index.html', context)