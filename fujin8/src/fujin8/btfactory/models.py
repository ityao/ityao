from django.db import models
from datetime import date

# Create your models here.

class MonthlyLink(models.Model):
    link = models.URLField(unique=True)
    enable = models.BooleanField(default=True)
        
    def __unicode__(self):
        return self.link

class DailyLink(models.Model):
    monthly_link = models.ForeignKey(MonthlyLink)
    label = models.CharField(max_length=255)    
    link = models.URLField(unique=True)
    parsed = models.BooleanField(default=False)
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.link

class Actress(models.Model):
    name = models.CharField(max_length=50,unique=True)
    co_names = models.CharField(max_length=255)
    photo = models.CharField(max_length=255)
    profile = models.CharField(max_length=500)
    update_date = models.DateField(auto_now=True)
    create_date = models.DateField(auto_now_add=True)
    
    def admin_thumbnail(self):
        return u'<img src="%s" height="100" />' % (self.photo)
    admin_thumbnail.short_description = 'Thumbnail'
    admin_thumbnail.allow_tags = True
    
    def __unicode__(self):
        return self.name
        
class MovieLink(models.Model):
    daily_link = models.ForeignKey(DailyLink)
    title = models.CharField(max_length=255)
    digestkey = models.CharField(max_length=255,unique=True)
    actress_names = models.CharField(max_length=255, blank=True)
    actress = models.ManyToManyField(Actress,blank=True)
    raw_desc = models.TextField()
    images = models.TextField()
    images_loaded = models.BooleanField(default=False)
    downloadlink = models.TextField()
    parsed = models.BooleanField(default=False)
    update_date = models.DateField(auto_now=True)
    create_date = models.DateField(auto_now_add=True)
    
    def admin_thumbnail(self):
        return u'<img src="%s" height="100" />' % (self.images.split(";")[0])
    admin_thumbnail.short_description = 'Thumbnail'
    admin_thumbnail.allow_tags = True
    
    def getImages(self):
        return str(self.images).split(";")
    
    def getLinks(self):
        return str(self.downloadlink).split(";")
        
    def __unicode__(self):
        return self.title
    
    

        
