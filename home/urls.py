#-*-coding:utf-8 -*-

from django.urls import path, include, re_path
from .views import *
from django.contrib import admin


urlpatterns = [
    re_path('^$', index),
    path('index/', index),
    path('register/', register, name="register"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),

    # 个人中心
    path('user_info/', user_info, name="user_info"),
    path('change_userinfo/', change_userinfo, name="change_userinfo"),
    path('change_password/', change_password, name="change_password"),
    path('forget_password/', forget_password, name="forget_password"),
    path('send_code/', send_code, name="send_code"),

    # 公交信息
    path('bus_message/', bus_message, name="bus_message"),
    path('bus_detail/<int:id>', bus_detail, name="bus_detail"),

    # 站台管理
    path('site_message/', site_message, name="site_message"),
    path('site_detail/<int:id>', site_detail, name="site_detail"),

    # index ajax删除浏览历史
    path('del_history', del_history, name="del_history"),

]

app_name = "home"


from .add_data import *
# 数据添加接口
urlpatterns += [
    # path('add_bus_type/', add_bus_type, name="add_bus_type"),
    # path('add_bus/', add_bus, name="add_bus"),
    # path('add_site/', add_site, name="add_site"),
    # path('del_bus_site/', del_bus_site, name="del_bus_site"),
    # path('add_bus_site/', add_bus_site, name="add_bus_site"),
]