# django shell import
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "imdbtrack.settings")
django.setup()

# imdb process import
from douban250.models import Movie
from django.utils import timezone
from decimal import Decimal

import urllib.request, json
import string
import sys, traceback 

html = r'https://api.douban.com/v2/movie/top250?start={page}'

# Save last rank if there is any
for mov in Movie.objects.exclude(rank=299):
    mov.last_rank = mov.rank
    mov.save()

# Clear all rank
Movie.objects.all().update(rank=299)      
    
print('begin...')
i = 1
p = 1
while p <=13:
    #print '=====START PAGE:',(p-1)*20
    #get a page each time
    try:
        response = urllib.request.urlopen(html.format(page=(p-1)*20))
        encoding = response.headers.get_content_charset()
        data = response.read().decode(encoding)
        hjson = json.loads(data)
    except Exception as e:
        print(e)
        traceback.print_exc(file=sys.stdout)
        exit
        
    for key in hjson['subjects']:

        if Movie.objects.filter(douban_id=str(key['id'])):
            # movies exists, updated new rank here
            print(i,':', key['original_title'].encode("utf-8"),'-- Exist')
            Movie.objects.filter(douban_id=key['id']).update(rank=i, rating=key['rating']['average'], poster=key['images']['small'], last_pub_date=timezone.now())
        else:
            # new movie
            print(i,':', key['original_title'].encode("utf-8"), '-- New')
            m = Movie(douban_id=key['id'], rank=i, title=key['title'].encode("utf-8"), year=key['year'], 
            director=key['directors'][0]['name'].encode("utf-8"),rating=key['rating']['average'],
            original_title=key['original_title'].encode("utf-8"),poster=key['images']['small'],
            last_pub_date=timezone.now())
            m.save()
        i+=1
    p+=1

print('over!')

#   douban_id = models.CharField(max_length=10)
#   rank = models.IntegerField(null=True)
#   title = models.CharField(max_length=200)
#   year = models.IntegerField(null=True)  
#   country = models.CharField(max_length=50, null=True)
#   directors = models.CharField(max_length=100, null=True)
#   rating = models.DecimalField(max_digits=2, decimal_places=1, null=True)
#   original_title = models.CharField(max_length=200)
#   poster = models.CharField(max_length=300, null=True)
#   runtime = models.CharField(max_length=10, null=True)
#   last_rank = models.IntegerField(null=True)
#   last_pub_date = models.DateTimeField('date ranked')
