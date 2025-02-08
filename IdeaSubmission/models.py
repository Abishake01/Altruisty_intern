from django.db import models

class statementshowcasecategoryform(models.Model):
    statementcategory = models.CharField(max_length=250)

    def __str__(self):
        return self.statementcategory

    class Meta:
        db_table = 'dynamic_statement_showcase_category'

class statementshowcaseform(models.Model):
    statement_id = models.CharField(max_length=40)
    statement  = models.CharField(max_length=5000)
    statementcategory = models.CharField(max_length=250)
    at1 = models.CharField(max_length=250,null=True,blank=True)
    at2 = models.CharField(max_length=250,null=True,blank=True)
    at3 = models.CharField(max_length=250,null=True,blank=True)
    at4 = models.CharField(max_length=250,null=True,blank=True)
    at5 = models.CharField(max_length=250,null=True,blank=True)
    def __str__(self):
        return self.statement

    class Meta:
        db_table = 'dynamic_statemnt_showcase'


class IdeaSubmission(models.Model):
    # Basic Information
    idea_id = models.CharField(max_length=35,null=True,blank=True)
    statement_id = models.CharField(max_length=45,null=True,blank=True)
    user_id = models.CharField(max_length=45,null=True,blank=True)
    name_of_innovator = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=50)
    dob = models.DateField()
    highest_education_qualification = models.CharField(max_length=255)

    # Project Information
    title_of_project = models.CharField(max_length=255)
    name_of_product = models.CharField(max_length=255)
    description = models.TextField(default='')  # Default set to empty string
    uniqueness = models.TextField(default='')  # Default set to empty string
    innovation_type = models.CharField(
        max_length=50,
        choices=[('new', 'New'), ('upgrade', 'Upgrade')],
        default='new'
    )
    existing_product_upgrade = models.TextField(blank=True, null=True)

    # Additional Information
    need = models.TextField(default='')  # Default set to empty string
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    price_advantage = models.TextField(default='')  # Default set to empty string
    social_impact = models.TextField(default='')  # Default set to empty string

    # File Upload
    proposal_file = models.BinaryField()  # FileField to handle uploads

    # Optional Attributes
    problem_statement_id = models.IntegerField(blank=True, null=True)
    attribute1 = models.CharField(max_length=100, blank=True, null=True)
    attribute2 = models.CharField(max_length=100, blank=True, null=True)
    attribute3 = models.CharField(max_length=100, blank=True, null=True)
    attribute4 = models.CharField(max_length=100, blank=True, null=True)
    attribute5 = models.CharField(max_length=100, blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_of_project

    class Meta:
        db_table = 'ideasubmissions'
