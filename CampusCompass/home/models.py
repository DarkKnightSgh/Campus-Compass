from django.db import models

from django.core.mail import send_mail
from django.dispatch import receiver

from django.db.models.signals import pre_save

import CampusCompass.settings as settings

# Create your models here.

class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    query= models.TextField()
    sent_on= models.DateTimeField(auto_now_add=True)
    response = models.TextField(null=True,blank=True)
    response_on= models.DateTimeField(auto_now_add=True,null=True,blank=True)
    closed= models.BooleanField(default=False,null=True,blank=True)
    def __str__(self):
        return self.name
    def send_response_mail(self):
        if self.response:      
            # update closed
            # self.closed=True
            # self.save()     
            send_mail(
                'Response to your query',
                self.response,
                settings.EMAIL_HOST_USER,
                [self.email],
                fail_silently=False,
            )

    

@receiver(pre_save, sender=ContactUs) # a trigger that's run everytime 
def ContactUs_pre_save(sender, instance, **kwargs):
    instance.send_response_mail()

