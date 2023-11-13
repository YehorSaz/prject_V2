"""
URL configuration for configs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from rest_framework.permissions import AllowAny

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title='RiaCloneAPI',
        default_version='v1',
        description='Clone',
        contact=openapi.Contact(email='admin@gmail.com')
    ),
    public=True,
    permission_classes=[AllowAny]
)
urlpatterns = [
    path('api_v1/auth', include('apps.auth.urls')),
    path('api_v1/users', include('apps.users.urls')),
    path('api_v1/posts', include('apps.posts.urls')),
    path('api_v1/cars', include('apps.cars.urls')),
    path('api_v1/email', include('apps.email_to_admin.urls')),
    path('api_v1/doc', schema_view.with_ui('swagger', cache_timeout=0))
]
