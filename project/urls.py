from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Schema view for API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Library Management System API",
        default_version='v1',
        description="A comprehensive library management system with user authentication, role-based permissions, and book management features.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.member.urls')),
    path('api/librarians/', include('apps.librarians.urls')),
    
    path('accounts/', include('allauth.urls')),
    path('api/', include('apps.subscriptions.urls')),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),  # JWT authentication endpoints

    re_path(r'^auth/', include('djoser.urls')),
    
    # API Documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
