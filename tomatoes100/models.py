from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
class Movie(models.Model):
    tomato_id = models.CharField(max_length=100)
    rank = models.IntegerField(null=True)
    title = models.CharField(max_length=200)
    year = models.IntegerField(null=True)  
    rating = models.CharField(null=True, max_length=5)
    tomatometer = models.CharField(null=True, max_length=10)
    review = models.IntegerField(null=True)
    poster = models.CharField(null=True, max_length=300)
    last_rank = models.IntegerField(null=True, editable=False)
    last_pub_date = models.DateTimeField('date ranked')
    is_imdb_250 = models.CharField(max_length=1, default='N', editable=True)
    is_douban_250 = models.CharField(max_length=1, default='N', editable=True)
 
    FORMAT = (
        ('MKV', 'MKV'),
        ('MP4', 'MP4'),
        ('RMVB', 'RMVB'),
        ('DAT', 'DAT'),
        ('OTH', 'Others'),
    )
    video_format = models.CharField(max_length=4, choices=FORMAT, null=True) 

    RESOLUTION = (
        ('360p', '360p'),
        ('480p', '480p'),
        ('576p', '576p'),
        ('720p', '720p'),
        ('1080p', '1080p'),
        ('OTH', 'Others'),
    )
    resolution = models.CharField(max_length=5, choices=RESOLUTION, null=True)  

    def __str__(self):
        return str(self.rank) + " - " + self.title
