# Generated by Django 5.1.4 on 2024-12-23 18:33

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(blank=True, max_length=30, null=True)),
                ('name', models.CharField(default='Unnamed Member', max_length=100)),
                ('category', models.CharField(default='General', max_length=50)),
                ('college_name', models.CharField(default='Unknown College', max_length=200)),
                ('year', models.IntegerField(default=2024)),
                ('domain', models.CharField(default='General', max_length=100)),
                ('startup_id', models.CharField(blank=True, max_length=50, null=True)),
                ('ep1', models.CharField(blank=True, max_length=300, null=True)),
            ],
            options={
                'db_table': 'members',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_number', models.IntegerField()),
                ('category_name', models.CharField(max_length=255)),
                ('question', models.TextField()),
                ('option1', models.CharField(max_length=255)),
                ('efficiency_1', models.IntegerField()),
                ('description_1', models.TextField(blank=True, null=True)),
                ('option2', models.CharField(max_length=255)),
                ('efficiency_2', models.IntegerField()),
                ('description_2', models.TextField(blank=True, null=True)),
                ('option3', models.CharField(max_length=255)),
                ('efficiency_3', models.IntegerField()),
                ('description_3', models.TextField(blank=True, null=True)),
                ('option4', models.CharField(max_length=255)),
                ('efficiency_4', models.IntegerField()),
                ('description_4', models.TextField(blank=True, null=True)),
                ('correct_option', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'costcuttingquestions',
            },
        ),
        migrations.CreateModel(
            name='StudentReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=25)),
                ('title', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('strengths', models.JSONField()),
                ('weakness', models.JSONField()),
                ('opportunity', models.JSONField()),
                ('threat', models.JSONField()),
                ('improvements', models.JSONField(blank=True, null=True)),
                ('addons', models.JSONField(blank=True, null=True)),
            ],
            options={
                'db_table': 'swotanalysis',
            },
        ),
        migrations.CreateModel(
            name='TeamCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Team ID')),
                ('team_category', models.CharField(max_length=50, unique=True, verbose_name='Team Category')),
            ],
            options={
                'db_table': 'team_category',
            },
        ),
        migrations.CreateModel(
            name='Userauth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=13, unique=True)),
                ('username', models.CharField(max_length=85)),
                ('password', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'user_authenthication',
            },
        ),
    ]
