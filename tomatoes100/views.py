import urllib.request, json
from django.shortcuts import get_object_or_404, render

from .models import Movie

def index(request):
    top_100_list = Movie.objects.order_by('rank')
    context = {'top_100_list': top_100_list}    
    return render(request, 'tomatoes100/index.html', context)
	
def filter(request, resolution_filter=None):
    if resolution_filter == "None":
        resolution_filter = None
    top_100_list = Movie.objects.filter(resolution=resolution_filter)
    top_100_list = top_100_list.order_by('rank')
    context = {'top_100_list': top_100_list}    
    return render(request, 'tomatoes100/index.html', context)