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
    
    for tr in table.find_all('tr', {'itemprop':'itemListElement'}):
    
        _rank = tr.select('td.bold')[0].text.replace(".","")
        _tomatometer = tr.select('td > span > span')[0]['class'][2]
        _rating = tr.select('td > span > span.tMeterScore')[0].text
        _tomatoid = tr.select('td > a')[0]['href'].replace("/m/" ,"").replace("/", "")
        _a = tr.select('td > a')[0].text
        _title = str(_a)[:-7]
        _year = str(_a)[-6:].strip('()')
        _review = tr.select('td.right')[0].text        

        print(_rank + " - " + str(_tomatometer) + " - " + _rating + " - " + str(_title.encode("utf8")) + " - " + _tomatoid + " - " + _year)
        
        if Movie.objects.filter(tomato_id=str(_tomatoid)):
            # movies exists, updated new rank here
            Movie.objects.filter(tomato_id=str(_tomatoid)).update(rank=_rank, rating=_rating, tomatometer=_tomatometer, review=_review, last_pub_date=timezone.now())
        else:
        
            # get poster for new
            _poster = ""
            try:
                r2 = requests.get(detail_url + _tomatoid + "/")
                html2 = r2.text
                soup2 = BeautifulSoup(html2, "html5lib")
                poster = soup2.find('img', {'class': 'posterImage'})
                #print(detail_url + _tomatoid + "/")
                #print(poster['src'])
                _poster = poster['src']
            except Exception as e:
                print(e)
                exit
        
            # new movies needs to be created
            m = Movie(tomato_id=str(_tomatoid), title=_title.encode("utf-8"), year=_year, 
            rank=_rank, last_pub_date=timezone.now(), rating=_rating, tomatometer=_tomatometer, review=_review, poster=_poster )
            m.save()                          

# sync top 100 list
sync_top100_by_soup()

#<tr itemprop="itemListElement" itemscope="" itemtype="https://schema.org/ListItem">
# <td class="bold">2.</td> 
# <td><span class="tMeterIcon tiny"> <span title="Certified&nbsp;Fresh" class="icon tiny certified"></span> <span class="tMeterScore">100%</span> </span> </td> 
# <td> <meta itemprop="position" content="1"> <a class="unstyled articleLink" target="_top" data-pageheader="" href="/m/the-third-man/" itemprop="url">The Third Man (1949)</a></td> 
# <td class="right hidden-xs">76</td> 
#</tr>
    