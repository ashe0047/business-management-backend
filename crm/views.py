from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from crm.models import *
from crm.serializers import *
from crm.permissions import DeleteCustomerPerm
# Create your views here.

class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated, DeleteCustomerPerm]


