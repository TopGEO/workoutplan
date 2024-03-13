from django import forms
from .models import WorkoutPlan

class WorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlan
        fields = ['workout_frequency', 'workout_goal', 'current_level']

