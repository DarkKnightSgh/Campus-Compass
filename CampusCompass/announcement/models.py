# Create your models here.
from django.db import models

from django.contrib.auth.models import User
from branch.models import *

from django.db.models import Q

class AnnouncementQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                Q(title__icontains=query) | 
                Q(content__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct().only(
                'announcement_id', 'title', 'content', 'date_created'
            )  # Add more fields as needed
        return qs

class Announcement(models.Model):
    announcement_id= models.BigAutoField(primary_key=True,auto_created=True)
    title = models.CharField(max_length=100)
    featured_img = models.ImageField(upload_to='annoncement/',null=True,blank=True)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    branch = models.ManyToManyField(Branch,related_name='branches')
    post_by = models.ForeignKey(User,on_delete=models.CASCADE)
    objects = AnnouncementQuerySet.as_manager()
    
    def __str__(self):
        return self.title
    def get_model_name(self):
        return 'Announcement'