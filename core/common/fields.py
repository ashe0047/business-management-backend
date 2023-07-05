from rest_framework.serializers import *
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist


class GenericForeignKeyRelatedField(RelatedField):
    def __init__(self, *args, **kwargs):
        self.content_type_field = kwargs.pop('content_type_field', 'content_type')
        self.object_id_field = kwargs.pop('object_id_field', 'object_id')
        self.app_label= kwargs.pop('app_label', None)
        self.content_type = None
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        voucher_sale_type = self.context.get('view').get_serializer().instance.voucher_sale_type
        if voucher_sale_type:
            voucher_class = voucher_sale_type.model_class()
            return voucher_class.objects.all()
        
        return super().get_queryset()
    
    def to_internal_value(self, data):
        try:
            self.content_type = ContentType.objects.get_by_natural_key(app_label=self.app_label, model=data[self.content_type_field])
        except ObjectDoesNotExist:
            raise ValidationError('ContentType with app_label='+self.app_label+' and model='+data[self.content_type_field]+' does not exists')
        
        try:
            self.object_id = int(data[self.object_id_field])
            if self.object_id <= 0:
                raise ValueError
        except (ValueError, TypeError):
            raise ValidationError('object_id must be a positive integer')
        
        try:
            self.content_object_class = self.content_type.model_class()
            self.content_object = self.content_object_class.objects.get(pk=self.object_id)
        except ObjectDoesNotExist:
            raise ValidationError('Content object not found, pk value might be invalid')
        
        return self.content_object
    
    def to_representation(self, value):
        self.content_object_class = ContentType.objects.get_for_model(value).model
        self.object_id = value.voucher_id

        return {
            self.content_type_field: self.content_object_class,
            self.object_id_field: self.object_id
        }