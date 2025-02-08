from django.db import models

# Create your models here.
def default_json():
    return {"internship_history": []}
def default_json2():
    return {"intern_project": []}
class InternRegistartion(models.Model):
    user_id=models.CharField(max_length=30,null=True,blank=True)
    student_Name = models.CharField(max_length=50)
    age = models.CharField(max_length=20)
    student_dob = models.CharField(max_length=30)
    contact_email = models.CharField(max_length=50)
    contact_phonenumber = models.CharField(max_length=15)
    College_name= models.CharField(max_length=50)
    Department= models.CharField(max_length=30)
    Current_year = models.CharField(max_length=25,null=True,blank=True)
    Year_of_graduation = models.CharField(max_length=5,null=True,blank=True)
    student_skills = models.CharField(max_length=50)
    Address_line_1 = models.CharField(max_length=30)
    Area = models.CharField(max_length=15)
    city = models.CharField(max_length=15)
    state = models.CharField(max_length=15)
    zipcode = models.CharField(max_length=6)
    domain = models.CharField(max_length=25)
    duration = models.CharField(max_length=25)
    Linkedin_link = models.CharField(max_length=100)
    Github_link = models.CharField(max_length=100)
    Resume_link = models.CharField(max_length=100)
    reason = models.CharField(max_length=300)
    status = models.CharField(max_length=300,null=True,blank=True)
    ep1 = models.CharField(max_length=300,null=True,blank=True)
    ep2 = models.JSONField()
    ep3 = models.JSONField()
    ep4 = models.CharField(max_length=300,null=True,blank=True)
    ep5 = models.CharField(max_length=300,null=True,blank=True)
    
    

    def __str__(self):
        return self.student_Name

    class Meta:
        db_table = 'intern_Registartion'  # Specify custom table name here


class dailyquestion(models.Model):
    question_id = models.CharField(max_length=35,null=True,blank=True)
    question = models.CharField(max_length=250,null=True,blank=True)
    sample_input = models.CharField(max_length=250,null=True,blank=True)
    sample_output = models.CharField(max_length=250,null=True,blank=True)
    actual_output = models.CharField(max_length=250,null=True,blank=True)
    posted_on = models.CharField(max_length=35,null=True,blank=True)
    def __str__(self):
        return self.question_id
    class Meta:
        db_table = 'Daily_challenge_questions'

class dailyquestionanswer(models.Model):
    question_gid = models.CharField(max_length=35,null=True,blank=True)
    user_id = models.CharField(max_length=35,null=True,blank=True)
    submitted_on = models.DateTimeField(auto_created=True)
    token = models.CharField(max_length=35,null=True,blank=True)

    def __str__(self):
        return self.question_gid
    class Meta:
        db_table = 'Daily_challenge_answers_submitted'

class weeklyquestion(models.Model):
    question_id = models.CharField(max_length=35,null=True,blank=True)
    question = models.CharField(max_length=250,null=True,blank=True)
    sample_input = models.CharField(max_length=250,null=True,blank=True)
    sample_output = models.CharField(max_length=250,null=True,blank=True)
    actual_output = models.CharField(max_length=250,null=True,blank=True)
    posted_on = models.CharField(max_length=35,null=True,blank=True)
    def __str__(self):
        return self.question_id
    class Meta:
        db_table = 'weekly_challenge_questions'

class weeklyquestionanswer(models.Model):
    question_gid = models.CharField(max_length=35,null=True,blank=True)
    user_id = models.CharField(max_length=35,null=True,blank=True)
    submitted_on = models.DateTimeField(auto_created=True)
    token = models.CharField(max_length=35,null=True,blank=True)

    def __str__(self):
        return self.question_gid
    class Meta:
        db_table = 'weekly_challenge_answers_submitted'

class commonquestion(models.Model):
    question_id = models.CharField(max_length=35,null=True,blank=True)
    question = models.CharField(max_length=250,null=True,blank=True)
    sample_input = models.CharField(max_length=250,null=True,blank=True)
    sample_output = models.CharField(max_length=250,null=True,blank=True)
    actual_output = models.CharField(max_length=250,null=True,blank=True)
    posted_on = models.CharField(max_length=35,null=True,blank=True)
    def __str__(self):
        return self.question_id
    class Meta:
        db_table = 'common_challenge_questions'

class commonquestionanswer(models.Model):
    question_gid = models.CharField(max_length=35,null=True,blank=True)
    user_id = models.CharField(max_length=35,null=True,blank=True)
    submitted_on = models.DateTimeField(auto_created=True)
    token = models.CharField(max_length=35,null=True,blank=True)

    def __str__(self):
        return self.question_gid
    class Meta:
        db_table = 'common_challenge_answers_submitted'



class bannerupload(models.Model):
    banner1 = models.FileField(upload_to='banner/', null=True, blank=True)
    banner2= models.FileField(upload_to='banner/', null=True, blank=True)
    banner3 = models.FileField(upload_to='banner/', null=True, blank=True)
    

    def __str__(self):
        return self.id
    class Meta:
        db_table = 'internbanner'



class InternTeams(models.Model):
    team_id = models.AutoField(primary_key=True)
    member1 = models.CharField(max_length=45, null=True, blank=True)
    member2 = models.CharField(max_length=45, null=True, blank=True)
    member3 = models.CharField(max_length=45, null=True, blank=True)
    member4 = models.CharField(max_length=45, null=True, blank=True)
    member5 = models.CharField(max_length=45, null=True, blank=True)



    class Meta:
        db_table = 'intern_teams'













