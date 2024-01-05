from typing import Any
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager

from datetime import datetime
import audition.models 

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
    def get_by_natural_key(self, email):
        return self.get(email=email)

class Company(models.Model):
    company_name = models.CharField(max_length=75)
    dba_name = models.CharField(max_length=30, blank=True, null=True)
    ein = models.CharField(max_length=10, blank=True, null=True)
    
    def __str__(self) -> str:
        if self.dba_name == "":
            return self.company_name
        return f"{self.company_name}, doing business as {self.dba_name}"
    
    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        
class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    profile_picture = models.ImageField(null=True, blank=True, upload_to="profile_pictures/")
    EMAIL_FIELD = "email"

    is_talent = models.BooleanField(default=False)
    is_representative = models.BooleanField(default=False)
    is_casting = models.BooleanField(default=False)
    is_production = models.BooleanField(default=False)
    
    REQUIRED_FIELDS = []
    first_name = models.CharField(max_length=255,)
    last_name = models.CharField(max_length=255,)
    date_joined = models.DateTimeField(default=timezone.now)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
   
    date_of_birth = models.DateField(null=True, blank=True)

    #TALENT Fields
    user_agency = models.ForeignKey(Company, on_delete=models.PROTECT, null=True, blank=True, related_name="user_agency")
    sag_id_number = models.CharField(blank=True, null=True, max_length = 13)

    #REPRESENTATIVE Fields
    class Line_Of_Business(models.TextChoices):
        VOICEOVER = "VO", gettext_lazy("VO")
        THEATRICAL = "TH", gettext_lazy("TH")
        ON_CAMERA_COMMERCIAL = "OCC", gettext_lazy("OCC")
        EQUITY = "EQY", gettext_lazy("EQY")
        APPEARANCES = "APP", gettext_lazy("APP")
        ACROSS_THE_BOARD = "ATB", gettext_lazy("ATB")

    line_of_business = models.CharField(
        max_length = 3,
        choices = Line_Of_Business.choices,
        null = True,
        blank = True
    )
    employer = models.ForeignKey(Company, on_delete=models.PROTECT, null=True)

    def get_age(self):
       return int((datetime.now().date() - self.date_of_birth).days / 365.25)
    
    def __str__(self) -> str:
        return self.email
    
    def set_profile_picture(self):
        """Sets the default profile picture if none is found, otherwise uses uploaded image."""
        _pic = self.profile_picture
        if not _pic:
            self.profile_picture="static/images/default_profile_picture.png"

    class Meta:
        verbose_name="User"
        verbose_name_plural = "Users"