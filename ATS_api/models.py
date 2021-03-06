from operator import iadd
from django.db import models

# Create your models here.

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=30)
    middle_name=models.CharField(max_length=30,null=True)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.task

class User_Role(models.Model):
    id = models.IntegerField(primary_key=True)
    role_id = models.ForeignKey(
        'Role',
         on_delete=models.CASCADE,
         )
    user_id = models.ForeignKey(
        'User',
         on_delete=models.CASCADE,
         )
    def __str__(self):
        return self.task

class Role(models.Model):
    id = models.IntegerField(primary_key=True)
    name= models.CharField(max_length=30)

    def __str__(self):
        return self.task

class Skill_Set(models.Model):
    id = models.IntegerField(primary_key=True)
    skill = models.CharField(max_length=1000)
    skill_level = models.CharField(max_length=30)
    applicant_cv_id = models.ForeignKey(
        'applicant_cv',
         on_delete=models.CASCADE,
         )
    def __str__(self):
        return self.task

class job_platforms(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    description= models.CharField(max_length=1000)

    def __str__(self):
        return self.task

class Company(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.task

   
class applicant_cv(models.Model):
    id = models.IntegerField(primary_key=True)
    date_created = models.DateTimeField(max_length=30)
    gender = models.CharField(max_length=30)
    summary = models.CharField(max_length=1000)
    last_updated = models.DateTimeField(max_length=30)
    zip_code=models.CharField(max_length=30,null=True)
    country=models.CharField(max_length=30)
    city=models.CharField(max_length=30)
    phone=models.CharField(max_length=30)
    phone2=models.CharField(max_length=30,null=True)
    training_certification = models.CharField(max_length=100)
    applicant_id = models.ForeignKey(
        'user',
         on_delete=models.CASCADE,
         )
    def __str__(self):
        return self.task

class Experience(models.Model):
    id = models.IntegerField(primary_key=True)
    orgnization = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    begin_date = models.DateTimeField(max_length=30)
    end_date = models.DateTimeField(max_length=30)
    applicant_cv_id = models.ForeignKey(
        'skill_set',
         on_delete=models.CASCADE,
         )
    def __str__(self):
        return self.task

class Education(models.Model):
    id = models.IntegerField(primary_key=True)
    institution_name = models.CharField(max_length=30)
    degree_obtained = models.CharField(max_length=30)
    date_attended_from= models.DateTimeField(max_length=30)
    date_attended_to = models.DateTimeField(max_length=30)
    applicant_cv_id = models.ForeignKey(
        'applicant_cv',
         on_delete=models.CASCADE,
         )
    def __str__(self):
        return self.task
    

class Job(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    date_published = models.DateTimeField(max_length=30)
    job_start_date = models.DateTimeField(max_length=30)
    job_deadline = models.DateTimeField(max_length=30)
    number_of_vacancies = models.IntegerField(unique=True)
    job_category_id = models.ForeignKey(
        'job_category',
         on_delete=models.CASCADE,
         )
    job_postion = models.CharField(max_length=30)
    job_platform_id = models.ForeignKey(
        'job_platforms',
         on_delete=models.CASCADE,
         )
    orgnization_id = models.ForeignKey(
        'company',
         on_delete=models.CASCADE,
         )
    def __str__(self):
        return self.task
  
   
class job_category(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.task

class Candidate(models.Model):
    id = models.IntegerField(primary_key=True)
    date_of_appliation = models.DateTimeField(max_length=30)
    job_id = models.ForeignKey(
        'job',
         on_delete=models.CASCADE,
         )
    applicant_cv_id = models.ForeignKey(
        'applicant_cv',
         on_delete=models.CASCADE,
         )
    appliation_status = models.CharField(max_length=30) 

    def __str__(self):
        return self.task

    
class Applicant_Document(models.Model):
    id = models.IntegerField(primary_key=True)
    name=models.CharField(max_length=30)
    document= models.BinaryField(max_length=100)
    url = models.CharField(max_length=10,null=True)
    last_updated = models.DateTimeField(max_length=30)
    application_cv_id  = models.ForeignKey(
        'applicant_cv',
         on_delete=models.CASCADE,
         )

    def __str__(self):
        return self.task

 
class candidate_Evaluation(models.Model):
    id = models.IntegerField(primary_key=True)
    notes= models.CharField(max_length=1000)
    recuiter_id  = models.ForeignKey(
        'User',
         on_delete=models.CASCADE,
         )
    applicant_cv_id  = models.ForeignKey(
        'applicant_cv',
         on_delete=models.CASCADE,
         )
    evaluation_result = models.IntegerField(unique=True)

    def __str__(self):
        return self.task


class Job_Description_Document(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    document= models.BinaryField(max_length=100)
    last_updated = models.DateTimeField(max_length=30)
    job_id  = models.ForeignKey(
        'job',
         on_delete=models.CASCADE,
         )

    def __str__(self):
        return self.task

