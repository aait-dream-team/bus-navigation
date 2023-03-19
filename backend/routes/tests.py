from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase,force_authenticate,APIClient
from admins.models import Admin, USER_TYPES
from agencies.models import Agency
from .models import RouteType, Route

import logging
logger = logging.getLogger(__name__)
class RouteViewSetTests(APITestCase):
    def setUp(self):
        logger.debug('Adding a new admin into database')
        self.s_admin = Admin(username='admins@gmail.com', password='admins1234', first_name = 'admins', last_name = 'admins', email = 'admins@gamil.com', user_type =  USER_TYPES[0][0])
        self.s_admin.save()
        self.admin = Admin(username='admin@gmail.com', password='admin1234', first_name = 'admin', last_name = 'admin', email = 'admin@gamil.com', user_type =  USER_TYPES[1][0])
        self.admin.save()
        
        self.agency = Agency(name = 'bus1', url = 'http://127.0.0.1:8000/', lang='en', time_zone='+3', phone = '+251991439281', admin = self.s_admin)
        self.agency.save()
        
        self.client = APIClient()
        logger.debug('Successfully added test admin into the database')
    def test_create_route_success(self):

        '''
            Test to create a Route success

        '''
        logger.debug('Starting test_create_route_success')
        url = reverse('routes-list')
        data = {
            'route_short_name' : 'r1',
            'route_long_name' : 'route1', 
            'route_desc' : 'route desc', 
            'route_type' : RouteType[0][0], 
            'route_color': 'Yellow',
            'agency': self.agency.id
        }
        logger.debug('Sending TEST data to url: %s'%url)
        # self.client.force_authenticate(user=self.admin)
        response = self.client.post(url,data)
        json = response.json()

        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json['route_short_name'] , json['route_short_name'])
        self.assertEqual(data['route_long_name'] , json['route_long_name'])
        self.assertEqual(data['route_desc'] , json['route_desc'])
        self.assertEqual(data['route_color'] , json['route_color'])
        self.assertEqual(data['route_type'] , json['route_type'])
        self.assertEqual(data['agency'] , json['agency'])
        self.assertNotEqual(json['id'], None)

        logger.debug("The test_create_route_success test has ended successfully")
    def test_create_route_with_missing_field(self):
        '''
            Test to create a Route with missing field

        '''
        logger.debug('Starting test_create_route_with_missing_field')
        url = reverse('routes-list')
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
        logger.debug("The test_create_route_with_missing_field test has ended successfully")
    def test_get_list_routes_success(self):
        '''
            Test to create a Route with missing field

        '''
        route = Route(route_short_name= 'r2',route_long_name = 'route2' , route_desc = 'route desc 2', route_type = RouteType[0][0], route_color = 'yellow', agency = self.agency)
        route.save()
        logger.debug('Starting test_get_list_routes_success')
        url = reverse('routes-list')
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.get(url)
        json = response.json()
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json) , 1)
        logger.debug("The test_get_list_routes_success test has ended successfully")
    
    def test_get_list_routes_with_empty_routes(self):
        '''
            Test to get a list of Routes 

        '''
        logger.debug('Starting test_get_list_routes_with_empty_routes')
        url = reverse('routes-list')
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.get(url)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json) , 0)
        logger.debug("The test_get_list_routes_with_empty_routes test has ended successfully")
    
    def test_get_route_with_id(self):
        '''
            Test to get a Route with id

        '''
        route = Route(route_short_name= 'r2',route_long_name = 'route2' , route_desc = 'route desc 2', route_type = RouteType[0][0], route_color = 'yellow', agency = self.agency)
        route.save()
        logger.debug('Starting test_get_route_with_id')
        url = reverse(f'routes-detail', kwargs = ({"pk" : route.id}))
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.get(url)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json['id'], route.id)
        self.assertEqual(json['route_short_name'], route.route_short_name)
        self.assertEqual(json['route_long_name'], route.route_long_name)
        self.assertEqual(json['route_desc'], route.route_desc)
        self.assertEqual(json['agency'], self.agency.id)
        logger.debug("The test_get_route_with_id test has ended successfully")


    def test_get_route_with_non_exist_id(self):
        '''
            Test to get a Route with id that does not exist

        '''
        logger.debug('Starting test_get_route_with_non_exist_id')
        url = reverse(f'routes-detail', kwargs = ({"pk" : 1}))
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.get(url)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json['detail'] , "Not found.")

        logger.debug("The test_get_route_with_non_exist_id test has ended successfully")
    def test_delete_route_with_id(self):
        '''
            Test to delete a Route with id 

        '''
        logger.debug('Starting test_delete_route_with_id')
        route = Route(route_short_name= 'r2',route_long_name = 'route2' , route_desc = 'route desc 2', route_type = RouteType[0][0], route_color = 'yellow', agency = self.agency)
        route.save()
        url = reverse(f'routes-detail', kwargs = ({"pk" : route.id}))
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.delete(url)
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        logger.debug("The test_delete_route_with_id test has ended successfully")
    def test_delete_route_with_non_exist_id(self):
        '''
            Test to delete a Route with id that does not exist

        '''
        logger.debug('Starting test_delete_route_with_non_exist_id')
        url = reverse(f'routes-detail', kwargs = ({"pk" : 1}))
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.delete(url)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json['detail'] , "Not found.")

        logger.debug("The test_delete_route_with_non_exist_id test has ended successfully")
    
    def test_put_route_with_id(self):
        '''
            Test to update a Route with id 

        '''
        self.client.force_authenticate(user=self.s_admin)
        logger.debug('Starting test_update_route_with_id')
        route = Route(route_short_name= 'r2',route_long_name = 'route2' , route_desc = 'route desc 2', route_type = RouteType[0][0], route_color = 'yellow', agency = self.agency)
        route.save()
        logger.debug('Starting test_delete_route_with_non_exist_id')
        url = reverse(f'routes-detail', kwargs = ({"pk" : route.id}))
        data = {
            'route_short_name' : 'route1',
            'route_long_name' : 'route1', 
            'route_desc' : 'route desc', 
            'route_type' : RouteType[0][0], 
            'route_color': 'Yellow',
            'agency': self.agency.id
        }
        logger.debug('Sending TEST data to url: %s\n'%url)
        response = self.client.put(url, data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d\n'%(response, response.status_code))
        print(json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json['route_short_name'] , data["route_short_name"])

        logger.debug("The test_update_route_with_id test has ended successfully")
    def test_put_route_with_non_exist_id(self):
        '''
            Test to update a Route with id that does not exist

        '''
        logger.debug('Starting test_put_route_with_non_exist_id')
        url = reverse(f'routes-detail', kwargs = ({"pk" : 1}))
        data = {
            'route_short_name' : 'route1',
            'route_long_name' : 'route1', 
            'route_desc' : 'route desc', 
            'route_type' : RouteType[0][0], 
            'route_color': 'Yellow',
            'agency': self.agency.id
        }
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.put(url, data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json['detail'] , "Not found.")

        logger.debug("The test_put_route_with_non_exist_id test has ended successfully")
    def test_patch_route_with_id(self):
        '''
            Test to update a Route with id 

        '''
        self.client.force_authenticate(user=self.s_admin)
        logger.debug('Starting test_patch_route_with_id')
        route = Route(route_short_name= 'r2',route_long_name = 'route2' , route_desc = 'route desc 2', route_type = RouteType[0][0], route_color = 'yellow', agency = self.agency)
        route.save()
        logger.debug('Starting test_delete_route_with_non_exist_id')
        url = reverse(f'routes-detail', kwargs = ({"pk" : route.id}))
        data = {
            'route_short_name' : 'route1',
            'route_long_name' : 'route1', 
            'route_desc' : 'route desc', 
            'route_type' : RouteType[0][0], 
            'route_color': 'Yellow',
            'agency': self.agency.id
        }
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.patch(url, data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json['route_short_name'] , data["route_short_name"])

        logger.debug("The test_patch_route_with_id test has ended successfully")
    def test_patch_route_with_non_exist_id(self):
        '''
            Test to update a Route with id that does not exist

        '''
        logger.debug('Starting test_patch_route_with_non_exist_id')
        url = reverse(f'routes-detail', kwargs = ({"pk" : 1}))
        data = {
            'route_short_name' : 'route1',
            'route_long_name' : 'route1', 
            'route_desc' : 'route desc', 
            'route_type' : RouteType[0][0], 
            'route_color': 'Yellow',
            'agency': self.agency.id
        }
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.patch(url, data)
        json = response.json()
        logger.debug(response)
        logger.debug('Testing status code response: %s, code: %d'%(response, response.status_code))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json['detail'] , "Not found.")

        logger.debug("The test_patch_route_with_non_exist_id test has ended successfully")