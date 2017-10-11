from django.conf.urls import include,url
from . import views, user, group, permission

urlpatterns = [
    #url(r'^login/$',views.login_view,name='user_login'),
    #url(r'^logout/$',views.logout_view,name='user_logout'),
    url(r'^login/$',views.UserLoginView.as_view(),name='user_login'),
    url(r'^logout/$',views.UserLogoutView.as_view(),name='user_logout'),
    #url(r'^user/list/$',views.user_list_view,name='user_list'),
    #url(r'^user/list/$',views.UserListView.as_view(),name='user_list'),
    url(r'^user/list/$',user.UserListView.as_view(),name='user_list'),

    url(r'^user/',include([
        url(r'^modify/',include([
            url(r'^status/$',user.ModifyUserStatusView.as_view(),name="user_modify_status"),
            url(r'^group/$',user.ModifyUserGroupView.as_view(),name="user_modify_group"),
        ])),
        url(r'^get/$',user.GetUserListView.as_view(),name="user_list_get"),
    ])),

    url(r'^group/',include([
        url(r'^$',group.GroupListView.as_view(),name="group_list"),
        url(r'^create/$',group.GroupCreateView.as_view(),name="group_create"),
        url(r'^userlist/$',group.GroupUserList.as_view(),name="group_userlist"),
        url(r'^grouppermissionlist/$',group.GroupPermissionListView.as_view(),name="group_permission_list"),
        # url(r'^permission/',include([
        #     url(r'^modify/$',group.ModifyGroupPermissionList.as_view(),name="group_permission_modify"),
        # ])),
    ])),

    url(r'^permission/',include([
        url(r'^list/$',permission.PermissionListView.as_view(),name="permission_list"),       
        url(r'^add/$',permission.PermissionCreateView.as_view(),name="permission_create"),       
    ])),
]
