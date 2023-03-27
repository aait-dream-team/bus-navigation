from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase,force_authenticate,APIClient
from admins.models import Admin, USER_TYPES
from agencies.models import Agency
from stops.models import Stop, LocationType
from .models import Transfer, TransferType


import logging
logger = logging.getLogger(__name__)
class TransferViewSetTests(APITestCase):
    def setUp(self):
        logger.debug('Adding a new admin, system admin, calendar and agency into database')
        self.s_admin = Admin(username='admins@gmail.com', password='admins1234', first_name = 'admins', last_name = 'admins', email = 'admins@gamil.com', user_type =  USER_TYPES[0][0])
        self.s_admin.save()
        self.admin = Admin(username='admin@gmail.com', password='admin1234', first_name = 'admin', last_name = 'admin', email = 'admin@gamil.com', user_type =  USER_TYPES[1][0])
        self.admin.save()
        
        self.agency = Agency(name = 'bus1', url = 'http://127.0.0.1:8000/', lang='en', time_zone='+3', phone = '+251991439281', admin = self.s_admin)
        self.agency.save()

        
        self.parent_station = Stop(stop_name = 's1', stop_desc = 'stop1' , stop_code = 'j8', stop_lat = '5343', stop_long = '7834', 
                                    stop_url = 'http://localhost:8000/transfers/', location_type = LocationType[0][0], 
                                    admin = self.admin )
        self.parent_station.save()


        self.from_stop = Stop(stop_name = 's1', stop_desc = 'stop1' , stop_code = 'j8', stop_lat = '5343', stop_long = '7834', 
                                    stop_url = 'http://localhost:8000/transfers/', location_type = LocationType[0][0], 
                                    admin = self.admin, parent_station = self.parent_station)
        self.from_stop.save()

        self.to_stop = Stop(stop_name = 's1', stop_desc = 'stop1' , stop_code = 'j8', stop_lat = '4321', stop_long = '1234', 
                            stop_url = 'http://localhost:8000/transfers/', location_type = LocationType[0][0], 
                            admin = self.admin, parent_station = self.parent_station)
        self.to_stop.save()

        self.client = APIClient()
        logger.debug('Successfully added test admin, system admin, calendar and agency into the database')
    def test_create_transfers_success(self):

        '''
            Test to create a Stop success

        '''
        # arrival_time = datetime.time(hour=2, minute=13, second=34, microsecond=342443)

        logger.debug('Starting test_create_transfers_success')
        url = reverse('transfers-list')
        data = {
            'to_stop' : self.to_stop.id,
            'from_stop' : self.from_stop.id,
            'transfer_type' : TransferType[0][0],
            'min_transfer_time' : 500,
            'admin' : self.admin.id,
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
        logger.debug("The test_create_transfers_success test has ended successfully")
    def test_create_transfers_with_missing_field(self):
        '''
            Test to create a Stop with missing field

        '''
        logger.debug('Starting test_create_transfers_with_missing_field')
        url = reverse('transfers-list')
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
        logger.debug("The test_create_transfers_with_missing_field test has ended successfully")

    def test_get_list_transfers_success(self):
        '''
            Test to get a list of transfers 

        '''
        transfers = Transfer(to_stop = self.to_stop, from_stop = self.from_stop, transfer_type = TransferType[0][0],
                             min_transfer_time = 500, admin = self.admin)
        transfers.save()
        logger.debug('Starting test_get_list_calendars_success')
        url = reverse('calendars-list')
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.get(url)
        json = response.json()
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json) , 0)
        logger.debug("The test_get_list_transfers_success test has ended successfully")
    
    def test_get_list_transfers_with_empty_routes(self):
        '''
            Test to get a list of transfers with empty list  

        '''
        logger.debug('Starting test_get_list_transfers_with_empty_routes')
        url = reverse('transfers-list')
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.get(url)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json) , 0)
        logger.debug("The test_get_list_transfers_with_empty_routes test has ended successfully")
    
    def test_get_transfers_with_id(self):
        '''
            Test to get a transfers with id

        '''
        transfers = Transfer(to_stop = self.to_stop, from_stop = self.from_stop, transfer_type = TransferType[0][0],
                             min_transfer_time = 500, admin = self.admin)
        transfers.save()
        logger.debug('Starting test_get_transfers_with_id')
        url = reverse(f'transfers-detail', kwargs = ({"pk" : transfers.id}))
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.get(url)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json['id'], transfers.id)
        data = vars(transfers)
        for key in json:
            if key in ['to_stop', 'from_stop', 'admin']:
                self.assertEqual(str(data[key+'_id']), str(json[key]))
                continue
            self.assertEqual(str(data[key]), str(json[key]))
        logger.debug("The test_get_transfers_with_id test has ended successfully")


    def test_get_transfers_with_non_exist_id(self):
        '''
            Test to get a Stop with id that does not exist

        '''
        logger.debug('Starting test_get_transfers_with_non_exist_id')
        url = reverse(f'transfers-detail', kwargs = ({"pk" : 1}))
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.get(url)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json['detail'] , "Not found.")

        logger.debug("The test_get_transfers_with_non_exist_id test has ended successfully")

    def test_delete_transfers_with_id(self):
        '''
            Test to delete a Stop with id 

        '''
        logger.debug('Starting test_delete_transfers_with_id')
        transfers = Transfer(to_stop = self.to_stop, from_stop = self.from_stop, transfer_type = TransferType[0][0],
                             min_transfer_time = 500, admin = self.admin)
        transfers.save()
        url = reverse(f'transfers-detail', kwargs = ({"pk" : transfers.id}))
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.delete(url)
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        logger.debug("The test_delete_transfers_with_id test has ended successfully")

    def test_delete_transfers_with_non_exist_id(self):
        '''
            Test to delete a Stop with id that does not exist

        '''
        logger.debug('Starting test_delete_transfers_with_id')
        url = reverse(f'transfers-detail', kwargs = ({"pk" : 10}))
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.delete(url)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json['detail'] , "Not found.")

        logger.debug("The test_delete_transfers_with_id test has ended successfully")
    
    def test_put_transfers_with_id(self):
        '''
            Test to update a Stop with id 

        '''
        self.client.force_authenticate(user=self.s_admin)
        logger.debug('Starting test_put_calendar_with_id')
        logger.debug('Starting test_put_transfers_with_id')
        transfers = Transfer(to_stop = self.to_stop, from_stop = self.from_stop, transfer_type = TransferType[0][0],
                             min_transfer_time = 500, admin = self.admin)
        transfers.save()
        url = reverse(f'transfers-detail', kwargs = ({"pk" : transfers.id}))
        data = {
            'to_stop' : self.to_stop.id,
            'from_stop' : self.from_stop.id,
            'transfer_type' : TransferType[0][0],
            'min_transfer_time' : 500,
            'admin' : self.admin.id,
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
        
        logger.debug("The test_put_transfers_with_id test has ended successfully")

    def test_put_transfers_with_non_exist_id(self):
        '''
            Test to update a transfers with id that does not exist

        '''
        logger.debug('Starting test_put_transfers_with_non_exist_id')
        url = reverse(f'transfers-detail', kwargs = ({"pk" : 1}))
        data = {
            'to_stop' : self.to_stop.id,
            'from_stop' : self.from_stop.id,
            'transfer_type' : TransferType[0][0],
            'min_transfer_time' : 500,
            'admin' : self.admin.id,
        }
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.put(url, data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json['detail'] , "Not found.")

        logger.debug("The test_put_transfers_with_non_exist_id test has ended successfully")

    def test_put_transfers_with_missing_fields_in_payload(self):
        '''
            Test to update a transfers with missing field

        '''
        logger.debug('Starting test_put_transfers_with_missing_fields_in_payload')
        transfers = Transfer(to_stop = self.to_stop, from_stop = self.from_stop, transfer_type = TransferType[0][0],
                             min_transfer_time = 500, admin = self.admin)
        transfers.save()
        self.client.force_authenticate(user=self.admin)
        logger.debug('Starting test_delete_route_with_non_exist_id')
        url = reverse(f'transfers-detail', kwargs = ({"pk" : transfers.id}))
        data = {}
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.put(url,data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        for message in json.values():
            self.assertEqual(message, ['This field is required.'])
        logger.debug("The test_put_transfers_with_missing_fields_in_payload test has ended successfully")

    def test_patch_transfers_with_id(self):
        '''
            Test to update a Stop with id 

        '''
        self.client.force_authenticate(user=self.s_admin)
        logger.debug('Starting test_patch_transfers_with_id')
        transfers = Transfer(to_stop = self.to_stop, from_stop = self.from_stop, transfer_type = TransferType[0][0],
                             min_transfer_time = 500, admin = self.admin)
        transfers.save()
        logger.debug('Starting test_delete_route_with_non_exist_id')
        url = reverse(f'transfers-detail', kwargs = ({"pk" : transfers.id}))
        data = {
            'to_stop' : self.to_stop.id,
            'from_stop' : self.from_stop.id,
            'transfer_type' : TransferType[1][0],
            'min_transfer_time' : 300,
            'admin' : self.admin.id,
        }
        self.client.force_authenticate(user=self.admin)
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.patch(url, data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in ['transfer_type', 'min_transfer_time']:
            self.assertEqual(str(json[key]) , str(data[key]))

        logger.debug("The test_patch_transfers_with_id test has ended successfully")

    def test_patch_transfers_with_non_exist_id(self):
        '''
            Test to update a transfers with id that does not exist

        '''
        logger.debug('Starting test_patch_transfers_with_non_exist_id')
        url = reverse(f'transfers-detail', kwargs = ({"pk" : 1}))
        data = {
            'to_stop' : self.to_stop.id,
            'from_stop' : self.from_stop.id,
            'transfer_type' : TransferType[1][0],
            'min_transfer_time' : 300,
            'admin' : self.admin.id,
        }
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.patch(url, data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json['detail'] , "Not found.")

        logger.debug("The test_patch_transfers_with_non_exist_id test has ended successfully")

    def test_patch_transfers_with_missing_fields_in_payload(self):
        '''
            Test to update a transfers with missing field

        '''
        logger.debug('Starting test_patch_transfers_with_missing_fields_in_payload')
        transfers = Transfer(to_stop = self.to_stop, from_stop = self.from_stop, transfer_type = TransferType[0][0],
                             min_transfer_time = 500, admin = self.admin)
        transfers.save()
        self.client.force_authenticate(user=self.admin)
        logger.debug('Starting test_delete_route_with_non_exist_id')
        url = reverse(f'transfers-detail', kwargs = ({"pk" : transfers.id}))
        data = {}
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.patch(url,data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(transfers.id, json['id'])
        logger.debug("The test_patch_transfers_with_missing_fields_in_payload test has ended successfully")
        