from django.urls import path, include

from marketing.views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('genericvoucher', GenericVoucherView)
router.register('itemvoucher', ItemVoucherView)
router.register('categoryvoucher', CategoryVoucherView)

app_name = 'marketing'

urlpatterns = [
    path('', include(router.urls)),
]

