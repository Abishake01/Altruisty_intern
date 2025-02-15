# Generated by Django 5.1.4 on 2025-01-05 04:34

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0002_startup_individual_score_startupscore'),
    ]

    operations = [
        migrations.CreateModel(
            name='CostCuttingCategoryMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categroy_name', models.CharField(default='General Category', max_length=50)),
                ('category_image', models.BinaryField(blank=True, null=True)),
            ],
            options={
                'db_table': 'costcuttingcategorymaster',
            },
        ),
        migrations.AlterField(
            model_name='startup_individual_score',
            name='attribute1',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
