import os
import django
from django.test import TestCase, Client
from django.core.exceptions import ValidationError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'short_urls_learn_main.settings')
django.setup()

from manage_urls.models import Url
from manage_urls.views import use_short_link


# Create your tests here.
class UrlTests(TestCase):
    # test create link
    def test_valid_url(self):
        # creating an object in django testing db
        new_link = Url.objects.create(original_url='https://validurl.com',
                                      tiny_url='4564dasfsa8')
        new_link.full_clean()
        new_link.save()

    #
    def test_invalid_url(self):
        # creating an object in django testing db
        # the _ in the url make it invalid.
        new_link = Url.objects.create(original_url='https://invalid_url.com',
                                      tiny_url='4564dasfsa8')
        with self.assertRaises(ValidationError):
            new_link.full_clean()

    def test_form_submission(self):
        # Create a valid form data dictionary
        original_url = 'https://www.example.com'
        form_data = {'original_url': original_url}

        # Send a POST request with the form data
        client = Client(HTTP_HOST='localhost')
        response = client.post('/', form_data)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that an object was created in the database
        self.assertEqual(Url.objects.count(), 1)
        self.assertEqual(Url.objects.filter(original_url=original_url).count(), 1)

    def test_redirect(self):
        # Create an object in the database with an original URL that does not exist
        new_url = r'https://NewUrl.com'
        tiny_url = '4564dasfsa8'
        Url.objects.create(original_url=new_url, tiny_url=tiny_url)
        # Send an HTTP GET request to the original URL of the new_url object
        client = Client(HTTP_HOST='localhost')
        response = client.get(f'/link/{tiny_url}/')
        self.assertRedirects(response, new_url, fetch_redirect_response=False, target_status_code=302)

    def test_invalid_redirect(self):
        # Create an object in the database with an original URL that does not exist
        non_exists_url = r'https://NewUrl.com'
        tiny_url = '4564dasfsa8'
        # Send an HTTP GET request to the original URL of the new_url object
        client = Client(HTTP_HOST='localhost')
        response = client.get(f'/link/{tiny_url}/')
        self.assertEqual(response.status_code, 404)

    def test_counter(self):
        # Create an object in the database with an original URL that does not exist
        new_url = r'https://NewUrl.com'
        tiny_url = '4564dasfsa8'
        Url.objects.create(original_url=new_url, tiny_url=tiny_url)
        # Send an HTTP GET request to the original URL of the new_url object
        client = Client(HTTP_HOST='localhost')
        response = client.get(f'/link/{tiny_url}/')
        self.assertEqual(Url.objects.get(original_url=new_url).click_counter, 1)
