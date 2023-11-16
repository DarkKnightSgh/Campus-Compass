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

from django.db.models import Q

class StudentQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                Q(student_id__icontains=query) | 
                Q(bio__icontains=query) |
                Q(user__username__icontains=query) |
                Q(user__email__icontains=query) |
                Q(college_email__icontains=query) |
                Q(whatsapp_number__icontains=query) |
                Q(year_of_passing_out__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct().only(
                'student_id', 'bio', 'user__username', 'college_email',
                'whatsapp_number', 'whatsapp_link', 'email_confirmed',
                'is_mentor', 'show_number', 'year_of_passing_out'
            )  # Add more fields as needed
        return qs

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
    objects = StudentQuerySet.as_manager()

    def __str__(self):
        return self.user.username
    def get_model_name(self):
        return 'Student'

    



class Mentor(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE,related_name='mentor')
    # username= models.CharField(max_length=300,blank=False,null=False,default="AnonymousUser")
    resume= models.FileField(upload_to='resume/')
    domain= TaggableManager()
    description= models.CharField(max_length=5000,null=True, blank= True)
    approved= models.BooleanField(default=False)
    last_application_date = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    # write list domains function which returns a string
    def list_domains(self):
        return ", ".join([p.name for p in self.domain.all()])
    def set_ismentor(self):
        if self.approved:
            # find student and update database
            s=Student.objects.get(pk=self.student.pk)
            s.is_mentor=True
            s.save()
        else:
            s=Student.objects.get(pk=self.student.pk)
            s.is_mentor=False
            s.save()
    def send_approval_mail(self):
        # seven_day_ago=timezone.now() - timezone.timedelta(days=7)
        if self.approved:
            u=User.objects.get(username=self.student.user.username)
            print("hello")
            email_from = settings.EMAIL_HOST_USER
            subject = 'Mentor Application Approved'
            message = 'Congratulations '+ u.first_name+" "+ u.last_name +'!! Your mentor application has been approved. You can now mentor students at our platform College Connect.'
            recipient_list = [self.student.college_email,u.email ]
            # send_mail( subject, message, email_from, recipient_list ,fail_silently=False)
            # u.email_user(subject,message)
            # elif self.last_application_date> seven_day_ago:
            try:
                send_mail(subject, message, email_from, recipient_list, fail_silently=False)
            except Exception as e:
                print(f"Email sending failed: {e}")
        else:
            u=User.objects.get(username=self.student.user.username)
            email_from = settings.EMAIL_HOST_USER
            subject = 'Removed as Mentor'
            message = 'Sorry '+ u.first_name+" "+ u.last_name +', You can no longer mentor students at our platform College Connect.'
            recipient_list = [self.student.college_email,u.email ]
            # send_mail( subject, message, email_from, recipient_list )
            # u.email_user(subject,message)
            try:
                send_mail(subject, message, email_from, recipient_list, fail_silently=False)
            except Exception as e:
                print(f"Email sending failed: {e}")

            
  
@receiver(pre_save, sender=Mentor) # a trigger that's run everytime 
def Mentor_pre_save(sender, instance, **kwargs):
    if instance.pk is not None:
        instance.set_ismentor()
        instance.send_approval_mail()


class Club(models.Model):
    club_name= models.CharField(max_length=200,unique=True)
    club_desc= models.CharField(max_length=200)
    club_id= models.BigAutoField(auto_created=True,primary_key=True)
    club_logo= models.ImageField(blank=True,null=True,upload_to='club_logo/')
    branch= models.ManyToManyField(Branch)
    def __str__(self):
        return self.club_name

class ClubMember(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    club=models.ForeignKey(Club,on_delete=models.CASCADE,blank=True,null=True)
    club_head = models.BooleanField(default=False)
    social_media_manager= models.BooleanField(default=False)
    joined_on = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    def __str__(self):
        return self.user.username + " (" + self.club.club_name +")"

