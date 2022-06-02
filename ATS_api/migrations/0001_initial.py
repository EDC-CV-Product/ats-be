# Generated by Django 4.0.4 on 2022-06-02 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='applicant_cv',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(max_length=30)),
                ('gender', models.CharField(max_length=30)),
                ('summary', models.CharField(max_length=1000)),
                ('last_updated', models.DateTimeField(max_length=30)),
                ('zip_code', models.CharField(max_length=30, null=True)),
                ('country', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=30)),
                ('phone2', models.CharField(max_length=30, null=True)),
                ('training_certification', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=1000, null=True)),
                ('date_published', models.DateTimeField()),
                ('job_deadline', models.DateTimeField()),
                ('number_of_vacancies', models.IntegerField()),
                ('job_position', models.CharField(max_length=30)),
                ('organization_name', models.CharField(default='', max_length=50, null=True)),
                ('file', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='job_category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='job_platforms',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=30)),
                ('middle_name', models.CharField(max_length=30, null=True)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('city', models.CharField(default='', max_length=30)),
                ('phone', models.CharField(default='', max_length=20)),
                ('country', models.CharField(default='', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='User_Role',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ATS_api.role')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ATS_api.user')),
            ],
        ),
        migrations.CreateModel(
            name='Skill_Set',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('skill', models.CharField(max_length=1000)),
                ('skill_level', models.CharField(max_length=30)),
                ('applicant_cv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ATS_api.applicant_cv')),
            ],
        ),
        migrations.CreateModel(
            name='Job_Description_Document',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('document', models.BinaryField(max_length=100)),
                ('last_updated', models.DateTimeField(max_length=30)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ATS_api.job')),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='job_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ATS_api.job_category'),
        ),
        migrations.AddField(
            model_name='job',
            name='job_platform',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ATS_api.job_platforms'),
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('organization', models.CharField(max_length=30)),
                ('title', models.CharField(max_length=30)),
                ('begin_date', models.DateTimeField(max_length=30)),
                ('end_date', models.DateTimeField(max_length=30)),
                ('applicant_cv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ATS_api.skill_set')),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('institution_name', models.CharField(max_length=30)),
                ('degree_obtained', models.CharField(max_length=30)),
                ('date_attended_from', models.DateTimeField(max_length=30)),
                ('date_attended_to', models.DateTimeField(max_length=30)),
                ('applicant_cv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ATS_api.applicant_cv')),
            ],
        ),
        migrations.CreateModel(
            name='candidate_Evaluation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('notes', models.CharField(max_length=1000)),
                ('evaluation_result', models.IntegerField(unique=True)),
                ('applicant_cv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ATS_api.applicant_cv')),
                ('recruiter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ATS_api.user')),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_of_application', models.DateTimeField(auto_now=True, max_length=30)),
                ('application_status', models.CharField(max_length=30)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ATS_api.job')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ATS_api.user')),
            ],
        ),
        migrations.CreateModel(
            name='Applicant_Document',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('document', models.FileField(upload_to='')),
                ('url', models.CharField(max_length=90, null=True)),
                ('last_updated', models.DateTimeField(max_length=30)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ATS_api.user')),
            ],
        ),
        migrations.AddField(
            model_name='applicant_cv',
            name='applicant_cv',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ATS_api.user'),
        ),
    ]
