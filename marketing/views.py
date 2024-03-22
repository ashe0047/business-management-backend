from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Prefetch
from django.db import transaction
from django.shortcuts import get_object_or_404
from marketing.models.models import *
from marketing.serializers.serializers import *
from drf_spectacular.utils import *
# Create your views here.

class GenericVoucherView(ModelViewSet):
    serializer_class = BaseGenericVoucherSerializer
    queryset = GenericVoucher.objects.all()
    # permission_classes = [IsAuthenticated]

class ItemVoucherView(ModelViewSet):
    serializer_class = BaseItemVoucherSerializer
    queryset = ItemVoucher.objects.all()
    # permission_classes = [IsAuthenticated]

class CategoryVoucherView(ModelViewSet):
    serializer_class = BaseCategoryVoucherSerializer
    queryset = CategoryVoucher.objects.all()
    # permission_classes = [IsAuthenticated]