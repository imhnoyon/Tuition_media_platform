# Generated by Django 5.0.2 on 2024-09-04 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tuition', '0005_subjectchoice_remove_tuition_subjects_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tuition',
            name='preferred_tutor_gender',
            field=models.CharField(blank=True, choices=[('B', 'Both'), ('M', 'Male'), ('F', 'Female')], help_text='Preferred gender of tutor', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='tuition',
            name='student_gender',
            field=models.CharField(blank=True, choices=[('B', 'Both'), ('M', 'Male'), ('F', 'Female')], max_length=50, null=True),
        ),
    ]