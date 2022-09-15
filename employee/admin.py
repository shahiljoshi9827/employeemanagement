from django.contrib import admin

from employee.models import Employee, AddressDetails, Qualification, Projects, WorkExperience

# Register your models here.
admin.site.register(Employee)
admin.site.register(AddressDetails)
admin.site.register(Qualification)
admin.site.register(Projects)
admin.site.register(WorkExperience)