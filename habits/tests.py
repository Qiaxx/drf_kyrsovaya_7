from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from habits.models import Habit

User = get_user_model()


class HabitTests(APITestCase):
    def setUp(self):
        # Создаем пользователя и активируем его
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword',
            is_active=True  # Активируем учетную запись
        )

        # Получаем JWT токен для пользователя
        self.token = self.get_token_for_user()

        # Добавляем токен в заголовки запросов
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Создаем тестовую привычку
        self.habit = Habit.objects.create(
            user=self.user,
            place='Home',
            time='07:00:00',
            action='Exercise',
            is_nice_habit=True,
            related_habit=None,
            periodicity='everyday',
            reward='Self-praise',
            time_to_complete=30,
            is_publish=True
        )

    def get_token_for_user(self):
        url = reverse('users:login')
        response = self.client.post(url, {
            'email': self.user.email,
            'password': 'testpassword'
        })
        # Проверяем, что запрос прошел успешно
        self.assertEqual(response.status_code, 200)
        # Возвращаем токен из ответа
        return response.data.get('access')

    def test_create_habit(self):
        url = reverse('habits:habits_create')
        data = {
            'place': 'New place',
            'time': '08:00:00',
            'action': 'New Habit',
            'is_nice_habit': False,
            'related_habit': None,
            'periodicity': 'everyday',
            'reward': 'New Reward',
            'time_to_complete': 60,
            'is_publish': True,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_habit(self):
        url = reverse('habits:habits_update', args=[self.habit.id])
        data = {
            'action': 'Updated Habit',
            'periodicity': 'every3days'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_habit(self):
        url = reverse('habits:habits_delete', args=[self.habit.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_user_habits(self):
        url = reverse('habits:user_habits')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_habit_with_invalid_periodicity(self):
        url = reverse('habits:habits_create')
        data = {
            'place': 'Invalid place',
            'time': '08:00:00',
            'action': 'Invalid Habit',
            'is_nice_habit': False,
            'related_habit': None,
            'periodicity': 'invalid_periodicity',  # Неверная периодичность
            'reward': 'Invalid Reward',
            'time_to_complete': 60,
            'is_publish': True,
        }
        response = self.client.post(url, data, format='json')
        if response.status_code != status.HTTP_400_BAD_REQUEST:
            print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_habit_with_related_habit_and_reward(self):
        related_habit = Habit.objects.create(
            user=self.user,
            place='Home',
            time='07:00:00',
            action='Related Habit',
            is_nice_habit=True,
            related_habit=None,
            periodicity='everyday',
            reward=None,
            time_to_complete=30,
            is_publish=True
        )
        url = reverse('habits:habits_create')
        data = {
            'place': 'Conflicting place',
            'time': '08:00:00',
            'action': 'Conflicting Habit',
            'is_nice_habit': True,
            'related_habit': related_habit.id,
            'periodicity': 'everyday',
            'reward': 'Conflicting Reward',  # Не должно быть вознаграждения при приятной привычке
            'time_to_complete': 60,
            'is_publish': True,
        }
        response = self.client.post(url, data, format='json')
        if response.status_code != status.HTTP_400_BAD_REQUEST:
            print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_habit_with_time_to_complete_exceeding_limit(self):
        url = reverse('habits:habits_create')
        data = {
            'place': 'Test place',
            'time': '08:00:00',
            'action': 'Test Habit',
            'is_nice_habit': False,
            'related_habit': None,
            'periodicity': 'everyday',
            'reward': 'Test Reward',
            'time_to_complete': 150,  # Превышает допустимый лимит
            'is_publish': True,
        }
        response = self.client.post(url, data, format='json')
        if response.status_code != status.HTTP_400_BAD_REQUEST:
            print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_habit_with_validators(self):
        url = reverse('habits:habits_create')
        valid_data = {
            'place': 'Valid place',
            'time': '09:00:00',
            'action': 'Valid Habit',
            'is_nice_habit': False,
            'related_habit': None,
            'periodicity': 'everyweek',  # Допустимая периодичность
            'reward': 'Valid Reward',
            'time_to_complete': 30,
            'is_publish': True,
        }
        response = self.client.post(url, valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
