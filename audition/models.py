from django.db import models
from account.models import User, Talent, Company, Casting 

class Project(models.Model):
    NON_UNION = "NU"
    NON_JURISDICTIONAL = "NJ"
    UNION = "U"
    UNION_STATUS_CHOICES = [
        (NON_UNION, "Non Union"),
        (NON_JURISDICTIONAL, "Non Jursidictional"),
        (UNION, "Union")
    ]

    FEATURE_ANIMATION = "FTR"
    TELEVISION_ANIMATION = "TVA"
    INTERACTIVE = "INT"
    DUBBING = "DUB"
    THEME_PARK = "THM"
    COMMERCIAL = "COM"
    AUDIOBOOK = "AUB"
    INDUSTRIAL = "IND"
    PROMO = "PMO"
    TRAILER = "TRL"
    NARRATION = "NAR"
    TOY = "TOY"
    LINE_OF_BUSINESS_CHOICES = [
        (FEATURE_ANIMATION, "Feature Animation"),
        (TELEVISION_ANIMATION,"Television Animation"),
        (INTERACTIVE, "Interactive"),
        (DUBBING, "Dubbing"),
        (THEME_PARK, "Theme Park"),
        (COMMERCIAL, "Commercial"),
        (AUDIOBOOK, "Audiobook"),
        (INDUSTRIAL, "Industrial"),
        (PROMO, "Promo"),
        (TRAILER, "Trailer"),
        (NARRATION, "Narrator"),
        (TOY, "Toy"),
    ]

    title = models.CharField(max_length=50)
    fka_name = models.CharField(max_length=50, null=True)
    code_name = models.CharField(max_length=50, null=True)
    slug = models.SlugField(max_length=20)
    casting_director = models.ForeignKey("account.Casting", on_delete=models.PROTECT)
    union_status = models.CharField(
        max_length=2,
        choices=UNION_STATUS_CHOICES,
        null=True
    )
    line_of_business = models.CharField(
        max_length=3,
        choices=LINE_OF_BUSINESS_CHOICES,
        null=True
    )

    def __str__(self) -> str:
        return self.title
   

class Role(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    CIS_MALE = "MAS"
    CIS_FEMALE = "FEM"
    NON_BINARY = "NBI"
    TRANSGENDER_FEMALE = "TFE"
    TRANSGENDER_MALE = "TMA"
    GENDER_NOT_LISTED = "GNL"
    GENDER_CHOICES = [
        (CIS_MALE, "Cis Male"),
        (CIS_FEMALE, "Cis Female"),
        (NON_BINARY, "Non-Binary"),
        (TRANSGENDER_FEMALE, "Transgender Female"),
        (TRANSGENDER_MALE, "Transgender Male"),
        (GENDER_NOT_LISTED, "Gender Not Listed"),
    ]

    STRAIGHT = "STR"
    GAY = "GAY"
    LESBIAN = "LES"
    BISEXUAL = "BIS"
    ORIENTATION_NOT_LISTED = "ONL" 
    SEXUAL_ORIENTATION_CHOICES = [
        (STRAIGHT, "STR"),
        (GAY, "GAY"),
        (LESBIAN, "LES"),
        (BISEXUAL, "BIS"),
        (ORIENTATION_NOT_LISTED , "ONL"),
    ]
    gender = models.CharField(
        max_length=3,
        choices=GENDER_CHOICES,
        null=True
    )

    sexual_orientation = models.CharField(
        max_length=3,
        choices=SEXUAL_ORIENTATION_CHOICES,
        null=True
    )

    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    age = models.IntegerField(null=True)
    name = models.CharField(max_length=25, default="enter name")

    def is_lgbt(self):
        if self.sexual_orientation in {self.GAY, self.LESBIAN, self.BISEXUAL, self.ORIENTATION_NOT_LISTED}:
            return True
        elif self.gender in {self.NON_BINARY, self.TRANSGENDER_FEMALE, self. TRANSGENDER_MALE, self.GENDER_NOT_LISTED}:
            return True
        return False
    def __str__(self) -> str:
        return self.name
    
    
class Breakdown(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    due_date = models.DateTimeField()
    role = models.ForeignKey(Role, null=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """if self.role.count > 2:
            title_role = f"{self.role.count} roles"
        else:
            title_role = self.role"""
        return f"{self.project} - {self.role} - {self.due_date}"
