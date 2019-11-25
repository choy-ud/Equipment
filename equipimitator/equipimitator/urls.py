"""equipimitator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path,include
from imitator import views
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',views.index,name="index"),
    url(r'^users/', include('django.contrib.auth.urls')),
    url(r'^index/',views.index,name="index"),
    url(r'^yourImitator/',views.yourImitator,name='yourImitator'),
    url(r'^register/',views.register,name='register'),
    url(r'^login/',views.login,name='login'),
    url(r'^register_get/',views.register_get,name='register_get'),
    url(r'^login_post/',views.login_post,name='login_post'),
    url(r'^login_out/',views.login_out,name='login_out'),
    url(r'^equipitem/',views.equipitem,name='equipitem'),
    url(r'^equipsave/',views.equipsave,name='equipsave'),
    url(r'^equipsaveover/',views.equipsaveover,name='equipsaveover'),
    url(r'^yourIndex/',views.yourIndex,name='yourIndex'),
    url(r'^equipset/',views.equipset,name='equipset'),
    url(r'^equipdelete/',views.equipdelete,name='equipdelete'),
    url(r'^aboutAuthor/',views.aboutAuthor,name='aboutAuthor'),
    url(r'^setcolor/',views.setcolor,name='setcolor'),
]
