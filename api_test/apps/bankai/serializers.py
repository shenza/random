from rest_framework import serializers
from django.conf import settings

from api_test.apps.bankai.models import Control
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

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
    
    #@swagger_auto_schema(method='put', auto_schema=None)
    class Meta:
        model = Control
        fields = ['id','name', 'type', 'maximum_rabi_rate', 'polar_angle']
        swagger_schema_fields = {
            "definitions": {},
            "$schema": "http://json-schema.org/draft-07/schema#",
            "$id": "http://example.com/root.json",
            "type": "object",
            "title": "The Root Schema",
            "required": [
                "data"
            ],
            "properties": {
                "data": {
                "$id": "#/properties/data",
                "type": "object",
                "title": "The Data Schema",
                "required": [
                    "id",
                    "type",
                    "attributes"
                ],
                "properties": {
#                    "id": {
#                    "$id": "#/properties/data/properties/id",
#                    "type": "integer",
#                    "title": "The Id Schema",
#                    "default": 0,
#                    "examples": [
#                        65
#                    ]
#                    },
                    "type": {
                    "$id": "#/properties/data/properties/type",
                    "type": "String",
                    "title": "The Type Schema",
                    "default": "",
                    "examples": [
                        "Control"
                    ],
                    "pattern": "^(.*)$"
                    },
                    "attributes": {
                    "$id": "#/properties/data/properties/attributes",
                    "type": "object",
                    "title": "The Attributes Schema",
                    "required": [
                        "name",
                        "type",
                        "maximum_rabi_rate",
                        "polar_angle"
                    ],
                    "properties": {
                        "name": {
                        "$id": "#/properties/data/properties/attributes/properties/name",
                        "type": "string",
                        "title": "The Name Schema",
                        "default": "",
                        "examples": [
                            "andras"
                        ],
                        "pattern": "^(.*)$"
                        },
                        "type": {
                        "$id": "#/properties/data/properties/attributes/properties/type",
                        "type": "string",
                        "title": "The Type Schema",
                        "default": "",
                        "examples": [
                               "Primitive", "CORPSE", "Gaussian", "CinBB", "CinSK"
                         
                        ],
                        "pattern": "^(.*)$"
                        },
                        "maximum_rabi_rate": {
                        "$id": "#/properties/data/properties/attributes/properties/maximum_rabi_rate",
                        "type": "integer",
                        "minimum": 0,
                        "maximum":100,
                        "title": "The maximum achievable angular frequency of the Rabi cycle for a driven quantum transition. Here, this is a number between 0 and 100.",
                        "default": "",
                        "examples": [
                            "64"
                        ],
                        "pattern": "^(.*)$"
                        },
                        "polar_angle": {
                        "$id": "#/properties/data/properties/attributes/properties/polar_angle",
                        "type": "float",
                        "minimum": 0,
                        "maximum":1,
                        "title": "An angle measured from the z-axis on the Bloch sphere. This is a number between 0 and 1 (units of pi).",
                        "default": "",
                        "examples": [
                            "0.27"
                        ],
                        "pattern": "^(.*)$"
                        }
                    }
                    }
                }
                }
            }
            }