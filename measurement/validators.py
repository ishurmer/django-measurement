from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.utils.six import string_types

def valid_unit_type(value):
    from .fields import DistanceField, D

    if not value: return
    if isinstance(value, string_types):
        r, f = DistanceField.parse_string(value)
        if r == None:
            units = filter(lambda g: '_' not in g, D.ALIAS.values())
            raise ValidationError(_("Please choose a valid distance unit from"+\
                " %(units)s." % {'units': ", ".join(units)}))