from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect ,get_object_or_404

from django.contrib.auth import authenticate, login 
from .models import JobSeeker, JobProvider
from .forms import JobPostForm, PaymentForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from .forms import *

# Create your views here.
def index(request): 
    posts = JobPost.objects.all()
    return render(request, 'home/index.html', {'posts':posts})

def contact(request):
    return render(request, 'home/contact.html')

def about(request):
    return render(request, 'home/about.html')

def seeker_registration(request):
    form = JobSeekerRegistrationForm
    return render(request,'home/employee_reg.html',{'form':form})

def submit_jobseeker(request):
    if request.method == 'POST':
        f = JobSeekerRegistrationForm(request.POST)
        print(f.errors)
        if f.is_valid():
            i_jobseeker = f.save()
            print('Form is valid')
            form = UserLoginForm()
            return render(request, 'home/login.html', {'form': form})
        else:
            print('Form is invalid', f.errors)
            return render(request, 'home/employee_reg.html', {'form': f})
        

def provider_registration(request):
    form =JobProviderRegistrationForm
    return render(request,'home/employer_reg.html',{'form':form})


def submit_jobprovider(request):
    if request.method == 'POST':

        f = JobProviderRegistrationForm(request.POST)
        print(f.errors)
        if f.is_valid():
            i_jobprovider = f.save()
            print('Form is valid')
            form = UserLoginForm()
            return render(request, 'home/login.html', {'form': form})
        else:
            print('Form is invalid', f.errors)
            return render(request, 'home/employer_reg.html', {'form': f})
    else:
        print("method!=post")

def login_form(request):
    form = UserLoginForm
    return render(request,'home/login.html',{'form':form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(user.user_type)
            if user.is_superuser:  # Redirect to superuser dashboard if user is a superuser
                return redirect("home:superuser")
            elif user.user_type == "job_seeker":  # Redirect to dashboard if user is a job seeker
                c_user = JobSeeker.objects.get(user=user)
                return render(request, "home/seeker_dashboard.html", {'current_user': c_user})
            elif user.user_type == "job_provider":  # Redirect to dashboard if user is a job provider
                c_user = JobProvider.objects.get(user=user)
                print("c_user approved", c_user.is_approved)
                form = JobPostForm()
                return render(request, "home/provider_dashboard.html", {'current_user': c_user, 'form': form})
        else:
            print("user is none")
            return redirect("home:login_form")  # Redirect back to login on failure
    print("request is not post")
    return redirect("home:login_form")  # Render login form on GET request


def jobseeker_login(request):
    form = UserLoginForm
    return render(request, 'home/jobseeker_login.html', {'form': form}) 

def jobprovider_login(request):
    form = UserLoginForm
    return render(request, 'home/jobprovider_login.html', {'form': form}) 



def available_jobs(request):
    job_posts = JobPost.objects.all()
    return render(request, 'home/available_jobs.html', {'job_posts': job_posts})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def job_provider_requests(request):
    pending_job_providers = JobProvider.objects.filter(is_approved=False)
    print("Pending Job Providers:", pending_job_providers)  # Debug statement
    if request.method == 'POST':
        provider_id = request.POST.get('provider_id')
        job_provider = JobProvider.objects.get(id=provider_id)
        if 'approve' in request.POST:
            job_provider.is_approved = True
            job_provider.save()
        elif 'reject' in request.POST:
            job_provider.delete()
        return redirect('home:superuser')
    print("Rendering Template with:", {'pending_job_providers': pending_job_providers})  # Debug statement
    return render(request, 'home/superuser.html', {'pending_job_providers': pending_job_providers})

@login_required
def superuser(request):    
    return render(request, 'home/superuser.html')
