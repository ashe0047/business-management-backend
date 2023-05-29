from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from pos.models import *
from pos.serializers import *
from pos.permissions import DeleteSalesPerm
from crm.serializers import *
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample


# Create your views here.

class SaleView(RetrieveUpdateAPIView, DestroyAPIView):
    serializer_class = SaleItemSaleSerializer
    queryset = Sale.objects.all()
    # permission_classes = [IsAuthenticated, DeleteSalesPerm]
    
    def get_object(self):
        prefetch_saleitem = Prefetch('saleitem', queryset=SaleItem.objects.all())
        sale = Sale.objects.prefetch_related(prefetch_saleitem).first()
        return sale

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        sale_instance = self.get_object()

    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

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
    def delete(self, request, *args, **kwargs):
        sale = self.get_object()
        if sale:
            sale_item_ids = request.query_params.getlist('saleitem')
            item_not_deleted = []
            if sale_item_ids:
                for sale_item_id in sale_item_ids:
                    try:
                        sale_item = SaleItem.objects.get(sales_item_id=sale_item_id)
                        sale_item.delete()
                    except SaleItem.DoesNotExist:
                        item_not_deleted.append(sale_item_id)

                if len(item_not_deleted) == 0:
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({'error': 'SaleItems with id in '+str(item_not_deleted)+" are not deleted"}, status=status.HTTP_404_NOT_FOUND)
            else:
                sale.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            
class SalesView(CreateAPIView, ListAPIView):
    serializer_class = SaleItemSaleSerializer
    queryset = Sale.objects.all()
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        sale_serializer = self.get_serializer(data=request.data)
        sale_serializer.is_valid(raise_exception=True)

        sales_item = []
        cust = {}
        if 'saleitem' in sale_serializer.validated_data:
            sales_item = sale_serializer.validated_data.pop('saleitem', [])
        
        if 'cust' in sale_serializer.validated_data:
            cust = sale_serializer.validated_data.pop('cust', {})

        cust_instance, created = Customer.objects.get_or_create(cust_nric=cust['cust_nric'], defaults=cust)

        sale_serializer.validated_data['cust_id'] = cust_instance.cust_id    
        sale_instance = sale_serializer.save()
        
        sale_item_instances = []
        sales_id = sale_instance.sales_id
        for item in sales_item:
            # sale_item_serializer = SaleItemSerializer(data=item)
            # sale_item_serializer.is_valid(raise_exception=True)
            # item['sales_id'] = sales_id
            # sale_item_instance = sale_item_serializer.save()
            if 'pkg_sub' in item:
                pkg_sub = item.pop('pkg_sub')
                pkg_sub['cust_id'] = cust_instance.cust_id
                pkg_sub_instance = PackageSubscription.objects.create(**pkg_sub)
                item['pkg_sub'] = pkg_sub_instance

            sale_item_instance = SaleItem.objects.create(sales_id=sales_id, **item)
            sale_item_instance.save()
            # if 'service' in sale_item_serializer.validated_data:
            #     service = sale_item_serializer.validated_data.pop('service')
            #     service_instance = get_object_or_404(Service, service_id=service)
            #     sale_item_instance.service = service_instance
                
            # elif 'pkg_sub' in sale_item_serializer.validated_data:
            #     pkg_sub = sale_item_serializer.validated_data.pop('pkg_sub')
            #     pkg_sub_instance = get_object_or_404(PackageSubscription, pkg_sub_id=pkg_sub)
            #     sale_item_instance.pkg_sub = pkg_sub_instance

            # elif 'prod' in sale_item_serializer.validated_data:
            #     prod = sale_item_serializer.validated_data.pop('prod')
            #     prod_instance = get_object_or_404(Product, prod_id=prod)
            #     sale_item_instance.prod = prod_instance
            
            sale_item_instances.append(sale_item_instance)
        sale_instance.saleitem.set(sale_item_instances)

        headers = self.get_success_headers(sale_serializer.data)
        return Response(sale_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class SaleItemView(RetrieveUpdateAPIView, DestroyAPIView):
    serializer_class = SaleItemSerializer
    queryset = SaleItem.objects.all()
    # permission_classes = [IsAuthenticated, DeleteSalesPerm]

    def put(self, request, *args, **kwargs):
        sale_item_instance = self.get_object()
        sale_item_serializer = self.get_serializer(sale_item_instance, data=request.data)
        sale_item_serializer.is_valid(raise_exception=True)

        if 'pkg_sub' in request.data:
            pkg_sub_data = sale_item_serializer.validated_data.pop('pkg_sub',{})
            old_pkg_sub = sale_item_instance.pkg_sub
            #customer auto obtained from the sales instance retrieved from request data as this field is mandatory in PUT method
            pkg_sub_data['cust'] = sale_item_serializer.validated_data['sales'].cust
            pkg_sub_instance = PackageSubscription.objects.create(**pkg_sub_data)
            pkg_sub_instance.save()
            sale_item_serializer.validated_data['pkg_sub'] = pkg_sub_instance
            #saleitem is linked to new pkg_sub after saving 
            sale_item_serializer.save()
            #pkg_sub delete method will automatically delete the related entry in junction table so that protected error will not be raised
            old_pkg_sub.delete()

        else:
            sale_item_serializer.save()

        return Response(sale_item_serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        sale_item_instance = self.get_object()
        sale_item_serializer = self.get_serializer(sale_item_instance, data=request.data, partial=True)
        sale_item_serializer.is_valid()

        if 'pkg_sub' in request.data:
            pkg_sub_data = sale_item_serializer.validated_data.pop('pkg_sub',{})
            old_pkg_sub = sale_item_instance.pkg_sub
            #customer auto obtained from the sales instance retrieved from request data as this field is mandatory in PUT method
            pkg_sub_data['cust'] = sale_item_serializer.validated_data['sales'].cust
            pkg_sub_instance = PackageSubscription.objects.create(**pkg_sub_data)
            pkg_sub_instance.save()
            sale_item_serializer.validated_data['pkg_sub'] = pkg_sub_instance
            #saleitem is linked to new pkg_sub after saving 
            sale_item_serializer.save()
            #pkg_sub delete method will automatically delete the related entry in junction table so that protected error will not be raised
            old_pkg_sub.delete()

        else:
            sale_item_serializer.save()

        return Response(sale_item_serializer.data, status=status.HTTP_200_OK)
    
class SaleItemsView(CreateAPIView, ListAPIView):
    serializer_class = SaleItemSerializer
    queryset = SaleItem.objects.all()
    # permission_classes = [IsAuthenticated]
    
    #custom post function for handling the creation of saleitem with nested packagesubscription
    def post(self, request, *args, **kwargs):
        sale_item_data = request.data
        sale_item_serializer = self.get_serializer(data=sale_item_data)
        sale_item_serializer.is_valid(raise_exception=True)

        if 'pkg_sub' in sale_item_serializer.validated_data:
                pkg_sub = sale_item_serializer.validated_data.pop('pkg_sub', {})
                #retireve customer_id
                pkg_sub['cust'] = sale_item_serializer.validated_data['sales'].cust
                pkg_sub_instance = PackageSubscription.objects.create(**pkg_sub)
                pkg_sub_instance.save()
                sale_item_serializer.validated_data['pkg_sub'] = pkg_sub_instance
        # sale_item_instance = SaleItem.objects.create(**sale_item_serializer.validated_data)

        sale_item_serializer.save()
        # sale_item_instance.save()
        headers = self.get_success_headers(sale_item_serializer.data)
        return Response(sale_item_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    