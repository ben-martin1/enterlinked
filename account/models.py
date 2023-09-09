from typing import Any
from django.db import models
from django.utils.translation import gettext_lazy


"""class Address(models.Model):
    street = models.CharField("Street", max_length=1024)
    city = models.CharField("City", max_length=1024)
    province = models.CharField("Province", max_length=1024)
    code = models.CharField("Zip", max_length=10)

    def get_address(self):
        return f"{self.street} {self.city}, {self._state} {self.code} "
"""

class User(models.Model):

    first_name = models.CharField(max_length=30,)
    last_name = models.CharField(max_length=30,)
    email_address = models.TextField(max_length=319,)

    """middle_name = models.CharField(max_length=30)
    country_code = models.CharField(max_length=4)
    area_code = models.CharField(max_length=4)
    phone_number = models.CharField(max_length=10)
    mailing_address = Address()
    date_of_birth = models.DateField()"""


    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    
class Languages(models.Model):
        # Languages spoken by user. Uses ISO 639-2/T conventions - need to consider creating a Languages.py and import it to cut back on lines here
        class Language_Choices(models.TextChoices):
            ABKHAZIAN = ("ABK", gettext_lazy("Abkhazian"))
            AFAR = ("AAR", gettext_lazy("Afar"))
            ENGLISH = ("ENG", gettext_lazy("English"))
            FRENCH = ("FRA", gettext_lazy("French"))
        
        class Proficiency_Choices(models.TextChoices):
            FLUENT = ("Fluent")
            CONVERSATIONAL = ("Conversational")
class Company(models.Model):
    company_name = models.TextField(max_length=250)
    dba_name = models.CharField(max_length=30, null=True)
    ein = models.CharField(max_length=10, null=True)
    
    def __str__(self) -> str:
        if self.dba_name == "":
            return self.company_name
        return f"{self.company_name}, doing business as {self.dba_name}"
    
class Talent(User):

    class Sag_Union_Status(models.TextChoices):
        UNION = "U", gettext_lazy("Union"),
        FICORE = "FI", gettext_lazy("Ficore"),
        MUST_JOIN = "MJ", gettext_lazy("Must Join"),
        TAFT_HARTLEY = "TH", gettext_lazy("Taft Hartley"),
        NON_UNION = "NU", gettext_lazy("Non Union")
    
    reps = models.ManyToManyField(Company)
    loanout = models.OneToOneField(Company, on_delete=models.SET_NULL, null=True, related_name="loanout")

    languages_spoken = models.CharField(
        max_length=3,
        choices=Languages.Language_Choices.choices, 
        default="ENG"
    )
    

    sag_id = models.IntegerField(null=True)
    
    #ssn = models.IntegerField()
    sag_union_status = models.CharField(
        max_length=2,
        choices = Sag_Union_Status.choices, 
        default="NU"
        )
    
    
    def get_union_status(self) -> Sag_Union_Status:
        # Get enum object for SAG union status
        return self.Sag_Union_Status[self.sag_union_status]
    
    
class Representative(User):
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
        null=True
    )
    def get_sag_union_status(self) -> Line_Of_Business:
        # returns the enum object for Line of Business
        return self.Line_Of_Business[self.line_of_business]
    employer = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)

class Casting(User):
    preferred_agencies = models.ManyToManyField(Company) 