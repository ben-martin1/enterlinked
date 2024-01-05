from django.shortcuts import render, redirect, reverse
from .forms import UserSignUpForm, UserSignInForm, UserUpdateInfoForm, TalentUpdateInfoForm, RepresentativeUpdateInfoForm, CompanyCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect

import audition.models
from . models import User, Company

User = get_user_model()

def sign_in_view(request):
    form=UserSignInForm()
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password1")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            update_form = UserUpdateInfoForm(instance=request.user)
            context = {"update_form":update_form}
            url = reverse("account:account_detail", args=[user.pk])
            return redirect(url, context)
    context = {"form":form}
    return render(request, "account/registration/login.html", context)

def log_out_user(request):
    logout(request)
    return redirect("login")

def sign_up_view(request):
    form=UserSignUpForm(request.POST)
    if request.method=="POST":
        if form.is_valid():
            form.save()
            messages.success(request, f"Account was created for {form.cleaned_data.get('first_name')}.")
            return redirect("login")

    context = {"form":form}
    return render(request, "account/registration/signup.html", context)
    
def home_page(request):
    if request.user.is_authenticated:
        form = UserUpdateInfoForm(initial={"first_name":request.user.first_name, 
                                           "last_name":request.user.last_name,
                                           "email":request.user.email,
                                           "role":request.user.role})
        context = {"form":form}
        return render(request, "../home.html", context)
    else:
        return render(request, sign_in_view)


def account_index(request):
    if request.user.is_authenticated == False:
        return redirect("login")
    talent_list = User.objects.filter(is_talent=True)
    representative_list = User.objects.filter(is_representative=True)
    casting_list = User.objects.filter(is_casting=True)
    company_list = Company.objects.order_by("id")
    context = {
            "talent_list":talent_list,
            "representative_list":representative_list,
            "casting_list":casting_list,
            "company_list":company_list,
                }
    return render(request,"account/index.html", context)

def account_detail(request, user_id):
    if request.user.is_authenticated == False:
        return redirect("login")
    user = User.objects.get(pk=user_id)
    base_update_form = UserUpdateInfoForm(initial={"first_name":request.user.first_name, 
                                           "last_name":request.user.last_name,
                                           "date_of_birth":request.user.date_of_birth,
                                           "is_talent":request.user.is_talent,
                                           "is_representative":request.user.is_representative,
                                           "is_casting":request.user.is_casting,
                                           "is_production":request.user.is_production,
                                           "profile_picture":request.user.profile_picture})
    talent_update_form = TalentUpdateInfoForm(initial={"sag_id_number":user.sag_id_number})
    representative_update_form = RepresentativeUpdateInfoForm()
    print(base_update_form.errors)
    print(talent_update_form.errors)
    if request.method == "POST":
        bound_base_update_form = UserUpdateInfoForm(request.POST)
        bound_talent_update_form = TalentUpdateInfoForm(request.POST)
        if bound_base_update_form.is_valid():
            print(request.POST)
            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")
            user.date_of_birth = request.POST.get("date_of_birth")
            user.sag_id_number = request.POST.get("sag_id_number")
            user.is_talent = (request.POST.get("is_talent") == "on")
            user.is_representative = (request.POST.get("is_representative") == "on")
            user.is_casting = (request.POST.get("is_casting") == "on")
            user.is_production = (request.POST.get("is_production") == "on")
            user.profile_picture = request.FILES.get("profile_picture")
            user.save()
        if bound_talent_update_form.is_valid():
            user.sag_id_number = request.POST.get("sag_id_number")
            user.save()
        return HttpResponseRedirect("")
    try:
        user_company = Company.objects.get(pk=user.employer_id)
    except Company.DoesNotExist:
        user_company = None
    context = {"user":user,
               "user_company":user_company,
               "base_update_form":base_update_form,
               "talent_update_form":talent_update_form,
               "representative_update_form":representative_update_form,}
    return render(request, "account/detail.html", context)

def company_detail(request, company_id):
    company = Company.objects.get(pk=company_id)
    if request.user.is_authenticated == False:
        return redirect("login")
    if request.method == "POST":
        print(request.POST)
        post_val_rep = request.POST.get("Representative", None)
        post_val_talent = request.POST.get("Talent", None)
        if post_val_rep == "Enterlink":
            print("Representative Enterlink.")
            request.user.employer=Company.objects.get(pk=company_id)
            request.user.save()
        elif post_val_rep == "Breaklink":
            print("Representative Breaklink.")
            request.user.employer = None
            request.user.save()
        elif post_val_talent == "Enterlink":
            print("joining agency.")
            request.user.user_agency = company
            request.user.save()
        elif post_val_talent == "Breaklink":
            print("Dropping agency.")
            request.user.user_agency = None
            request.user.save() 
    employees = User.objects.filter(employer_id=company_id)
    client_list = User.objects.filter(user_agency=company_id)
    context = {"employee_list":employees,
               "client_list":client_list,
               "company":company,}
    return render(request, "account/company/detail.html", context)

def register_company(request):
    form = CompanyCreationForm(request.POST)
    if request.method == "POST":
        print(form.errors)
        if form.is_valid():
            new_company = Company.objects.create()
            new_company.company_name = request.POST.get("company_name")
            new_company.dba_name = request.POST.get("dba_name")
            new_company.ein = request.POST.get("ein")
            new_company.save()
            context = {"new_company":new_company}
            return render(request, "account/company/register.html", context)
    context = {"form":form,}
    return render(request, "account/company/register.html", context)