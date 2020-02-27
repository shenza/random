from django.db import models
from django.test import TestCase
from rest_framework import serializers

from ..serializers import ChoiceDisplayValueField


class ChoiceDisplayValueFieldTestCase(TestCase):
    class QualityChoices(models.TextChoices):
        POOR = 'poor', 'Poor quality'
        MEDIUM = 'medium', 'Medium quality'
        GOOD = 'good', 'Good quality'

    @classmethod
    def setUpTestData(cls):
        cls.field = ChoiceDisplayValueField(choices=cls.QualityChoices.choices)

    def test_data_is_value(self):
        """If data is a valid choice value."""
        for choice in self.QualityChoices.values:
            self.assertEqual(self.field.to_internal_value(choice), choice)

    def test_data_not_value_not_label(self):
        with self.assertRaises(serializers.ValidationError):
            self.field.to_internal_value('Nice quality')

    def test_data_is_label(self):
        """If data is a valid choice label (human-readable display value)."""
        for value, label in zip(self.QualityChoices.values,
                                self.QualityChoices.labels):
            self.assertEqual(self.field.to_internal_value(label), value)

    def test_to_representation(self):
        for value, label in zip(self.QualityChoices.values,
                                self.QualityChoices.labels):
            self.assertEqual(self.field.to_representation(value), label)
        with self.assertRaises(serializers.ValidationError):
            self.field.to_representation('Nice')
