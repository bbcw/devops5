from django.conf.urls import include, url

from . import views
from accounts import  user,group,permission
urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='user_login'),
    url(r'^logout/$', views.LogoutView.as_view(), name="user_logout"),
    # url(r'^user/list/$', views.UserListView.as_view(), name="user_list"),
    url(r'^user/',include([
        url(r'^modify/',include([
            url(r'status/$',user.MOdifyUserStatusView.as_view(),name='user_modify_status'),
        ])),
        url(r'^list/', include([
            url(r'^$', views.UserListView.as_view(), name='user_list')
        ])),
        url(r'^group/', include([
            url(r'^$', user.UserGroupListView.as_view(), name='user_group'),
        ])),
    ])),
    url(r'^group/',include([
        url(r'^$',group.GroupListView.as_view(),name='group_list'),
        url(r'^create/$', group.GroupCreateView.as_view(), name='group_create'),
        url(r'^delete/$', group.GroupCreateView.as_view(), name='group_del'),
        url(r'^userlist/$', group.GroupUserList.as_view(), name='group_userlist'),
        url(r'^permission/',include([
            url(r"^modify/$",group.ModifyGroupPermissionList.as_view(),name="group_permission_modify"),
            url(r"^show/$", group.showGroupPermission.as_view(), name="show_group_permission"),
        ])),
    ])),
    url(r'^permission/',include([
        url(r"list/$",permission.PermissionListView.as_view(),name='permission_list'),
        url(r"changename/$",permission.PermissionChangeView.as_view(),name='permission_change_name'),
        url(r"add/$", permission.PermissionCreateView.as_view(), name='permission_create'),
    ]))
]

