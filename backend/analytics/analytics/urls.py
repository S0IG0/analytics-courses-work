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
from django.urls import path

from files.views import FileUploadView, FileList
from tasks.views import RetrieveTask, StartAnalytic

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/upload/', FileUploadView.as_view(), name='file-upload'),
    path('api/files/', FileList.as_view(), name='file-list'),
    path('api/task/<int:pk>', RetrieveTask.as_view(), name='task-retrieve'),
    path('api/analytic/', StartAnalytic.as_view(), name='analytic-start'),
]
