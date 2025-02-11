from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, JobSeeker, JobProvider, JobPost, Payment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Row,Column,Submit

# Job Seeker Registration Form
class JobSeekerRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=200, required=True)
    pin_code = forms.CharField(max_length=6, required=True)
    upi_number = forms.CharField(max_length=12, required=True)
    age = forms.IntegerField(required=True)
    district = forms.CharField(max_length=30, required=True)
    city = forms.CharField(max_length=30, required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'phone_number', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'job_seeker'  # Mark as job seeker
        if commit:
            user.save()
            JobSeeker.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                pin_code=self.cleaned_data['pin_code'],
                upi_number=self.cleaned_data['upi_number'],
                age=self.cleaned_data['age'],
                district=self.cleaned_data['district'],
                city=self.cleaned_data['city']
            )
        return user

# Job Provider Registration Form (Needs Approval)

class JobProviderRegistrationForm(UserCreationForm):
    company_name = forms.CharField(max_length=200, required=True)
    company_address = forms.CharField(widget=forms.Textarea, required=True)
    hr_name = forms.CharField(max_length=200, required=True)
    alternative_phone_number = forms.CharField(max_length=15, required=False)
    district = forms.CharField(max_length=100, required=True)
    place = forms.CharField(max_length=100, required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'phone_number', 'password1', 'password2', 'company_name', 'company_address', 'hr_name', 'alternative_phone_number', 'district', 'place']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'job_provider'  # Mark as job provider
        if commit:
            user.save()
            JobProvider.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                company_address=self.cleaned_data['company_address'],
                hr_name=self.cleaned_data['hr_name'],
                alternative_phone_number=self.cleaned_data['alternative_phone_number'],
                district=self.cleaned_data['district'],
                place=self.cleaned_data['place'],
            )
        return user

# Login Form (Allows login for both user types)
class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
    
class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = [
            'Job_Title', 'district', 'place', 'venue', 'location_url','start_date', 'end_date', 'start_time','end_time', 'number_of_workers', 
            'payment_per_worker', 'job_description']
        
        widgets ={'Job_Title': forms.TextInput(attrs = {'class':'form-control'}),'district': forms.TextInput(attrs = {'class':'form-control'}),'place': forms.TextInput(attrs = {'class':'form-control'}),
                   'venue': forms.TextInput(attrs = {'class':'form-control'}),                   'venue': forms.TextInput(attrs = {'class':'form-control'}),'location_url': forms.TextInput(attrs = {'class':'form-control'}),'start_date': forms.DateInput(attrs={'type': 'date','class':'form-control'}),'end_date': forms.DateInput(attrs={'type': 'date','class':'form-control'}),
                'start_time': forms.TimeInput(attrs={'type': 'time','class':'form-control'}),'end_time': forms.TimeInput(attrs={'type': 'time','class':'form-control'}),
                'no.of workers': forms.NumberInput(attrs = {'class':'form-control'}),'payment_per_worker': forms.NumberInput(attrs = {'class':'form-control'}),'Job_description': forms.Textarea(attrs = {'class':'form-control'})}
    def save(self, commit=True):
        job_post = super().save(commit=False)
        if commit:
            job_post.save()
        return job_post
    
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.helper = FormHelper()
    
        self.helper.layout = Layout(
                    'job_Title', 'district', 'place', 'venue', 'location_url',
            Row(
                Column('start_date', css_class='form-group col-md-6'),
                Column('end_date', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('start_time', css_class='form-group col-md-6'),
                Column('end_time', css_class='form-group col-md-6'),
                css_class='form-row'
            ),          'number_of_workers','payment_per_worker', 'job_description',
            Submit('submit', 'Post Job', css_class='btn btn-primary'))

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['transaction_id']
        
