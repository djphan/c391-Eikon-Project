from django.conf.urls import patterns, url

from main import views

urlpatterns = patterns(
    '',
    url(r'^$', views.loginPage, name='loginPage'),
    url(r'^login/$', views.loginPage, name='loginPage'),
    url(r'^register/$', views.register, name='register'),
    url(r"^index/$", views.temp_main_page, name='index'),
)
