from django.conf.urls import include, url
from . import views, idc


urlpatterns = [
    url(r'idc/', include([
        url(r'add/$', idc.CreateIdcView.as_view(), name='idc_add'),
        url(r'list/$', idc.IdcListView.as_view(), name='idc_list'),
    ]))
]
