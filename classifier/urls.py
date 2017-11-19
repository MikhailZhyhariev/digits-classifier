from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^', views.FrontendAppView.as_view(), name="index"),
    url(r'^image_add/$', views.FrontendAppView.as_view(), name="image_add"),
]
