from django.http import HttpResponseRedirect
from django.urls import reverse
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
        """
        Handles creation of a new Url object with a random tiny_url field.
        Returns the created object's tiny_url field in the Location header of the response.
        """
        # Create a serializer instance with the data from the request
        serializer = self.get_serializer(data=request.data)

        # Validate the data and raise an exception if the data is invalid
        if serializer.is_valid(raise_exception=True):
            # Generate a random 8-character string for the tiny_url field
            tiny_url = uuid.uuid4().hex[:8]
            # Set the tiny_url field in the serializer's validated_data to the generated string
            serializer.validated_data['tiny_url'] = tiny_url
            # Save the serializer and store the resulting Url object in the 'url' variable
            url = serializer.save()

            # Generate the URL for the new tiny URL using the reverse() function
            tiny_url_link = request.get_host() + reverse('url-detail', args=[tiny_url])
            # Include the URL in the Location header of the response
            return Response(tiny_url_link, status=status.HTTP_201_CREATED)

    # Redirects to the original_url from the tiny_url and increment the click_counter field in db
    def retrieve(self, request, slug):
        # Retrieve the Url object with the tiny_url field equal to the slug argument
        # If the object does not exist, return a 404 Not Found response
        url = get_object_or_404(Url, tiny_url=slug)
        # Increment the click_counter field of the Url object
        url.click_counter += 1
        # Save the updated object in the database
        url.save()
        # Initialize a serializer instance with the url object as its data
        serializer = self.get_serializer(url)
        # Return an HTTP response that redirects the client's browser to the original_url field of the serialized data
        return HttpResponseRedirect(serializer.data['original_url'])

