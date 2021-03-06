from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.utils.six import string_types

def valid_unit_type(value):
    from .fields import DistanceField, D

    if not value: return
    if isinstance(value, string_types):
        try:
            r, f = DistanceField.parse_string(value)
        except ValueError:
            raise ValidationError(_("Please enter a valid distance."))
        if r == None:
            units = [g for g in list(D.ALIAS.values()) if '_' not in g]
            raise ValidationError(_("Please choose a valid distance unit from"+\
                " %(units)s." % {'units': ", ".join(units)}))