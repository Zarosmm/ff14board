"""
URL configuration for ff14board project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.api import views as apiViews
from apps.admin import views as adminViews
from rest_framework import routers, permissions

schema_view = get_schema_view(
    openapi.Info(
        title="FF14 招募板 API",
        default_version='v1',
        description="FF14 招募板系统 API 文档",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    authentication_classes=[JWTAuthentication,],
    permission_classes=[permissions.AllowAny,],
)


apiRouter = routers.SimpleRouter()

apiRouter.register('server', apiViews.ServerViewSet, basename='server')
apiRouter.register('character', apiViews.CharacterViewSet, basename='character')
apiRouter.register('team', apiViews.TeamViewSet, basename='team')

adminRouter = routers.SimpleRouter()

adminRouter.register('server', adminViews.ServerViewSet, basename='server')
adminRouter.register('character', adminViews.CharacterViewSet, basename='character')
adminRouter.register('team', adminViews.TeamViewSet, basename='team')

urlpatterns = [
    path('login', apiViews.UserLoginView.as_view()),
    path('register', apiViews.UserRegisterView.as_view()),
    path('api/', include(apiRouter.urls)),
    path('admin/', include(adminRouter.urls)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)