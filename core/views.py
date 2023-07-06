from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, DestroyAPIView, ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Prefetch
from django.db import transaction
from django.shortcuts import get_object_or_404
from core.models import *
from core.serializers import *
from core.utils import share_size_calculation
from drf_spectacular.utils import *

# Create your views here.
# Wrap view methods in transaction.atomic to ensure rollback is triggered when db operation fails
   
class ProductCommissionStructureViewset(ModelViewSet):
    serializer_class = ProductCommissionStructureSerializer
    queryset = ProductCommissionStructure.objects.all()
    permission_classes = [IsAdminUser, IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
class ServiceCommissionStructureViewset(ModelViewSet):
    serializer_class = ServiceCommissionStructureSerializer
    queryset = ServiceCommissionStructure.objects.all()
    permission_classes = [IsAdminUser, IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class VoucherCommissionStructureViewset(ModelViewSet):
    serializer_class = VoucherCommissionStructureSerializer
    queryset = VoucherCommissionStructure.objects.all()
    # permission_classes = [IsAdminUser, IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class PercentageMultiplierThresholdViewset(ModelViewSet):
    serializer_class = PercentageMultiplierThresholdSerializer
    queryset = PercentageMultiplierThreshold.objects.all()
    # permission_classes = [IsAdminUser, IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    
'''
    1. If granularity is sale then only a single commissionsharingdetail object is  needed 
    2. If granularity is saleitem then create as many commissionsharingdetail object as saleitem
    3. Only POST method uses many=True serializer to accomodate creating multiple commissionsharingdetail object
    4. Other methods are all uses a single object serializer
'''   
class CommissionView(RetrieveUpdateAPIView):
    serializer_class = BaseCommissionSerializer
    queryset = Commission.objects.all()
    # permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        method = self.request.method
        if method in ['PUT', 'PATCH']:
            return CommissionWriteSerializer
        elif method in ['GET']:
            return CommissionReadSerializer
    
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())        
        return serializer_class(*args, **kwargs)
    
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

 
class CommissionsView(ListCreateAPIView, DestroyAPIView):
    serializer_class = BaseCommissionSerializer
    queryset = Commission.objects.all()
    # permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        method = self.request.method
        if method in ['POST']:
            return CommissionWriteSerializer
        elif method in ['GET']:
            return CommissionReadSerializer
    
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        if self.request.method in ['POST']:
            kwargs.setdefault('many', True)
        
        return serializer_class(*args, **kwargs)


    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            commissions_serializer = self.get_serializer(data=request.data)
            commissions_serializer.is_valid(raise_exception=True)
            #auto calculate share percent and share amount
            share_size_calculation(commissions_serializer.validated_data)
            
            for commission_item in commissions_serializer.validated_data:
                emp_share_percent = commission_item.pop('emp_share_percent', [])
                # commissionsharingdetail_instance = commissionsharingdetail_serializer.save()
                commission_instance = Commission(**commission_item)
                commission_instance.save()
                emp_instances = []
                for item in emp_share_percent:
                    item['emp'] = item['emp']
                    # Create an instance of EmployeeCommissionSharing
                    employeecommission_instance = EmployeeCommission(
                        com=commission_instance,
                        **item
                    )
                    employeecommission_instance.save()
                    emp_instances.append(item['emp'])
                commission_instance.emp_share_percent.add(*emp_instances)

                # commissionsharingdetail_instance.emp_share_percent.set(emp_share_percent)

            headers = self.get_success_headers(commissions_serializer.data)

            return Response(commissions_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="commission",
                description= "Specify 'com_id(s)' to delete a single/multiple SalesSharingDetail record",
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
        com_ids = request.query_params.getlist('commission', [])
        item_not_deleted = []
        if com_ids:
            for com_id in com_ids:
                try:
                    commission = Commission.objects.get(com_id=com_id)
                    commission.emp_share_percent.clear()
                    commission.delete()               
                except Exception as e:
                    item_not_deleted.append({"com_id": com_id, "err_msg": str(e)})
            if len(item_not_deleted) == 0:
                    return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'SalesSharingDetail with id(s) in '+str(item_not_deleted)+" are not deleted"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': "Please provide at least one commissionsharingdetail to delete"}, status=status.HTTP_404_NOT_FOUND)

# class FixedCommissionSharingView(RetrieveUpdateAPIView):
#     serializer_class = BaseFixedCommissionSharingSerializer
#     queryset = FixedCommissionSharing.objects.all()
#     # permission_classes = [IsAuthenticated]

#     def get_serializer_class(self):
#         method = self.request.method
#         if method in ['PUT', 'PATCH']:
#             return FixedCommissionSharingWriteSerializer
#         elif method in ['GET']:
#             return FixedCommissionSharingReadSerializer
        
# class FixedCommissionSharingsView(CreateAPIView, ListAPIView, DestroyAPIView):
#     serializer_class = BaseFixedCommissionSharingSerializer
#     queryset = FixedCommissionSharing.objects.all()
#     permission_classes = [IsAuthenticated]

#     def get_serializer_class(self):
#         method = self.request.method
#         if method in ['POST']:
#             return FixedCommissionSharingWriteSerializer
#         elif method in ['GET']:
#             return FixedCommissionSharingReadSerializer
    
#     @transaction.atomic
#     def post(self, request, *args, **kwargs):
#         try:
#             fixedcomsharing_serializer = self.get_serializer(data=request.data)
#             fixedcomsharing_serializer.is_valid(raise_exception=True)
#             #auto calculate share percent and share amount
#             share_size_calculation(fixedcomsharing_serializer.validated_data)
            
#             for commission_item in fixedcomsharing_serializer.validated_data:
#                 emp_share_percent = commission_item.pop('emp_share_percent', [])
#                 # commissionsharingdetail_instance = commissionsharingdetail_serializer.save()
#                 commission_instance = Commission(**commission_item)
#                 commission_instance.save()
#                 emp_instances = []
#                 for item in emp_share_percent:
#                     item['emp'] = item['emp']
#                     # Create an instance of EmployeeCommissionSharing
#                     employeecommission_instance = EmployeeCommission(
#                         sales_sharing_detail=commission_instance,
#                         **item
#                     )
#                     employeecommission_instance.save()
#                     emp_instances.append(item['emp'])
#                 commission_instance.emp_share_percent.add(*emp_instances)

#                 # commissionsharingdetail_instance.emp_share_percent.set(emp_share_percent)

#             headers = self.get_success_headers(fixedcomsharing_serializer.data)

#             return Response(fixedcomsharing_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, *args, **kwargs):
#         return super().delete(request, *args, **kwargs)
