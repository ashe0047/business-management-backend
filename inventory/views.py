from rest_framework.viewsets import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from inventory.models import *
from inventory.serializers import *
from inventory.permissions import DeleteInventoryPerm
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample


# Create your views here.
class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated, DeleteInventoryPerm]


class ProductSupplierViewSet(ModelViewSet):
    serializer_class = ProductSupplierSerializer
    queryset = ProductSupplier.objects.all()
    permission_classes = [IsAuthenticated, DeleteInventoryPerm]


class ServiceViewSet(ModelViewSet):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    permission_classes = [IsAuthenticated, DeleteInventoryPerm]

class InventoryCategoryViewset(ModelViewSet):
    serializer_class = InventoryCategorySerializer
    queryset = InventoryCategory.objects.all()
    # permission_classes = [IsAuthenticated, DeleteInventoryPerm]

class ServicePackageViewSet(ModelViewSet):
    serializer_class = ServicePackageSerializer
    queryset = ServicePackage.objects.all()
    # permission_classes = [IsAuthenticated, DeleteInventoryPerm]

    def create(self, request, *args, **kwargs):
        services = []

        service_pkg_serializer = self.get_serializer(data=request.data)
        service_pkg_serializer.is_valid(raise_exception=True)

        if 'service' in service_pkg_serializer.validated_data:
            services = service_pkg_serializer.validated_data.pop('service', [])

        # service_instances = []
        # for service in services:
        #     service_serializer = ServiceSerializer(data=service)
        #     service_serializer.is_valid(raise_exception=True)
        #     service_instances.append(service_serializer.save())

        service_pkg_instance = service_pkg_serializer.save()
        service_pkg_instance.service.set(services)
        
        headers = self.get_success_headers(service_pkg_serializer.data)
        return Response(service_pkg_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        services = []
        service_pkg_instance = self.get_object()
        service_pkg_serializer = self.get_serializer(service_pkg_instance, data=request.data)
        service_pkg_serializer.is_valid(raise_exception=True)

        if 'service' in service_pkg_serializer.validated_data:
            services = service_pkg_serializer.validated_data.pop('service', [])
        
        service_pkg_instance = service_pkg_serializer.save()
        service_pkg_instance.service.clear()
        service_pkg_instance.service.set(services)

        return Response(service_pkg_serializer.data, status=status.HTTP_200_OK)
    
    def partial_update(self, request, *args, **kwargs):
        services = []
        service_pkg_instance = self.get_object()
        service_pkg_serializer = self.get_serializer(service_pkg_instance, data=request.data, partial=True)
        service_pkg_serializer.is_valid(raise_exception=True)

        if 'service' in service_pkg_serializer.validated_data:
            services = service_pkg_serializer.validated_data.pop('service', [])
        
        service_pkg_serializer.save()
        
        for service in services:
            if service not in service_pkg_instance.service.all():
                service_pkg_instance.service.add(service)

        return Response(service_pkg_serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="service",
                description= "Specify 'service_id(s)' to delete a single/multiple Service record or leave empty to delete entire ServicePackage",
                required=False,
                type={'type': 'array', 'items': {'type': 'number'}},
                location=OpenApiParameter.QUERY)
            ],
        responses={
            '404': OpenApiResponse(response=str, examples=[OpenApiExample(name="404",value={"error": "error_message"})]),
            '204': OpenApiResponse(examples=[OpenApiExample(name='204', description='No message will be returned')])
        }
    )
    def destroy(self, request, *args, **kwargs):
        pkg = self.get_object()
        if pkg:
            service_ids = request.query_params.getlist('service')
            item_not_deleted = []
            if service_ids:
                for service_id in service_ids:
                    try:
                        service_item = Service.objects.get(service_id=service_id)
                        pkg.service.remove(service_item)
                    except Exception as e:
                        item_not_deleted.append({'err_msg': str(e), 'item_id': service_id})

                if len(item_not_deleted) == 0:
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({'error': 'Service with id in '+str(item_not_deleted)+" are not deleted"}, status=status.HTTP_404_NOT_FOUND)
            else:
                pkg.service.clear()
                pkg.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            