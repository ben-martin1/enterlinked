from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import User, Company

class TalentAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None, 
            {
                "fields": ["first_name", "last_name", "email_address","sag_id","sag_union_status", "languages_spoken", "reps", "date_of_birth"]
            },
        ),
    ]

admin.site.register(Company)
admin.site.register(User)