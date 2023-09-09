from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path("", views.account_index, name="account main"),
    # ex: /account/1/
    path("<int:user_id>/", views.account, name="account"),
    # ex: /account/company/
    path("company/", views.company_index, name="company index"),
    # /account/company/1/
    path("company/<int:company_id>/", views.company_detail, name="company detail"),
    # /account/talent/1/
    path("talent/<int:user_id>/", views.talent_detail, name="talent detail"),
    # /account/representative/1/
    path("representative/<int:user_id>/", views.representative_detail, name="representative detail"),

    # /account/test/
    path("test/<int:user_id>/", views.test, name="test")

]