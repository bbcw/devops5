from django.conf.urls import url, include
from . import idc, server, product

urlpatterns = [
    url(r'^server/', include([
        url(r'^report/$', server.ServerInfoAutoReport, name="server_report"),
        url(r'^list/$', server.ServerListView.as_view(), name="server_list"),
        url(r'^status/$', server.ModifyServerStatus.as_view(), name="server_status"),
    ])),
    url(r'^idc/', include([
        url(r'^add/$', idc.CreateIdcView.as_view(), name="idc_add"),
        url(r'^list/$', idc.IdcListView.as_view(), name="idc_list"),
    ])),
    url(r'^product/', include([
        url(r'^add/$', product.CreateProductView.as_view(), name="product_add"),
        #url(r'^list/$', product.ServerListView.as_view(), name="product_list"),
    ])),
]
