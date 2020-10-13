"""
@Time     : 2020/10/13 13:28
@Author   : Czy
@Describe : 
"""
from django.conf.urls import url

from modules.moments import views

urlpatterns = [
    url("^getMoments/$", views.GetMoments.as_view())
]