from django.db import models

from django.utils import timezone

import CampusCompass.settings as settings
# send mail
from django.core.mail import send_mail

from django.db.models.signals import pre_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from django.contrib.auth.models import auth
from branch.models import Department,Branch
from taggit.managers import TaggableManager
# Create your models here.

class Student(models.Model):
    student_id= models.CharField(primary_key=True,max_length=100,blank=False,null=False) # SRN
    bio= models.CharField(max_length=500,null=True, blank= True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='student')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True) # one to many
    college_email = models.EmailField(max_length=500,null=False,blank=False) # ends with @pesu.pes.edu
    whatsapp_number = models.CharField(null=True, blank=True, max_length=15) # for contact
    whatsapp_link=models.CharField(max_length=500,null=True,blank=True) # for connecting with mentors
    email_confirmed = models.BooleanField(default=False) # college email confirmed or not
    is_mentor= models.BooleanField(default=False)
    show_number=models.BooleanField(default=False) # choice for users to show their chat option
    year_of_passing_out= models.IntegerField(null=True,blank=True)
    def __str__(self):
        return self.user.username

