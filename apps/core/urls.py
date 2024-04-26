from django.urls import path, include

urlpatterns = [
    # APIs
    path('api/', include('apps.core.api.urls')),
]
