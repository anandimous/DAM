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

class ValidateTestCases(TestCase):

    def test_details(self):
        response= self.client.post('/loans/reserve/2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['email'],'mhertz@buffalo.edu')
    
    def test_invalid_email(self):
        response= self.client.post('/loans/reserve/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['email'],'mhertz@buf.aalo.edu')

    def test_negative_id(self):
        response= self.client.post('/loans/reserve/2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['id'],'-2')

    def test_zero_id(self):
        response= self.client.post('/loans/reserve/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['id'],'0')

    def test_negative_id(self):
        response= self.client.post('/loans/reserve/3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['id'],'-2')


class ClientTest(TestCase):
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
