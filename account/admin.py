from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'location', 'birth_date', 'profile_picture']

admin.site.register(Profile, ProfileAdmin)
