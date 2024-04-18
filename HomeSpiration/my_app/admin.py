from django.contrib import admin
from .models import Professional, ProfessionalDetails , NormalUser

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import User

admin.site.register(Professional)
admin.site.register(ProfessionalDetails)
admin.site.register(NormalUser)
admin.site.register(User, UserAdmin)