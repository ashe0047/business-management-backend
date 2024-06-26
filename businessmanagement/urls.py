"""businessmanagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include('.urls') function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from businessmanagement import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    re_path(r'^(?!api|admin).*$', TemplateView.as_view(template_name='index.html')),
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name='api-schema'),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),
    path("api/auth/", include('auth_core.urls')),
    path("api/core/", include('core.urls')),
    path("api/crm/", include('crm.urls')),
    path("api/hrm/", include('hrm.urls')),
    path("api/inventory/", include('inventory.urls')),
    path("api/marketing/", include('marketing.urls')),
    path("api/pos/", include('pos.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

