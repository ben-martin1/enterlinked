from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Company
from datetime import date

User = get_user_model()

class UserSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "is_talent", "is_representative", "is_casting", "is_production", "password1", "password2")
        widgets = {"password":forms.HiddenInput}
        labels = {"is_talent":"Talent", "is_representative":"Representative", "is_casting":"Casting Professional", "is_production":"Production Professional"}

class UserSignInForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password")
        widgets = {"password":forms.HiddenInput}

class UserUpdateInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "date_of_birth",  "is_talent", "is_representative", "is_casting", "is_production", "profile_picture")
        current_year = date.today().year
        applicable_years = [x for x in range(current_year-100, current_year+1)]
        widgets = {"password":forms.HiddenInput,
                   "date_of_birth":forms.SelectDateWidget(years=applicable_years)}
        labels = {"is_talent":"Talent", "is_representative":"Representative", "is_casting":"Casting Professional", "is_production":"Production Professional"}

class TalentUpdateInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("sag_id_number",)

class RepresentativeUpdateInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("line_of_business",)

class CompanyCreationForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ("company_name", "dba_name", "ein")
        labels = {"dba_name":"Doing Business as",
                  "ein":"EIN",}