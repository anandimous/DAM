from django.contrib.auth import SESSION_KEY
from django.test import TestCase

from .models import User


class LogInTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            email='test@example.com',
            password='password',
            # TODO: remove when access to admin is no longer needed.
            is_staff=True,
        )

    def test_page_loads(self):
        response = self.client.get('/users/log-in/')
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'Log in')

    def test_correct_credentials(self):
        response = self.client.post(
            '/users/log-in/',
            {
                'email': 'test@example.com',
                'password': 'password',
            },
            follow=True,
        )
        self.assertIn(SESSION_KEY, self.client.session)
        self.assertRedirects(response, '/dashboard/')

    def test_incorrect_email(self):
        response = self.client.post('/users/log-in/', {
            'email': 'fail@example.com',
            'password': 'password',
        })
        self.assertContains(
            response,
            'Please enter a correct email address and password.',
        )
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_incorrect_password(self):
        response = self.client.post('/users/log-in/', {
            'email': 'test@example.com',
            'password': 'fail',
        })
        self.assertContains(
            response,
            'Please enter a correct email address and password.',
        )
        self.assertNotIn(SESSION_KEY, self.client.session)


class LogOutTest(TestCase):
    def test_log_out(self):
        User.objects.create_user(
            email='test@example.com',
            password='password',
        )
        self.client.login(
            email='test@example.com',
            password='password',
        )
        self.assertIn(SESSION_KEY, self.client.session)
        response = self.client.get('/users/log-out/')
        self.assertNotIn(SESSION_KEY, self.client.session)
        self.assertRedirects(response, '/')

