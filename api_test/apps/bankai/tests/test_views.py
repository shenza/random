from decimal import Decimal
import unittest

from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from ..models import Control


class ControlTestCase(APITestCase, URLPatternsTestCase):
    fixtures = ['controls.json']
    urlpatterns = [
        path('api/', include('qctrl.api.urls')),
    ]

    @classmethod
    def setUpTestData(cls):
        cls.control_count = Control.objects.count()

    def _response_result_equal_control(self,
                                       result,
                                       control,
                                       type_display_value=True):
        self.assertEqual(result['name'], control.name)
        self.assertEqual(
            result['type'],
            control.get_type_display() if type_display_value else control.type)
        self.assertEqual(Decimal(result['maximum_rabi_rate']),
                         control.maximum_rabi_rate)
        self.assertEqual(Decimal(result['polar_angle']), control.polar_angle)

    def test_create_control(self):
        url = reverse('control-list')
        data = {
            'name': 'New Control',
            'type': 'Gaussian',
            'maximum_rabi_rate': 70.03844,
            'polar_angle': 0.09843
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Control.objects.count(), self.control_count + 1)
        self.assertEqual(Control.objects.latest('id').name, 'New Control')

    def test_create_invalid_control_type(self):
        url = reverse('control-list')
        data = {
            'name': 'New Control',
            'type': 'Non-existent type',
            'maximum_rabi_rate': 70.03844,
            'polar_angle': 0.09843
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_control_maximum_rabi_rate(self):
        url = reverse('control-list')
        for invalid_rate in ('-0.0001', '100.1', '2.333333'):
            data = {
                'name': 'New Control',
                'type': 'Gaussian',
                'maximum_rabi_rate': invalid_rate,
                'polar_angle': 0.09843
            }
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_control_polar_angle(self):
        url = reverse('control-list')
        for invalid_angle in ('-0.0001', '1.1', '0.333333'):
            data = {
                'name': 'New Control',
                'type': 'Gaussian',
                'maximum_rabi_rate': 70.03844,
                'polar_angle': invalid_angle
            }
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_controls(self):
        url = reverse('control-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)

        controls = Control.objects.all()[:5]

        for result, control in zip(response.data['results'], controls):
            self._response_result_equal_control(result, control)

    def test_get_one_control(self):
        pk = 1
        url = reverse('control-detail', args=[pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        control = Control.objects.get(pk=pk)
        self._response_result_equal_control(response.data, control)

    def test_edit_control(self):
        pk = 1
        url = reverse('control-detail', args=[pk])
        control = Control.objects.get(pk=pk)
        new_polar_angle = Decimal('0.34567')
        data = {
            'name': control.name,
            'type': control.type,
            'maximum_rabi_rate': control.maximum_rabi_rate,
            'polar_angle': new_polar_angle
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        control = Control.objects.get(pk=pk)
        self.assertEqual(control.polar_angle, new_polar_angle)

    def test_delete_control(self):
        pk = 1
        url = reverse('control-detail', args=[pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Control.objects.count(), self.control_count - 1)

    @unittest.skip("Django does not parse data binary correctly.")
    def test_csv_upload(self):
        url = reverse('control-upload')
        with open('qctrl/api/fixtures/controls.csv', 'rb') as f:
            response = self.client.post(url, {'data': f}, format='csv')
            self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)

    def test_csv_download(self):
        url = reverse('control-download')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        controls = Control.objects.all()
        for result, control in zip(response.data, controls):
            self._response_result_equal_control(result,
                                                control,
                                                type_display_value=False)
