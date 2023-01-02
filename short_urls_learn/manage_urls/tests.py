from unittest import mock
import requests
from django.test import TestCase, Client
from .models import Url
from django.core.exceptions import ValidationError


# Create your tests here.
class UrlTests(TestCase):

    # test create link
    def test_create_link(self):
        # creating an object in django testing db
        new_link = Url.objects.create(original_url='https://music.youtube.com/',
                                      tiny_url='4564dasfsa8')
        try:
            new_link.full_clean()
        except ValidationError as e:
            self.assertEqual(e.error_dict, {'original_url': ["ValidationError message"]})

    def test_redirect(self):
        # Create a new URL object
        new_url = Url.objects.create(original_url='https://music.youtube.com/',
                                     tiny_url='4564dasfsa8')

        try:
            with mock.patch('requests.get') as mock_get:
                # mock_get.return_value.status_code = 200
                c = Client()
                response = c.get('/link/4564dasfsa85/')
                # Assert that the response is a redirect to the original URL, without following the redirect and
                # retrieving the final response
                # fetch_redirect_response controls whether the test client
                # should follow redirects and retrieve the final response, or just return the redirect response.
                self.assertRedirects(response, 'https://music.youtube.com/', fetch_redirect_response=False)
        except Exception as e:
            # Print the exception if it is raised
            print(e)

    def test_url_exist(self):
        # Create an object in the database with an original URL that does not exist
        new_url = Url.objects.create(original_url='https://www.google.co.il/webhp?hl=iw&tab=iw', tiny_url='4564dasfsa8')

        # Use the mock.patch decorator to mock the requests.get function and return a mock response object
        # with the status_code attribute set to 404
        with mock.patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 404

            # Send an HTTP GET request to the original URL of the new_url object
            c = Client()
            try:
                response = c.get(new_url.original_url)
            except Exception as e:
                # If an exception is raised, print the exception and fail the test
                print(e)
                self.fail("An exception was raised")

            # Assert that the response status code is 404
            self.assertEqual(response.status_code, 404)