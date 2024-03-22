from django.urls import path, include

from core.views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('productcommissionstructure', ProductCommissionStructureViewset)
router.register('servicecommissionstructure', ServiceCommissionStructureViewset)
router.register('vouchercommissionstructure', VoucherCommissionStructureViewset)
router.register('percentagemultiplierthreshold', PercentageMultiplierThresholdViewset)
app_name = 'core'

urlpatterns = [
    path('', include(router.urls)),
    path('last_rec_id/<str:app>/<str:resource>/', get_last_record_id, name='retrieve_last_record_id'),
    path('commission/', CommissionsView.as_view(), name='commissions_view'),
    path('commission/<int:pk>/', CommissionView.as_view(), name='commission_view'),
]

