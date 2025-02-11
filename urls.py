from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from .import views

app_name ='home'
urlpatterns = [   
    path('', index, name='index'),   
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('login_form/',login_form, name='login_form'),
    path('jobseeker_login/', jobseeker_login,name='job_seeker_login'),
    path('jobprovider_login/',jobprovider_login,name='job_seeker_login'),
    path("dashboard/", login_view, name="dashboard"),
    path('seeker_registration_form', seeker_registration, name='seeker_registration'),
    path('provider_registration_form', provider_registration, name='provider_registration'),
    path('submitted_jobseeker/', submit_jobseeker, name='submitted_jobseeker'), 
    path('submitted_jobprovider/', submit_jobprovider, name='submitted_jobprovider'),
    path('employer_reg/', provider_registration, name='employer_reg'),
    path('employee_reg/', seeker_registration, name='employee_reg'), 
    path('available_jobs/', available_jobs, name='available_jobs'),
    path('superuser/', views.job_provider_requests, name='superuser'),

    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
