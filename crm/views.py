from rest_framework.generics import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from crm.models.models import *
from crm.serializers import *
from crm.permissions import DeleteCustomerPerm
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class CustomerView(RetrieveUpdateAPIView, DestroyAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated, DeleteCustomerPerm]

    def get_serializer(self, *args, **kwargs):
        if self.request.method in ['GET']:
            return CustomerTreatmentSerializer
        return CustomerSerializer
    
    def destroy(self, request, *args, **kwargs):
        customer = self.get_object()

        try:
            customer.treatment.all().delete()
            if customer.treatment.exists():
                return Response({'error': 'Error deleting treatments associated with customer, cannot proceed to delete customer'}, status=status.HTTP_400_BAD_REQUEST)
            
            customer.delete()
            self.get_object()
            # If the customer still exists, return a 400 Bad Request response
            return Response({'message': 'Customer deletion failed'}, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            # If the customer does not exist, return a 204 No Content response
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomersView(CreateAPIView, ListAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated]

class TreatmentViewset(ModelViewSet):
    serializer_class = TreatmentSerializer
    queryset = Treatment.objects.all()
    # permission_classes = [IsAuthenticated]


