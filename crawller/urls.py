from django.urls import path
from . import views

urlpatterns = {
    path('', views.crawl, name='crawl'),
    path('all', views.crawlAll, name='all'),
    path('form', views.form, name='form'),
    path('robot', views.readRobots, name='robot'),

}