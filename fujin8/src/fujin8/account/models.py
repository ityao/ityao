from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)
    # Other fields here
    username = models.TextField();
    
    def __str__(self):  
        return "%s's profile" % self.user  

def create_user_profile(sender, instance, created, **kwargs):  
    if created:
        UserProfile.objects.get_or_create(user=instance)
      

post_save.connect(create_user_profile, sender=User) 