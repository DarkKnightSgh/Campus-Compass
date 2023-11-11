# Create your models here.
from django.db import models

from django.contrib.auth.models import User
from branch.models import *

class Announcement(models.Model):
    announcement_id= models.BigAutoField(primary_key=True,auto_created=True)
    title = models.CharField(max_length=100)
    featured_img = models.ImageField(upload_to='annoncement/',null=True,blank=True)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    branch = models.ManyToManyField(Branch,related_name='branches')
    post_by = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.title