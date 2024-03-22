from rest_framework import serializers
from rest_framework.serializers import traceback, model_meta, raise_errors_on_nested_writes
from crm.models.models import *
from crm.models.exceptions import RecordAlreadyExists

class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = '__all__'
        read_only_fields = []
class CustomerSerializer(serializers.ModelSerializer):

    #remove uniquetogether validator for cust_nric field as the uniqueness will be handled by returning the said instance if it exists
    def get_unique_together_validators(self):
        validators = super().get_unique_together_validators()
        validators_without_cust_nric = [validator for validator in validators if validator.fields[0] not in ['cust_nric', 'cust_email', 'cust_phone_num']]
        return validators_without_cust_nric
    
    #handling of cust_nric uniqueness enforcement by looking up model with the same cust_nric value and raise Exception if value already exists thus preventing duplicate
    def create(self, validated_data):
        raise_errors_on_nested_writes('create', self, validated_data)

        ModelClass = self.Meta.model

        # Remove many-to-many relationships from validated_data.
        # They are not valid arguments to the default `.create()` method,
        # as they require that the instance has already been saved.
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            cust_nric = validated_data.pop('cust_nric', None)
            instance, created = ModelClass._default_manager.get_or_create(cust_nric=cust_nric, defaults=validated_data)
            if not created:
                raise RecordAlreadyExists('Existing record is found with cust_nric='+str(cust_nric)+' therefore, instance is not created')
            
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                'Got a `TypeError` when calling `%s.%s.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.%s.create()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception was:\n %s' %
                (
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    self.__class__.__name__,
                    tb
                )
            )
            raise TypeError(msg)

        # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                field.set(value)

        return instance
    
    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ['cust_id']

class CustomerTreatmentSerializer(CustomerSerializer):
    treatments = TreatmentSerializer(many=True, required=False)
    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ['cust_id']