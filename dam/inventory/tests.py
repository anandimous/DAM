from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from dam.inventory.models import Inventory, Item
from dam.loans.models import ItemLoan, ItemReservation


User = get_user_model()


class InventoryAvailabilityTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.item_user = User.objects.create(email='borrower@example.com')
        cls.loan_approver = User.objects.create(email='approver@example.com')

        cls.inventory = Inventory.objects.create()

        cls.test_item = Item.objects.create(
            name='Name 1',
            description='Description 1.',
            quantity=10,
            inventory=cls.inventory,
        )

        # Add some reservations and loans as noise to ensure that only the records
        # for the specific item under test are taken into consideration.
        noise_item = Item.objects.create(
            name='Name 2',
            description='Description 2.',
            quantity=20,
            inventory=cls.inventory,
        )
        ItemReservation.objects.create(
            item=noise_item,
            user=cls.item_user,
            is_active=False,
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
            returned_at=timezone.now(),
        )

    def test_full_availability(self):
        item = Item.objects.with_availability().first()
        self.assertEqual(item.quantity, 10)
        self.assertEqual(item.available, 10)

    def test_reservation_active(self):
        ItemReservation.objects.create(
            item=self.test_item,
            user=self.item_user,
            is_active=True,
        )
        item = Item.objects.with_availability().first()
        self.assertEqual(item.quantity, 10)
        self.assertEqual(item.available, 9)

    def test_reservation_inactive(self):
        ItemReservation.objects.create(
            item=self.test_item,
            user=self.item_user,
            is_active=False,
        )
        item = Item.objects.with_availability().first()
        self.assertEqual(item.quantity, 10)
        self.assertEqual(item.available, 10)

    def test_loan_active(self):
        ItemLoan.objects.create(
            item=self.test_item,
            user=self.item_user,
            approved_by=self.loan_approver,
        )
        item = Item.objects.with_availability().first()
        self.assertEqual(item.quantity, 10)
        self.assertEqual(item.available, 9)

    def test_loan_inactive(self):
        ItemLoan.objects.create(
            item=self.test_item,
            user=self.item_user,
            approved_by=self.loan_approver,
            returned_at=timezone.now(),
        )
        item = Item.objects.with_availability().first()
        self.assertEqual(item.quantity, 10)
        self.assertEqual(item.available, 10)

    def test_reservations_and_loans(self):
        ItemReservation.objects.create(
            item=self.test_item,
            user=self.item_user,
            is_active=True,
        )
        ItemLoan.objects.create(
            item=self.test_item,
            user=self.item_user,
            approved_by=self.loan_approver,
        )
        item = Item.objects.with_availability().first()
        self.assertEqual(item.quantity, 10)
        self.assertEqual(item.available, 8)


class InventoryDetailsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.inventory = Inventory.objects.create(name='Test')
        cls.test_item = Item.objects.create(
            name='Name 1',
            description='Description 1.',
            quantity=10,
            inventory=cls.inventory,
        )

    def test_view_uses_correct_template(self):
        response = self.client.get('/inventory/details/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/details.html')

    def test_response_on_valid_item(self):
        response = self.client.get('/inventory/details/1/')
        self.assertEqual(response.context['item'], self.test_item)

    def test_response_on_invalid_item(self):
        response = self.client.get('/inventory/details/0/')
        self.assertEqual(response.status_code, 404)

    def test_authenticated_user_can_reserve(self):
        User.objects.create_user(email='example@buffalo.edu', password='password')
        self.client.login(username='example@buffalo.edu', password='password')

        response = self.client.get('/inventory/details/1/')
        self.assertContains(response, 'Reserve')
        self.assertNotContains(response, 'This item is currently unavailable')
        self.assertNotContains(response, 'You must <a href="/users/log-in/?next=/inventory/details/1/">log in</a>')

    def test_anonymous_user_cannot_reserve(self):
        response = self.client.get('/inventory/details/1/')
        self.assertNotContains(response, 'Reserve')
        self.assertNotContains(response, 'This item is currently unavailable')
        self.assertContains(response, 'You must <a href="/users/log-in/?next=/inventory/details/1/">log in</a>')

    def test_unavailable(self):
        Item.objects.create(id=2, quantity=0, inventory=self.inventory)
        response = self.client.get('/inventory/details/2/')
        self.assertContains(response, 'This item is currently unavailable')
