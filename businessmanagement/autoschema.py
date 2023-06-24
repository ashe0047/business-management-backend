
from drf_spectacular.openapi import AutoSchema as BaseAutoSchema
from rest_framework.generics import *
from rest_framework.views import *

from django.utils.translation import gettext_lazy as _

class AutoSchema(BaseAutoSchema):

    def is_field_serializer(self, serializer, direction, name):
        # print(serializer.context)
        if serializer._context.get('parent'):
            return "Field" + name
        else:
            return name
        
    def _get_serializer_name(self, serializer, direction, bypass_extensions=False):
        name = super()._get_serializer_name(serializer, direction, bypass_extensions)
        name = self.is_field_serializer(serializer, direction, name)
        return name


    