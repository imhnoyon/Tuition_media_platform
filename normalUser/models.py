from django.db import models
from django.contrib.auth.models import User
from .constrains import *
# Create your models here.

class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='normalUser/images/')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,null=True,blank=True)
    mobile=models.CharField(max_length=15,null=True,blank=True)
    location = models.CharField(max_length=100,null=True,blank=True)
    tuition_district = models.CharField(max_length=100,null=True,blank=True)
    # minimum_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # status = models.CharField(max_length=20, choices=TUTORING_STATUS_CHOICES, default='Available',null=True,blank=True)
    # days_per_week = models.IntegerField(default=5,null=True,blank=True)
    school = models.CharField(max_length=500,null=True,blank=True)
    Group = models.CharField(max_length=50,null=True,blank=True)
    medium_of_instruction = models.CharField(max_length=20, choices=MEDIUM_OF_INSTRUCTION_CHOICES,null=True,blank=True)

    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
