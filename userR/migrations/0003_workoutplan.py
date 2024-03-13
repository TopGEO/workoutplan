# Generated by Django 5.0.3 on 2024-03-12 16:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userR', '0002_musclegroup_remove_exercise_target_muscles_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkoutPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workout_frequency', models.IntegerField()),
                ('workout_goal', models.CharField(choices=[('cut', 'Cut'), ('bulk', 'Bulk'), ('gain_mass', 'Gain Mass')], max_length=50)),
                ('current_level', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced'), ('hero', 'Hero')], max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
