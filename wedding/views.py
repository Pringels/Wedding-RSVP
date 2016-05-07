import json
import os
import random
import string

from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from django.http import HttpResponse

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from wedding import GMUSIC_API
from gedeck.models import Invitation, Guest

from .forms import UploadFileForm

def home(request):
    return render(request, 'wedding/upload.html')

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

@csrf_exempt
def upload(request):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponse('success');
    else:
        return HttpResponse('not allowed');
    return HttpResponse('uplaod failed :()');

def handle_uploaded_file(f):
    name, extension = os.path.splitext(f.name)
    fname = os.path.join(settings.MEDIA_ROOT, f.name)
    counter = 0

    while os.path.isfile(fname):
        new_name = name + "_" + str(counter) + extension
        fname = os.path.join(settings.MEDIA_ROOT, new_name)
        counter += 1

    with open(os.path.join(fname), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
