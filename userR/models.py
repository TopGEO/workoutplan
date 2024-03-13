from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class MuscleGroup(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    instructions = models.TextField()
    target_muscles = models.ManyToManyField(MuscleGroup, related_name='exercises')

    def __str__(self):
        return self.name





class WorkoutPlan(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('hero', 'Hero'),
    ]
    GOAL_CHOICES = [
        ('cut', 'Cut'),
        ('bulk', 'Bulk'),
    ]

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    workout_frequency = models.IntegerField(
        validators=[
            MinValueValidator(3, "Frequency must be at least 3 day per week"),
            MaxValueValidator(7, "Frequency cannot exceed 7 days per week")
        ]
    )
    workout_goal = models.CharField(max_length=50, choices=GOAL_CHOICES)
    current_level = models.CharField(max_length=50, choices=LEVEL_CHOICES)

    def __str__(self):
        return f"{self.user.username}'s Workout Plan"


class WorkoutDay(models.Model):
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name='workout_days')
    day_number = models.IntegerField()  # or day_name if you prefer names like 'Day 1', 'Day 2', etc.

    def __str__(self):
        return f"{self.workout_plan.user.username}'s Workout Plan: Day {self.day_number}"

class DayExercise(models.Model):
    workout_day = models.ForeignKey(WorkoutDay, on_delete=models.CASCADE, related_name='day_exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField()
    reps = models.CharField(max_length=10)
    def __str__(self):
        return f"{self.exercise.name} - Sets: {self.sets}, Reps: {self.reps}"