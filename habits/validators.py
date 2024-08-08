from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

periodicity = [
    "everyday",
    "everyhour",
    "everyminute",
    "every2days",
    "every3days",
    "every4days",
    "every5days",
    "every6days",
    "everyweek",
]


def validate_related_habit_or_reward(instance):
    """Проверка на одновремменость добавления связанной привычки и вознаграждения"""
    if instance.related_habit and instance.reward:
        raise ValidationError(
            _("Нельзя одновременно указать связанную привычку и вознаграждение.")
        )


def validate_time_to_complete(value):
    """Проверка времени выполнения (не более 120 секунд)"""
    if value and value > 120:
        raise ValidationError(_("Время на выполнение не должно превышать 120 секунд."))


def validate_habit_frequency(periodicity_):
    """Проверка, что периодичность выполнения допустима"""
    if periodicity_ not in periodicity:
        raise ValidationError(
            _(f"Неправильная периодичность. Допустимые значения: {periodicity}")
        )


def validate_habit_execution_frequency(periodicity_):
    """Проверка: Нельзя выполнять привычку реже, чем 1 раз в 7 дней"""
    if periodicity_ not in periodicity:
        raise ValidationError(_("Нельзя выполнять привычку реже, чем 1 раз в 7 дней."))
