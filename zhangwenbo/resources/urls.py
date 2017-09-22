from django.conf.urls import include, url
from . import idc, server ,product

urlpatterns = [
    url(r'^server/', include([
        url(r'^report/$', server.ServerInfoAutoReport, name="server_report"),
        url(r'^list/$', server.ServerListView.as_view(), name="server_list"),
        url(r'^modify/',include([
            url(r'^status/$', server.ModifyServerStatus.as_view(),name="server_modify_status"),
            url(r'^add/$', server.AddServerStatus.as_view(),name="server_add_status"),
        ]))
    ])),
    url(r'^product/', include([
        url(r'^add/$', product.ProductAddView.as_view(), name="product_add"),
    ])),
    url(r'^idc/', include([
        url(r'^add/$', idc.CreateIdcView.as_view(), name="idc_add"),
        url(r'^list/$',idc.IdcViewList.as_view(), name="idc_list"),
        url(r'^delete/$',idc.IdcDelete.as_view(), name="idc_delete"),
    ]))
]