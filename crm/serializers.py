from rest_framework import serializers
from crm.models import *

class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = '__all__'
        read_only_fields = []
class CustomerSerializer(serializers.ModelSerializer):
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