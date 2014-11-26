from django.conf.urls import patterns, include, url
from django.contrib import admin
from main import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_tutorial.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.redirectLogin, name='redirectLoginPage'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^main/', include('main.urls')),
)
