from django.db import models

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
    
    def __unicode__(self):
        return self.link

class Actress(models.Model):
    name = models.CharField(max_length=50)
    other_names = models.CharField(max_length=255)
    photo = models.URLField();    
    
    def __unicode__(self):
        return self.name
        
class MovieLink(models.Model):
    daily_link = models.ForeignKey(DailyLink)
    title = models.CharField(max_length=255)
    digestkey = models.CharField(max_length=255,unique=True)
    actress = models.ManyToManyField(Actress)
    raw_desc = models.TextField()
    images = models.TextField()
    parsed = models.BooleanField(default=False)
    
    def getImages(self):
        return str(self.images).split(";")
        
    def __unicode__(self):
        return self.title
    
    

        
