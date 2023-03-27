from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase,force_authenticate,APIClient
from admins.models import Admin, USER_TYPES


import logging
logger = logging.getLogger(__name__)

class AgencyViewSetTests(APITestCase):
    def setUp(self):
        logger.debug('Adding a new admin into database')
        self.admin = Admin(username='admin@gmail.com', password='admin1234', first_name = 'admin', last_name = 'admin', email = 'admin@gamil.com', user_type =  USER_TYPES[0][0])
        self.admin.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)
        logger.debug('Successfully added test admin into the database')

    def test_create_agency(self):

        '''
            Test to create an Agency
        '''
        logger.debug('Starting test create agency')
        url = reverse('agencies-list')
        data = {
            'name' : 'sheger',
            'url'  : 'http://127.0.0.1:8000/agencies/',
            'lang' : 'en',
            'time_zone' :"+3",
            'phone' : '+251991439581',
            'admin' : self.admin.id,
        }
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.post(url,data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response.json(), response.status_code))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data['name'] , json['name'])
        self.assertEqual(data['url'] , json['url'])
        self.assertEqual(data['lang'] , json['lang'])
        self.assertEqual(data['phone'] , json['phone'])
        self.assertEqual(str(data['admin']) , json['admin'])
        logger.debug("The test_create_agency test has ended successfully")





