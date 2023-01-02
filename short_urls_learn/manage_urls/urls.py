from django.urls import path, include
from . import views as Manage_Urls_Views
from django.views.generic import TemplateView


urlpatterns = [
    path('', Manage_Urls_Views.home),
    path('link/<slug:slug>/', Manage_Urls_Views.use_short_link)
]