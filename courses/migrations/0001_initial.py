# Generated by Django 5.1.4 on 2024-12-31 15:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('dob', models.DateField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=6)),
                ('phone_number', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=50)),
                ('current_status', models.CharField(choices=[('employed', 'Employed'), ('unemployed', 'Unemployed'), ('government', 'Government Worker')], max_length=15)),
                ('pan_number', models.CharField(max_length=10, unique=True)),
                ('aadhar_number', models.CharField(max_length=12, unique=True)),
                ('epf_number', models.CharField(blank=True, max_length=22, null=True)),
                ('facebook_profile', models.CharField(blank=True, max_length=200, null=True)),
                ('twitter_profile', models.CharField(blank=True, max_length=200, null=True)),
                ('instagram_profile', models.CharField(blank=True, max_length=200, null=True)),
                ('youtube_channel', models.CharField(blank=True, max_length=200, null=True)),
                ('about_you', models.TextField(blank=True, null=True)),
                ('house_no', models.CharField(max_length=100)),
                ('area_street', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=25)),
                ('state', models.CharField(max_length=25)),
                ('country', models.CharField(max_length=25)),
                ('pincode', models.CharField(max_length=6)),
                ('business_name', models.CharField(blank=True, max_length=100, null=True)),
                ('business_type', models.CharField(blank=True, choices=[('service', 'Service'), ('manufacturing', 'Manufacturing')], max_length=15, null=True)),
                ('business_address', models.CharField(blank=True, max_length=200, null=True)),
                ('product_name', models.CharField(blank=True, max_length=100, null=True)),
                ('institution_name', models.CharField(max_length=100)),
                ('degree', models.CharField(max_length=50)),
                ('percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('passed_out_year', models.IntegerField()),
                ('bank_name', models.CharField(max_length=100)),
                ('branch_name', models.CharField(max_length=100)),
                ('ifsc_code', models.CharField(max_length=11)),
                ('micr_code', models.CharField(max_length=9)),
                ('account_number', models.CharField(max_length=18)),
                ('profile_photo', models.BinaryField(blank=True, null=True)),
                ('resume', models.BinaryField(blank=True, null=True)),
                ('pan_card', models.BinaryField(blank=True, null=True)),
                ('aadhar_card', models.BinaryField(blank=True, null=True)),
                ('bank_passbook', models.BinaryField(blank=True, null=True)),
                ('attribute1', models.CharField(blank=True, max_length=100, null=True)),
                ('attribute2', models.CharField(blank=True, max_length=100, null=True)),
                ('attribute3', models.CharField(blank=True, max_length=100, null=True)),
                ('attribute4', models.CharField(blank=True, max_length=100, null=True)),
                ('attribute5', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'instructorMaster',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(editable=False, max_length=10, unique=True)),
                ('course_title', models.CharField(max_length=100)),
                ('skill_level', models.CharField(choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], max_length=50)),
                ('category', models.CharField(choices=[('music', 'Music'), ('computer', 'Computer'), ('arts', 'Arts'), ('science', 'Science')], max_length=50)),
                ('deadline', models.DateField()),
                ('language', models.CharField(choices=[('English', 'English'), ('Tamil', 'Tamil'), ('Telugu', 'Telugu'), ('Kannada', 'Kannada')], max_length=50)),
                ('short_description', models.TextField(max_length=300)),
                ('about_course', models.TextField()),
                ('what_we_learn', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('course_image_box', models.BinaryField(blank=True, null=True)),
                ('course_image_list', models.BinaryField(blank=True, null=True)),
                ('course_intro_video', models.BinaryField(blank=True, null=True)),
                ('attribute1', models.CharField(blank=True, max_length=100, null=True)),
                ('attribute2', models.CharField(blank=True, max_length=100, null=True)),
                ('attribute3', models.CharField(blank=True, max_length=100, null=True)),
                ('attribute4', models.CharField(blank=True, max_length=100, null=True)),
                ('attribute5', models.CharField(blank=True, max_length=100, null=True)),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.instructor')),
            ],
            options={
                'db_table': 'courses',
            },
        ),
        migrations.CreateModel(
            name='LectureMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lecture_name', models.CharField(max_length=100)),
                ('lecture_duration', models.PositiveIntegerField(help_text='Duration in minutes')),
                ('intro_title', models.CharField(max_length=255)),
                ('intro_video', models.BinaryField(blank=True, null=True)),
                ('intro_video_duration', models.PositiveIntegerField(help_text='Duration in minutes')),
                ('material_title', models.CharField(max_length=255)),
                ('material_video', models.BinaryField(blank=True, null=True)),
                ('video_duration', models.PositiveIntegerField(help_text='Duration in minutes')),
                ('task', models.TextField(blank=True, null=True)),
                ('reading_material', models.BinaryField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('attribute1', models.CharField(blank=True, max_length=100, null=True)),
                ('attribute2', models.CharField(blank=True, max_length=100, null=True)),
                ('attribute3', models.CharField(blank=True, max_length=100, null=True)),
                ('attribute4', models.CharField(blank=True, max_length=100, null=True)),
                ('attribute5', models.CharField(blank=True, max_length=100, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lecture_materials', to='courses.course')),
            ],
            options={
                'db_table': 'lecture_materials',
            },
        ),
    ]
