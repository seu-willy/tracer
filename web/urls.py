"""tracer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from web.views import account, home, project

urlpatterns = [
    url(r'^register/$', account.register, name='register'),
    url(r'^login/code/$', account.login_code, name='login_code'),
    url(r'^login/$', account.login, name='login'),
    url(r'^send/code/$', account.send_code, name='send_code'),
    url(r'^image/code/$', account.image_code, name='image_code'),
    url(r'^index/$', home.index, name='index'),
    url(r'^logout/$', account.logout, name='logout'),
    # 项目管理
    url(r'^project/list/$', project.project_list, name='project_list'),
]
