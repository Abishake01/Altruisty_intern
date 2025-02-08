from django.db import models

import uuid
class CostCuttingCategoryMaster(models.Model):
    categroy_name = models.CharField(max_length=50, default='General Category')  # Default category name
    category_image = models.BinaryField(blank=True, null=True)  # Optional field

    def __str__(self):
        return self.categroy_name

    class Meta:
        db_table = 'costcuttingcategorymaster'
class Question(models.Model):
    question_number = models.IntegerField()
    category_name = models.CharField(max_length=255)  # Category name for the question
    question = models.TextField()  # The question text
    option1 = models.CharField(max_length=255)  # First option
    efficiency_1 = models.IntegerField()  # Efficiency percentage for the first option
    description_1 = models.TextField(null=True, blank=True)
    option2 = models.CharField(max_length=255)  # Second option
    efficiency_2 = models.IntegerField()  # Efficiency percentage for the second option
    description_2 = models.TextField(null=True, blank=True)
    option3 = models.CharField(max_length=255)  # Third option
    efficiency_3 = models.IntegerField()  # Efficiency percentage for the third option
    description_3 = models.TextField(null=True, blank=True)
    option4 = models.CharField(max_length=255)  # Fourth option
    efficiency_4 = models.IntegerField()  # Efficiency percentage for the fourth option
    description_4 = models.TextField(null=True, blank=True)
    correct_option = models.CharField(max_length=255)  # Correct answer (matching one of the options)

    def _str_(self):
        return f"Question {self.question_number}: {self.question[:50]}..."  # Truncated question for readability
    class Meta:
        db_table = 'costcuttingquestions'

class Member(models.Model):
    user_id=models.CharField(max_length=30,null=True,blank=True)
    name = models.CharField(max_length=100, default="Unnamed Member")  # Default name
    category = models.CharField(max_length=50, default="General")  # Default category
    college_name = models.CharField(max_length=200, default="Unknown College")  # Default college name
    year = models.IntegerField(default=2024)  # Default year
    domain = models.CharField(max_length=100, default="General")  # Default domain
    startup_id = models.CharField(max_length=50, null=True, blank=True)  # No default for optional startup_id
    
    ep1 = models.CharField(max_length=300,null=True,blank=True)



    class Meta:
        db_table = 'members'


class StudentReport(models.Model):
    student_id = models.CharField(max_length=25)
    title = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    strengths = models.JSONField()
    weakness = models.JSONField()
    opportunity = models.JSONField()
    threat = models.JSONField()
    improvements = models.JSONField(null=True, blank=True)
    addons = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'swotanalysis'  # Specify custom table name here

class Userauth(models.Model):
    user_id = models.CharField(unique=True,max_length=13)
    username = models.CharField(max_length=85)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.user_id

    class Meta:
        db_table = 'user_authenthication'

class TeamCategory(models.Model):
    team_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="Team ID")
    team_category = models.CharField(max_length=50, unique=True, verbose_name="Team Category")

    def _str_(self):
        return self.team_category

    class Meta:
        db_table = 'team_category'

class Question(models.Model):
    question_number = models.IntegerField()
    category_name = models.CharField(max_length=255)  # Category name for the question
    question = models.TextField()  # The question text
    option1 = models.CharField(max_length=255)  # First option
    efficiency_1 = models.IntegerField()  # Efficiency percentage for the first option
    description_1 = models.TextField(null=True, blank=True)
    option2 = models.CharField(max_length=255)  # Second option
    efficiency_2 = models.IntegerField()  # Efficiency percentage for the second option
    description_2 = models.TextField(null=True, blank=True)
    option3 = models.CharField(max_length=255)  # Third option
    efficiency_3 = models.IntegerField()  # Efficiency percentage for the third option
    description_3 = models.TextField(null=True, blank=True)
    option4 = models.CharField(max_length=255)  # Fourth option
    efficiency_4 = models.IntegerField()  # Efficiency percentage for the fourth option
    description_4 = models.TextField(null=True, blank=True)
    correct_option = models.CharField(max_length=255)  # Correct answer (matching one of the options)

    def __str__(self):
        return f"Question {self.question_number}: {self.question[:50]}..."  # Truncated question for readability
    class Meta:
        db_table = 'costcuttingquestions'


class startupscore(models.Model):
    startup_id = models.TextField(null=True,blank = True)
    game_name = models.TextField(null=True,blank = True)
    score = models.TextField(null=True,blank = True)
    category = models.TextField(null=True,blank = True)
    attribute1 = models.TextField(null=True,blank = True)
    attribute2 = models.TextField(null=True,blank = True)
    attribute3 = models.TextField(null=True,blank = True)
    attribute4 = models.TextField(null=True,blank = True)
    attribute5 = models.TextField(null=True,blank = True)
    attribute6 = models.TextField(null=True,blank = True)
    attribute7 = models.TextField(null=True,blank = True)
    attribute8 = models.TextField(null=True,blank = True)
    attribute9 = models.TextField(null=True,blank = True)
    attribute10 = models.TextField(null=True,blank = True)
    attribute11 = models.TextField(null=True,blank = True)
    attribute12 = models.TextField(null=True,blank = True)

    def __str__(self):
        return f"{self.startup_id}:{self.game_name}"

    class Meta:
        db_table = 'startup_game_score'


class startup_individual_score(models.Model):
    user_id = models.TextField(null=True,blank = True)
    startup_id = models.TextField(null=True,blank = True)
    game_name = models.TextField(null=True,blank = True)
    score = models.TextField(null=True,blank = True)
    category = models.TextField(null=True,blank = True)
    attribute1 =models.DateTimeField(auto_now_add=True)
    attribute2 = models.TextField(null=True,blank = True)
    attribute3 = models.TextField(null=True,blank = True)
    attribute4 = models.TextField(null=True,blank = True)
    attribute5 = models.TextField(null=True,blank = True)
    attribute6 = models.TextField(null=True,blank = True)
    attribute7 = models.TextField(null=True,blank = True)
    attribute8 = models.TextField(null=True,blank = True)
    attribute9 = models.TextField(null=True,blank = True)
    attribute10 = models.TextField(null=True,blank = True)
    attribute11 = models.TextField(null=True,blank = True)
    attribute12 = models.TextField(null=True,blank = True)

    def __str__(self):
        return f"{self.user_id}:{self.game_name}"

    class Meta:
        db_table = 'individual_startup_game_score'


class StartupRegistartion(models.Model):
    
    user_id=models.CharField(max_length=30,null=True,blank=True)
    startup_Name = models.CharField(max_length=30)
    founder_Name = models.CharField(max_length=50)
    founded_date = models.CharField(max_length=20)
    contact_email = models.CharField(max_length=50)
    contact_phonenumber = models.CharField(max_length=15)
    sector = models.CharField(max_length=30)
    company_stage = models.CharField(max_length=30)
    employee_count = models.CharField(max_length=10)
    Funding_Received = models.CharField(max_length=30)
    Key_technology = models.CharField(max_length=50)
    Address_line_1 = models.CharField(max_length=30)
    Area = models.CharField(max_length=15)
    city = models.CharField(max_length=15)
    state = models.CharField(max_length=15)
    zipcode = models.CharField(max_length=6)
    Focus_area = models.CharField(max_length=25)
    Funding_duration = models.CharField(max_length=15)
    Linkedin_link = models.CharField(max_length=100)
    Github_link = models.CharField(max_length=100)
    Pitch_deck_link = models.CharField(max_length=100)
    reason = models.CharField(max_length=300)
    status = models.CharField(max_length=300,null=True,blank=True)
    ep1 = models.CharField(max_length=300,null=True,blank=True)
    ep2 = models.CharField(max_length=300,null=True,blank=True)
    ep3 = models.CharField(max_length=300,null=True,blank=True)
    ep4 = models.CharField(max_length=300,null=True,blank=True)
    ep5 = models.CharField(max_length=300,null=True,blank=True)

    def __str__(self):
        return self.startup_Name

    class Meta:
        db_table = 'Startup_Registartion' 


class banneruploadstartup(models.Model):
    banner1 = models.BinaryField(null=True, blank=True)
    banner2= models.BinaryField(null=True, blank=True)
    banner3 = models.BinaryField(null=True, blank=True)
    

    def __str__(self):
        return self.id
    class Meta:
        db_table = 'startupbanner'


