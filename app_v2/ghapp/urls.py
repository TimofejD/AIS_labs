from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from . import views

"""
    Подключение URI для приложения weatherapp.
    Корневые URI представлены в базовом модуле application/urls.py
"""

# Метаданные Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="Smart Greenhouse API",
      default_version='v1',
      description="Smart Greenhouse API",
      terms_of_service="https://example.com",
      contact=openapi.Contact(email="contact@mail.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('ghdata/<str:greenhouse_name>', views.GetDelAllGreenhouseData.as_view()),
    path('ghdata', views.GetPostPutGreenhouseData.as_view()),
    path('greenhouse/<str:plant_name>', views.GetDelAllGreenhouse.as_view()),
    path('greenhouse', views.GetPostPutGreenhouse.as_view()),
    path('plant', views.GetPostPutDelPlant.as_view()),
    path('schedule', views.GetPostPutDelSchedule.as_view()),
    path('smartmodule', views.GetPostDelSmartModule.as_view()),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]
