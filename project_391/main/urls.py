from django.conf.urls import patterns, url
from django.conf import settings
from main import views

urlpatterns = patterns(
    '',
    url(r'^$', views.loginPage, name='loginPage'),
    url(r'^login/$', views.loginPage, name='loginPage'),
    url(r'^register/$', views.register, name='register'),
    url(r"^index/$", views.temp_main_page, name='index'),
    url(r"^home/$", views.home_page, name='home'),
    url(r"^upload/$", views.upload, name='upload'),
    url(r"^photo_details/$", views.photo_details, name='photo_details'),
    url(r"^group_management/$", views.group_management, name='group_management'),
    url(r"^remove_user_from_group/$", views.remove_user_from_group, name='remove_user_from_group'),
    url(r"^add_group/$", views.add_group, name='add_group'),
    url(r"^add_user_to_group/$", views.add_user_to_group, name='add_user_to_group'),
    url(r"^get_user_groups/$", views.get_user_groups, name='get_user_groups'),
    url(r"^upload_images/$", views.upload_images, name='upload_images'),
    url(r"^modify_image_details/$", views.modify_image_details, name='modify_image_details'),
    url(r"logout/$", views.logout, name='logout'),
    url(r"^get_image_data/$", views.get_image_data, name='get_image_data'),
    url(r"^delete_group/$", views.delete_group, name='delete_group'),
    url(r"^delete_image/$", views.delete_image, name='delete_image'),
    url(r"^olap/$", views.olap, name='olap'),
    url(r"^get_olap_data/$", views.get_olap_data, name='get_olap_data'),
    url(r"^add_view/$", views.add_view, name='add_view'),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
