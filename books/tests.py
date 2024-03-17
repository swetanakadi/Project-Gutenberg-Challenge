from django.urls import reverse
from rest_framework.test import APITestCase
from .models import *


# Create your tests here.


class SearchViewTestCase(APITestCase):

    def setUp(self) -> None:
        self.url = reverse('search')
        self.valid_keys = ['book_id', 'language', 'mime-type', 'topic', 'author', 'title', 'page']

        self.valid_all_query_parameters = {'book_id': '14,25,16',
                                           'language': 'en,fr',
                                           'mime-type': 'text/plain',
                                           'topic': 'child,infant',
                                           'author': 'lewis,mark',
                                           'title': 'inaugural'}

        self.empty_query_parameters = {}

        self.invalid_query_parameter = {'genre': 'horror'}

    def test_search_with_invalid_query_parameters(self):
        response = self.client.get(self.url, data=self.invalid_query_parameter)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(response.data['results'], [])

    def test_search_with_no_query_parameters(self):
        response = self.client.get(self.url, data=self.empty_query_parameters)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(response.data['results'], [])

    def test_search_with_all_query_parameters(self):
        response = self.client.get(self.url, data=self.valid_all_query_parameters)
        if response.data['count'] > 0:
            response_key_len = len(response.data['results'][0].keys())
            actual_key_len = 7
            self.assertEqual(response_key_len, actual_key_len)
        else:
            self.assertEqual(response.data['results'], [])

    def test_search_with_multiple_query_parameters(self):
        response = self.client.get(self.url, data=self.valid_all_query_parameters)
        if response.data['count'] > 0:
            response_key_len = len(response.data['results'][0].keys())
            actual_key_len = 7
            self.assertEqual(response_key_len, actual_key_len)
        else:
            self.assertEqual(response.data['results'], [])
