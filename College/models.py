from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class collegeRegistartion(models.Model):
    user_id=models.CharField(max_length=30,null=True,blank=True)
    Name = models.CharField(max_length=50)
    contact_email = models.CharField(max_length=50)
    contact_phonenumber = models.CharField(max_length=15)
    College_name = models.CharField(max_length=50)
    Address_line_1 = models.CharField(max_length=30)
    Area = models.CharField(max_length=15)
    city = models.CharField(max_length=15)
    state = models.CharField(max_length=15)
    zipcode = models.CharField(max_length=6)
    status = models.CharField(max_length=300,null=True,blank=True)
    ep1 = models.CharField(max_length=300,null=True,blank=True)
    ep2 = models.CharField(max_length=300,null=True,blank=True)
    ep3 = models.CharField(max_length=300,null=True,blank=True)
    ep4 = models.CharField(max_length=300,null=True,blank=True)
    ep5 = models.CharField(max_length=300,null=True,blank=True)
    
    

    def __str__(self):
        return self.Name

    class Meta:
        db_table = 'College_Registartion'  # Specify custom table name here

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
    ep2 = models.CharField(max_length=300,null=True,blank=True)
    ep3 = models.CharField(max_length=300,null=True,blank=True)
    ep4 = models.CharField(max_length=300,null=True,blank=True)
    ep5 = models.CharField(max_length=300,null=True,blank=True)
    
    

    def __str__(self):
        return self.student_Name

    class Meta:
        db_table = 'intern_registartion'  # Specify custom table name here
       
class Banner(models.Model):
    banner1 = models.BinaryField(null=True, blank=True)
    banner2 = models.BinaryField(null=True, blank=True)
    banner3 = models.BinaryField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'collegebanner'
        managed = False  # Important: tells Django not to manage this table

    def __str__(self):
        return f"Banner {self.id} - {self.uploaded_at}"

class HomeImage(models.Model):
    college_home = models.BinaryField(null=True, blank=True)
    intern_home = models.BinaryField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'homeimage'

    def __str__(self):
        return f"HomeImage {self.id} - {self.uploaded_at}"
    
class Events_update(models.Model):
    
    events = models.BinaryField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'eventsimage'

    def __str__(self):
        return f"Events_update {self.id} - {self.uploaded_at}"
#abi-123