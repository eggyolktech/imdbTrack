import urllib.request, json
from django.shortcuts import get_object_or_404, render

from .models import Movie

def detail(request, douban_id):

	# get json from doubanapi
    url = "https://api.douban.com//v2/movie/subject/"
    print("Request: [" + url + douban_id + "]")
    response = urllib.request.urlopen(url + douban_id)
    data = response.read()
    encoding = response.info().get_content_charset('utf-8')
    douban_json = json.loads(data.decode(encoding))
	
    return render(request, 'douban250/detail.html', {'douban_data': douban_json})

def index(request):
    top_250_list = Movie.objects.order_by('rank')
    context = {'top_250_list': top_250_list}    
    return render(request, 'douban250/index.html', context)
	
def filter(request, resolution_filter=None):
    if resolution_filter == "None":
        resolution_filter = None
    top_250_list = Movie.objects.filter(resolution=resolution_filter)
    top_250_list = top_250_list.order_by('rank')
    context = {'top_250_list': top_250_list}    
    return render(request, 'douban250/index.html', context)