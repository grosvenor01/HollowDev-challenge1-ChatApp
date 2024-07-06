from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
# Create your models here.
User = get_user_model()
class room(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    room_name= models.CharField(max_length=30)
    date = models.DateField(auto_now=True)

class message(models.Model):
    sender = models.ForeignKey(User , on_delete=models.CASCADE)
    chat_room = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now=True)
    message = models.TextField()

class profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    description = models.TextField()
    joined_us = models.DateTimeField(auto_now=True)
    specilality = models.CharField(max_length=30)
    #as i don't have a lot of data or unused data to send to the frontend 
    #i am adding this two to just add graphql functionality 
    idk = models.CharField(max_length=30)
    idk2 = models.CharField(max_length=50)


@receiver(post_save, sender=User) 
def create_profile(sender, instance, created, **kwargs):
        if created:
            descreption = " i add this for testing the graphql only you ccan modify it from the admin panel "
            specilality = " bnadem no life maandouch speciality (jk had data creyitha b signal tssema random)"
            idk = " hna aslan manaach rayhin nsh9ouha tssema 3amer brk"
            idk2 = " same "
            prfl = profile.objects.create(user=instance ,description=descreption,specilality=specilality , idk = idk , idk2=idk2)
            prfl.save()