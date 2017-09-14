from django.conf.urls import include, url

from . import idc

urlpatterns = [
    url(r'idc/', include([
        url(r'add/$', idc.CreateIdcView.as_view(), name="idc_add"),
        url(r'list/$',idc.IdcViewList.as_view(), name="idc_list"),
        url(r'delete/$',idc.IdcDelete.as_view(), name="idc_delete"),
    ]))
]