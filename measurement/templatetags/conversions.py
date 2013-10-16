from django import template
from django.utils.safestring import mark_safe

from ..fields import D, DistanceField
import copy, json

register = template.Library()

UNITS = copy.copy(D.UNITS)
for k, v in D.ALIAS.iteritems( ):
    UNITS[k] = UNITS[v]

@register.simple_tag
def conversions_json( ): return mark_safe(json.dumps(UNITS))

@register.simple_tag
def unit_regex( ): return json.dumps(DistanceField.ALPHA_REGEX.pattern)