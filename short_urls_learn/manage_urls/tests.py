from django.urls import reverse
from django.test import Client
from rest_framework import status
from rest_framework.test import APITestCase

from manage_urls.models import Url
from manage_urls.serializers import UrlSerializer


class CreateUrlTest(APITestCase):
    def setUp(self):
        self.valid_url = 'https://www.google.com'
        self.invalid_url = 'invalid'
        self.costume_client = Client(HTTP_HOST='localhost')

    def test_create_valid_url(self):
        """
        Ensure we can create a new url object with a valid original_url.
        """
        data = {'original_url': self.valid_url}
        response = self.costume_client.post(reverse('url-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Url.objects.count(), 1)
        self.assertEqual(Url.objects.last().original_url, self.valid_url)

    def test_create_invalid_url(self):
        """
        Ensure we get a 400 Bad Request response when trying to create a new url object with an invalid original_url.
        """
        data = {'original_url': self.invalid_url}
        response = self.costume_client.post(reverse('url-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Url.objects.count(), 0)


class RedirectUrlTest(APITestCase):
    def setUp(self):
        self.url = Url.objects.create(original_url='https://www.google.com', tiny_url='55ae07f8')
        self.serializer = UrlSerializer(instance=self.url)
        self.costume_client = Client(HTTP_HOST='localhost')

    def test_redirect_url(self):
        # Make a GET request to the view with the slug of the Url object
        response = self.costume_client.get(f'/shorturls/{self.url.tiny_url}')
        # Assert that the response status code is a redirect (status code 302)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        # Assert that the response contains the correct Location header
        self.assertEqual(response['Location'], self.url.original_url)

    def test_redirect_url_not_exist(self):
        # Make a GET request to the view with a slug that doesn't match any Url objects
        response = self.costume_client.get(f'/shorturls/some-invalid-slug')
        # Assert that the response status code is a 404 Not Found
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
