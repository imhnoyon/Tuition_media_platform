from django.contrib import admin
from .models import Application
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

class ApplicationModelAdmin(admin.ModelAdmin):
    list_display=['teacher_name','Student_name','tuition_name','status','applied_at','cancel']

    def Student_name(self,obj):
        return obj.student.user.first_name
    
    def tuition_name(self,obj):
        return obj.tuition.title
    def teacher_name(self,obj):
        return obj.tuition.author.user.first_name
    
    def save_model(self,request,obj,form,change):
        obj.save()
        if obj.status=='Accepted':
            email_subject="Your Application is Accepted.."
            email_body=render_to_string('admin_email.html',{'student':obj.student.user})
            email=EmailMultiAlternatives(email_subject,'',to=[obj.student.user.email])
            email.attach_alternative(email_body,"text/html")
            email.send()


admin.site.register(Application,ApplicationModelAdmin)