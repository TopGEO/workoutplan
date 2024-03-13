# Generated by Django 5.0.3 on 2024-03-12 19:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userR', '0004_alter_workoutplan_current_level_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workoutplan',
            name='workout_frequency',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, 'Frequency must be at least 1 day per week'), django.core.validators.MaxValueValidator(7, 'Frequency cannot exceed 7 days per week')]),
        ),
    ]
