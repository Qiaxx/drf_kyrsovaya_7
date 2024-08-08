from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from config import settings
from habits.validators import (validate_habit_execution_frequency,
                               validate_habit_frequency,
                               validate_related_habit_or_reward,
                               validate_time_to_complete)


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="создатель",
    )
    place = models.CharField(
        max_length=150, blank=True, null=True, verbose_name="Место"
    )
    time = models.TimeField(
        auto_now_add=False, blank=True, null=True, verbose_name="Время выполнения"
    )
    action = models.CharField(
        max_length=256, blank=True, null=True, verbose_name="Действие"
    )
    is_nice_habit = models.BooleanField(
        default=False, blank=True, null=True, verbose_name="Признак приятной привычки"
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Связанная привычка",
    )
    periodicity = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        default="everyday",
        verbose_name="Периодичность",
    )
    reward = models.CharField(
        max_length=256, blank=True, null=True, verbose_name="Вознаграждение"
    )
    time_to_complete = models.IntegerField(
        null=True, blank=True, verbose_name="Время на выполнение"
    )
    is_publish = models.BooleanField(default=False, verbose_name="Признак публичности")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return f"{self.user} - {self.action}"

    def clean(self):
        # Проверка на одновременность связанной привычки и вознаграждения
        validate_related_habit_or_reward(self)
        # Проверка на соответствие времени выполнения
        if self.time_to_complete is not None:
            validate_time_to_complete(self.time_to_complete)
        # Проверка: У приятной привычки не может быть вознаграждения или связанной привычки
        if self.is_nice_habit:
            if self.related_habit or self.reward:
                raise ValidationError(
                    _(
                        "У приятной привычки не может быть вознаграждения или связанной привычки."
                    )
                )
        # Проверка: Связанная привычка должна быть приятной привычкой
        if self.related_habit and not self.related_habit.is_nice_habit:
            raise ValidationError(
                _("Связанная привычка должна быть приятной привычкой.")
            )

        # Проверка на соответствие периодичности выполнения (для создания тестовых моделей)
        # validate_habit_frequency(self.periodicity)

        # Проверка на соответствие частоте выполнения
        validate_habit_execution_frequency(self.periodicity)
