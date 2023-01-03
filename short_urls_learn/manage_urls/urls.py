from django.urls import path, include
from . import views as Manage_Urls_Views
from django.views.generic import TemplateView


urlpatterns = [
    path('shorturls/create/', Manage_Urls_Views.UrlViewSet.as_view({'post': 'create'}), name='url-create'),
    path('shorturls/<slug:slug>', Manage_Urls_Views.UrlViewSet.as_view({'get': 'retrieve'}), name='url-detail')
]