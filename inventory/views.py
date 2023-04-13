from rest_framework.viewsets import *
from rest_framework.permissions import IsAuthenticated
from inventory.models import Product, ProductSupplier, Service
from inventory.serializers import ProductSerializer, ProductSupplierSerializer, ServiceSerializer
from inventory.permissions import DeleteInventoryPerm

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
