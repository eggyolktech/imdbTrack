# django shell import
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "imdbtrack.settings")
django.setup()

# imdb process import
from tomatoes100.models import Movie
from django.utils import timezone
from bs4 import BeautifulSoup
from decimal import Decimal
import urllib.request, json
import requests
import re
 
top100_url = "https://www.rottentomatoes.com/top/bestofrt/"
detail_url = "https://www.rottentomatoes.com/m/"

def sync_top100_by_soup():

    r = requests.get(top100_url)
    html = r.text
    soup = BeautifulSoup(html, "html5lib")
    
    # Save last rank if there is any
    for mov in Movie.objects.exclude(rank=299):
        mov.last_rank = mov.rank
        mov.save()
    
    # Clear all rank
    Movie.objects.all().update(rank=299)

    table = soup.find('table', {'class': 'table'})
    
    for tr in table.find_all('tr')[1:]:
    
        _rank = tr.select('td.bold')[0].text.replace(".","")
        _tomatometer = tr.select('td > span > span')[0]['class'][2]
        _rating = tr.select('td > span > span.tMeterScore')[0].text
        _tomatoid = tr.select('td > a')[0]['href'].replace("/m/" ,"").replace("/", "")
        _a = tr.select('td > a')[0].text
        _title = str(_a)[:-7].replace('\n', '').strip()
        _year = str(_a)[-6:].strip('()')
        _review = tr.select('td.right')[0].text        
        
        print(_rank + " - " + str(_tomatometer) + " - " + str(_rating.replace(u'\xa0', '')) + " - " + str(_title.encode("utf8")) + " - " + _tomatoid + " - " + _year)
        
        if Movie.objects.filter(tomato_id=str(_tomatoid)):
        
            _poster = ""
        
            try:
                _poster = get_poster_detail(_tomatoid)
            except Exception as e:
                _poster = ""
                
            if _poster:
                print("---- update existing record with poster")
                
                # movies exists, updated new rank here
                Movie.objects.filter(tomato_id=str(_tomatoid)).update(rank=_rank, rating=_rating, tomatometer=_tomatometer, review=_review, last_pub_date=timezone.now(), poster=_poster)
            else:
                print("---- update existing record without poster")
                
                # movies exists, updated new rank here
                Movie.objects.filter(tomato_id=str(_tomatoid)).update(rank=_rank, rating=_rating, tomatometer=_tomatometer, review=_review, last_pub_date=timezone.now())
        else:
        
            print("---- new record found")
            
            try:
                _poster = get_poster_detail(_tomatoid)
            except Exception as e:
                print(e)
                sys.exit(0)
        
            # new movies needs to be created
            m = Movie(tomato_id=str(_tomatoid), title=_title.encode("utf-8"), year=_year, 
            rank=_rank, last_pub_date=timezone.now(), rating=_rating, tomatometer=_tomatometer, review=_review, poster=_poster )
            m.save()                          

# sync top 100 list

def get_poster_detail(tomato_id):

    # get poster for new
    _poster = ""

    try:
        r2 = requests.get(detail_url + tomato_id + "/")
        html2 = r2.text
        soup2 = BeautifulSoup(html2, "html5lib")
        poster = soup2.find('img', {'class': 'posterImage'})
        
        #print(detail_url + _tomatoid + "/")
        #print(poster['src'])
        #print("wow: " + detail_url + tomato_id + "/")
        _poster = poster['src']
        #print("poster: " + _poster)
    except Exception as e:
        print("get_poster_detail exception: " + e)
        raise
        
    return _poster
    
sync_top100_by_soup()

# <table class="table">
    # <thead>
    # <tr>
        # <th>Rank</th>
        # <th><span class="hidden-xs">Rating</span><span class="visible-xs">Tomatometer</span></th>
        # <th>Title</th>
        # <th class="right hidden-xs">No. of Reviews</th>
    # </tr>
    # </thead>
    # <tr>
    # <td class="bold">1.</td>
    # <td><span class="tMeterIcon tiny"><span class="icon tiny certified"></span><span class="tMeterScore">&nbsp;99%</span></span></td>
    # <td>

        # <a href="/m/the_wizard_of_oz_1939" class="unstyled articleLink">
            # The Wizard of Oz (1939)</a>
    # </td>
    # <td class="right hidden-xs">109</td>
# </tr>
# <tr>
    # <td class="bold">2.</td>
    # <td><span class="tMeterIcon tiny"><span class="icon tiny certified"></span><span class="tMeterScore">&nbsp;100%</span></span></td>
    # <td>

        # <a href="/m/citizen_kane" class="unstyled articleLink">
            # Citizen Kane (1941)</a>
    # </td>
    # <td class="right hidden-xs">73</td>
# </tr>
    