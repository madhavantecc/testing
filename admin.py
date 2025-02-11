from django.contrib import admin
from .models import JobSeeker, JobProvider, JobPost,CustomUser

# Register your models here.
admin.site.register(JobSeeker)
admin.site.register(JobPost)
admin.site.register(JobProvider)
admin.site.register(CustomUser)


# class JobProviderAdmin(admin.ModelAdmin):
#     list_display = ['name', 'email', 'phone', 'approved']
#     list_filter = ['approved']  # Filter by approval status
#     actions = ['approve_job_provider']

#     def approve_job_provider(self, request, queryset):
#         queryset.update(approved=True)
#         self.message_user(request, "Selected job providers have been approved.")

#     approve_job_provider.short_description = "Approve selected job poviders"