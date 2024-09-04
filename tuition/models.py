from django.db import models
from normalUser.models import Student
from .constrains import *
from admin_pannel.models import AdminModel
# Create your models here.

class SubjectChoice(models.Model):
    name = models.CharField(max_length=50, choices=SUBJECT_CHOICES)

    def __str__(self):
        return self.name


class Tuition(models.Model):
    author=models.ForeignKey(AdminModel,on_delete=models.CASCADE,null=True,blank=True)
    title=models.CharField(max_length=100)
    subjects = models.ManyToManyField(SubjectChoice, related_name='tuitions', null=True,blank=True)
    tuition_class = models.CharField(max_length=50, choices=CLASS_CHOICES,null=True,blank=True)
    availability = models.BooleanField(default=True, help_text="Availability status of the tuition")
    description = models.TextField(null=True,blank=True,help_text="Detailed Description of the tuition")
    medium = models.CharField(max_length=50, choices=MEDIUM_OF_INSTRUCTION_CHOICES,null=True,blank=True, help_text="Medium of instruction")
    student_gender = models.CharField(max_length=50, choices=GENDER_CHOICES,null=True,blank=True)
    tutor_gender = models.CharField(max_length=50, choices=GENDER_CHOICES1,null=True,blank=True, help_text="Preferred gender of tutor")
    tutoring_time = models.CharField(max_length=20, choices=TIME_CHOICES,null=True,blank=True, help_text="Time for tutoring")
    number_of_students = models.PositiveIntegerField(default=1,null=True,blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, help_text="Salary offered per month",null=True,blank=True)
    location=models.CharField(max_length=100,null=True,blank=True)
    tutoring_experience = models.CharField(max_length=20,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Review(models.Model):
    reviewer=models.ForeignKey(Student,on_delete=models.CASCADE) # ektu confused a chi ekhane
    tuition=models.ForeignKey(Tuition,on_delete=models.CASCADE)
    body=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating=models.CharField(max_length=100,choices=STAR_CHOICES)

    def __str__(self):
        return f'Student: {self.reviewer.user.first_name} {self.reviewer.user.first_name} Review at Tuition :{self.tuition.title} and Teacher : {self.tuition.author.user.first_name}'