from django.conf.urls import url
from . import views

urlpatterns = [
   url(r'^$', views.index),
   url(r'^process_login$', views.process_login),
   url(r'^dashboard$', views.dashboard),
   url(r'^create_quote$', views.create_quote),
   url(r'^add_favorites/(?P<id>\d+)$', views.add_favorites),
   url(r'^un_favorites/(?P<id>\d+)$', views.un_favorites),
   url(r'^quote/(?P<id>\d+)$', views.quote),
   url(r'^logout$', views.logout),
]