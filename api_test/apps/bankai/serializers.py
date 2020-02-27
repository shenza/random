from rest_framework import serializers
from django.conf import settings

from api_test.apps.bankai.models import Control


class ChoiceDisplayValueField(serializers.ChoiceField):
    """Allow use of display value for ChoiceField when reading and writing."""

    def to_representation(self, value):
        try:
            return self._choices[value]
        except KeyError:
            raise serializers.ValidationError(
                "Acceptable values are {0}".format(list(self._choices.keys())))

    def to_internal_value(self, data):
        if data in self._choices.keys():
            return data
        # get choice value from label

        inverted_choices = {v: k for k, v in self._choices.items()}
        print (inverted_choices)
        try:
            return inverted_choices[data]
        except KeyError:
            raise serializers.ValidationError(
                "Acceptable values are {0}".format(list(
                    self._choices.values())))


class ControlSerializer(serializers.HyperlinkedModelSerializer):
    #owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Control
        fields = ['id','name', 'type', 'maximum_rabi_rate', 'polar_angle']