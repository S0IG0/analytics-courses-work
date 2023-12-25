"""
URL configuration for analytics project.

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
from django.contrib import admin
from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from files.views import FileUploadView, FileList, MacaroniList
from tasks.views import TaskRetrieve, StartAnalytic, TaskList, SupplyList

schema_view = get_schema_view(
    openapi.Info(
        title="API Сервиса аналитики",
        default_version='v1',
        description="Данный сервис создан для анализа поставок",
        terms_of_service="http://localhost/api/",
        contact=openapi.Contact(email="example@mail.com"),
        license=openapi.License(name="License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/upload/', FileUploadView.as_view(), name='file-upload'),
    path('api/files/', FileList.as_view(), name='file-list'),
    path('api/tasks/', TaskList.as_view(), name='task-list'),
    path('api/supplies/', SupplyList.as_view(), name='supply-list'),
    path('api/macaroni/', MacaroniList.as_view(), name='macaroni-list'),
    path('api/task/<int:pk>', TaskRetrieve.as_view(), name='task-retrieve'),
    path('api/analytic/', StartAnalytic.as_view(), name='analytic-start'),

    re_path(r'^api/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
