from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from habits.models import Habit


class HabitSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"

    def validate(self, data):
        habit = Habit(**data)
        try:
            habit.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return data
