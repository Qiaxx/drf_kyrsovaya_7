from django.urls import path

from habits.apps import HabitsConfig
from habits.views import (HabitCreate, HabitDelete, HabitUpdate,
                          PublicHabitViewSet, UserHabit)

app_name = HabitsConfig.name

urlpatterns = [
    path("user_habits/", UserHabit.as_view(), name="user_habits"),
    path(
        "public_habits/",
        PublicHabitViewSet.as_view({"get": "list"}),
        name="public_habits",
    ),
    path("habits/create/", HabitCreate.as_view(), name="habits_create"),
    path("habits/<int:pk>/", HabitUpdate.as_view(), name="habits_update"),
    path("habits/<int:pk>/delete/", HabitDelete.as_view(), name="habits_delete"),
]
