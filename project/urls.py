
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.member.urls')),
    path('api/',include('apps.authentication.urls')),
    path('api/', include('apps.member.urls')),
    path('accounts/', include('allauth.urls')),
    path('api/', include('apps.subscriptions.urls')),
]
