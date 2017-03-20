from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^/', include('gt.urls')),
    url(r'^admin2/', admin.site.urls),
]
