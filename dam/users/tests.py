from django.contrib.auth import SESSION_KEY
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.utils.html import escape

from .models import User


class CreateAccountTest(TestCase):
    def test_page_loads(self):
        response = self.client.get('/users/create-account/')
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'Create account')

    def test_valid_data_succeeds(self):
        response = self.client.post(
            '/users/create-account/',
            {
                'email': 'test@example.com',
                'first_name': 'First',
                'last_name': 'Last',
                'password1': 'Secret password!',
                'password2': 'Secret password!',
            }
        )

        # User should have been created with correct data.
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'First')
        self.assertEqual(user.last_name, 'Last')
        self.assertNotEqual(user.password, 'Secret password!')  # should be hashed
        self.assertTrue(check_password('Secret password!', user.password))

        # User should automatically be logged in
        self.assertIn(SESSION_KEY, self.client.session)
        self.assertRedirects(response, '/dashboard/')

    def test_duplicate_user_fails(self):
        User.objects.create(email='test@example.com')

        response = self.client.post(
            '/users/create-account/',
            {
                'email': 'test@example.com',
                'first_name': 'First',
                'last_name': 'Last',
                'password1': 'Secret password!',
                'password2': 'Secret password!',
            }
        )

        # A second User should not have been created.
        self.assertEqual(User.objects.count(), 1)

        # User should see the error.
        self.assertContains(
            response,
            'User with this Email address already exists.',
        )

    def test_different_passwords_fails(self):
        response = self.client.post(
            '/users/create-account/',
            {
                'email': 'test@example.com',
                'first_name': 'First',
                'last_name': 'Last',
                'password1': 'Secret one',
                'password2': 'Secret two',
            }
        )

        # User should not have been created.
        self.assertEqual(User.objects.count(), 0)

        # User should see the error.
        self.assertContains(
            response,
            escape("The two password fields didn't match."),
        )


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

    def test_invalid_email(self):
        response = self.client.post('/users/log-in/', {
            'email': 'a@b.c',
            'password': 'password',
        })
        self.assertContains(
            response,
            'Enter a valid email address.',
        )
        self.assertNotIn(SESSION_KEY, self.client.session)

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

