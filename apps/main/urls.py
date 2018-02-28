from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^registration$', views.registration, name="registration"),
    url(r'^login$', views.login, name="login"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^travel$', views.travel, name="travel"),
    url(r'^add_plan$', views.add_plan, name="add_plan"),
    url(r'^create_plan$', views.create_plan, name="create_plan"),
    url(r'^show/(?P<travel_id>\d+)$', views.show, name="show"),
    url(r'^join/(?P<travel_id>\d+)$', views.join, name="join"),
]