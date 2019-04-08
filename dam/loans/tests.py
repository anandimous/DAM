from datetime import datetime, timedelta
from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase
import pytz

from dam.inventory.models import Item
from dam.loans.models import ItemLoan, ItemReservation


User = get_user_model()


class ReservationPossibleTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.item_user = User.objects.create(email='borrower@example.com')
        cls.loan_approver = User.objects.create(email='approver@example.com')

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
            user=cls.item_user,
            is_active=True,
        )
        ItemReservation.objects.create(
            item=noise_item,
            user=cls.item_user,
        )
        ItemLoan.objects.create(
            item=noise_item,
            user=cls.item_user,
            approved_by=cls.loan_approver,
        )
        ItemLoan.objects.create(
            item=noise_item,
            user=cls.item_user,
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
            user=self.item_user,
            is_active=True,
        )
        item = Item.objects.with_availability().first()
        self.assertEqual(item.quantity, 10)
        self.assertEqual(item.available, 9)


class ReserveItemTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='example@buffalo.edu',
            password='password',
        )

    def test_anonymous_user(self):
        response = self.client.post(
            '/loans/reserve/1/',
            follow=True,
        )

        self.assertRedirects(response, '/users/log-in/?next=/loans/reserve/1/')

    def test_invalid_item(self):
        self.client.login(username='example@buffalo.edu', password='password')
        response = self.client.post(
            '/loans/reserve/1/',
            follow=True,
        )

        self.assertEqual(response.status_code, 404)

    def test_valid_and_available(self):
        # Create item to be reserved.
        Item.objects.create(id=2, quantity=2)

        reserved_at = datetime(2018, 12, 7, tzinfo=pytz.utc)
        reservation_ends = reserved_at + timedelta(days=5)

        # Reserve the item.
        self.client.login(username='example@buffalo.edu', password='password')
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=reserved_at)):
            response = self.client.post(
                '/loans/reserve/2/',
                follow=True,
            )

        # Verify that the correct data was stored.
        self.assertEqual(ItemReservation.objects.count(), 1)
        reservation = ItemReservation.objects.first()
        self.assertEqual(reservation.item_id, 2)
        self.assertEqual(reservation.user, self.user)
        self.assertTrue(reservation.is_active)
        self.assertEqual(reservation.reserved_at, reserved_at)
        self.assertEqual(reservation.reservation_ends, reservation_ends)

        # Verify that the user got the expected behavior.
        self.assertRedirects(response, '/inventory/details/2/')
        self.assertContains(response, 'The item has been reserved!')

    def test_valid_and_unavailable(self):
        # Create item to be reserved.
        Item.objects.create(id=2, quantity=0)

        # Reserve the item.
        self.client.login(username='example@buffalo.edu', password='password')
        response = self.client.post(
            '/loans/reserve/2/',
            follow=True,
        )

        # Verify that the reservation was not created.
        self.assertEqual(ItemReservation.objects.count(), 0)

        # Verify that the user got the expected behavior.
        self.assertRedirects(response, '/inventory/details/2/')
        self.assertContains(response, 'The item you tried to reserve is not available.')
