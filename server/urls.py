from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="SERVICE API",
      default_version='v1',
      description="MRC",
      contact=openapi.Contact(email="abc@mail.com"),
   ),
   validators=['flex'],
   public=True,
   permission_classes=(permissions.AllowAny,),
)

admin.site.site_header = "Admin"
admin.site.site_title = "MRC"
admin.site.index_title = "MRC"

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('mrc/', include(('mrc.urls', 'mrc'), namespace='mrc')),  
]
