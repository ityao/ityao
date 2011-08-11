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
    name = models.CharField(max_length=200)
    photo = models.URLField();
    
    def __unicode__(self):
        return self.name
        
class MovieLink(models.Model):
    attress = models.ForeignKey(Actress)
    link = models.CharField(max_length=200,unique=True)
    
    def __unicode__(self):
        return self.attress +":"+ self.link
    
    

        
