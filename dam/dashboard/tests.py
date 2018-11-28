from django.test import TestCase
from dam.users.models import User


class DashboardTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            email='test@example.com',
            password='password',
            is_staff=True,
        )

    def test_page_login_required(self):
        response = self.client.get('/dashboard/')
        self.assertRedirects(response, '/users/log-in/?next=/dashboard/')

    def test_authenticated_can_access(self):
        self.client.login(username='test@example.com', password='password')
        response = self.client.get('/dashboard/')
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'Dashboard')
