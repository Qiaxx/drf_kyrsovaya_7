from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User


class UserTests(APITestCase):

    def setUp(self):
        # URL-адреса для регистрации, входа и обновления токена
        self.register_url = reverse('users:register')
        self.login_url = reverse('users:login')
        self.refresh_url = reverse('users:token_refresh')

        # Данные для тестового пользователя
        self.user_data = {
            'email': 'newuser@example.com',
            'password': 'testpassword'
        }

        # Создаем тестового пользователя для проверки логина
        self.user = User.objects.create_user(email='newuserf@example.com', password='testpassword', is_active=True)

    def test_register_user(self):
        """Тест регистрации пользователя"""
        response = self.client.post(self.register_url, self.user_data, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            print("Данные ответа:", response.data)  # Вывод данных ответа для отладки

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_user = User.objects.get(email=self.user_data['email'])
        self.assertTrue(created_user.is_active)

        self.assertEqual(User.objects.count(), 2)  # Один пользователь из setUp, один новый пользователь
        self.assertEqual(User.objects.last().email, self.user_data['email'])

    def test_login_user(self):
        """Тест входа пользователя"""
        # Вывод данных для отладки
        print("Попытка входа с данными:", self.user_data)

        response = self.client.post(self.login_url, {
            'email': self.user.email,
            'password': 'testpassword'
        })
        if response.status_code != status.HTTP_200_OK:
            print("Ошибка входа, данные ответа:", response.data)  # Вывод данных ответа для отладки

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_refresh(self):
        """Тест обновления JWT токена"""
        # Входим в систему, чтобы получить токен обновления
        login_response = self.client.post(self.login_url, {
            'email': self.user.email,
            'password': 'testpassword'
        })
        if login_response.status_code != status.HTTP_200_OK:
            print("Ошибка входа, данные ответа:", login_response.data)  # Вывод данных ответа для отладки

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        refresh_token = login_response.data['refresh']
        refresh_data = {'refresh': refresh_token}

        # Обновляем токен
        response = self.client.post(self.refresh_url, refresh_data, format='json')
        if response.status_code != status.HTTP_200_OK:
            print("Ошибка обновления токена, данные ответа:", response.data)  # Вывод данных ответа для отладки

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_login_inactive_user(self):
        """Тест, что неактивный пользователь не может войти"""
        inactive_user = User.objects.create_user(email='inactive@example.com', password='testpassword', is_active=False)
        response = self.client.post(self.login_url, {'email': inactive_user.email, 'password': 'testpassword'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

