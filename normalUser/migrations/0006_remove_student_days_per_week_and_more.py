# Generated by Django 5.0.2 on 2024-09-04 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('normalUser', '0005_rename_teacher_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='days_per_week',
        ),
        migrations.RemoveField(
            model_name='student',
            name='minimum_salary',
        ),
        migrations.RemoveField(
            model_name='student',
            name='status',
        ),
        migrations.RemoveField(
            model_name='student',
            name='tutoring_experience',
        ),
    ]