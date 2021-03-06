"""Blog URL Configuration

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
from django.urls import path, include
from bus import urls as bus_urls
urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('wx', include(wx_urls)),
    # path('learn', include(learn_urls)),
    # path('bus/', include(bus_urls)),
    url('bus/', include(bus_urls)),
    # novel
    url('v1/novel/', include("novel.urls")),
    url('v1/auth/', include("modules.wechat_mini_auth.urls")),
    url('v1/moments/', include("modules.moments.urls")),
]
