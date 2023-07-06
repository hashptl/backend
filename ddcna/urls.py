"""DDCNA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/sign-up/', sign_up_api, name='sign_up'),
    path('api/sign-in/', sign_in_api, name='sign_in'),
    path('api/intake-form/', intake_form_api, name='intake_form'),
    path('api/user/list/', user_list_api, name='user_list'),
    path('api/user/add/', user_add_api, name='user_add'),
    path('api/user/update/<str:user_id>/', user_update_api, name='user_update'),
    path('api/user/delete/<str:user_id>/', user_delete_api, name='user_delete'),
    path('api/template/list/', template_list_api, name='template_list_api'),
    path('api/template/form/', template_form_api, name='template_form_api'),
    path('api/request/list/', request_list_api, name='request_list_api'),
    path('api/request/details/<str:request_id>/', request_details_api, name='request_details_api'),
]
