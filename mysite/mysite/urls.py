"""mysite URL Configuration

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
from django.urls import path
from app01 import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('depart/list/', views.depart_list),
    path('depart/add/', views.depart_add),
    path('depart/delete/', views.depart_delete),
    path('depart/<int:nid>/edit/', views.depart_edit),
    #用户
    path('user/list/', views.user_list),
    path('user/add/', views.user_add),
    path('user/<int:nid>/edit/', views.user_edit),
    path('user/del/', views.user_del),
    path('user/model/form/add/', views.user_modeform_add),
    #靓号
    path('pretty/list/', views.pretty_list),
    path('pretty/add/', views.pretty_add),
    path('pretty/del/', views.pretty_del),
    path('pretty/<int:nid>/edit/', views.pretty_edit),
    #管理员
    path('admin/list/', views.admin_list),
    path('admin/add/', views.admin_add),
    path('admin/del/', views.admin_del),
    path('admin/<int:nid>/edit/', views.admin_edit),
    path('admin/<int:nid>/reset/', views.admin_reset),
    #登录
    path('login', views.login),
    #注销
    path('logout', views.logout),
    path('image/code/', views.image_code),

]
