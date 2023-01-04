from django.urls import reverse
from django.test import Client
from rest_framework import status
from rest_framework.test import APITestCase

from manage_urls.models import Url


class CreateUrlTest(APITestCase):
    """
    Test cases for the `create` method of the `UrlViewSet` class.
    """
    def setUp(self):
        """
        Set up test data for the test cases.
        """
        # A valid URL
        self.valid_url = 'https://www.google.com'
        # An invalid URL
        self.invalid_url = 'invalid'
        # A client with the `HTTP_HOST` header set to 'localhost'
        self.costume_client = Client(HTTP_HOST='localhost')

    def test_create_valid_url(self):
        """
        Test that a new URL object can be created with a valid original_url.
        """
        # Data to be sent with the request
        data = {'original_url': self.valid_url}
        # Make a POST request to the `url-create` endpoint
        response = self.costume_client.post(reverse('url-create'), data, format='json')
        # Check that the response status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check that there is only 1 URL object in the database
        self.assertEqual(Url.objects.count(), 1)
        # Check that the original_url of the URL object in the database is the valid URL
        self.assertEqual(Url.objects.last().original_url, self.valid_url)

    def test_create_invalid_url(self):
        """
        Test that attempting to create a new url object with an invalid original_url results in a 400 Bad Request response.
        Additionally, ensure that no new url object is created in the database.
        """
        # Create a request data dictionary with an invalid url
        data = {'original_url': self.invalid_url}
        # Send a POST request to the url-create endpoint with the invalid url data
        response = self.costume_client.post(reverse('url-create'), data, format='json')
        # Assert that the response status code is a 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Assert that the Url model's objects count is 0 (no new object was created)
        self.assertEqual(Url.objects.count(), 0)


class RedirectUrlTest(APITestCase):
    def setUp(self):
        # Create a new Url object with an original_url of 'https://www.google.com' and a tiny_url of '55ae07f8'
        self.url = Url.objects.create(original_url='https://www.google.com', tiny_url='55ae07f8')
        # Create a new Client instance with the HTTP_HOST header set to 'localhost'
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
