from django.conf.urls import include,url
from . import idc, server, product

urlpatterns = [
    url(r'^server/',include([
        url(r'^report/$',server.ServerInfoAutoReport, name="server_report"),
        url(r'^list/$',server.ServerListView.as_view(), name="server_list"),
        url(r'^get/$',server.GetServerListView.as_view(), name="server_get"),
        url(r'^modify/',include([
            url(r'^product/$',server.ServerModifyProductView.as_view(),name="server_modify_product"),
        ])),
    ])),
    url(r'^idc/',include([
        url(r'^add/$',idc.CreateIdcView.as_view(),name="idc_add"),
        url(r'^list/$',idc.IdcListView.as_view(),name="idc_list"),
    ])),
url(r'^product/',include([
        url(r'^add/$',product.ProductAddView.as_view(),name="product_add"),
        url(r'^get/$',product.ProductGetView.as_view(),name="product_get"),
        url(r'^manage/$',product.ProductManageView.as_view(),name="product_manage"),
    ])),
]
