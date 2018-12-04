from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from dam.inventory.models import Item
from dam.loans.models import Client, ItemLoan, ItemReservation


User = get_user_model()


class ReservationPossibleTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.item_client = Client.objects.create()
        cls.loan_approver = User.objects.create()

        cls.test_item = Item.objects.create(
            name='Name 1',
            description='Description 1.',
            quantity=10,
        )
    # Add some reservations and loans as noise to ensure that only the records
    # for the specific item under test are taken into consideration.
        noise_item = Item.objects.create(
            name='Name 2',
            description='Description 2.',
            quantity=20,
        )
        ItemReservation.objects.create(
            item=noise_item,
            client=cls.item_client,
            is_active=True,
        )
        ItemReservation.objects.create(
            item=noise_item,
            client=cls.item_client,
        )
        ItemLoan.objects.create(
            item=noise_item,
            client=cls.item_client,
            approved_by=cls.loan_approver,
        )
        ItemLoan.objects.create(
            item=noise_item,
            client=cls.item_client,
            approved_by=cls.loan_approver,
            returned_at=datetime.utcnow(),
        )

    def test_see_all_reservations(self):
        count = ItemReservation.objects.all().count()
        item = Item.objects.with_availability().first()
        self.assertEqual(count, 2)

    def test_see_all_loans(self):
        count = ItemLoan.objects.all().count()
        item = Item.objects.with_availability().first()
        self.assertEqual(count, 2)

    def test_reservation_active(self):
        ItemReservation.objects.create(
            item=self.test_item,
            client=self.item_client,
            is_active=True,
        )
        item = Item.objects.with_availability().first()
        self.assertEqual(item.quantity, 10)
        self.assertEqual(item.available, 9)


class ReserveItemTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            email='example@buffalo.edu',
            password='password',
        )

    def test_anonymous_user(self):
        response = self.client.post(
            '/loans/reserve/1/',
            {
                'email': 'example@buffalo.edu',
                'first_name': 'First',
                'last_name': 'Last',
            },
            follow=True,
        )

        self.assertRedirects(response, '/users/log-in/?next=/loans/reserve/1/')

    def test_invalid_item(self):
        self.client.login(username='example@buffalo.edu', password='password')

        response = self.client.post(
            '/loans/reserve/1/',
            {
                'email': 'example@buffalo.edu',
                'first_name': 'First',
                'last_name': 'Last',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 404)

    def test_valid_and_available(self):
        self.client.login(username='example@buffalo.edu', password='password')

        # Create item to be reserved.
        Item.objects.create(id=2, quantity=2)

        # Reserve the item.
        response = self.client.post(
            '/loans/reserve/2/',
            {
                'email': 'example@buffalo.edu',
                'first_name': 'First',
                'last_name': 'Last',
            },
            follow=True,
        )

        # Verify that the correct data was stored.
        self.assertEqual(ItemReservation.objects.count(), 1)
        reservation = ItemReservation.objects.first()
        self.assertEqual(reservation.item_id, 2)
        self.assertEqual(reservation.client, Client(id=1))
        self.assertTrue(reservation.is_active)

        # Verify that the user got the expected behavior.
        self.assertRedirects(response, '/inventory/details/2/')
        self.assertContains(response, 'The item has been reserved!')

    def test_valid_and_unavailable(self):
        self.client.login(username='example@buffalo.edu', password='password')

        # Create item to be reserved.
        Item.objects.create(id=2, quantity=0)

        # Reserve the item.
        response = self.client.post(
            '/loans/reserve/2/',
            {
                'email': 'example@buffalo.edu',
                'first_name': 'First',
                'last_name': 'Last',
            },
            follow=True,
        )

        # Verify that the reservation was not created.
        self.assertEqual(ItemReservation.objects.count(), 0)

        # Verify that the user got the expected behavior.
        self.assertRedirects(response, '/inventory/details/2/')
        self.assertContains(response, 'The item you tried to reserve is not available.')

    def test_invalid_email(self):
        self.client.login(username='example@buffalo.edu', password='password')

        # Create item to be reserved.
        Item.objects.create(id=2, quantity=2)

        # Reserve the item.
        response = self.client.post(
            '/loans/reserve/2/',
            {
                'email': 'example@invalid.edu',
                'first_name': 'First',
                'last_name': 'Last',
            },
            follow=True,
        )

        # Verify that the reservation was not created.
        self.assertEqual(ItemReservation.objects.count(), 0)


class ClientTests(TestCase):
    def test_get_email_address_direct(self):
        client = Client.objects.create(
            first_name='First',
            last_name='Last',
            email='first.last@example.com',
        )
        self.assertEqual(client.get_email_address(), 'first.last@example.com')

    def test_get_email_address_indirect(self):
        user = User.objects.create(
            first_name='First',
            last_name='Last',
            email='first.last@example.com',
        )
        client = Client.objects.create(user=user)
        self.assertEqual(client.get_email_address(), 'first.last@example.com')

    def test_get_full_name_direct(self):
        client = Client.objects.create(
            first_name='First',
            last_name='Last',
            email='first.last@example.com',
        )
        self.assertEqual(client.get_full_name(), 'First Last')

    def test_get_full_name_indirect(self):
        user = User.objects.create(
            first_name='First',
            last_name='Last',
            email='first.last@example.com',
        )
        client = Client.objects.create(user=user)
        self.assertEqual(client.get_full_name(), 'First Last')
