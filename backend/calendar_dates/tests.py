from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase,force_authenticate,APIClient
from admins.models import Admin, USER_TYPES
from agencies.models import Agency
from calendars.models import Calendar
from .models import CalendarDate, ExceptionType
from datetime import date
import logging
logger = logging.getLogger(__name__)
class CAlendarDateViewSetTests(APITestCase):
    def setUp(self):
        logger.debug('Adding a new admin, system admin, calendar and agency into database')
        self.s_admin = Admin(username='admins@gmail.com', password='admins1234', first_name = 'admins', last_name = 'admins', email = 'admins@gamil.com', user_type =  USER_TYPES[0][0])
        self.s_admin.save()
        self.admin = Admin(username='admin@gmail.com', password='admin1234', first_name = 'admin', last_name = 'admin', email = 'admin@gamil.com', user_type =  USER_TYPES[1][0])
        self.admin.save()
        
        self.agency = Agency(name = 'bus1', url = 'http://127.0.0.1:8000/', lang='en', time_zone='+3', phone = '+251991439281', admin = self.s_admin)
        self.agency.save()

        self.calendar = Calendar(
            monday = True, tuesday = True, wednesday = True, thursday = True, friday = True,saturday = True,
             sunday = True, start_date = date(2023, 3, 10), end_date = date(2023, 3, 24), agency = self.agency)
        self.calendar.save()
        

        self.client = APIClient()
        logger.debug('Successfully added test admin, system admin, calendar and agency into the database')
    def test_create_calendar_date_success(self):

        '''
            Test to create a CalendarDate success

        '''
        logger.debug('Starting test_create_calendar_date_success')
        url = reverse('calendar_dates-list')
        data = {
            'service' : self.calendar.id,
            'exception_type' : ExceptionType[0][0],
            'date' : date(2023, 3, 29)
        }
        logger.debug('Sending TEST data to url: %s'%url)
        # self.client.force_authenticate(user=self.admin)
        response = self.client.post(url,data)
        json = response.json()

        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code)) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key in data:
            self.assertEqual(str(data[key]), str(json[key]))
        self.assertNotEqual(json['id'], None)

        logger.debug("The test_create_calendar_date_success test has ended successfully")
    def test_create_calendar_date_with_missing_field(self):
        '''
            Test to create a CalendarDate with missing field

        '''
        logger.debug('Starting test_create_calendar_date_with_missing_field')
        url = reverse('calendar_dates-list')
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
        logger.debug("The test_create_calendar_date_with_missing_field test has ended successfully")
    def test_get_list_calendar_dates_success(self):
        '''
            Test to get a list of CalendarDates 

        '''
        calendar_date = CalendarDate(service = self.calendar, exception_type = ExceptionType[0][0], date = date(2023, 3, 29))
        calendar_date.save()
        logger.debug('Starting test_get_list_calendars_success')
        url = reverse('calendars-list')
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.get(url)
        json = response.json()
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json) , 1)
        logger.debug("The test_get_list_calendar_dates_success test has ended successfully")
    
    def test_get_list_calendar_dates_with_empty_routes(self):
        '''
            Test to get a list of CalendarDates with empty list  

        '''
        logger.debug('Starting test_get_list_calendar_dates_with_empty_routes')
        url = reverse('calendar_dates-list')
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.get(url)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json) , 0)
        logger.debug("The test_get_list_calendar_dates_with_empty_routes test has ended successfully")
    
    def test_get_calendar_with_id(self):
        '''
            Test to get a Calendar with id

        '''
        calendar_date = CalendarDate(service = self.calendar, exception_type = ExceptionType[0][0], date = date(2023, 3, 29))
        calendar_date.save()
        logger.debug('Starting test_get_calendar_with_id')
        url = reverse(f'calendar_dates-detail', kwargs = ({"pk" : calendar_date.id}))
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.get(url)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json['id'], calendar_date.id)
        self.assertEqual(json['service'], calendar_date.service.id)
        self.assertEqual(json['date'], str(calendar_date.date))
        self.assertEqual(json['exception_type'], calendar_date.exception_type)
        logger.debug("The test_get_calendar_with_id test has ended successfully")


    def test_get_calendar_date_with_non_exist_id(self):
        '''
            Test to get a CalendarDate with id that does not exist

        '''
        logger.debug('Starting test_get_calendar_date_with_non_exist_id')
        url = reverse(f'calendar_dates-detail', kwargs = ({"pk" : 1}))
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.get(url)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json['detail'] , "Not found.")

        logger.debug("The test_get_calendar_date_with_non_exist_id test has ended successfully")
    def test_delete_calendar_date_with_id(self):
        '''
            Test to delete a CalendarDate with id 

        '''
        logger.debug('Starting test_delete_calendar_date_with_id')
        calendar_date = CalendarDate(service = self.calendar, exception_type = ExceptionType[0][0], date = date(2023, 3, 29))
        calendar_date.save()
        url = reverse(f'calendar_dates-detail', kwargs = ({"pk" : calendar_date.id}))
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.delete(url)
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        logger.debug("The test_delete_calendar_date_with_id test has ended successfully")
    def test_delete_calendar_date_with_non_exist_id(self):
        '''
            Test to delete a CalendarDate with id that does not exist

        '''
        logger.debug('Starting test_delete_calendar_date_with_id')
        url = reverse(f'calendar_dates-detail', kwargs = ({"pk" : 1}))
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.delete(url)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json['detail'] , "Not found.")

        logger.debug("The test_delete_calendar_date_with_id test has ended successfully")
    
    def test_put_calendar_date_with_id(self):
        '''
            Test to update a CalendarDate with id 

        '''
        self.client.force_authenticate(user=self.s_admin)
        logger.debug('Starting test_put_calendar_with_id')
        logger.debug('Starting test_put_calendar_date_with_id')
        calendar_date = CalendarDate(service = self.calendar, exception_type = ExceptionType[0][0], date = date(2023, 3, 29))
        calendar_date.save()
        url = reverse(f'calendar_dates-detail', kwargs = ({"pk" : calendar_date.id}))
        data = {
            'service' : self.calendar.id,
            'exception_type' : ExceptionType[0][0],
            'date' : date(2023, 3, 29)
        }
        logger.debug('Sending TEST data to url: %s\n'%url)
        response = self.client.put(url, data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d\n'%(response, response.status_code))
        print(json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in data:
            self.assertEqual(str(json[key]), str(data[key]))
        

        logger.debug("The test_put_calendar_date_with_id test has ended successfully")
    def test_put_calendar_date_with_non_exist_id(self):
        '''
            Test to update a CalendarDates with id that does not exist

        '''
        logger.debug('Starting test_put_calendar_date_with_non_exist_id')
        url = reverse(f'calendar_dates-detail', kwargs = ({"pk" : 1}))
        data = {
            'service' : self.calendar.id,
            'exception_type' : ExceptionType[0][0],
            'date' : date(2023, 3, 29)
        }
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.put(url, data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json['detail'] , "Not found.")

        logger.debug("The test_put_calendar_date_with_non_exist_id test has ended successfully")
    def test_put_calendar_dates_with_missing_fields_in_payload(self):
        '''
            Test to update a CalendarDates with missing field

        '''
        logger.debug('Starting test_put_calendar_dates_with_missing_fields_in_payload')
        calendar_date = CalendarDate(service = self.calendar, exception_type = ExceptionType[0][0], date = date(2023, 3, 29))
        calendar_date.save()
        self.client.force_authenticate(user=self.s_admin)
        logger.debug('Starting test_delete_route_with_non_exist_id')
        url = reverse(f'calendar_dates-detail', kwargs = ({"pk" : calendar_date.id}))
        data = {}
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.put(url,data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        for message in json.values():
            self.assertEqual(message, ['This field is required.'])
        logger.debug("The test_put_calendar_dates_with_missing_fields_in_payload test has ended successfully")
    def test_patch_calendar_date_with_id(self):
        '''
            Test to update a CalendarDate with id 

        '''
        self.client.force_authenticate(user=self.s_admin)
        logger.debug('Starting test_patch_calendar_date_with_id')
        calendar_date = CalendarDate(service = self.calendar, exception_type = ExceptionType[0][0], date = date(2023, 3, 29))
        calendar_date.save()
        logger.debug('Starting test_delete_route_with_non_exist_id')
        url = reverse(f'calendar_dates-detail', kwargs = ({"pk" : calendar_date.id}))
        data = {
            'service' : self.calendar.id,
            'exception_type' : ExceptionType[1][0],
            'date' : date(2023, 10, 29)
        }
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.patch(url, data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in ['exception_type', 'date']:
            self.assertEqual(str(json[key]) , str(data[key]))

        logger.debug("The test_patch_calendar_date_with_id test has ended successfully")
    def test_patch_calendar_date_with_non_exist_id(self):
        '''
            Test to update a CalendarDates with id that does not exist

        '''
        logger.debug('Starting test_patch_calendar_date_with_non_exist_id')
        url = reverse(f'calendar_dates-detail', kwargs = ({"pk" : 1}))
        data = {
            'service' : self.calendar.id,
            'exception_type' : ExceptionType[1][0],
            'exception_type' : date(2023, 10, 29)
        }
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.patch(url, data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json['detail'] , "Not found.")

        logger.debug("The test_patch_calendar_date_with_non_exist_id test has ended successfully")
    def test_patch_calendar_date_with_missing_fields_in_payload(self):
        '''
            Test to update a CalendarDates with missing field

        '''
        logger.debug('Starting test_patch_calendar_date_with_missing_fields_in_payload')
        calendar_date = CalendarDate(service = self.calendar, exception_type = ExceptionType[0][0], date = date(2023, 3, 29))
        calendar_date.save()
        self.client.force_authenticate(user=self.s_admin)
        logger.debug('Starting test_delete_route_with_non_exist_id')
        url = reverse(f'calendar_dates-detail', kwargs = ({"pk" : calendar_date.id}))
        data = {}
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.patch(url,data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(calendar_date.id, json['id'])
        logger.debug("The test_patch_calendar_date_with_missing_fields_in_payload test has ended successfully")
        