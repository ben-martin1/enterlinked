from django.contrib import admin
from .models import User, Talent, Representative, Company, Casting

class TalentAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None, 
            {
                "fields": ["first_name", "last_name", "email_address","sag_id","sag_union_status", "languages_spoken", "reps"]
            },
        ),
    ]
admin.site.register(Talent, TalentAdmin)
admin.site.register(Representative)
admin.site.register(Company)
admin.site.register(Casting)