# django shell import
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "imdbtrack.settings")
django.setup()

# imdb process import
from top250.models import Movie
from django.utils import timezone
from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request, json
import requests
import re
 
top250_url = "http://www.imdb.com/chart/top"

def sync_top250_by_soup():
    r = requests.get(top250_url)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    exit = 0
    
    # Save last rank if there is any
    for mov in Movie.objects.exclude(rank=299):
        mov.last_rank = mov.rank
        mov.save()
    
    # Clear all rank
    Movie.objects.all().update(rank=299)
    
    tbody = soup.find('tbody', {'class': 'lister-list'})
    
    for tr in tbody.find_all('tr'):
    
        poster_col = tr.find('td', {'class': 'posterColumn'})
        title_col = tr.find('td', {'class': 'titleColumn'})
        rating_col = tr.find('td', {'class': 'imdbRating'})
        
        if poster_col:
            i = poster_col.select('img')[0]
            _poster = i['src']
        
        if title_col:            
            a = title_col.select('a')[0]
            s = title_col.select('span')[0]            
            _title = a.text.strip(" \t\n\r")
            _url = a['href']
            _casting = a['title']      
            _id = re.search(r'/tt(\d+?)/', _url).group(1)
            _rank = re.search(r'chttp_tt_(\d+)', _url).group(1)
            _year = s.text.strip("()")
        
        if rating_col:        
            t = rating_col.select('strong')[0]        
            _rating = t.text.strip()
            _rating = Decimal(_rating)
        
        print(_rank + " - " + str(_title.encode("utf-8")) + " [tt" + _id + ", " + _year + ", " + str(_rating) + "]")
        
        if Movie.objects.filter(imdb_id=str(_id)):
            # movies exists, updated new rank here
            Movie.objects.filter(imdb_id=str(_id)).update(rank=_rank, rating=_rating, poster=_poster, last_pub_date=timezone.now())
        else:
            # get other 250 details from omdb api
            _json = get_top250_other_detail(_id)
            _runtime = _json['Runtime']
            _genre = _json['Genre']
            _director = _json['Director']
            _country = _json['Country']
            _writer = _json['Writer']
            _actors = _json['Actors']
            _plot = _json['Plot']
            _language = _json['Language']
            #_poster = _json['Poster']
            #print("Other Info [Poster: " + _poster + "]")
            
            # download the poster if new entry
            #if _poster and _poster != 'N/A':
            #    download_remote_file(_poster, os.path.join('top250', 'medias', 'tt' + _id + '.jpg'))

            # new movies needs to be created
            m = Movie(imdb_id=str(_id), title=_title.encode("utf-8"), casting=_casting.encode("utf-8"), year=_year, 
            rank=_rank, last_pub_date=timezone.now(), country=_country, rating=_rating, runtime=_runtime, genre=_genre, language=_language, plot=_plot, poster=_poster )
            m.save()                   

def get_top250_other_detail(imdb_id):
    url = "http://www.omdbapi.com/?i={}&plot=full&r=json"
    print (url.format(imdb_id))
    response = urllib.request.urlopen(url.format("tt" + imdb_id))
    data = response.read()
    encoding = response.info().get_content_charset('utf-8')
    movie_json = json.loads(data.decode(encoding))
    print ("get omdbapi successfully!")
    return movie_json
            
            
def download_remote_file(url, filepath):    
    file = urllib.request.URLopener()
    file.retrieve(url, filepath)
            
# sync top 250 list
sync_top250_by_soup()

# list all movies in django
#print(Movie.objects.all())
#Movie.objects.all().delete()