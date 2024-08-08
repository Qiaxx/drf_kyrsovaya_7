from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from .models import Habit
from .services import send_notification


@shared_task
def send_habit_reminder(habit_id):
    try:
        habit = Habit.objects.get(id=habit_id)
    except Habit.DoesNotExist:
        return

    reminder_text = f"Напоминание: Время выполнить привычку '{habit.action}'!"

    chat_id = (
        habit.user.profile.tg_chat_id
    )  # Замените на правильное поле в вашей модели, если нужно
    if chat_id:
        send_notification(reminder_text, chat_id)
    else:
        print("Chat ID отсутствует для пользователя.")


@shared_task
def schedule_habit_reminders():
    now = timezone.now()
    habits = Habit.objects.filter(is_publish=True)

    for habit in habits:
        if habit.periodicity == "everyday":
            next_time = now + timedelta(days=1)
        elif habit.periodicity == "everyweek":
            next_time = now + timedelta(weeks=1)
        else:
            try:
                days = int(habit.periodicity.replace("every", "").replace("days", ""))
                next_time = now + timedelta(days=days)
            except ValueError:
                continue  # Пропускаем неправильные значения периодичности

        # Планируем напоминание для следующего выполнения привычки
        send_habit_reminder.apply_async((habit.id,), eta=next_time)
