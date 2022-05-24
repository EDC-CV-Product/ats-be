from rest_framework import serializers
from ATS_api.models import User,User_Role,Role,Skill_Set,job_platforms,Company,applicant_cv,Experience,Education,Job,job_category,Candidate,Applicant_Document,candidate_Evaluation,Job_Description_Document

class UserSerializer(serializers.ModelSerializer):
   class Meta:
       model = User
       fields = ('id', 'first_name', 'middle_name', 'last_name','email','password')


class User_RoleSerializer(serializers.ModelSerializer):
   class Meta:
       model = User_Role
       fields = ('id', 'role_id', 'user_id')

class RoleSerializer(serializers.ModelSerializer):
   class Meta:
       model = Role
       fields = ('id', 'name')

class Skill_SetSerializer(serializers.ModelSerializer):
   class Meta:
       model = Skill_Set
       fields = ('id', 'skill','skill_level','applicant_cv_id')

class job_platformsSerializer(serializers.ModelSerializer):
   class Meta:
       model = job_platforms
       fields = ('id', 'code','name','description')


class CompanySerializer(serializers.ModelSerializer):
   class Meta:
       model = Company
       fields = ('id', 'code','name','description')

class applicant_cvSerializer(serializers.ModelSerializer):
   class Meta:
       model = applicant_cv
       fields = ('id', 'date_created','gender','summary','last_updated','zip_code','country','city','phone','phone2','training_certification','applicant_id')


class ExperianceSerializer(serializers.ModelSerializer):
   class Meta:
       model = Experience
       fields = ('id', 'orgnization','title','begin_date','end_date','applicant_cv_id')


class EducationSerializer(serializers.ModelSerializer):
   class Meta:
       model = Education
       fields = ('id', 'institution_name','degree_obtained','date_attended_from','date_attended_to','applicant_cv_id')


class JobSerializer(serializers.ModelSerializer):
   class Meta:
       model = Job
       fields = ('id', 'code','name','description','date_published','job_start_date','job_deadline','number_of_vacancies','job_category_id','job_postion','job_platform_id','orgnization_id')


class job_categorySerializer(serializers.ModelSerializer):
   class Meta:
       model = job_category
       fields = ('id', 'code','name','description')

class CandidateSerializer(serializers.ModelSerializer):
   class Meta:
       model = Candidate
       fields = ('id', 'date_of_appliation','job_id','applicant_cv_id','appliation_status')

class applicant_DocumentSerializer(serializers.ModelSerializer):
   class Meta:
       model = Applicant_Document
       fields = ('id', 'name','document','url','last_updated')

class candidate_EvaluationSerializer(serializers.ModelSerializer):
   class Meta:
       model = candidate_Evaluation
       fields = ('id', 'notes','recuiter_id','applicant_cv_id','evaluation_result')

class Job_Discription_DocumentSerializer(serializers.ModelSerializer):
   class Meta:
       model = Job_Description_Document
       fields = ('id', 'name','document','url','last_updated','job_id')