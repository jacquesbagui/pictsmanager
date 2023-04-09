from django.contrib import admin
from django.conf import settings  # new
from django.conf.urls.static import static  # new
from django.urls import include, re_path

urlpatterns = [
    re_path(r'^', include('api.urls')),
    re_path(r'^admin/', admin.site.urls)
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    #urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)