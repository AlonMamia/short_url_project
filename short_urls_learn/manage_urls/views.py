from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Url
from .serializers import UrlSerializer
import uuid


# Url view
class UrlViewSet(viewsets.ModelViewSet):
    serializer_class = UrlSerializer

    def get_queryset(self):
        return Url.objects.get(tiny_url=self.kwargs['slug'])

    def create(self, request, *args, **kwargs):
        # Initialize serializer with request data
        serializer = self.get_serializer(data=request.data)
        # Validate serializer and raise exception if invalid
        try:
            if serializer.is_valid(raise_exception=True):
                # Set up flag to track whether a new URL has been created
                created = False
                # Set up counter to limit number of iterations
                relative_counter = 0
                # Loop until new URL is created or max iterations reached
                while not created and relative_counter < 9999999:
                    # Generate random 8-character string using UUID
                    tiny_url = uuid.uuid4().hex[:8]
                    # Attempt to create new URL with tiny_url field set to generated string
                    url, created = Url.objects.get_or_create(tiny_url=tiny_url)
                    # If URL creation was successful, set tiny_url field of serialized data
                    # and save serialized data
                    if created:
                        serializer.validated_data['tiny_url'] = tiny_url
                        serializer.save()
                    # Increment counter
                    relative_counter += 1
                # Construct URL using host and reverse-resolved URL pattern
                tiny_url_link = request.get_host() + reverse('url-detail', args=[tiny_url])
                # Return constructed URL in response with 201 status code
                return Response(tiny_url_link, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Catch any exceptions and return a response with an appropriate error message
            # and status code
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Redirects to the original_url from the tiny_url and increment the click_counter field in db
    def retrieve(self, request, slug):
        # Retrieve the Url object with the tiny_url field equal to the slug argument
        # If the object does not exist, return a 404 Not Found response
        url = get_object_or_404(Url, tiny_url=slug)
        # Use a database transaction to update the hit counter atomically
        with transaction.atomic():
            # Increment the click_counter field of the Url object
            url.click_counter += 1
            # Save the updated object in the database
            url.save()
        # Initialize a serializer instance with the url object as its data
        serializer = self.get_serializer(url)
        # Return an HTTP response that redirects the client's browser to the original_url field of the serialized data
        return HttpResponseRedirect(serializer.data['original_url'])