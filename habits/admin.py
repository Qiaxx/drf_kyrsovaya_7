from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitsAdmin(admin.ModelAdmin):
    list_display = ("action", "user")
    list_filter = ("action",)
    search_fields = ("action", "user")
