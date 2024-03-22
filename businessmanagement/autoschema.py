
from drf_spectacular.openapi import AutoSchema as BaseAutoSchema
from rest_framework.generics import *
from rest_framework.views import *
from rest_framework import serializers
from pos.serializers.fields import *

import copy
import functools
import re
import typing
from collections import defaultdict

import uritemplate
from django.core import exceptions as django_exceptions
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import permissions, renderers, serializers
from rest_framework.fields import _UnvalidatedField, empty
from rest_framework.generics import CreateAPIView, GenericAPIView, ListCreateAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.schemas.inspectors import ViewInspector
from rest_framework.schemas.utils import get_pk_description  # type: ignore
from rest_framework.settings import api_settings
from rest_framework.utils.model_meta import get_field_info
from rest_framework.views import APIView

from drf_spectacular.authentication import OpenApiAuthenticationExtension
from drf_spectacular.contrib import *  # noqa: F403, F401
from drf_spectacular.drainage import add_trace_message, get_override, has_override
from drf_spectacular.extensions import (
    OpenApiFilterExtension, OpenApiSerializerExtension, OpenApiSerializerFieldExtension,
)
from drf_spectacular.plumbing import (
    ComponentRegistry, ResolvedComponent, UnableToProceedError, append_meta,
    assert_basic_serializer, build_array_type, build_basic_type, build_choice_field,
    build_examples_list, build_generic_type, build_listed_example_value, build_media_type_object,
    build_mocked_view, build_object_type, build_parameter_type, build_serializer_context, error,
    filter_supported_arguments, follow_field_source, follow_model_field_lookup, force_instance,
    get_doc, get_list_serializer, get_manager, get_type_hints, get_view_model, is_basic_serializer,
    is_basic_type, is_field, is_list_serializer, is_list_serializer_customized,
    is_patched_serializer, is_serializer, is_trivial_string_variation,
    modify_media_types_for_versioning, resolve_django_path_parameter, resolve_regex_path_parameter,
    resolve_type_hint, safe_ref, sanitize_specification_extensions, warn, whitelisted,
)
from drf_spectacular.settings import spectacular_settings
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiCallback, OpenApiParameter, OpenApiRequest, OpenApiResponse

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

    def _get_serializer_field_meta(self, field, direction):
        if not isinstance(field, serializers.Field):
            return {}

        meta = {}
        if field.read_only:
            meta['readOnly'] = True
        if field.write_only:
            meta['writeOnly'] = True
        if field.allow_null:
            meta['nullable'] = True
        if isinstance(field, serializers.CharField) and not field.allow_blank:
            # blank check only applies to inbound requests
            if spectacular_settings.COMPONENT_SPLIT_REQUEST:
                if direction == 'request':
                    meta['minLength'] = 1
            elif spectacular_settings.ENFORCE_NON_BLANK_FIELDS:
                if not field.read_only:
                    meta['minLength'] = 1
        if field.default is not None and field.default != empty and not callable(field.default):
            if isinstance(
                field,
                (
                    serializers.ModelField,
                    serializers.SerializerMethodField,
                    serializers.PrimaryKeyRelatedField,
                    serializers.SlugRelatedField,
                ),
            ):
                # Skip coercion for lack of a better solution. These are special in that they require
                # a model instance or object (which we don't have) instead of a plain value.
                default = field.default
            else:
                try:
                    # gracefully attempt to transform value or just use as plain on error
                    default = field.to_representation(field.default)
                    

                except:  # noqa: E722
                    default = field.default

            if isinstance(default, set):
                default = list(default)
            meta['default'] = default
        if field.label and not is_trivial_string_variation(field.label, field.field_name):
            meta['title'] = str(field.label)
        if field.help_text:
            meta['description'] = str(field.help_text)
        
        
        return meta

    # def _map_serializer_field(self, field, direction, bypass_extensions=False):
    #    #skip showing these auto calculated fields in api input schema
    #    if field.field_name not in ['gross_sales_item_unit_price', 'net_sales_item_unit_price', 'gross_sales_item_total_price', 'net_sales_item_total_price']:
    #         return super()._map_serializer_field(field, direction, bypass_extensions)
    #    else:
    #        return None
        