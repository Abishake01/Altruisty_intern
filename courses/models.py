from django.db import models
from django.utils.translation import gettext_lazy as _


class Instructor(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('employed', 'Employed'),
        ('unemployed', 'Unemployed'),
        ('government', 'Government Worker'),
    ]
    
    BUSINESS_TYPE_CHOICES = [
        ('service', 'Service'),
        ('manufacturing', 'Manufacturing'),
    ]

    # Personal Information
    name = models.CharField(max_length=50)
    dob = models.DateField()
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    current_status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    pan_number = models.CharField(max_length=10, unique=True)
    aadhar_number = models.CharField(max_length=12, unique=True)
    epf_number = models.CharField(max_length=22, blank=True, null=True)

    # Social Media Links
    facebook_profile = models.CharField(max_length=200, blank=True, null=True)
    twitter_profile = models.CharField(max_length=200, blank=True, null=True)
    instagram_profile = models.CharField(max_length=200, blank=True, null=True)
    youtube_channel = models.CharField(max_length=200, blank=True, null=True)


    # About You Section
    about_you = models.TextField(blank=True, null=True)

    # Address Information
    house_no = models.CharField(max_length=100)
    area_street = models.CharField(max_length=100)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    country = models.CharField(max_length=25)
    pincode = models.CharField(max_length=6)

    # Business/Company Information
    business_name = models.CharField(max_length=100, blank=True, null=True)
    business_type = models.CharField(max_length=15, choices=BUSINESS_TYPE_CHOICES, blank=True, null=True)
    business_address = models.CharField(max_length=200, blank=True, null=True)
    product_name = models.CharField(max_length=100, blank=True, null=True)

    # Education Information
    institution_name = models.CharField(max_length=100)
    degree = models.CharField(max_length=50)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    passed_out_year = models.IntegerField()

    # Bank Information
    bank_name = models.CharField(max_length=100)
    branch_name = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=11)
    micr_code = models.CharField(max_length=9)
    account_number = models.CharField(max_length=18)

    # Upload Section (stored as binary data)
    profile_photo = models.BinaryField(blank=True, null=True)
    resume = models.BinaryField(blank=True, null=True)
    pan_card = models.BinaryField(blank=True, null=True)
    aadhar_card = models.BinaryField(blank=True, null=True)
    bank_passbook = models.BinaryField(blank=True, null=True)

    # Additional attributes
    attribute1 = models.CharField(max_length=100, blank=True, null=True)
    attribute2 = models.CharField(max_length=100, blank=True, null=True)
    attribute3 = models.CharField(max_length=100, blank=True, null=True)
    attribute4 = models.CharField(max_length=100, blank=True, null=True)
    attribute5 = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'instructorMaster'

    def __str__(self):
        return self.name



class Course(models.Model):
    course_id = models.CharField(max_length=10, unique=True, editable=False)
    course_title = models.CharField(max_length=100)
    skill_level = models.CharField(max_length=50, choices=[
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced')
    ])
    category = models.CharField(max_length=50, choices=[
        ('music', 'Music'),
        ('computer', 'Computer'),
        ('arts', 'Arts'),
        ('science', 'Science')
    ])
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    deadline = models.DateField()
    language = models.CharField(max_length=50, choices=[
        ('English', 'English'),
        ('Tamil', 'Tamil'),
        ('Telugu', 'Telugu'),
        ('Kannada', 'Kannada')
    ])
    short_description = models.TextField(max_length=300)
    about_course = models.TextField()
    what_we_learn = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Binary fields for images and video
    course_image_box = models.BinaryField(blank=True, null=True)
    course_image_list = models.BinaryField(blank=True, null=True)
    course_intro_video = models.BinaryField(blank=True, null=True)

    attribute1 = models.CharField(max_length=100, blank=True, null=True)
    attribute2 = models.CharField(max_length=100, blank=True, null=True)
    attribute3 = models.CharField(max_length=100, blank=True, null=True)
    attribute4 = models.CharField(max_length=100, blank=True, null=True)
    attribute5 = models.CharField(max_length=100, blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.course_id:  # Generate course_id only if it's not already set
            last_course = Course.objects.all().order_by('id').last()
            if last_course:
                # Increment the last course_id
                new_id = int(last_course.course_id) + 1
                self.course_id = f"{new_id:010d}"  # Format as 10 digits, zero-padded
            else:
                # If no courses exist, start with 0000000001
                self.course_id = "0000000001"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course_title} ({self.course_id})"

    class Meta:
        db_table = 'courses'

class LectureMaterial(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name="lecture_materials")
    lecture_name = models.CharField(max_length=100)
    lecture_duration = models.PositiveIntegerField(help_text=_("Duration in minutes"))

    intro_title = models.CharField(max_length=255)
    intro_video = models.BinaryField(blank=True, null=True)  # Storing intro videos as binary data
    intro_video_duration = models.PositiveIntegerField(help_text=_("Duration in minutes"))

    material_title = models.CharField(max_length=255)
    material_video = models.BinaryField(blank=True, null=True)  # Storing lecture videos as binary data
    video_duration = models.PositiveIntegerField(help_text=_("Duration in minutes"))

    task = models.TextField(blank=True, null=True)
    reading_material = models.BinaryField(blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)  # Automatically set on creation

    attribute1 = models.CharField(max_length=100, blank=True, null=True)
    attribute2 = models.CharField(max_length=100, blank=True, null=True)
    attribute3 = models.CharField(max_length=100, blank=True, null=True)
    attribute4 = models.CharField(max_length=100, blank=True, null=True)
    attribute5 = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.lecture_name} ({self.course.course_title})"

    class Meta:
        db_table = "lecture_materials"
