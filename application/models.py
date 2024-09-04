from django.db import models
from normalUser.models import Student
from tuition.models import Tuition
# Create your models here.
APPLICATION_STATUS=[
    ('applied', 'Applied'),
    ('accepted', 'Accepted')
    ]
class Application(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    tuition=models.ForeignKey(Tuition,on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS ,default='applied',null=True,blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    cancel=models.BooleanField(default=False)
    def __str__(self):
        return f' {self.student.user.username} applied'