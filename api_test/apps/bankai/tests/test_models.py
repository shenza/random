from django.core.exceptions import ValidationError
from django.test import TestCase
from qctrl.api.models import Control


class ControlTestCase(TestCase):
    def test_maximum_rabi_rate_range(self):
        for invalid_rate in ('-0.00001', '100.1', '2.333333'):
            control = Control.objects.create(
                name='Control',
                type=Control.ControlChoices.values[0],
                maximum_rabi_rate=invalid_rate,
                polar_angle='0.5')
            with self.assertRaises(ValidationError):
                control.full_clean()

        for valid_rate in ('0', '-0.0', '100', '99.99999', '50.5'):
            control = Control.objects.create(
                name='Control',
                type=Control.ControlChoices.values[0],
                maximum_rabi_rate=valid_rate,
                polar_angle='0.5')
            control.full_clean()

    def test_polar_angle_range(self):
        for invalid_angle in ('-0.00001', '1.1', '0.333333'):
            control = Control.objects.create(
                name='Control',
                type=Control.ControlChoices.values[0],
                maximum_rabi_rate='50',
                polar_angle=invalid_angle)
            with self.assertRaises(ValidationError):
                control.full_clean()

        for valid_angle in ('0', '-0.0', '1', '0.99999', '0.5'):
            control = Control.objects.create(
                name='Control',
                type=Control.ControlChoices.values[0],
                maximum_rabi_rate='50',
                polar_angle=valid_angle)
            control.full_clean()
