from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase,force_authenticate,APIClient
from admins.models import Admin, USER_TYPES
from agencies.models import Agency
from calendars.models import Calendar
from .models import Stop, LocationType
from datetime import date
import logging
logger = logging.getLogger(__name__)
class StopViewSetTests(APITestCase):
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
        
        self.parent_station = Stop(stop_name = 's1', stop_desc = 'stop1' , stop_code = 'j8', stop_lat = '5343', stop_long = '7834', 
                                    stop_url = 'http://localhost:8000/stops/', location_type = LocationType[0][0], 
                                    admin = self.admin )
        self.parent_station.save()

        self.client = APIClient()
        logger.debug('Successfully added test admin, system admin, calendar and agency into the database')
    def test_create_stops_success(self):

        '''
            Test to create a Stop success

        '''
        logger.debug('Starting test_create_stops_success')
        url = reverse('stops-list')
        data = {
            'stop_name' : 's1',
            'stop_desc' : 'stop1',
            'stop_lat' : '7878',
            'stop_long' : '7878',
            'stop_code' : 'j8',
            'stop_url' : 'http://localhost:8000/stops/',
            'location_type' : LocationType[0][0],
            'admin' : self.admin.id,
            'parent_station' : self.parent_station.id,
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
        logger.debug("The test_create_stops_success test has ended successfully")
    def test_create_stops_with_missing_field(self):
        '''
            Test to create a Stop with missing field

        '''
        logger.debug('Starting test_create_stops_with_missing_field')
        url = reverse('stops-list')
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
        logger.debug("The test_create_stops_with_missing_field test has ended successfully")
    def test_get_list_stops_success(self):
        '''
            Test to get a list of Stops 

        '''
        stops = Stop(stop_name = 's1', stop_desc = 'stop1' , stop_code = 'j8', stop_lat = '5343', stop_long = '7834', 
                         stop_url = 'http://localhost:8000/stops/', location_type = LocationType[0][0],
                          admin = self.admin , parent_station = self.parent_station)
        stops.save()
        logger.debug('Starting test_get_list_calendars_success')
        url = reverse('calendars-list')
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.get(url)
        json = response.json()
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json) , 1)
        logger.debug("The test_get_list_stops_success test has ended successfully")
    
    def test_get_list_stops_with_empty_routes(self):
        '''
            Test to get a list of Stops with empty list  

        '''
        logger.debug('Starting test_get_list_stops_with_empty_routes')
        url = reverse('stops-list')
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.get(url)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json) , 1)
        logger.debug("The test_get_list_stops_with_empty_routes test has ended successfully")
    
    def test_get_calendar_with_id(self):
        '''
            Test to get a Calendar with id

        '''
        stops = Stop(stop_name = 's1', stop_desc = 'stop1' , stop_code = 'j8', stop_lat = '5343', stop_long = '7834', 
                      stop_url = 'http://localhost:8000/stops/', location_type = LocationType[0][0], 
                      admin = self.admin , parent_station = self.parent_station)
        stops.save()
        logger.debug('Starting test_get_calendar_with_id')
        url = reverse(f'stops-detail', kwargs = ({"pk" : stops.id}))
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.get(url)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json['id'], stops.id)
        data = vars(stops)
        print(vars(stops))
        for key in json:
            if key in ['admin', 'parent_station']:
                self.assertEqual(str(data[key+'_id']), str(json[key]))
                continue
            self.assertEqual(str(data[key]), str(json[key]))
        print(stops.__dict__)
        logger.debug("The test_get_calendar_with_id test has ended successfully")


    def test_get_stops_with_non_exist_id(self):
        '''
            Test to get a Stop with id that does not exist

        '''
        logger.debug('Starting test_get_stops_with_non_exist_id')
        url = reverse(f'stops-detail', kwargs = ({"pk" : 1}))
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.get(url)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json['detail'] , "Not found.")

        logger.debug("The test_get_stops_with_non_exist_id test has ended successfully")
    def test_delete_stops_with_id(self):
        '''
            Test to delete a Stop with id 

        '''
        logger.debug('Starting test_delete_stops_with_id')
        stops = Stop(stop_name = 's1', stop_desc = 'stop1' , stop_code = 'j8', stop_lat = '5343', stop_long = '7834', 
                      stop_url = 'http://localhost:8000/stops/', location_type = LocationType[0][0], 
                      admin = self.admin , parent_station = self.parent_station)
        stops.save()
        url = reverse(f'stops-detail', kwargs = ({"pk" : stops.id}))
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.delete(url)
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        logger.debug("The test_delete_stops_with_id test has ended successfully")
    def test_delete_stops_with_non_exist_id(self):
        '''
            Test to delete a Stop with id that does not exist

        '''
        logger.debug('Starting test_delete_stops_with_id')
        url = reverse(f'stops-detail', kwargs = ({"pk" : 10}))
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.delete(url)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json['detail'] , "Not found.")

        logger.debug("The test_delete_stops_with_id test has ended successfully")
    
    def test_put_stops_with_id(self):
        '''
            Test to update a Stop with id 

        '''
        self.client.force_authenticate(user=self.s_admin)
        logger.debug('Starting test_put_calendar_with_id')
        logger.debug('Starting test_put_stops_with_id')
        stops = Stop(stop_name = 's1', stop_desc = 'stop1' , stop_code = 'j8', stop_lat = '5343', stop_long = '7834', 
                      stop_url = 'http://localhost:8000/stops/', location_type = LocationType[0][0], 
                      admin = self.admin , parent_station = self.parent_station)
        stops.save()
        url = reverse(f'stops-detail', kwargs = ({"pk" : stops.id}))
        data = {
            'stop_name' : 's1',
            'stop_desc' : 'stop1',
            'stop_lat' : '7878',
            'stop_long' : '7878',
            'stop_code' : 'j8',
            'stop_url' : 'http://localhost:8000/stops/',
            'location_type' : LocationType[0][0],
            'admin' : self.admin.id,
            'parent_station' : self.parent_station.id,
        }
        self.client.force_authenticate(user=self.admin)
        logger.debug('Sending TEST data to url: %s\n'%url)
        response = self.client.put(url, data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d\n'%(response, response.status_code))
        # print(json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in data:
            self.assertEqual(str(json[key]), str(data[key]))
        

        logger.debug("The test_put_stops_with_id test has ended successfully")
    def test_put_stops_with_non_exist_id(self):
        '''
            Test to update a Stops with id that does not exist

        '''
        logger.debug('Starting test_put_stops_with_non_exist_id')
        url = reverse(f'stops-detail', kwargs = ({"pk" : 1}))
        data = {
            'stop_name' : 's1',
            'stop_desc' : 'stop1',
            'stop_lat' : '7878',
            'stop_long' : '7878',
            'stop_code' : 'j8',
            'stop_url' : 'http://localhost:8000/stops/',
            'location_type' : LocationType[0][0],
            'admin' : self.admin.id,
            'parent_station' : self.parent_station.id,
        }
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.put(url, data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json['detail'] , "Not found.")

        logger.debug("The test_put_stops_with_non_exist_id test has ended successfully")
    def test_put_stops_with_missing_fields_in_payload(self):
        '''
            Test to update a Stops with missing field

        '''
        logger.debug('Starting test_put_stops_with_missing_fields_in_payload')
        stops = Stop(stop_name = 's1', stop_desc = 'stop1' , stop_code = 'j8', stop_lat = '5343', stop_long = '7834', 
                      stop_url = 'http://localhost:8000/stops/', location_type = LocationType[0][0], 
                      admin = self.admin , parent_station = self.parent_station)
        stops.save()
        self.client.force_authenticate(user=self.admin)
        logger.debug('Starting test_delete_route_with_non_exist_id')
        url = reverse(f'stops-detail', kwargs = ({"pk" : stops.id}))
        data = {}
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.put(url,data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        for message in json.values():
            self.assertEqual(message, ['This field is required.'])
        logger.debug("The test_put_stops_with_missing_fields_in_payload test has ended successfully")
    def test_patch_stops_with_id(self):
        '''
            Test to update a Stop with id 

        '''
        self.client.force_authenticate(user=self.s_admin)
        logger.debug('Starting test_patch_stops_with_id')
        stops = Stop(stop_name = 's1', stop_desc = 'stop1' , stop_code = 'j8', stop_lat = '5343', stop_long = '7834', 
                      stop_url = 'http://localhost:8000/stops/', location_type = LocationType[0][0], 
                      admin = self.admin , parent_station = self.parent_station)
        stops.save()
        logger.debug('Starting test_delete_route_with_non_exist_id')
        url = reverse(f'stops-detail', kwargs = ({"pk" : stops.id}))
        data = {
            'stop_name' : 's1',
            'stop_desc' : 'stop12',
            'stop_lat' : '78782',
            'stop_long' : '78782',
            'stop_code' : 'j8',
            'stop_url' : 'http://localhost:8000/stops/',
            'location_type' : LocationType[0][0],
            'admin' : self.admin.id,
            'parent_station' : self.parent_station.id,
        }
        self.client.force_authenticate(user=self.admin)
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.patch(url, data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in ['stop_desc', 'stop_lat', 'stop_long']:
            self.assertEqual(str(json[key]) , str(data[key]))

        logger.debug("The test_patch_stops_with_id test has ended successfully")
    def test_patch_stops_with_non_exist_id(self):
        '''
            Test to update a Stops with id that does not exist

        '''
        logger.debug('Starting test_patch_stops_with_non_exist_id')
        url = reverse(f'stops-detail', kwargs = ({"pk" : 1}))
        data = {
            'stop_name' : 's1',
            'stop_desc' : 'stop12',
            'stop_lat' : '78782',
            'stop_long' : '78782',
            'stop_code' : 'j8',
            'stop_url' : 'http://localhost:8000/stops/',
            'location_type' : LocationType[0][0],
            'admin' : self.admin.id,
            'parent_station' : self.parent_station.id,
        }
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.patch(url, data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json['detail'] , "Not found.")

        logger.debug("The test_patch_stops_with_non_exist_id test has ended successfully")
    def test_patch_stops_with_missing_fields_in_payload(self):
        '''
            Test to update a Stops with missing field

        '''
        logger.debug('Starting test_patch_stops_with_missing_fields_in_payload')
        stops = Stop(stop_name = 's1', stop_desc = 'stop1' , stop_code = 'j8', stop_lat = '5343', stop_long = '7834', 
                      stop_url = 'http://localhost:8000/stops/', location_type = LocationType[0][0], 
                      admin = self.admin , parent_station = self.parent_station)
        stops.save()
        self.client.force_authenticate(user=self.admin)
        logger.debug('Starting test_delete_route_with_non_exist_id')
        url = reverse(f'stops-detail', kwargs = ({"pk" : stops.id}))
        data = {}
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.patch(url,data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(stops.id, json['id'])
        logger.debug("The test_patch_stops_with_missing_fields_in_payload test has ended successfully")
        