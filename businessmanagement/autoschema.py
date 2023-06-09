
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

  
        assert_basic_serializer(serializer)
        serializer = force_instance(serializer)
        
        # serializers provided through @extend_schema will not receive the mock context
        # via _get_serializer(). Establish behavioral symmetry for those use-cases.
        if not serializer.context:
            serializer.context.update(build_serializer_context(self.view))
        required = set()
        properties = {}

        for field in serializer.fields.values():
            if isinstance(field, serializers.HiddenField):
                continue
            if field.field_name in get_override(serializer, 'exclude_fields', []):
                continue
            # if isinstance(serializer, BaseSaleItemSaleSerializer):
            #     if isinstance(field, ListSerializer):
            #         print(field.child._context)
            schema = self._map_serializer_field(field, direction)
            # skip field if there is no schema for the direction
            if schema is None:
                continue

            add_to_required = (
                field.required
                or (schema.get('readOnly') and not spectacular_settings.COMPONENT_NO_READ_ONLY_REQUIRED)
            )
            if add_to_required:
                required.add(field.field_name)

            self._insert_field_validators(field, schema)

            if field.field_name in get_override(serializer, 'deprecate_fields', []):
                schema['deprecated'] = True

            properties[field.field_name] = safe_ref(schema)

        if is_patched_serializer(serializer, direction):
            required = []

        return build_object_type(
            properties=properties,
            required=required,
            description=get_doc(serializer.__class__),
        )