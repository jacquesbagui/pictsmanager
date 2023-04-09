from django.urls import include, re_path, path
from rest_framework import routers
from . import views

# API Endpoints for Albums, Pictures, and Users
urlpatterns = [
    re_path(r'^$', views.api_root),
    re_path(r'^api/albums/$', views.AlbumList.as_view(), name='album-list'),
    re_path(r'^api/albums/(?P<pk>[0-9]+)/$', views.AlbumDetail.as_view()),
    re_path(r'^api/pictures/$', views.PictureList.as_view(), name='picture-list'),
    re_path(r'^api/pictures/(?P<pk>[0-9]+)/$', views.PictureDetail.as_view()),
    re_path(r'^api/users/$', views.UserList.as_view(), name='user-list'),
    re_path(r'^api/users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]

# Login and Register and Logout views for the browse-able API
urlpatterns += [
    re_path(r'^api/api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    re_path(r'^api/token-auth', views.UserAuthToken.as_view(), name='token-auth'),
    re_path(r'^api/register', views.RegisterUserAPIView.as_view(), name='register'),
]