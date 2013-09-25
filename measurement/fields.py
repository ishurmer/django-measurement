from django.contrib.gis.measure import D as _D
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.db import models
from django.db.models import signals
from django.utils.six import with_metaclass
from django.utils.translation import ugettext as _

from . import forms, validators

import re

''' A "compound" field that represents a distance measurement, from 
    django.contrib.gis.measure. Stores the field internally using two (or,
    optionally, three) fields:

        a) Measurement value - a float field representing the actual value of
           the measurement. This is the data stored by the main field.
           Internally we convert to whatever is stored in the default_units
           kwarg.
        b) Measurement unit - a String field representing the default unit name,
           e.g. 'mi'. This is the units that were used to create the distance.
           If the field name is not supplied through the "unit_field_"
           kwarg, then it will be retrieved in the "default_unit" format.
'''

try:
    basestring
except NameError:
    basestring = (str, unicode)

class D(_D):
    UNITS = _D.UNITS
    UNITS.update({
        'u': 0.04445
    })

    def __unicode__(self):
        return "%d%s" % (getattr(self, self._default_unit), self._default_unit)

class DistanceFieldDescriptor(object):
    def __init__(self, field):
        self.field = field

    def __get__(self, instance=None, owner=None):
        if instance is None:
            raise AttributeError(
                "The '%s' attribute can only be accessed from %s instances."
                % (self.field.name, owner.__name__))

        return instance.__dict__[self.field.name]

    def __set__(self, instance, value):
        parsed = False
        if value == None or value == '':
            instance.__dict__[self.field.name] = None
        elif isinstance(value, basestring):
            dist, has_units = DistanceField.parse_string(
                value, self.field.default_unit)
            instance.__dict__[self.field.name] = dist
            self.field._has_no_units = not has_units
        elif isinstance(value, D):
            instance.__dict__[self.field.name] = value
        else:
            self.field._has_no_units = True
            dist = D(**{self.field.default_unit: float(value)})
            instance.__dict__[self.field.name] = dist

        self.field.update_unit_fields(instance)


class DistanceField(models.Field):
    ALPHA_REGEX = re.compile('([\s\-\_a-z]+)$', re.I)

    descriptor_class = DistanceFieldDescriptor
    default_validators = [validators.valid_unit_type]

    def __init__(self, decimal_places=4, max_digits=12,
                 unit_field=None, unit='m', *args, **kwargs):
        self.decimal_places = decimal_places
        self.max_digits = max_digits
        self.unit_field = unit_field
        self.default_unit = unit
        super(DistanceField, self).__init__(*args, **kwargs)

    def formfield(self, form_class=None, choices_form_class=None, **kwargs):
        return super(DistanceField, self).formfield(
            form_class=forms.DistanceField,
            choices_form_class=choices_form_class, **kwargs)

    def get_internal_type(self):
        return 'DecimalField'

    def contribute_to_class(self, cls, name):
        super(DistanceField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, self.descriptor_class(self))
        signals.post_init.connect(self.update_after_init, sender=cls)

    @staticmethod
    def parse_string(value, default_units='m'):
        if not value: return None, False
        units = DistanceField.ALPHA_REGEX.findall(value)
        has_units = False
        if not units:
            units = default_units
            value = float(value)
        else:
            has_units = True
            units = units[0].strip( )
            value = float(value.replace(units, ''))
        try:
            return (D(**{D.unit_attname(units): value}), has_units)
        except:
            return None, False

    @staticmethod
    def distance_to_parts(distance):
        if distance == None: return (None, None, None)
        u = distance._default_unit
        return (getattr(distance, u), u, distance.m)

    def update_after_init(self, instance, *args, **kwargs):
        if getattr(self, '_has_no_units', False) and self.unit_field:
            dist = getattr(instance, self.name)
            units = getattr(instance, self.unit_field)
            if not units: return
            parts = DistanceField.distance_to_parts(dist)
            if parts[1] != units:
                conv = getattr(dist, units)
                dist = D(**{units: conv})
                instance.__dict__[self.name] = dist

    def update_unit_fields(self, instance, *args, **kwargs):
        if not self.unit_field: return

        distance = DistanceField.distance_to_parts(getattr(
                                                   instance, self.attname))
        try:
            if distance[0] == None:
                setattr(instance, self.unit_field, None)
            else:
                setattr(instance, self.unit_field, distance[1])
        except AttributeError:
            raise ImproperlyConfigured, "DistanceField %s has unit field " % (
                self.name)+"property %s specified, but field cannot be " % (
                    self.unit_field) +"found on instance."

    def pre_save(self, model_instance, add=False):
        self.update_unit_fields(model_instance)
        return getattr(model_instance, self.name)

    def get_prep_value(self, value):
        converted = getattr(value, self.default_unit)
        return converted

    def get_db_prep_value(self, value, connection, prepared=False):
        # Convert it to the "default_unit" format.
        value = super(DistanceField, self).get_db_prep_value(value, connection,
                                                             prepared)
        return connection.ops.value_to_db_decimal(value,
                self.max_digits, self.decimal_places)

    def get_prep_value(self, value):
        if value == None or value == '':
            return None
        elif isinstance(value, basestring):
            dist, has_units = DistanceField.parse_string(
                value, self.default_unit)
        elif isinstance(value, D):
            dist = value
        else:
            try:
                return float(value)
            except:
                raise ValueError, 'Comparison value must be a string, '+\
                    'number, or distance object.'

        return getattr(dist, self.default_unit)

    def get_prep_lookup(self, lookup_type, value):
        if lookup_type in ('exact', 'iexact', 'gt', 'gte', 'lt', 'lte'):
            return self.get_prep_value(value)
        elif lookup_type == 'in':
            return [self.get_prep_value(v) for v in value]
        else:
            raise TypeError('Lookup type %r not supported.' % lookup_type)

try:
    from south.modelsinspector import add_introspection_rules
    rules = [(
        (DistanceField, ),
        [], {
            "max_digits": ["max_digits", {"default": 12}],
            "decimal_places": ["decimal_places", {"default": 4}],
            "unit_field": ["unit_field", {"default": None}],
            "default_unit": ["default_unit", {"default": "m"}]
        }
    )]
    add_introspection_rules(rules, ["^measurement.fields.DistanceField"])
except ImportError:
    pass