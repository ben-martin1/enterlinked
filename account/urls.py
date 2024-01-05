from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    path("", views.account_index, name="account_index"),
    # path account/login/
    path("login/", views.sign_in_view, name="login"),
    # path account/logout/
    path('logout/', views.log_out_user, name="logout"),
    #path account/register/
    path("register/", views.sign_up_view, name="sign_up"),
    # path home/
    path("home/", views.home_page, name="home"),
    # ex: /account/1/
    path("<int:user_id>/", views.account_detail, name="account_detail"),
    # /account/company/1/
    path("company/<int:company_id>/", views.company_detail, name="company_detail"),
    # ex: /account/registercompany/
    path("company/register/", views.register_company, name="register_company")
]