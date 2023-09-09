from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from . models import User, Talent, Company, Representative

def account_index(request):
    talent_list = Talent.objects.order_by("id")
    representative_list = Representative.objects.order_by("id") 
    company_list = Company.objects.order_by("id")
    context = {
            "talent_list":talent_list,
            "representative_list":representative_list,
            "company_list":company_list,
                }
    return render(request,"account/index.html", context)

def talent_detail(request, user_id):
    user = Talent.objects.get(pk=user_id)
    context = {"user":user}
    return render(request, "account/talent/detail.html", context)

def account(request, user_id):
    user = Talent.objects.get(pk=user_id)
    if isinstance(user, Talent):
        return HttpResponse(f"Talent, {user.first_name}")
    return HttpResponse(f"You're looking at {user}'s page.")

def company_index(request):
    company_list = Company.objects.all()
    context = {"company_list":company_list}
    return render(request, "account/company/index.html", context)

def company_detail(request, company_id):
    employees = Representative.objects.filter(employer_id=company_id)
    client_list = Talent.objects.filter(reps=company_id)
    context = {"employee_list":employees,
               "client_list":client_list}
    return render(request, "account/company/detail.html", context)

def representative_detail(request, user_id):
    representative = Representative.objects.get(pk=user_id)
    context={"representative" : representative}
    return render(request, "account/representative/detail.html", context)

def test(request, user_id):
    user = User.objects.get(pk=user_id)
    try:
        talent = Talent.objects.get(pk=user_id)
    except Talent.DoesNotExist:
        talent = None
    else:
        return HttpResponse(f"Talent + {user.class_type}")
    try:
        rep = Representative.objects.get(pk=user_id)
    except Representative.DoesNotExist:
        rep = None
    else:
        return HttpResponse(f"Rep+ {user.class_type}")
    try:
        company = Company.objects.get(pk=user_id)
    except Company.DoesNotExist:
        company = None
    else:
        return HttpResponse(f"Company+ {user.class_type}")