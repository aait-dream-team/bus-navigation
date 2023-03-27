from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase,force_authenticate,APIClient
from admins.models import Admin, USER_TYPES
from agencies.models import Agency
from stops.models import Stop, LocationType
from trips.models import Trip
from .models import StopTime
from datetime import time


import logging
logger = logging.getLogger(__name__)

class StopTimeViewSetTests(APITestCase):
    def setUp(self):
        logger.debug('Adding a new admin, system admin, calendar and agency into database')
        self.s_admin = Admin(username='admins@gmail.com', password='admins1234', first_name = 'admins', last_name = 'admins', email = 'admins@gamil.com', user_type =  USER_TYPES[0][0])
        self.s_admin.save()
        self.admin = Admin(username='admin@gmail.com', password='admin1234', first_name = 'admin', last_name = 'admin', email = 'admin@gamil.com', user_type =  USER_TYPES[1][0])
        self.admin.save()
        
        self.agency = Agency(name = 'bus1', url = 'http://127.0.0.1:8000/', lang='en', time_zone='+3', phone = '+251991439281', admin = self.s_admin)
        self.agency.save()

        
        self.parent_station = Stop(stop_name = 's1', stop_desc = 'stop1' , stop_code = 'j8', stop_lat = '5343', stop_long = '7834', 
                                    stop_url = 'http://localhost:8000/stop_times/', location_type = LocationType[0][0], 
                                    admin = self.admin )
        self.parent_station.save()


        self.stop = Stop(stop_name = 's1', stop_desc = 'stop1' , stop_code = 'j8', stop_lat = '5343', stop_long = '7834', 
                                    stop_url = 'http://localhost:8000/stop_times/', location_type = LocationType[0][0], 
                                    admin = self.admin, parent_station = self.parent_station)
        self.stop.save()

        self.trip = Trip(headsign = 'headsign', direction = True, short_name = 'short_name', agency = self.agency)
        self.trip.save()

        self.client = APIClient()
        logger.debug('Successfully added test admin, system admin, calendar and agency into the database')
    def test_create_stop_times_success(self):

        '''
            Test to create a Stop success

        '''
        # arrival_time = datetime.time(hour=2, minute=13, second=34, microsecond=342443)

        logger.debug('Starting test_create_stop_times_success')
        url = reverse('stop_times-list')
        data = {
            'arrival_time' : time(hour = 2, minute = 13, second=45),
            'departure_time' : time(hour = 2, minute = 18, second=00),
            'stop_sequence' : 2,
            'stop_headsign' : 'headsign',
            'agency' : self.agency.id,
            'trip' : self.trip.id,
            'stop' : self.stop.id
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
        logger.debug("The test_create_stop_times_success test has ended successfully")
    def test_create_stop_times_with_missing_field(self):
        '''
            Test to create a Stop with missing field

        '''
        logger.debug('Starting test_create_stop_times_with_missing_field')
        url = reverse('stop_times-list')
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
        logger.debug("The test_create_stop_times_with_missing_field test has ended successfully")
    def test_get_list_stop_times_success(self):
        '''
            Test to get a list of stop_times 

        '''
        stop_times = StopTime( arrival_time = time(hour = 2, minute = 13, second=45), departure_time = time(hour = 2, minute = 18, second=00), stop_sequence = 2, stop_headsign = 'headsign',
                            agency = self.agency, stop = self.stop, trip = self.trip)
        stop_times.save()
        logger.debug('Starting test_get_list_calendars_success')
        url = reverse('calendars-list')
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.get(url)
        json = response.json()
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json) , 0)
        logger.debug("The test_get_list_stop_times_success test has ended successfully")
    
    def test_get_list_stop_times_with_empty_routes(self):
        '''
            Test to get a list of stop_times with empty list  

        '''
        logger.debug('Starting test_get_list_stop_times_with_empty_routes')
        url = reverse('stop_times-list')
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.get(url)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json) , 0)
        logger.debug("The test_get_list_stop_times_with_empty_routes test has ended successfully")
    
    def test_get_stop_times_with_id(self):
        '''
            Test to get a stop_times with id

        '''
        stop_times = StopTime( arrival_time = time(hour = 2, minute = 13, second=45), departure_time = time(hour = 2, minute = 18, second=00), stop_sequence = 2, stop_headsign = 'headsign',
                            agency = self.agency, stop = self.stop, trip = self.trip)
        stop_times.save()
        logger.debug('Starting test_get_stop_times_with_id')
        url = reverse(f'stop_times-detail', kwargs = ({"pk" : stop_times.id}))
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.get(url)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json['id'], stop_times.id)
        data = vars(stop_times)
        for key in json:
            if key in ['trip', 'stop', 'agency']:
                self.assertEqual(str(data[key+'_id']), str(json[key]))
                continue
            self.assertEqual(str(data[key]), str(json[key]))
        logger.debug("The test_get_stop_times_with_id test has ended successfully")


    def test_get_stop_times_with_non_exist_id(self):
        '''
            Test to get a Stop with id that does not exist

        '''
        logger.debug('Starting test_get_stop_times_with_non_exist_id')
        url = reverse(f'stop_times-detail', kwargs = ({"pk" : 1}))
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.get(url)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json['detail'] , "Not found.")

        logger.debug("The test_get_stop_times_with_non_exist_id test has ended successfully")
    def test_delete_stop_times_with_id(self):
        '''
            Test to delete a Stop with id 

        '''
        logger.debug('Starting test_delete_stop_times_with_id')
        stop_times = StopTime( arrival_time = time(hour = 2, minute = 13, second=45), departure_time = time(hour = 2, minute = 18, second=00), stop_sequence = 2, stop_headsign = 'headsign',
                            agency = self.agency, stop = self.stop, trip = self.trip)
        stop_times.save()
        url = reverse(f'stop_times-detail', kwargs = ({"pk" : stop_times.id}))
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.delete(url)
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        logger.debug("The test_delete_stop_times_with_id test has ended successfully")
    def test_delete_stop_times_with_non_exist_id(self):
        '''
            Test to delete a Stop with id that does not exist

        '''
        logger.debug('Starting test_delete_stop_times_with_id')
        url = reverse(f'stop_times-detail', kwargs = ({"pk" : 10}))
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.delete(url)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json['detail'] , "Not found.")

        logger.debug("The test_delete_stop_times_with_id test has ended successfully")
    
    def test_put_stop_times_with_id(self):
        '''
            Test to update a Stop with id 

        '''
        self.client.force_authenticate(user=self.s_admin)
        logger.debug('Starting test_put_calendar_with_id')
        logger.debug('Starting test_put_stop_times_with_id')
        stop_times = StopTime( arrival_time = time(hour = 2, minute = 13, second=45), departure_time = time(hour = 2, minute = 18, second=00), stop_sequence = 2, stop_headsign = 'headsign',
                            agency = self.agency, stop = self.stop, trip = self.trip)
        stop_times.save()
        url = reverse(f'stop_times-detail', kwargs = ({"pk" : stop_times.id}))
        data = {
            'arrival_time' : time(hour = 2, minute = 13, second=45),
            'departure_time' : time(hour = 2, minute = 18, second=00),
            'stop_sequence' : 2,
            'stop_headsign' : 'headsign',
            'agency' : self.agency.id,
            'trip' : self.trip.id,
            'stop' : self.stop.id
        }
        self.client.force_authenticate(user=self.s_admin) # TODO it works with s_admin this should not be this case 
        logger.debug('Sending TEST data to url: %s\n'%url)
        response = self.client.put(url, data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d\n'%(response, response.status_code))
        # print(json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in data:
            self.assertEqual(str(json[key]), str(data[key]))
        
        logger.debug("The test_put_stop_times_with_id test has ended successfully")

    def test_put_stop_times_with_non_exist_id(self):
        '''
            Test to update a stop_times with id that does not exist

        '''
        logger.debug('Starting test_put_stop_times_with_non_exist_id')
        url = reverse(f'stop_times-detail', kwargs = ({"pk" : 1}))
        data = {
            'arrival_time' : time(hour = 2, minute = 13, second=45),
            'departure_time' : time(hour = 2, minute = 18, second=00),
            'stop_sequence' : 2,
            'stop_headsign' : 'headsign',
            'agency' : self.agency.id,
            'trip' : self.trip.id,
            'stop' : self.stop.id
        }
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.put(url, data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json['detail'] , "Not found.")

        logger.debug("The test_put_stop_times_with_non_exist_id test has ended successfully")

    def test_put_stop_times_with_missing_fields_in_payload(self):
        '''
            Test to update a stop_times with missing field

        '''
        logger.debug('Starting test_put_stop_times_with_missing_fields_in_payload')
        stop_times = StopTime( arrival_time = time(hour = 2, minute = 13, second=45), departure_time = time(hour = 2, minute = 18, second=00), stop_sequence = 2, stop_headsign = 'headsign',
                            agency = self.agency, stop = self.stop, trip = self.trip)
        stop_times.save()
        self.client.force_authenticate(user=self.s_admin)
        logger.debug('Starting test_delete_route_with_non_exist_id')
        url = reverse(f'stop_times-detail', kwargs = ({"pk" : stop_times.id}))
        data = {}
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.put(url,data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        for message in json.values():
            self.assertEqual(message, ['This field is required.'])
        logger.debug("The test_put_stop_times_with_missing_fields_in_payload test has ended successfully")

    def test_patch_stop_times_with_id(self):
        '''
            Test to update a Stop with id 

        '''
        self.client.force_authenticate(user=self.s_admin)
        logger.debug('Starting test_patch_stop_times_with_id')
        stop_times = StopTime( arrival_time = time(hour = 2, minute = 13, second=45), departure_time = time(hour = 2, minute = 18, second=00), stop_sequence = 2, stop_headsign = 'headsign',
                            agency = self.agency, stop = self.stop, trip = self.trip)
        stop_times.save()
        logger.debug('Starting test_delete_route_with_non_exist_id')
        url = reverse(f'stop_times-detail', kwargs = ({"pk" : stop_times.id}))
        data = {
            'arrival_time' : time(hour = 2, minute = 14, second=45),
            'departure_time' : time(hour = 2, minute = 20, second=00),
            'stop_sequence' : 3,
            'stop_headsign' : 'headsign',
            'agency' : self.agency.id,
            'trip' : self.trip.id,
            'stop' : self.stop.id
        }
        self.client.force_authenticate(user=self.s_admin)
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.patch(url, data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in ['arrival_time', 'departure_time', 'stop_sequence']:
            self.assertEqual(str(json[key]) , str(data[key]))

        logger.debug("The test_patch_stop_times_with_id test has ended successfully")
    def test_patch_stop_times_with_non_exist_id(self):
        '''
            Test to update a stop_times with id that does not exist

        '''
        logger.debug('Starting test_patch_stop_times_with_non_exist_id')
        url = reverse(f'stop_times-detail', kwargs = ({"pk" : 1}))
        data = {
            'arrival_time' : time(hour = 2, minute = 14, second=45),
            'departure_time' : time(hour = 2, minute = 20, second=00),
            'stop_sequence' : 3,
            'stop_headsign' : 'headsign',
            'agency' : self.agency.id,
            'trip' : self.trip.id,
            'stop' : self.stop.id
        }
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.patch(url, data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json['detail'] , "Not found.")

        logger.debug("The test_patch_stop_times_with_non_exist_id test has ended successfully")

    def test_patch_stop_times_with_missing_fields_in_payload(self):
        '''
            Test to update a stop_times with missing field

        '''
        logger.debug('Starting test_patch_stop_times_with_missing_fields_in_payload')
        stop_times = StopTime( arrival_time = time(hour = 2, minute = 13, second=45), departure_time = time(hour = 2, minute = 18, second=00), stop_sequence = 2, stop_headsign = 'headsign',
                            agency = self.agency, stop = self.stop, trip = self.trip)
        stop_times.save()
        self.client.force_authenticate(user=self.s_admin)
        logger.debug('Starting test_delete_route_with_non_exist_id')
        url = reverse(f'stop_times-detail', kwargs = ({"pk" : stop_times.id}))
        data = {}
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.patch(url,data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(stop_times.id, json['id'])
        logger.debug("The test_patch_stop_times_with_missing_fields_in_payload test has ended successfully")
        