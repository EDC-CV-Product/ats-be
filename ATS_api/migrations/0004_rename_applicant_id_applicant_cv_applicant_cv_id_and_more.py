# Generated by Django 4.0.4 on 2022-05-26 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ATS_api', '0003_rename_application_cv_id_candidate_evaluation_applicant_cv_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='applicant_cv',
            old_name='applicant_id',
            new_name='applicant_cv_id',
        ),
        migrations.AddField(
            model_name='job',
            name='file',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(default='', max_length=20),
        ),
    ]