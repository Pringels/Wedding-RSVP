import json

from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from wedding import GMUSIC_API
from gedeck.models import Invitation, Guest

def home(request):
    return render(request, 'wedding/home.html')

def check_rsvp(request):
    email = request.GET.get('email')
    print email

    try:
        guest = Guest.objects.get(email=email)
    except:
        return render(request, 'wedding/home.html', {
		      'alert': 'We did not find your email address on the guest list.'
	    })

    invite = Invitation.objects.filter(guests=guest).first()
    return redirect('invitation', invitation_ref=invite.ref)


def venue(request):
    return render(request, 'wedding/venue.html')

def song_search(request):

    title = request.GET.get('title');
    results = GMUSIC_API.search_all_access(title)

    results = results['song_hits']
    tracks = {}

    for item in results:
        tracks[item["track"]['storeId']] = item["track"]['artist'] + " - " + item["track"]['title']

    json_obj = json.dumps(tracks)

    return HttpResponse(json_obj);

def add_song(request):

    # results = GMUSIC_API.get_all_playlists()
    #
    # print results

    title = str([request.GET.get('title')][0])
    name = str([request.GET.get('name')][0])
    ref = str([request.GET.get('ref')][0])

    invite = get_object_or_404(Invitation, ref=ref, active=True)

    if invite.song:
        return HttpResponse('failed');

    invite.song = name
    invite.save()

    results = GMUSIC_API.add_songs_to_playlist('0391d1e9-9090-4a42-a511-f76066c50566', title);

    return HttpResponse('success');
