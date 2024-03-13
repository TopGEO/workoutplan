from django.urls import path
from .views import signup_view, login_view, logout_view, home_view, create_workout_plan_view, workout_plan_detail, \
    reset_workout_plan

urlpatterns = [
    path('', home_view, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('workout-plan/<int:pk>/', workout_plan_detail, name='workout_plan_detail'),
    path('create-workout-plan/', create_workout_plan_view, name='create_workout_plan'),
    path('reset-workout-plan/', reset_workout_plan, name='reset_workout_plan'),
]