from django.test import TestCase
from django.contrib.gis.geos import Point
from django.conf import settings

from tests.models import Place, SpatialPlace
from tests.forms import LocationForm

from pyquery import PyQuery as pq

import json


class LocationFieldTest(TestCase):
    def test_plain(self):
        vals = {
            'city': 'Bauru',
            'location': '-22.2878573,-49.0905487',
        }

        obj = Place.objects.create(**vals)

        self.assertEqual(obj.city, 'Bauru')
        self.assertEqual(obj.location, '-22.2878573,-49.0905487')

    def test_spatial(self):
        vals = {
            'city': 'Bauru',
            'location': 'POINT(-22.2878573 -49.0905487)',
        }

        obj = SpatialPlace.objects.create(**vals)

        self.assertEqual(obj.city, 'Bauru')
        self.assertEqual(obj.location, Point(-22.2878573, -49.0905487))

    def test_field_options(self):
        form = LocationForm(initial={})
        d = pq(str(form))

        opts = json.loads(d('[data-location-field-options]').attr(
            'data-location-field-options'))

        location_field_opts = settings.LOCATION_FIELD

        for key, value in location_field_opts.items():
            self.assertEqual(value, opts[key])
