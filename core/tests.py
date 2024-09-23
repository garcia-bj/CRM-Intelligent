from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Lead

class LeadTests(APITestCase):
    def test_create_lead(self):
        url = reverse('lead-list-create')
        data = {'cliente': 1, 'fuente': 'web', 'estado': 'nuevo', 'vendedor': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# Create your tests here.
