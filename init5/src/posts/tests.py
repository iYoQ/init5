from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class ArticleTestCase(APITestCase):
    articles_list_url = '/api/articles/'

    def setUp(self):
        self.user = self.client.post('/api/users/registration/', data={
            'email': 'test@test.com', 
            'username': 'testName', 
            'password': 'qwSd-234d'
            })
        response = self.client.post('/auth/jwt/create/', data={'email': 'test@test.com', 
        'username': 'testName', 
        'password': 'qwSd-234d'
        })
        self.token = response.data['access']
        self.api_authentication()
    
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+self.token)
        self.create_article()

    def create_article(self):
        self.client.post(f'{self.articles_list_url}create_article/', data={
            'headline': 'test article', 
            'content': 'test'
        })
    
    def test_create_article(self):
        response = self.client.post(f'{self.articles_list_url}create_article/', data={
            'headline': 'new article', 
            'content': 'new content'
        })
        print(f'test create article: {response.data}\n')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_list_article(self):
        response = self.client.get(self.articles_list_url)
        print(f'test list article: {response.data}\n')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_article_detail_retrieve(self):
        response = self.client.get(reverse('articles-detail', kwargs={'pk': 1}))
        print(f'test article detail retrieve: {response.data}\n')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_update_article(self):
        response = self.client.patch(reverse('articles-detail', kwargs={'pk': 1}), data={'content': 'update content'})
        print(f'test update article: {response.data}\n')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
