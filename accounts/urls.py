#!/usr/bin/python
# coding=utf8

from django.conf.urls import include, url
from . import views, user, group, permission


urlpatterns = [

    url(r'^login/$', views.LoginView.as_view(), name='user_login'),     # 登录 url
    url(r'^logout/$', views. LogoutView.as_view(), name='user_logout'),     # 登出 url
    # url(r'^user/list/$', views.User_TemplateView.as_view(), name='user_list'),
    # url(r'^user/list/$', views.User_TemplateView.as_view()),
    url(r'^user/list/$', user.UserListView.as_view(), name='user_list'),        # 用户展示页

    url(r'^user/', include([
        url(r'^modify/', include([
            url(r'^status/$', user.ModifyUserStatusView.as_view(), name='user_modify_status'),  # 修改用户状态 url
            url(r'^group/$', user.ModifyUserGroupView.as_view(), name='user_modify_group'), # 添加用户到用户组 url
        ]))
    ])),

    url(r'^group/', include([
        url(r'^$', group.GroupListView.as_view(), name='group_list'),   # 用户组 url
        url(r'create/$', group.GroupCreateView.as_view(), name='group_create'),  # 用户组创建 url
        url(r'userlist/$', group.GroupUserList.as_view(), name='group_userlist'),   # 查看组成员 url
        url(r'delete/$', group.GroupDeleteView.as_view(), name='group_delete'),     # 删除用户组 url
        url(r'permission/', include([
            url(r'modify/$', group.ModifyGroupPermissionList.as_view(), name='group_permission_modify'),     # 用户组权限修改 url
            url(r'get/$', group.GroupPermissionListView.as_view(), name='group_permission_get'),    # 用户组权限查询
        ])),

    ])),

    url(r'permission/', include([
        url(r'list/$', permission.PermissionListView.as_view(), name='permission_list'),   # 权限展示
        url(r'add/$', permission.PermissionAddView.as_view(), name='permission_add'),       # 增加权限
    ])),


]
