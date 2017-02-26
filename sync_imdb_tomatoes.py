# django shell import
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "imdbtrack.settings")
django.setup()

import re

# imdb process import
from tomatoes100.models import Movie as TomatoMovie
from top250.models import Movie as ImdbMovie

print("start sync IMDB to Tomatoes...")

# Loop all existing IMDB Top250 movies and locate the corresponding douban id
for imdbMovie in ImdbMovie.objects.all():

    for tomatoMovie in TomatoMovie.objects.all():

        iTitle = imdbMovie.title
        tTitle = tomatoMovie.title.split('(')[0].strip()
        
        tSubTitle = ""
        if '(' in tomatoMovie.title:
            tSubTitle = tomatoMovie.title.split('(')[1].split(')')[0].strip()

        if len(iTitle) == len(tTitle) and iTitle.lower() == tTitle.lower():
            if tomatoMovie.resolution != imdbMovie.resolution:
                print("Sync Imdb Movie: [" + str(iTitle.encode("utf8")) + ", " + str(tTitle.encode("utf8")) + "]")
                tomatoMovie.video_format = imdbMovie.video_format
                tomatoMovie.resolution = imdbMovie.resolution
                tomatoMovie.is_imdb_250='Y'
                tomatoMovie.save()
        elif len(iTitle) == len(tSubTitle) and iTitle.lower() == tSubTitle.lower():
            if tomatoMovie.resolution != imdbMovie.resolution:
                print("Sync Imdb Movie: [" + str(iTitle.encode("utf8")) + ", " + str(tSubTitle.encode("utf8")) + "]")
                tomatoMovie.video_format = imdbMovie.video_format
                tomatoMovie.resolution = imdbMovie.resolution
                tomatoMovie.is_imdb_250='Y'
                tomatoMovie.save()
            
print("over...")
