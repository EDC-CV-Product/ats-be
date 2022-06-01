from pyexpat import model
from urllib import response
from warnings import filters
from django.shortcuts import render
from itsdangerous import Serializer

# Create your views here.
from rest_framework import viewsets

from ATS_api.serializers import UserSerializer, User_RoleSerializer,RoleSerializer,Skill_SetSerializer,job_platformsSerializer,CompanySerializer,applicant_cvSerializer,ExperianceSerializer,EducationSerializer,JobSerializer,job_categorySerializer,ApplicationSerializer,applicant_DocumentSerializer,candidate_EvaluationSerializer,Job_Discription_DocumentSerializer
from ATS_api.models import User, User_Role,Role,Skill_Set, job_category,job_platforms,Company,applicant_cv,Experience,Education,Job,job_category,Application,Applicant_Document,candidate_Evaluation,Job_Description_Document

# for email View
from .models import User
from .serializers import UserSerializer
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend



class UserViewSet(viewsets.ModelViewSet):
   queryset = User.objects.all()
   serializer_class = UserSerializer


class User_RoleViewSet(viewsets.ModelViewSet):
   queryset = User_Role.objects.all()
   serializer_class = User_RoleSerializer

class RoleViewSet(viewsets.ModelViewSet):
   queryset = Role.objects.all()
   serializer_class = RoleSerializer

class Skill_SetViewSet(viewsets.ModelViewSet):
   queryset = Skill_Set.objects.all()
   serializer_class = Skill_SetSerializer
   
class job_platformsViewSet(viewsets.ModelViewSet):
   queryset = job_platforms.objects.all()
   serializer_class = job_platformsSerializer


class CompanyViewSet(viewsets.ModelViewSet):
   queryset = Company.objects.all()
   serializer_class = CompanySerializer
   
class applicant_cvViewSet(viewsets.ModelViewSet):
   queryset = applicant_cv.objects.all()
   serializer_class = applicant_cvSerializer


class ExperianceViewSet(viewsets.ModelViewSet):
   queryset = Experience.objects.all()
   serializer_class = ExperianceSerializer
   
class EducationViewSet(viewsets.ModelViewSet):
   queryset = Education.objects.all()
   serializer_class = EducationSerializer


class JobViewSet(viewsets.ModelViewSet):
   queryset = Job.objects.all()
   serializer_class = JobSerializer
   
class job_categoryViewSet(viewsets.ModelViewSet):
   queryset = job_category.objects.all()
   serializer_class = job_categorySerializer


class ApplicationViewSet(viewsets.ModelViewSet):
   queryset = Application.objects.all()
   serializer_class = ApplicationSerializer
   
class Applicant_DocuemntViewSet(viewsets.ModelViewSet):
   queryset = Applicant_Document.objects.all()
   serializer_class = applicant_DocumentSerializer

   
class candidate_EvaluationViewSet(viewsets.ModelViewSet):
   queryset = candidate_Evaluation.objects.all()
   serializer_class = candidate_EvaluationSerializer


class Job_Discription_DocumentViewSet(viewsets.ModelViewSet):
   queryset = Job_Description_Document.objects.all()
   serializer_class = Job_Discription_DocumentSerializer

# To Filter Using Email Address    
"""class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend)
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id','=email']"""

"""class EmailViewSet(generics.ListAPIView):
    queryset = User.objects.all()
    Serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ['id', 'first_name']
    search_fields=['id','first_name']"""

