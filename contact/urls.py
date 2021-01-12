from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('contact/', views.Contact.as_view(), name='contact'),
    path('success/', views.ContactSuccess.as_view(), name='success'),
]
