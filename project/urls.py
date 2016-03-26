
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^gedeck/', include('gedeck.urls')),
    url(r'^', include('wedding.urls')),
]
