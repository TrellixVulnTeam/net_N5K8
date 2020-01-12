from django.urls import path
from . import views

from django.conf.urls import url
from django.urls import path, include

from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    #path('', views.crawl, name='crawl'),
    path('form', views.form, name='form'),
    url(r'^crawl/$', views.crawl),  # for REST API test
    url(r'^apitest/$',views.calctest), # for REST API test
    url(r'^apitestt/$', views.gettest),  # for REST API test

]