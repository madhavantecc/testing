from django.contrib.auth.models import AbstractUser,User
from django.db import models
from django.utils import timezone

# Custom User Model (For Authentication)
class CustomUser(AbstractUser):
    default=0
    USER_TYPE_CHOICES = (
        ('job_seeker', 'Job Seeker'),
        ('job_provider', 'Job Provider'),
    )
    
    email = models.EmailField(unique=True)  # Email-based login
    phone_number = models.CharField(max_length=12, unique=True, blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='job_seeker')

    USERNAME_FIELD = 'email'  # Login with email
    REQUIRED_FIELDS = ['username', 'user_type']
    is_approved = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.email} ({self.user_type})"



class JobPost(models.Model):
    provider = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='job_posts',default=1)
    Job_Title = models.CharField(max_length=100,default="")
    district = models.CharField(max_length=100,default="")
    place = models.CharField(max_length=100,default="")
    venue = models.CharField(max_length=200,default = "")
    location_url = models.URLField(max_length=200,default="https://example.com")
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now)
    number_of_workers = models.IntegerField(default=1)
    payment_per_worker = models.DecimalField(max_digits=10, decimal_places=2,default=100.00)
    job_description = models.TextField(default="")
    # track jobseekers who applied
    applied_by = models.ManyToManyField(CustomUser,related_name = 'applied_jobs',blank=True)


    def __str__(self):
        return self.Job_Title
    

    def get_seekers(self):
        return self.seekers.all()
    



# Job Provider Model (Requires Admin Approval)
class JobProvider(models.Model):    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='job_provider_profile')
    hr_name = models.CharField(max_length=200,default=0)
    alternative_phone_number = models.CharField(max_length=15,default="")
    district = models.CharField(max_length=100,default="")
    place = models.CharField(max_length=100,default="")
    company_name = models.CharField(max_length=200,default=0)
    company_address = models.TextField(default=0)
    is_approved = models.BooleanField(default=False)


    def __str__(self):
        return self.company_name
    
    
    
    

# Job Seeker Model (Linked to CustomUser)
class JobSeeker(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='job_seeker_profile')
    full_name = models.CharField(max_length=200)
    pin_code = models.CharField(max_length=6)
    upi_number = models.CharField(max_length=12, unique=True)
    age = models.IntegerField(default=0)
    district = models.CharField(max_length=30, default="Palakkad")
    city = models.CharField(max_length=30, default="Palakkad")
    provider = models.ManyToManyField(JobProvider,related_name='job_seekers',blank=True)

    def __str__(self):
        return self.full_name
    
    def apply_to_job(self,job):
        self.applied_jobs.add(job)
    



    
    @property
    def number_of_days(self):
        # Calculates the number of days between start and end date
        return (self.end_date - self.start_date).days

    @property
    def number_of_hours(self):
        # Calculates the number of hours for the job based on start and end time
        delta = datetime.combine(date.today(), self.end_time) - datetime.combine(date.today(), self.start_time)
        return delta.seconds//3600


class Payment(models.Model):
    default=0
    transaction_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id
    

