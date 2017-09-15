from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^success/(?P<next>[\s\S]*)/$', views.SuccessView.as_view(), name='success'),
    # \s\S 是匹配所有 大小写字母   \\u4e00-\\u9fa5  匹配所有的中文字符
    url(r'^error/(?P<next>[\s\S]*)/(?P<msg>[\s\S\\u4e00-\\u9fa5]*)/$', views.ErrorView.as_view(), name="error"),
]
