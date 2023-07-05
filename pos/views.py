from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, DestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Prefetch
from django.db import transaction
from pos.models.models import *
from pos.serializers.saleitem_serializers import *
from pos.serializers.sale_serializers import *
from pos.permissions import DeleteSalesPerm
from pos.utils import update_pkg_sub_payment
from crm.serializers import *
from drf_spectacular.utils import *


# Create your views here.
#use try-except block
#use serializer where possible

class SaleView(RetrieveUpdateAPIView):
    serializer_class = BaseSaleItemSaleSerializer
    queryset = Sale.objects.all()
    # permission_classes = [IsAuthenticated, DeleteSalesPerm]
    
    def get_serializer_class(self):
        method = self.request.method
        if method in ['PUT', 'PATCH']:
            return SaleItemSaleWriteSerializer
        elif method in ['GET']:
            return SaleItemSaleReadSerializer

    #override get_object to prefetch salesitem for sales object
    @transaction.atomic
    def get_object(self):
        instance = super().get_object()
        prefetch_saleitem = Prefetch('saleitem', queryset=SaleItem.objects.all())
        instance = Sale.objects.prefetch_related(prefetch_saleitem).get(sales_id=instance.sales_id)
        
        return instance
    
    # @transaction.atomic
    # def put(self, request, *args, **kwargs):
    #     sale_instance = self.get_object()
    #     sale_serializer = self.get_serializer(sale_instance, data=request.data)
    #     sale_serializer.is_valid(raise_exception=True)
    #     saleitem = []
    #     cust = {}
    #     try:
    #         if 'cust' in sale_serializer.validated_data:
    #             cust = sale_serializer.validated_data.pop('cust', {})
    #             cust_instance = Customer.objects.get(cust_nric=cust['cust_nric'])
    #             sale_serializer.validated_data['cust'] = cust_instance               

    #         if 'saleitem' in sale_serializer.validated_data:
    #             saleitem = sale_serializer.validated_data.pop('saleitem',  [])
    #         sale_instance = sale_serializer.save()
    #         if saleitem:
    #             sale_instance.saleitem.all().delete()

    #             sale_item_instances = []
    #             sales_id = sale_instance.sales_id
    #             for item in saleitem:
    #                 if 'pkg_sub' in item:
    #                     pkg_sub = item.pop('pkg_sub')
    #                     pkg_sub['cust_id'] = cust_instance.cust_id
    #                     pkg_sub_instance = PackageSubscription.objects.create(**pkg_sub)
    #                     item['pkg_sub'] = pkg_sub_instance

    #                 sale_item_instance = SaleItem.objects.create(sales_id=sales_id, **item)
    #                 sale_item_instance.save()
    #                 sale_item_instances.append(sale_item_instance)
    #             sale_instance.saleitem.set(sale_item_instances)
    #         return Response(sale_serializer.data, status=status.HTTP_200_OK)
        
    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # @transaction.atomic
    # def patch(self, request, *args, **kwargs):
    #     sale_instance = self.get_object()
    #     sale_serializer = self.get_serializer(sale_instance, data=request.data, partial=True)
    #     sale_serializer.is_valid(raise_exception=True)
    #     saleitem = []
    #     cust = {}
    #     try:
    #         if 'cust' in sale_serializer.validated_data:
    #             cust = sale_serializer.validated_data.pop('cust', {})
    #             cust_instance = Customer.objects.get(cust_nric=cust['cust_nric'])
    #             sale_serializer.validated_data['cust'] = cust_instance    

    #         if 'saleitem' in sale_serializer.validated_data:
    #             saleitem = sale_serializer.validated_data.pop('saleitem',  [])
    #         sale_instance = sale_serializer.save()

    #         if saleitem:
    #             sale_instance.saleitem.all().delete()
    #             sale_item_instances = []
    #             sales_id = sale_instance.sales_id
    #             for item in saleitem:
    #                 if 'pkg_sub' in item:
    #                     pkg_sub = item.pop('pkg_sub')
    #                     pkg_sub['cust_id'] = cust_instance.cust_id
    #                     pkg_sub_instance = PackageSubscription.objects.create(**pkg_sub)
    #                     item['pkg_sub'] = pkg_sub_instance

    #                 sale_item_instance = SaleItem.objects.create(sales_id=sales_id, **item)
    #                 sale_item_instance.save()
    #                 sale_item_instances.append(sale_item_instance)
    #             sale_instance.saleitem.set(sale_item_instances)
    #         return Response(sale_serializer.data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        '''
        *** IMPORTANT ***
        SaleView is only responsible for updating the Sale instance's fields and not the fields of any nested object.
        Nested field will be updated by deleting the old associated instance and a new instance will be created from the data and reassociated with the field

        Fields:
            cust: cust_nric field from cust data will be used to lookup the Customer model to check if an instance exists and return it if so else a new Customer instance will be created with using the cust data
        '''
        return super().put(request, *args, **kwargs)
    
    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        '''    
        *** IMPORTANT ***
        SaleView is only responsible for updating the Sale instance's fields and not the fields of any nested object.
        Nested field will be updated by deleting the old associated instance and a new instance will be created from the data and reassociated with the field

        Fields:
            cust: cust_nric field from cust data will be used to lookup the Customer model to check if an instance exists and return it if so else a new Customer instance will be created with using the cust data
        '''
        return super().patch(request, *args, **kwargs)
    
class SalesView(CreateAPIView, ListAPIView, DestroyAPIView):
    serializer_class = BaseSaleItemSaleSerializer
    queryset = Sale.objects.all()
    # permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        method = self.request.method
        if method in ['POST']:
            return SaleItemSaleWriteSerializer
        elif method in ['GET']:
            return SaleItemSaleReadSerializer
        
    # @transaction.atomic       
    # def create(self, request, *args, **kwargs):
    #     '''
    #     MOD:

        
    #     '''
    #     cust_instance = Customer.objects.filter(cust_nric=request.data['cust']['cust_nric'])
    #     if cust_instance.exists():
    #         request.data.pop('cust')
    #         cust_instance = cust_instance.first()
    #     sale_serializer = self.get_serializer(data=request.data)
    #     sale_serializer.is_valid(raise_exception=True)

    #     sales_item = []
    #     cust = {}
    #     if 'saleitem' in sale_serializer.validated_data:
    #         sales_item = sale_serializer.validated_data.pop('saleitem', [])
        
    #     if 'cust' in sale_serializer.validated_data:
    #         cust = sale_serializer.validated_data.pop('cust', {})
    #         cust_serializer = CustomerSerializer(data=cust)
    #         cust_serializer.is_valid(raise_exception=True)
    #         cust_instance = cust_serializer.save()

    #     sale_serializer.validated_data['cust'] = cust_instance   
    #     sale_instance = sale_serializer.save()
        
    #     sale_item_instances = []
    #     sales_id = sale_instance.sales_id
    #     for item in sales_item:
    #         # sale_item_serializer = SaleItemSerializer(data=item)
    #         # sale_item_serializer.is_valid(raise_exception=True)
    #         # item['sales_id'] = sales_id
    #         # sale_item_instance = sale_item_serializer.save()
    #         if 'pkg_sub' in item:
    #             pkg_sub = item.pop('pkg_sub')
    #             pkg_sub['cust_id'] = cust_instance.cust_id
    #             pkg_sub_instance = PackageSubscription.objects.create(**pkg_sub)
    #             item['pkg_sub'] = pkg_sub_instance

    #         sale_item_instance = SaleItem.objects.create(sales_id=sales_id, **item)
    #         sale_item_instance.save()
    #         # if 'service' in sale_item_serializer.validated_data:
    #         #     service = sale_item_serializer.validated_data.pop('service')
    #         #     service_instance = get_object_or_404(Service, service_id=service)
    #         #     sale_item_instance.service = service_instance
                
    #         # elif 'pkg_sub' in sale_item_serializer.validated_data:
    #         #     pkg_sub = sale_item_serializer.validated_data.pop('pkg_sub')
    #         #     pkg_sub_instance = get_object_or_404(PackageSubscription, pkg_sub_id=pkg_sub)
    #         #     sale_item_instance.pkg_sub = pkg_sub_instance

    #         # elif 'prod' in sale_item_serializer.validated_data:
    #         #     prod = sale_item_serializer.validated_data.pop('prod')
    #         #     prod_instance = get_object_or_404(Product, prod_id=prod)
    #         #     sale_item_instance.prod = prod_instance
            
    #         sale_item_instances.append(sale_item_instance)
    #     sale_instance.saleitem.set(sale_item_instances)

    #     headers = self.get_success_headers(sale_serializer.data)
    #     return Response(sale_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        '''
        Fields:
            cust: cust_nric field from cust data will be used to lookup the Customer model to check if an instance exists and return it if so else a new Customer instance will be created with using the cust data
        '''
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="sale",
                description= "Specify 'sale_id(s)' to delete a single/multiple Sale record",
                required=False,
                type={'type': 'array', 'items': {'type': 'number'}},
                location=OpenApiParameter.QUERY)
            ],
        responses={
            '400': OpenApiResponse(response=str, examples=[OpenApiExample(name="400",value={"error": "error_message"})]),
            '204': OpenApiResponse(examples=[OpenApiExample(name='204', description='No message will be returned')])
        }
    )
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        #deletes all linked sale item to prevent protected error then delete sale
        sales_ids = request.query_params.getlist('sale', [])
        item_not_deleted = []
        if sales_ids:
            for sales_id in sales_ids:
                try:
                    sale = get_object_or_404(self.get_queryset(), sales_id=sales_id)
                    sale.saleitem.all().delete()
                    sale.delete()               
                except Exception as e:
                    item_not_deleted.append({"sales_id": sales_id, "err_msg": str(e)})
            if len(item_not_deleted) == 0:
                    return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'Sale with id(s) in '+str(item_not_deleted)+" are not deleted"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': "Please provide at least one sale to delete"}, status=status.HTTP_404_NOT_FOUND)
        # option to delete selected saleitem from sale
        # if sale:
        #     sale_item_ids = request.query_params.getlist('saleitem')
        #     item_not_deleted = []
        #     if sale_item_ids:
        #         for sale_item_id in sale_item_ids:
        #             try:
        #                 sale_item = SaleItem.objects.get(sales_item_id=sale_item_id)
        #                 sale_item.delete()
        #             except SaleItem.DoesNotExist:
        #                 item_not_deleted.append(sale_item_id)

        #         if len(item_not_deleted) == 0:
        #             return Response(status=status.HTTP_204_NO_CONTENT)
        #         else:
        #             return Response({'error': 'SaleItems with id in '+str(item_not_deleted)+" are not deleted"}, status=status.HTTP_404_NOT_FOUND)
        #     else:
        #         sale.delete()
        #         return Response(status=status.HTTP_204_NO_CONTENT)
    
    @transaction.atomic
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
class SaleItemView(RetrieveUpdateAPIView):
    serializer_class = BaseSaleItemSerializer
    queryset = SaleItem.objects.all()
    # permission_classes = [IsAuthenticated, DeleteSalesPerm]
    
    def get_serializer_class(self):
        method = self.request.method
        if method in ['PUT', 'PATCH']:
            return SaleItemWriteSerializer
        elif method in ['GET']:
            return SaleItemReadSerializer
   
    # @transaction.atomic
    # def put(self, request, *args, **kwargs):
    #     '''
    #     MOD:
    #         1. Using serializer to create PackageSubscription instead of using model directly
        
    #     *** IMPORTANT ***
    #     SaleItemView is only responsible for updating the SaleItem instance's fields and not the fields of any nested object
        
    #     1. pkg_sub update logic: pkg_sub field can only be updated to a new instance be creating a new instance and not by referencing an existing instance as PackageSubscription cannot be created standalone without a SaleItem binding
    #     '''
    #     sale_item_instance = self.get_object()
    #     #reset existing special fields in saleitem
    #     special_fields = ['prod', 'service', 'pkg_sub']
    #     for field in special_fields:
    #         if field in request.data:
    #             for existing_field in special_fields:
    #                 #unlink and delete only if exisiting field for saleitem is pkg_sub
    #                 setattr(sale_item_instance, existing_field, None)
                    
    #     sale_item_serializer = self.get_serializer(sale_item_instance, data=request.data)
    #     sale_item_serializer.is_valid(raise_exception=True)

    #     if 'pkg_sub' in request.data:
    #         pkg_sub_data = sale_item_serializer.validated_data.pop('pkg_sub',{})
    #         old_pkg_sub = sale_item_instance.pkg_sub
    #         #customer auto obtained from the sales instance retrieved from request data as this field is mandatory in PUT method
    #         pkg_sub_data['cust'] = sale_item_serializer.validated_data['sales'].cust
    #         pkg_sub_serializer = PackageSubscriptionWriteSerializer(data=pkg_sub_data)
    #         pkg_sub_serializer.is_valid(raise_exception=True)
    #         pkg_sub_instance = pkg_sub_serializer.save()
    #         sale_item_serializer.validated_data['pkg_sub'] = pkg_sub_instance
    #         #saleitem is linked to new pkg_sub after saving 
    #         sale_item_serializer.save()
    #         #pkg_sub delete method will automatically delete the related entry in junction table so that protected error will not be raised
    #         old_pkg_sub.delete()

    #     else:
    #         sale_item_serializer.save()

    #     return Response(sale_item_serializer.data, status=status.HTTP_200_OK)
    
    # @transaction.atomic
    # def patch(self, request, *args, **kwargs):
    #     '''
    #     MOD:
    #         1. Using serializer to create PackageSubscription instead of using model directly

    #     *** IMPORTANT ***
    #     SaleItemView is only responsible for updating the SaleItem instance's fields and not the fields of any nested object

    #     1. pkg_sub partial update logic: pkg_sub field can only be updated to a new instance be creating a new instance and not by referencing an existing instance as PackageSubscription cannot be created standalone without a SaleItem binding

    #     '''
    #     sale_item_instance = self.get_object()
    #     #reset existing special fields in saleitem
    #     special_fields = ['prod', 'service', 'pkg_sub']
    #     for field in special_fields:
    #         if field in request.data:
    #             for existing_field in special_fields:
    #                 #unlink and delete only if exisiting field for saleitem is pkg_sub
    #                 setattr(sale_item_instance, existing_field, None)

    #     sale_item_serializer = self.get_serializer(sale_item_instance, data=request.data, partial=True)
    #     sale_item_serializer.is_valid(raise_exception=True)
                
    #     if 'pkg_sub' in request.data:
    #         pkg_sub_data = sale_item_serializer.validated_data.pop('pkg_sub',{})
    #         old_pkg_sub = sale_item_instance.pkg_sub
    #         #customer auto obtained from the sales instance retrieved from request data as this field is mandatory in PUT method
    #         pkg_sub_data['cust'] = sale_item_serializer.validated_data['sales'].cust
    #         pkg_sub_serializer = PackageSubscriptionWriteSerializer(data=pkg_sub_data)
    #         pkg_sub_serializer.is_valid(raise_exception=True)
    #         pkg_sub_instance = pkg_sub_serializer.save()
    #         sale_item_serializer.validated_data['pkg_sub'] = pkg_sub_instance
    #         #saleitem is linked to new pkg_sub after saving 
    #         sale_item_serializer.save()
    #         #pkg_sub delete method will automatically delete the related entry in junction table so that protected error will not be raised
    #         old_pkg_sub.delete()

    #     else:
    #         sale_item_serializer.save()

    #     return Response(sale_item_serializer.data, status=status.HTTP_200_OK)
    
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        '''
        MOD:
            1. Using serializer to create PackageSubscription instead of using model directly
        
        *** IMPORTANT ***
        SaleItemView is only responsible for updating the SaleItem instance's fields and not the fields of any nested object
        
        1. pkg_sub update logic: pkg_sub field can only be updated to a new instance be creating a new instance and not by referencing an existing instance as PackageSubscription cannot be created standalone without a SaleItem binding
        '''
        return super().put(request, *args, **kwargs)

    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        '''
        MOD:
            1. Using serializer to create PackageSubscription instead of using model directly

        *** IMPORTANT ***
        SaleItemView is only responsible for updating the SaleItem instance's fields and not the fields of any nested object

        1. pkg_sub partial update logic: pkg_sub field can only be updated to a new instance be creating a new instance and not by referencing an existing instance as PackageSubscription cannot be created standalone without a SaleItem binding

        '''
        return super().patch(request, *args, **kwargs)
    
class SaleItemsView(CreateAPIView, ListAPIView, DestroyAPIView):
    serializer_class = BaseSaleItemSerializer
    queryset = SaleItem.objects.all()
    # permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        method = self.request.method
        if method in ['POST']:
            return SaleItemWriteSerializer
        elif method in ['GET']:
            return SaleItemReadSerializer
        
    #custom post function for handling the creation of saleitem with nested packagesubscription
    # @transaction.atomic
    # def post(self, request, *args, **kwargs):
    #     '''
    #     MOD:
    #         1. Using serializer to create PackageSubscription instead of model directly

    #     1. If this endpoint is called to update the payment of a PackageSubscription, then the pkg_sub_id must be specified in the data
    #     '''
    #     sale_item_data = request.data
    #     sale_item_serializer = self.get_serializer(data=sale_item_data)
    #     sale_item_serializer.is_valid(raise_exception=True)

    #     if 'pkg_sub' in sale_item_serializer.validated_data:
    #             pkg_sub = sale_item_serializer.validated_data.pop('pkg_sub', {})
    #             #payment handler for existing pkg_sub
    #             if 'pkg_sub_id' in pkg_sub:
    #                 pkg_sub_id = pkg_sub.pop('pkg_sub_id', None)
    #                 pkg_sub_instance = update_pkg_sub_payment(pkg_sub_id, sale_item_serializer.validated_data['net_sales_item_price'])
    #                 # pkg_sub_instance = PackageSubscription.objects.get(pkg_sub_id=pkg_sub_id)
    #                 # #update paid amount
    #                 # pkg_sub['paid_amt'] = pkg_sub_instance.paid_amt + sale_item_serializer.validated_data['net_sales_item_price']
    #                 # pkg_sub_serializer = PackageSubscriptionWriteSerializer(
    #                 #     instance=pkg_sub_instance,
    #                 #     data=pkg_sub,
    #                 #     partial=True
    #                 #     )
    #                 # pkg_sub_serializer.is_valid(raise_exception=True)
    #                 # pkg_sub_instance = pkg_sub_serializer.save()
    #             else:
    #                 #retrieve customer_id
    #                 pkg_sub['cust'] = sale_item_serializer.validated_data['sales'].cust
    #                 pkg_sub_serializer = PackageSubscriptionWriteSerializer(data=pkg_sub)
    #                 pkg_sub_serializer.is_valid(raise_exception=True)
    #                 pkg_sub_instance = pkg_sub_serializer.save()
    #             sale_item_serializer.validated_data['pkg_sub'] = pkg_sub_instance
    #     # sale_item_instance = SaleItem.objects.create(**sale_item_serializer.validated_data)

    #     sale_item_serializer.save()
    #     # sale_item_instance.save()
    #     headers = self.get_success_headers(sale_item_serializer.data)
    #     return Response(sale_item_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        '''
        MOD:
            1. Using serializer to create PackageSubscription instead of model directly

        1. If this endpoint is called to update the payment of a PackageSubscription, then the pkg_sub_id must be specified in the data
        '''
        return super().post(request, *args, **kwargs)
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="saleitem",
                description= "Specify 'sale_item_id(s)' to delete a single/multiple SaleItem record or leave empty to delete entire Sale",
                required=False,
                type={'type': 'array', 'items': {'type': 'number'}},
                location=OpenApiParameter.QUERY)
            ],
        responses={
            '404': OpenApiResponse(response=str, examples=[OpenApiExample(name="404",value={"error": "error_message"})]),
            '204': OpenApiResponse(examples=[OpenApiExample(name='204', description='No message will be returned')])
        }
    )
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        sales_item_ids = request.query_params.getlist('saleitem', [])
        item_not_deleted = []
        if sales_item_ids:
            for sales_item_id in sales_item_ids:
                try:
                    sale_item = get_object_or_404(self.get_queryset(), sales_item_id=sales_item_id)
                    sale_item.delete()
                except Exception as e:
                    item_not_deleted.append({'sales_item_id': sales_item_id, "err_msg": str(e)})

            if len(item_not_deleted) == 0:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'SaleItems with id(s) in '+str(item_not_deleted)+" are not deleted"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': "Please provide at least one saleitem to delete"}, status=status.HTTP_404_NOT_FOUND)
        
    @transaction.atomic
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)