from django.db import models

# Create your models here.

class Department(models.Model):
    department_name= models.CharField(max_length=500,null=True, blank= True,unique=True)
    department_id= models.BigAutoField(primary_key=True, auto_created=True)

    def __str__(self):
        return self.department_name

class Branch(models.Model):
    branch_name = models.CharField(max_length=200, null=True, blank=True)
    branch_code= models.BigAutoField(primary_key=True, auto_created=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='branches') # one to many
    def __str__(self):
        return self.branch_name+" ("+ self.department.department_name +")"