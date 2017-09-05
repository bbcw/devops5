from django.conf.urls import url, include
from . import views, user, group, permission

urlpatterns = [
#    url(r'^admin/', admin.site.urls),
#    url(r'^login/$', views.login_view, name='user_login'),
#    url(r'^logout/$', views.logout_view, name='user_logout'),
#    url(r'^user/list/$', views.user_list_view, name="user_list"),

    url(r'^login/$', views.LoginView.as_view(), name='user_login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='user_logout'),
    #url(r'^user/list/$', views.UserListView.as_view(), name="user_list"),

    # 使用ListView 实现分页 
    url(r'^user/list/$', user.UserListView.as_view(), name="user_list"),

    url(r'^user/', include([
        url(r'^modify/', include([
            url(r'^status/$', user.ModifyUserStatus.as_view(), name="user_modify_status"),
            url(r'^group/$', user.ModifyUserGroup.as_view(), name="user_modify_group"),
        ]))
    ])),
    url(r'^group/', include([
        url(r'^$', group.GroupListView.as_view(), name="group_list"),
        url(r'^create/$', group.GroupCreateView.as_view(), name="group_create"),
        url(r'^userlist/$', group.GroupUserListView.as_view(), name="group_user_list"),
        url(r'^delete/$', group.ModifyGroupListView.as_view(), name="group_delete"),

        url(r'^permission/', include([
            url(r'^modify/$',group.ModifyGroupPermissionListView.as_view(), name="modify_group_permission_list"),
            url(r'^list/$',group.GroupPermissionListView.as_view(), name="group_permission_list"),
        ])), 
    ])),
    url(r'^permission/',include([
        url(r'^list/$', permission.PermissionListView.as_view(),name="permission_list"),
        url(r'^create/$', permission.CreatePermissionView.as_view(),name="permission_add"),
    ])),
]
