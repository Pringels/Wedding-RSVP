from django.conf.urls import patterns, include, url
from wedding import views


urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^venue/', views.venue, name='venue'),
    url(r'^check-rsvp/', views.check_rsvp, name='check-rsvp'),
    url(r'^song-search/', views.song_search, name='song_search'),
    url(r'^add-song/', views.add_song, name='add_song'),
    url(r'^upload/', views.upload, name='upload'),
)
