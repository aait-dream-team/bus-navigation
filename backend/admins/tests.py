from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase,APIClient
from .models import Admin, USER_TYPES
import logging
logger = logging.getLogger(__name__)

class AdminViewSetsTests(APITestCase):
    def setUp(self) -> None:
        logger.debug('Adding new system admin and admin into database')
        self.s_admin = Admin(username = 'admins@gmail.com', password='admins1234', first_name = 'admins', last_name = 'admins', email = "admins@gmail.com", user_type = USER_TYPES[0][0])
        self.s_admin.save()
        self.admin = Admin(username='admin@gmail.com', password='admin1234', first_name = 'admin', last_name = 'admin', email = 'admin@gamil.com', user_type =  USER_TYPES[1][0])
        self.admin.save()

        self.client = APIClient()
        self.client.force_authenticate(user=self.s_admin)
        logger.debug('Successfully added test admins in the database')

    def test_create_admin_success(self):
        logger.debug("Starting test_create_admin_success")
        url = reverse('admins_create-list')
        data = {
            'username': 'admin1@mail.com',
            'password': '1234admin',
            'first_name': 'admins',
            'last_name': 'bus',
            'email': 'admin1@mail.com',
            'user_type': USER_TYPES[0][0]
        }
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.post(url, data)
        json = response.json()

        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data['username'] , json['username'])
        self.assertEqual(data['first_name'] , json['first_name'])
        self.assertEqual(data['last_name'] , json['last_name'])
        self.assertEqual(data['email'] , json['email'])
        self.assertEqual(data['user_type'] , json['user_type'])
        logger.debug("The test_create_admin_success test has ended successfully")
    
    def test_retrieve_admin_success(self):
        logger.debug("Starting test_retrieve_admin_success")
        url = reverse('admins-detail', args=[self.admin.id])
        response = self.client.get(url)
        data = response.json()
        print(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['email'], self.admin.email)
        logger.debug("The test_retrieve_admin_success test has ended successfully")

    def test_update_admin_success(self):
        logger.debug("Starting test_update_admin_success")
        url = reverse('admins-detail', args=[self.admin.id])
        data = {'first_name': 'Updated First Name'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.admin.refresh_from_db()
        self.assertEqual(self.admin.first_name, data['first_name'])
        logger.debug("The test_update_admin_success test has ended successfully")

    def test_delete_admin_success(self):
        logger.debug("Starting test_delete_admin_success")
        url = reverse('admins-detail', args=[self.admin.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Admin.objects.filter(id=self.admin.id).exists())
        logger.debug("The test_delete_admin_success test has ended successfully")

    def test_create_admin_fail_unauthorized(self):
        logger.debug("Starting test_create_admin_fail_unauthorized")
        url = reverse('admins_create-list')
        data = {
            'username': 'admin1@mail.com',
            'password': '1234admin',
            'first_name': 'admins',
            'last_name': 'bus',
            'email': 'admin1@mail.com',
            'user_type': USER_TYPES[0][0]
        }
        client = APIClient()
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        logger.debug("The test_create_admin_fail_unauthorized test has ended successfully")

    def test_create_admin_validation_error(self):
        logger.debug("Starting test_create_admin_validation_error")
        url = reverse('admins_create-list')
        data = {
            'username': 'admin2@mail.com',
            'password': '1234admin',
            'first_name': 'admins',
            'last_name': 'bus',
            'email': 'admin2@mail.com'
        }
        logger.debug('Sending TEST data to url: %s' % url)
        response = self.client.post(url, data)
        logger.debug('Testing status code response: %s, code: %d' % (response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user_type', response.json())
        logger.debug("The test_create_admin_validation_error test has ended successfully")
    def test_create_admin_missing_field(self):
        url = reverse('admins_create-list')
        data = {
            'username': 'admin2@mail.com',
            'password': '1234admin',
            'first_name': 'admins',
            'last_name': 'bus',
        }

        response = self.client.post(url, data)
        json = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user_type', json)

    def test_create_admin_invalid_user_type(self):
        url = reverse('admins_create-list')
        data = {
            'username': 'admin1@mail.com',
            'password': '1234admin',
            'first_name': 'admins',
            'last_name': 'bus',
            'email': 'admin1@mail.com',
            'user_type': 'invalid_user_type'
        }

        response = self.client.post(url, data)
        json = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user_type', json)

    def test_create_admin_existing_email(self):
        url = reverse('admins_create-list')
        data = {
            'username': 'admins@gmail.com',
            'password': '1234admin',
            'first_name': 'admins',
            'last_name': 'bus',
            'email': 'admins@gmail.com',
            'user_type': USER_TYPES[0][0]
        }

        response = self.client.post(url, data)
        json = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', json)
        self.assertEqual(json['username'][0], 'A user with that username already exists.')
