from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="почта")
    is_active = models.BooleanField(
        default=False, blank=True, null=True, verbose_name="Статус активности"
    )
    tg_chat_id = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Телеграм chat_id"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
