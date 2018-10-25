from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from dam.inventory.models import Item
from dam.loans.models import Client, ItemLoan, ItemReservation


User = get_user_model()


class InventoryAvailabilityTest(TestCase):

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
            is_active=False,
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
            returned_at=timezone.now(),
        )

    def test_full_availability(self):
        item = Item.objects.with_availability().first()
        self.assertEqual(item.quantity, 10)
        self.assertEqual(item.available, 10)

    def test_reservation_active(self):
        ItemReservation.objects.create(
            item=self.test_item,
            client=self.item_client,
            is_active=True,
        )
        item = Item.objects.with_availability().first()
        self.assertEqual(item.quantity, 10)
        self.assertEqual(item.available, 9)

    def test_reservation_inactive(self):
        ItemReservation.objects.create(
            item=self.test_item,
            client=self.item_client,
            is_active=False,
        )
        item = Item.objects.with_availability().first()
        self.assertEqual(item.quantity, 10)
        self.assertEqual(item.available, 10)

    def test_loan_active(self):
        ItemLoan.objects.create(
            item=self.test_item,
            client=self.item_client,
            approved_by=self.loan_approver,
        )
        item = Item.objects.with_availability().first()
        self.assertEqual(item.quantity, 10)
        self.assertEqual(item.available, 9)

    def test_loan_inactive(self):
        ItemLoan.objects.create(
            item=self.test_item,
            client=self.item_client,
            approved_by=self.loan_approver,
            returned_at=timezone.now(),
        )
        item = Item.objects.with_availability().first()
        self.assertEqual(item.quantity, 10)
        self.assertEqual(item.available, 10)

    def test_reservations_and_loans(self):
        ItemReservation.objects.create(
            item=self.test_item,
            client=self.item_client,
            is_active=True,
        )
        ItemLoan.objects.create(
            item=self.test_item,
            client=self.item_client,
            approved_by=self.loan_approver,
        )
        item = Item.objects.with_availability().first()
        self.assertEqual(item.quantity, 10)
        self.assertEqual(item.available, 8)


class InventoryDetailsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_item = Item.objects.create(
            name='Name 1',
            description='Description 1.',
            quantity=10,
        )

    def test_view_uses_correct_template(self):
        response = self.client.get('/details/1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/details.html')

    def test_response_on_valid_item(self):
        response = self.client.get('/details/1')
        self.assertEqual(response.context['item_id'], 1)
        self.assertEqual(response.context['item_name'], 'Name 1')
        self.assertEqual(response.context['item_description'], 'Description 1.')

    def test_response_on_invalid_item(self):
        response = self.client.get('/details/0')
        self.assertEqual(response.status_code, 404)