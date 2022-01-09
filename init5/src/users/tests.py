from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class ProfileTestCase(APITestCase):
    profile_list_url = reverse('user-list')

    def setUp(self):
        self.user = self.client.post('/auth/users/', data={'email': 'test@test.com', 'username': 'testName', 'password': 'qwSd-234d'})
        response = self.client.post('/auth/jwt/create/', data={'email': 'test@test.com', 'username': 'testName', 'password': 'qwSd-234d'})
        self.token = response.data['access']
        self.api_authentication()
    
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+self.token)

    def test_profile_list_authenticated(self):
        response = self.client.get(self.profile_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_profile_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.profile_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_detail_retrieve(self):
        response = self.client.get(reverse('user-detail', kwargs={'username': 'testName'}))
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile(self):
        profile_data={'description':'I am a Test', 'is_newsmaker':'true'}
        response = self.client.put(reverse('user-detail', kwargs={'username': 'testName'}), data=profile_data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
