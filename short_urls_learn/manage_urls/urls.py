from django.urls import path, include
from . import views

urlpatterns = [
    # url endpoint for creating a new tiny_url
    path('shorturls/create/', views.UrlViewSet.as_view({'post': 'create'}), name='url-create'),
    # url endpoint for redirecting to the original url from the tiny_url
    path('shorturls/<slug:slug>', views.UrlViewSet.as_view({'get': 'retrieve'}), name='url-detail')
]
