from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, UpdateAPIView)
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.viewsets import ReadOnlyModelViewSet

from habits.models import Habit
from habits.paginators import HabitPagination
from habits.serializers import HabitSerializer
from users.permissions import IsOwner


class UserHabit(ListAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = HabitPagination

    def get_queryset(self):
        # Возвращаем только привычки, принадлежащие текущему пользователю
        return Habit.objects.filter(user=self.request.user)


class PublicHabitViewSet(ReadOnlyModelViewSet):
    queryset = Habit.objects.filter(is_publish=True)
    serializer_class = HabitSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]


class HabitCreate(CreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitUpdate(UpdateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class HabitDelete(DestroyAPIView):
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
