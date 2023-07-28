from rest_framework import serializers
from marketing.models.models import *
from marketing.serializers.validators import GenericVoucherValidator, CategoryVoucherValidator, ItemVoucherValidator
from pos.models.models import SaleItem, Sale
from core.utils import context_update_parent

class BaseGenericVoucherSerializer(serializers.ModelSerializer):
    sale = serializers.PrimaryKeyRelatedField(read_only=True, many=True) #reverse relation

    def get_validators(self):
        custom_validators = super().get_validators()
        default_validators = self.get_unique_together_validators() + self.get_unique_for_date_validators()
        return custom_validators+default_validators
    
    class Meta:
        model = GenericVoucher
        fields = '__all__'
        read_only_fields = ('voucher_code', 'voucher_created_date', 'voucher_redemption_count',)
        validators = [GenericVoucherValidator()]

class BaseItemVoucherSerializer(serializers.ModelSerializer):
    saleitem_sale = serializers.PrimaryKeyRelatedField(read_only=True, many=True) #reverse relation
    saleitem_use = serializers.PrimaryKeyRelatedField(read_only=True, many=True) #reverse relation

    def get_validators(self):
        custom_validators = super().get_validators()
        default_validators = self.get_unique_together_validators() + self.get_unique_for_date_validators()
        return custom_validators+default_validators

    class Meta:
        model = ItemVoucher
        fields = '__all__'
        read_only_fields = ('voucher_code', 'voucher_created_date', 'voucher_redemption_count',)
        validators = [ItemVoucherValidator()]

class BaseCategoryVoucherSerializer(serializers.ModelSerializer):
    saleitem_sale = serializers.PrimaryKeyRelatedField(read_only=True, many=True) #reverse relation
    saleitem_use = serializers.PrimaryKeyRelatedField(read_only=True, many=True) #reverse relation

    def get_validators(self):
        custom_validators = super().get_validators()
        default_validators = self.get_unique_together_validators() + self.get_unique_for_date_validators()
        return custom_validators+default_validators
    
    class Meta:
        model = CategoryVoucher
        fields = '__all__'
        read_only_fields = ('voucher_code', 'voucher_created_date', 'voucher_redemption_count',)
        validators = [CategoryVoucherValidator()]


