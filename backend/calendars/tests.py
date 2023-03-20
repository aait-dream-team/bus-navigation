from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase,force_authenticate,APIClient
from admins.models import Admin, USER_TYPES
from agencies.models import Agency
from .models import Calendar
from datetime import date
import logging
logger = logging.getLogger(__name__)
class CalendarViewSetTests(APITestCase):
    def setUp(self):
        logger.debug('Adding a new admin, system admin and agency into database')
        self.s_admin = Admin(username='admins@gmail.com', password='admins1234', first_name = 'admins', last_name = 'admins', email = 'admins@gamil.com', user_type =  USER_TYPES[0][0])
        self.s_admin.save()
        self.admin = Admin(username='admin@gmail.com', password='admin1234', first_name = 'admin', last_name = 'admin', email = 'admin@gamil.com', user_type =  USER_TYPES[1][0])
        self.admin.save()
        
        self.agency = Agency(name = 'bus1', url = 'http://127.0.0.1:8000/', lang='en', time_zone='+3', phone = '+251991439281', admin = self.s_admin)
        self.agency.save()
        
        self.client = APIClient()
        logger.debug('Successfully added test admin, system admin and agency into the database')
    def test_create_calendar_success(self):

        '''
            Test to create a Calendar success

        '''
        logger.debug('Starting test_create_calendar_success')
        url = reverse('calendars-list')
        data = {
            'monday' : True,
            'tuesday' : True,
            'wednesday' : True,
            'thursday' : True,
            'friday' : True,
            'saturday' : True,
            'sunday' : True,
            'start_date' : date(2023, 3, 10),
            'end_date' : date(2023, 3, 24),
            'agency': self.agency.id
        }
        logger.debug('Sending TEST data to url: %s'%url)
        # self.client.force_authenticate(user=self.admin)
        response = self.client.post(url,data)
        json = response.json()

        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code)) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data['monday'] , json['monday'])
        self.assertEqual(data['tuesday'] , json['tuesday'])
        self.assertEqual(data['wednesday'] , json['wednesday'])
        self.assertEqual(data['thursday'] , json['thursday'])
        self.assertEqual(data['friday'] , json['friday'])
        self.assertEqual(data['saturday'] , json['saturday'])
        self.assertEqual(data['sunday'] , json['sunday'])
        self.assertEqual(str(data['start_date']) , json['start_date'])
        self.assertEqual(str(data['end_date']) , json['end_date'])

        self.assertNotEqual(json['id'], None)

        logger.debug("The test_create_calendar_success test has ended successfully")
    def test_create_calendar_with_missing_field(self):
        '''
            Test to create a Calendar with missing field

        '''
        logger.debug('Starting test_create_calendar_with_missing_field')
        url = reverse('calendars-list')
        data = {
        }
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.post(url,data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        for message in json.values():
            self.assertEqual(message, ['This field is required.'])
        logger.debug("The test_create_calendar_with_missing_field test has ended successfully")
    def test_get_list_calendars_success(self):
        '''
            Test to create a Calendar with missing field

        '''
        calendar = Calendar(
            monday = True, tuesday = True, wednesday = True, thursday = True, friday = True,saturday = True,
             sunday = True, start_date = date(2023, 3, 10), end_date = date(2023, 3, 24), agency = self.agency)
        calendar.save()
        logger.debug('Starting test_get_list_calendars_success')
        url = reverse('calendars-list')
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.get(url)
        json = response.json()
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json) , 1)
        logger.debug("The test_get_list_calendars_success test has ended successfully")
    
    def test_get_list_calendars_with_empty_routes(self):
        '''
            Test to get a list of Calendars with empty list  

        '''
        logger.debug('Starting test_get_list_calendars_with_empty_routes')
        url = reverse('calendars-list')
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.get(url)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json) , 0)
        logger.debug("The test_get_list_calendars_with_empty_routes test has ended successfully")
    
    def test_get_calendar_with_id(self):
        '''
            Test to get a Calendar with id

        '''
        calendar = Calendar(
            monday = True, tuesday = True, wednesday = True, thursday = True, friday = True,saturday = True,
             sunday = True, start_date = date(2023, 3, 10), end_date = date(2023, 3, 24), agency = self.agency)
        calendar.save()
        logger.debug('Starting test_get_calendar_with_id')
        url = reverse(f'calendars-detail', kwargs = ({"pk" : calendar.id}))
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.get(url)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json['id'], calendar.id)
        self.assertEqual(json['monday'], calendar.monday)
        self.assertEqual(json['start_date'], str(calendar.start_date))
        self.assertEqual(json['agency'], self.agency.id)
        logger.debug("The test_get_calendar_with_id test has ended successfully")


    def test_get_calendar_with_non_exist_id(self):
        '''
            Test to get a Calendar with id that does not exist

        '''
        logger.debug('Starting test_get_calendar_with_non_exist_id')
        url = reverse(f'calendars-detail', kwargs = ({"pk" : 1}))
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.get(url)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json['detail'] , "Not found.")

        logger.debug("The test_get_calendar_with_non_exist_id test has ended successfully")
    def test_delete_calendar_with_id(self):
        '''
            Test to delete a Calendar with id 

        '''
        logger.debug('Starting test_delete_route_with_id')
        calendar = Calendar(
            monday = True, tuesday = True, wednesday = True, thursday = True, friday = True,saturday = True,
             sunday = True, start_date = date(2023, 3, 10), end_date = date(2023, 3, 24), agency = self.agency)
        calendar.save()
        url = reverse(f'calendars-detail', kwargs = ({"pk" : calendar.id}))
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.delete(url)
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        logger.debug("The test_delete_route_with_id test has ended successfully")
    def test_delete_calendar_with_non_exist_id(self):
        '''
            Test to delete a Calendar with id that does not exist

        '''
        logger.debug('Starting test_delete_calendar_with_non_exist_id')
        url = reverse(f'calendars-detail', kwargs = ({"pk" : 1}))
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.delete(url)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json['detail'] , "Not found.")

        logger.debug("The test_delete_calendar_with_non_exist_id test has ended successfully")
    
    def test_put_calendar_with_id(self):
        '''
            Test to update a Calendar with id 

        '''
        self.client.force_authenticate(user=self.s_admin)
        logger.debug('Starting test_put_calendar_with_id')
        calendar = Calendar(
            monday = True, tuesday = True, wednesday = True, thursday = True, friday = True,saturday = True,
             sunday = True, start_date = date(2023, 3, 10), end_date = date(2023, 3, 24), agency = self.agency)
        calendar.save()
        logger.debug('Starting test_delete_route_with_non_exist_id')
        url = reverse(f'calendars-detail', kwargs = ({"pk" : calendar.id}))
        data = {
            'monday' : False,
            'tuesday' : False,
            'wednesday' : True,
            'thursday' : True,
            'friday' : True,
            'saturday' : True,
            'sunday' : True,
            'start_date' : date(2023, 3, 1),
            'end_date' : date(2023, 3, 24),
            'agency': self.agency.id
        }
        logger.debug('Sending TEST data to url: %s\n'%url)
        response = self.client.put(url, data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d\n'%(response, response.status_code))
        print(json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json['monday'] , data["monday"])
        self.assertEqual(json['tuesday'] , data["tuesday"])
        self.assertEqual(json['start_date'] , str(data["start_date"]))

        logger.debug("The test_put_calendar_with_id test has ended successfully")
    def test_put_calendar_with_non_exist_id(self):
        '''
            Test to update a Calendars with id that does not exist

        '''
        logger.debug('Starting test_put_calendar_with_non_exist_id')
        url = reverse(f'calendars-detail', kwargs = ({"pk" : 1}))
        data = {
            'monday' : True,
            'tuesday' : True,
            'wednesday' : True,
            'thursday' : True,
            'friday' : True,
            'saturday' : True,
            'sunday' : True,
            'start_date' : date(2023, 3, 10),
            'end_date' : date(2023, 3, 24),
            'agency': self.agency.id
        }
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.put(url, data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json['detail'] , "Not found.")

        logger.debug("The test_put_calendar_with_non_exist_id test has ended successfully")
    def test_put_calendar_with_missing_fields_in_payload(self):
        '''
            Test to update a Calendar with missing field

        '''
        logger.debug('Starting test_put_calendar_with_missing_fields_in_payload')
        calendar = Calendar(
            monday = True, tuesday = True, wednesday = True, thursday = True, friday = True,saturday = True,
             sunday = True, start_date = date(2023, 3, 10), end_date = date(2023, 3, 24), agency = self.agency)
        calendar.save()
        self.client.force_authenticate(user=self.s_admin)
        logger.debug('Starting test_delete_route_with_non_exist_id')
        url = reverse(f'calendars-detail', kwargs = ({"pk" : calendar.id}))
        data = {}
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.put(url,data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        for message in json.values():
            self.assertEqual(message, ['This field is required.'])
        logger.debug("The test_put_calendar_with_missing_fields_in_payload test has ended successfully")
    def test_patch_calendar_with_id(self):
        '''
            Test to update a Calendar with id 

        '''
        self.client.force_authenticate(user=self.s_admin)
        logger.debug('Starting test_patch_calendar_with_id')
        calendar = Calendar(
            monday = True, tuesday = True, wednesday = True, thursday = True, friday = True,saturday = True,
             sunday = True, start_date = date(2023, 3, 10), end_date = date(2023, 3, 24), agency = self.agency)
        calendar.save()
        logger.debug('Starting test_delete_route_with_non_exist_id')
        url = reverse(f'calendars-detail', kwargs = ({"pk" : calendar.id}))
        data = {
            'monday' : False,
            'tuesday' : False,
            'wednesday' : True,
            'thursday' : True,
            'friday' : True,
            'saturday' : True,
            'sunday' : True,
            'start_date' : date(2023, 3, 1),
            'end_date' : date(2023, 3, 24),
            'agency': self.agency.id
        }
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.patch(url, data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in ['monday', 'tuesday', 'start_date']:
            self.assertEqual(str(json[key]) , str(data[key]))

        logger.debug("The test_patch_calendar_with_id test has ended successfully")
    def test_patch_calendar_with_non_exist_id(self):
        '''
            Test to update a Calendars with id that does not exist

        '''
        logger.debug('Starting test_patch_calendar_with_non_exist_id')
        url = reverse(f'calendars-detail', kwargs = ({"pk" : 1}))
        data = {
            'monday' : True,
            'tuesday' : True,
            'wednesday' : True,
            'thursday' : True,
            'friday' : True,
            'saturday' : True,
            'sunday' : True,
            'start_date' : date(2023, 3, 10),
            'end_date' : date(2023, 3, 24),
            'agency': self.agency.id
        }
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.patch(url, data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json['detail'] , "Not found.")

        logger.debug("The test_patch_calendar_with_non_exist_id test has ended successfully")
    def test_patch_calendar_with_missing_fields_in_payload(self):
        '''
            Test to update a Calendar with missing field

        '''
        logger.debug('Starting test_patch_calendar_with_missing_fields_in_payload')
        calendar = Calendar(
            monday = True, tuesday = True, wednesday = True, thursday = True, friday = True,saturday = True,
             sunday = True, start_date = date(2023, 3, 10), end_date = date(2023, 3, 24), agency = self.agency)
        calendar.save()
        self.client.force_authenticate(user=self.s_admin)
        logger.debug('Starting test_delete_route_with_non_exist_id')
        url = reverse(f'calendars-detail', kwargs = ({"pk" : calendar.id}))
        data = {}
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.patch(url,data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(calendar.id, json['id'])
        logger.debug("The test_patch_calendar_with_missing_fields_in_payload test has ended successfully")
        