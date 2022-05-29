
from django.urls import include, path

from rest_framework import routers

from ATS_api.views import UserViewSet,User_RoleViewSet,RoleViewSet,Skill_SetViewSet,job_platformsViewSet,CompanyViewSet,applicant_cvViewSet,ExperianceViewSet,EducationViewSet,JobViewSet,job_categoryViewSet,ApplicationViewSet,Applicant_DocuemntViewSet,candidate_EvaluationViewSet,Job_Discription_DocumentViewSet
router = routers.DefaultRouter()
router.register(r'User', UserViewSet)
router.register(r'User_Role', User_RoleViewSet)
router.register(r'Role', RoleViewSet)
router.register(r'Skill_Set', Skill_SetViewSet)
router.register(r'job_platforms', job_platformsViewSet)
router.register(r'Company', CompanyViewSet)
router.register(r'applicant_cv', applicant_cvViewSet)
router.register(r'Experience', ExperianceViewSet)
router.register(r'Education', EducationViewSet)
router.register(r'Job', JobViewSet)
router.register(r'job_category', job_categoryViewSet)
router.register(r'Application', ApplicationViewSet)
router.register(r'Applicant_Document', Applicant_DocuemntViewSet)
router.register(r'candidate_Evaluation', candidate_EvaluationViewSet)
router.register(r'Job_Discription_Document', Job_Discription_DocumentViewSet)

urlpatterns = [
   path('', include(router.urls)),
]

