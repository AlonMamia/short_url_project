from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, HttpResponseRedirect
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .forms import EnterUrlForm
from .models import Url
from .serializers import UrlSerializer
import uuid


# handle url adding

class UrlViewSet(viewsets.ModelViewSet):
    serializer_class = UrlSerializer

    def get_queryset(self):
        return Url.objects.get(tiny_url=self.kwargs['slug'])

    def create(self, request, *args, **kwargs):
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
            # Return a response with the serialized data and a status code of 201 (Created)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, slug):
        # Retrieve the Url object with the tiny_url field equal to the slug argument
        url = get_object_or_404(Url, tiny_url=slug)
        # Initialize a serializer instance with the url object as its data
        serializer = self.get_serializer(url)
        # Return an HTTP response that redirects the client's browser to the original_url field of the serialized data
        return HttpResponseRedirect(serializer.data['original_url'])
