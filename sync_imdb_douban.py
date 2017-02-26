# django shell import
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "imdbtrack.settings")
django.setup()

# imdb process import
from douban250.models import Movie as DoubanMovie
from top250.models import Movie as ImdbMovie

import urllib.request, json
import re
import time

#print(sys.stdout.encoding)

	# get json from doubanapi
    #url = "https://api.douban.com/v2/movie/imdb/tt"
    #response = urllib.request.urlopen(url + imdb_id)
    #data = response.read()
    #encoding = response.info().get_content_charset('utf-8')
    #douban_json = json.loads(data.decode(encoding))
    #douban_json['mobile_link'] = douban_json['mobile_link'].replace('m.','www.')

html = r'https://api.douban.com/v2/movie/imdb/tt'

print("start sync IMDB to Douban...")

# Loop all existing IMDB Top250 movies and locate the corresponding douban id
for imdbMovie in ImdbMovie.objects.all():

    douban_id = ""

    if imdbMovie.douban_id:
        douban_id = imdbMovie.douban_id
    else:
        # Get json from doubanapi and presist to imdbMovie
        #print(html + imdbMovie.imdb_id)
        response = urllib.request.urlopen(html + imdbMovie.imdb_id)
        data = response.read()
        encoding = response.info().get_content_charset('utf-8')
        douban_json = json.loads(data.decode(encoding))
        douban_id = re.search(r'/subject/(\d+?)/', douban_json['mobile_link']).group(1)    
        imdbMovie.douban_id = douban_id
        imdbMovie.save()
        time.sleep(5)
    
    # sync imdb movie spec to douban
    if DoubanMovie.objects.filter(douban_id=str(douban_id)):
        doubanMovie = DoubanMovie.objects.filter(douban_id=str(douban_id));
        
        if doubanMovie[0].resolution != imdbMovie.resolution:
            # Sync imdb movie to douban movie if there is discrepancy
            print("Sync Imdb Movie [" + str(imdbMovie.rank) + " - " + str(imdbMovie.title.encode("utf-8")) + ", " + imdbMovie.video_format + ", " + imdbMovie.resolution+ "] to Douban...")
            doubanMovie.update(video_format=imdbMovie.video_format, resolution=imdbMovie.resolution, is_imdb_250='Y')
            
print("over...")

# Sample mobile_link: https://m.douban.com/movie/subject/1295644