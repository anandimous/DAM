from django.test import TestCase
from django.test import Client 

# Create your tests here.

class ValidateTestCases(TestCase):
    def setUp(self):
        self.client= Client()

    def test_details(self):
        response= self.client.get('/client/details/(id=item_id)')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['email'],'mhertz@buffalo.edu')
    
    def invalid_email(self):
        response= self.client.get('/client/details/(id=item_id)')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['email'],'mhertz@buf.aalo.edu')

    def negative_id(self):
        response= self.client.get('/client/details/(id=item_id)')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['id'],'-2')

    def zero_id(self):
        response= self.client.get('/client/details/(id=item_id)')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['id'],'0')

    def negative_id(self):
        response= self.client.get('/client/details/(id=item_id)')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['id'],'-2')







   # @mock.patch ('app.utils.requests.get')
    #def valid_email(self, mock_get):
        #mock_response= mock.Mock()
        #expected_val= {
           # 'first_name':'Matthew',
           # 'last_name':'Hertz',
            #'email':'mhertz@buffalo.edu'
            #'item_id':'2'
        #}
        #mock_response.json.return_value= expected_val
        #mock_get.return_value= mock_response
        #result= ValidateTestCases()

    #def invalid_email(self, mock_get):
        






def 