from random import sample

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .forms import WorkoutPlanForm
from .models import Exercise, WorkoutPlan, WorkoutDay, DayExercise


@login_required
def workout_plan_detail(request, pk):
    workout_plan = get_object_or_404(WorkoutPlan, pk=pk)
    return render(request, 'workout_plan_detail.html', {'workout_plan': workout_plan})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    # Your view logic here
    return Response({"message": "Hello, world!"})

def home_view(request):
    workout_plan = None
    if request.user.is_authenticated:
        try:
            workout_plan = WorkoutPlan.objects.get(user=request.user)
        except WorkoutPlan.DoesNotExist:
            workout_plan = None

    context = {
        'workout_plan': workout_plan,
    }
    return render(request, 'home.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # log the user in
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                # error message if authentication fails
                form.add_error(None, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def generate_workout_plan(frequency, goal, level):
    # Exercise categories
    exercises = {
        'chest': ['Bench Press', 'Incline Bench Press', 'Chest Fly', 'Cable Crossover'],
        'legs': ['Squat', 'Leg Press', 'Lunges', 'Deadlift', 'Leg Curl', 'Glute-Ham Raise', 'Calf Raise'],
        'shoulders': ['Military Press', 'Lateral Raise', 'Front Raise', 'Arnold Press', 'Reverse Fly'],
        'back': ['Pull-Up', 'Barbell Row', 'Deadlift', 'Lat Pull-Down', 'Seated Row'],
        'arms': ['Bicep Curl', 'Tricep Pushdown', 'Hammer Curl', 'Skull Crushers'],
    }

    # Sets and reps based on goal and level
    sets_reps = {
        ('bulk', 'beginner'): (3, '8-10'),
        ('bulk', 'intermediate'): (4, '6-8'),
        ('bulk', 'hero'): (4, '8-10'),
        ('cut', 'beginner'): (3, '10-12'),
        ('cut', 'intermediate'): (4, '10-12'),
        ('cut', 'hero'): (4, '12-15'),
    }

    # Schedule for each day
    day_schedule = [
        ('shoulders', 'arms'),
        ('legs',),
        ('back', 'chest'),
    ]

    while len(day_schedule) < frequency:
        day_schedule.extend(day_schedule[i] for i in range(frequency - len(day_schedule)))

    generated_days = []
    for i, categories in enumerate(day_schedule, start=1):
        day_plan = {'day_number': i, 'exercises': []}

        for category in categories:
            if category == 'arms' and 'shoulders' in categories:
                selected_exercises = sample(exercises[category], 3)
            else:
                selected_exercises = exercises[category]

            for name in selected_exercises:
                sets, reps = sets_reps[(goal, level)]
                if name == 'Push-Up':
                    if goal == 'cut':
                        if level == 'beginner':
                            reps = '10'
                        elif level == 'intermediate':
                            reps = '20'
                        else:  # hero
                            sets = 4
                            reps = '25'
                    else:
                        continue

                try:
                    exercise_instance = Exercise.objects.filter(name=name).first()
                    if exercise_instance:
                        day_plan['exercises'].append({
                            'exercise': exercise_instance,
                            'sets': sets,
                            'reps': reps
                        })
                except Exercise.DoesNotExist:
                    pass

        generated_days.append(day_plan)

    return generated_days


@login_required
def create_workout_plan_view(request):
    if request.method == 'POST':
        form = WorkoutPlanForm(request.POST)
        if form.is_valid():
            workout_plan = form.save(commit=False)
            workout_plan.user = request.user
            workout_plan.save()
            form.save_m2m()  # Save any many-to-many fields related to the form

            # Generate the workout days and exercises
            generated_days = generate_workout_plan(
                frequency=workout_plan.workout_frequency,
                goal=workout_plan.workout_goal,
                level=workout_plan.current_level
            )

            # Iterate over the generated days to create WorkoutDay and DayExercise instances
            for day_info in generated_days:
                workout_day = WorkoutDay.objects.create(
                    workout_plan=workout_plan,
                    day_number=day_info['day_number']
                )

                for exercise_info in day_info['exercises']:
                    DayExercise.objects.create(
                        workout_day=workout_day,
                        exercise=exercise_info['exercise'],
                        sets=exercise_info['sets'],
                        reps=exercise_info['reps']
                    )

            return redirect('workout_plan_detail', pk=workout_plan.pk)
    else:
        form = WorkoutPlanForm()

    return render(request, 'create_workout_plan.html', {'form': form})

def reset_workout_plan(request):
    WorkoutPlan.objects.filter(user=request.user).delete()
    return redirect('create_workout_plan')

def workout_plan_detail(request, pk):
    workout_plan = get_object_or_404(WorkoutPlan, pk=pk)
    workout_days = workout_plan.workout_days.all()

    context = {
        'workout_plan': workout_plan,
        'workout_days': workout_days,
    }
    return render(request, 'workout_plan_detail.html', context)