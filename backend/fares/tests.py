# from django.urls import reverse
# from rest_framework.test import APITestCase, APIClient
# from rest_framework.views import status

# from admins.models import Admin
# from .models import Fare
# from .serializer import FareSerializer
# from agencies.models import Agency
# from routes.models import Route
# from stops.models import Stop

# import logging
# logger = logging.getLogger(__name__)

# # define the tests for the FareViewSet
# class FareViewSetTestCase(APITestCase):
#     client = APIClient()

#     # set up test data
#     def setUp(self):
#         logger.debug('Adding a new admin into database')
#         self.s_admin = Admin(username='admins@gmail.com', password='admins1234', first_name = 'admins', last_name = 'admins', email = 'admins@gamil.com', user_type =  USER_TYPES[0][0])
#         self.s_admin.save()
#         self.admin = Admin(username='admin@gmail.com', password='admin1234', first_name = 'admin', last_name = 'admin', email = 'admin@gamil.com', user_type =  USER_TYPES[1][0])
#         self.admin.save()
        
#         self.agency = Agency(name = 'bus1', url = 'http://127.0.0.1:8000/', lang='en', time_zone='+3', phone = '+251991439281', admin = self.s_admin)
#         self.agency.save()
        
#         self.client = APIClient()
#         route = Route(route_short_name= 'r2',route_long_name = 'route2' , route_desc = 'route desc 2', route_type = RouteType[0][0], route_color = 'yellow', agency = self.agency)
#         route.save()

#         start_stop = Stop.objects.create(stop_name='Start Stop')
#         start_stop.save()
#         end_stop = Stop.objects.create(stop_name='End Stop')
#         end_stop.save()
#         self.fare = Fare.objects.create(price=10.0, agency=self.agency, route=route, start_stop=start_stop, end_stop=end_stop)

#     # test the GET method for retrieving all fares
#     def test_get_all_fares(self):
#         # hit the API endpoint
#         response = self.client.get(reverse('fare-list'))
#         # fetch the data from db
#         fares = Fare.objects.all()
#         serializer = FareSerializer(fares, many=True)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.json(), serializer.data)

#     # test the GET method for retrieving a single fare
#     def test_get_single_fare(self):
#         # hit the API endpoint
#         response = self.client.get(reverse('fare-detail', kwargs={'pk': self.fare.id}))
#         # fetch the data from db
#         fare = Fare.objects.get(id=self.fare.id)
#         serializer = FareSerializer(fare)
#         self.assertEqual(response.json(), serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     # test the POST method for creating a new fare
#     def test_create_fare(self):
#         agency = Agency.objects.create(name='Test Agency 2')
#         route = Route.objects.create(name='Test Route 2')
#         start_stop = Stop.objects.create(name='Test Start Stop 2')
#         end_stop = Stop.objects.create(name='Test End Stop 2')
#         data = {'price': 20.0, 'agency': agency.id, 'route': route.id, 'start_stop': start_stop.id, 'end_stop': end_stop.id}
#         response = self.client.post(reverse('fare-list'), data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     # test the PUT method for updating an existing fare
#     def test_update_fare(self):
#         agency = Agency.objects.create(name='Test Agency 3')
#         route = Route.objects.create(name='Test Route 3')
#         start_stop = Stop.objects.create(name='Test Start Stop 3')
#         end_stop = Stop.objects.create(name='Test End Stop 3')
#         data = {'price': 30.0, 'agency': agency.id, 'route': route.id, 'start_stop': start_stop.id, 'end_stop': end_stop.id}
#         response = self.client.put(reverse('fare-detail', kwargs={'pk': self.fare.id}), data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     # test the DELETE method for deleting an existing fare
#     def test_delete_fare(self):
#         response = self.client.delete(reverse('fare-detail', kwargs={'pk': self.fare.id}))
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#     def test_create_fare_invalid_input(self):
#         self.client.force_authenticate(user=self.system_admin)
#         data = {'price': 'abc', 'agency': self.agency.id, 'route': self.route.id, 
#                 'start_stop': self.start_stop.id, 'end_stop': self.end_stop.id}
#         response = self.client.post(self.create_url, data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_update_fare_unauthorized(self):
#         data = {'price': 9.99, 'agency': self.agency.id, 'route': self.route.id, 
#                 'start_stop': self.start_stop.id, 'end_stop': self.end_stop.id}
#         response = self.client.patch(self.detail_url, data)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_update_fare_invalid_input(self):
#         self.client.force_authenticate(user=self.system_admin)
#         data = {'price': 'abc', 'agency': self.agency.id, 'route': self.route.id, 
#                 'start_stop': self.start_stop.id, 'end_stop': self.end_stop.id}
#         response = self.client.patch(self.detail_url, data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_delete_fare_unauthorized(self):
#         response = self.client.delete(self.detail_url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_delete_fare_forbidden(self):
#         self.client.force_authenticate(user=self.passenger)
#         response = self.client.delete(self.detail_url)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
