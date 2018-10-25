from django.contrib.auth import get_user_model
from django.test import TestCase
from datetime import datetime
from dam.inventory.models import Item
from dam.loans.models import Client, ItemLoan, ItemReservation
from dam.loans.views import reservations
#timezone instead of datetime
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


# Create your tests here.
