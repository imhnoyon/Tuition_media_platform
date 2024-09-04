from django.contrib import admin
from .models import Tuition,Review,SubjectChoice
# Register your models here.

class TuitionModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'tuition_class', 'availability', 'medium', 'student_gender', 'tutor_gender', 'number_of_students','tutoring_experience', 'salary','location')
    list_filter = ('tuition_class',)
    search_fields = ('title', 'description')
admin.site.register(Tuition,TuitionModelAdmin)
admin.site.register(Review)
admin.site.register(SubjectChoice)