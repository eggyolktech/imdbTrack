from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from .forms import MovieForm

# imdb process import
from douban250.models import Movie as DoubanMovie
from tomatoes100.models import Movie as TomatoMovie
from top250.models import Movie as ImdbMovie

def index(request):
    #imdbCount = Movie.objects.count()    
    context = {}    
    return render(request, 'homepage/index.html', context)
    

def get_movie(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MovieForm(request.POST)
        # check whether it's valid:
        
        #table.objects.filter(string__icontains='pattern')
        if form.is_valid():
            # process the data in form.cleaned_data as required
             
            search_movie = form.cleaned_data['search_movie']
            #print("search string=" + str(search_movie))
            tList = TomatoMovie.objects.filter(title__icontains=search_movie)
            dList = DoubanMovie.objects.filter(original_title__icontains=search_movie)
            iList = ImdbMovie.objects.filter(title__icontains=search_movie)
            
            # ...
            # redirect to a new URL:
            return render(request, 'homepage/search_movie.html', {'form': form, 'tList': tList, 'dList': dList, 'iList': iList})
        return HttpResponseRedirect('/')