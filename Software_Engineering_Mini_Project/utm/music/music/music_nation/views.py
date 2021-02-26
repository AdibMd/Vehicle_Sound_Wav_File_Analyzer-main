import base64
import io
import urllib

import IPython.display as ipd
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import (
    get_object_or_404,
    redirect
)
from django.utils import timezone

from .forms import NewAlbum, NewSong
from .forms import SignUpForm
from .models import Album, Song, ContactForm, SendForm, VehicleSpec


##########################################################

def Showemp(request):
    resultsdisplay = ContactForm.objects.all()
    return render(request, "music_nation/homepage.html", {'ContactForm': resultsdisplay})

def showspec(request):
    myresult = VehicleSpec.objects.all()
    resultsdisplay = ContactForm.objects.all()
    return render(request, "music_nation/showspec.html", {'VehicleSpec': myresult, 'ContactForm': resultsdisplay})


def showgallery(request):
    resultsdisplay = ContactForm.objects.all()
    displayresults = SendForm.objects.all()
    return render(request, "music_nation/gallery.html", {'ContactForm': resultsdisplay, 'SendForm': displayresults})


# def Insertrecord(request):
#     if request.method == 'POST':
#         if request.POST.get('empname') and request.POST.get('email') and request.POST.get('salary'):
#             saverecord = ContactForm()
#             saverecord.empname = request.POST.get('empname')
#             saverecord.email = request.POST.get('email')
#             saverecord.salary = request.POST.get('salary')
#             saverecord.save()
#             # message.success(request, 'Record save successfully!!!')
#             return render(request, "music_nation/homepage.html")
#     else:
#             return render(request, "music_nation/homepage.html")

def home(request):
    # show all albums in chronological order of it's upload
    albums = Album.objects.all()
    return render(request, 'music_nation/homepage.html', {'albums': albums})


# ........................................................#

def profile_detail(request, username):
    # show all albums of the artist
    albums = get_object_or_404(User, username=username)
    albums = albums.albums.all()
    return render(request, 'music_nation/artist_information.html', {'albums': albums, 'username': username})


# ........................................................#

@login_required
def add_album(request, username):
    user = get_object_or_404(User, username=username)
    # only currently logged in user can add album else will be redirected to home
    if user == request.user:
        if request.method == 'POST':
            form = NewAlbum(request.POST, request.FILES)
            if form.is_valid():
                # form.save(commit='False')
                album = Album.objects.create(
                    album_logo=form.cleaned_data.get('album_logo'),
                    album_name=form.cleaned_data.get('album_name'),
                    album_genre=form.cleaned_data.get('album_genre'),
                    uploaded_on=timezone.now(),
                    album_artist=request.user
                )
                return redirect('music_nation:profile_detail', username=request.user)
        else:
            form = NewAlbum()
        return render(request, 'music_nation/create_new_album.html', {'form': form})
    else:
        return redirect('music_nation:profile_detail', username=user)


# ........................................................#

def album_detail(request, username, album):
    # show album details here. single album's details.
    album = get_object_or_404(Album, album_name=album)
    songs = get_object_or_404(User, username=username)
    songs = songs.albums.get(album_name=str(album))
    songs = songs.songs.all()
    return render(request, 'music_nation/album_information.html', {'songs': songs, 'album': album, 'username': username
                                                                   })


# ........................................................#

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('music_nation:home')
        else:
            message = 'Looks like a username with that email or password already exists'
            return render(request, 'music_nation/user_signup.html', {'form': form, 'message': message})
    else:
        form = SignUpForm()
        return render(request, 'music_nation/user_signup.html', {'form': form})


# ........................................................#

@login_required
def delete_album(request, username, album):
    user = get_object_or_404(User, username=username)
    if request.user == user:
        album_to_delete = get_object_or_404(User, username=username)
        album_to_delete = album_to_delete.albums.get(album_name=album)
        song_to_delete = album_to_delete.songs.all()
        for song in song_to_delete:
            song.delete_media()  # deletes the song_file
        album_to_delete.delete_media()  # deletes the album_logo
        album_to_delete.delete()  # deletes the album from database
        return redirect('music_nation:profile_detail', username=username)
    else:
        return redirect('music_nation:profile_detail', username=username)


# ........................................................#

@login_required
def add_song(request, username, album):
    user = get_object_or_404(User, username=username)

    if request.user == user:

        album_get = Album.objects.get(album_name=album)

        if request.method == 'POST':
            form = NewSong(request.POST, request.FILES)
            if form.is_valid():
                # form.save(commit='False')
                song = Song.objects.create(
                    song_name=form.cleaned_data.get('song_name'),
                    song_file=form.cleaned_data.get('song_file'),
                    song_album=album_get
                )
                return redirect('music_nation:album_detail', username=username, album=album)

        else:
            form = NewSong()
            return render(request, 'music_nation/create_new_song.html', {'form': form})
    else:
        return redirect('music_nation:album_detail', username=username, album=album)


from django.shortcuts import render
from .forms import FormContactForm


def showform(request):
    form = FormContactForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()

    context = {'form': form}

    return render(request, 'music_nation/upload.html', context)


def main(request):
    if request.method == "POST":
        audio_data = request.FILES.get('data')
        path = default_storage.save('123' + '.wav', ContentFile(audio_data.read()))
        return render(request, 'music_nation/homepage.html')
    else:
        return render(request, 'music_nation/homepage.html')


# def gallery(request):
#     galaries = ContactForm.objects.all()
#     return render(request, 'music_nation/gallery.html', {'galaries':galaries})

# def uploadTutorial(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             # return redirect('tutorial_list')
#     else:
#         form = ContactForm()
#     return render(request, 'music_nation/homepage.html', {'form' : form})

import mysql.connector
# from flask import Flask, redirect, url_for, render_template, request, flash

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="django"
)

cursor = mydb.cursor()
sql = '''SELECT spectrogram, file from file_viewer ORDER BY ID DESC LIMIT 1'''
cursor.execute(sql)
result = cursor.fetchall();
for row in result:
    print(row[1])
    print(row[0])
# fuck = str(result)[3:-4]
# render_template('music_nation/gallery.html', result=result)
# print(str(result)[1:-1])


mydb.close()

asd_file = "media/" + row[1]
asd, sr = librosa.load(asd_file)
sample_duration = 1 / sr
tot_samples = len(asd)
tot_samples
duration = 1 / sr * tot_samples

# Create your views here.
def SoundSpectrogram5(request):
    ipd.Audio(asd_file)
    plt.figure(figsize=(10, 8))
    plt.subplot(2, 1, 1)
    librosa.display.waveplot(asd, alpha=0.5)
    plt.ylim((-1, 1))
    plt.title(row[0])

    fig = plt.gcf()
    # convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    return render(request, 'music_nation/gallery.html', {'data': uri})


debussy_file = "media/user_15/Honda_Civic.wav"
debussy, sr = librosa.load(debussy_file)
sample_duration = 1 / sr
tot_samples = len(debussy)
tot_samples
duration = 1 / sr * tot_samples

# Create your views here.
def SoundSpectrogram0(request):
    ipd.Audio(debussy_file)
    plt.figure(figsize=(10, 8))
    plt.subplot(2, 1, 1)
    librosa.display.waveplot(debussy, alpha=0.5)
    plt.ylim((-1, 1))
    plt.title("Honda Civic")

    fig = plt.gcf()
    # convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    return render(request, 'music_nation/gallery.html', {'data': uri})

mustang_file = "media/user_15/Mustang.wav"
mustang, sr = librosa.load(mustang_file)
sample_duration = 1 / sr
tot_samples = len(mustang)
tot_samples
duration = 1 / sr * tot_samples

# Create your views here.
def SoundSpectrogram1(request):
    ipd.Audio(mustang_file)
    plt.figure(figsize=(10, 8))
    plt.subplot(2, 1, 1)
    librosa.display.waveplot(mustang, alpha=0.5)
    plt.ylim((-1, 1))
    plt.title("Ford Mustang")

    fig = plt.gcf()
    # convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    return render(request, 'music_nation/gallery.html', {'data': uri})


mercedes_file = "media/user_15/mercedes_x-class.wav"
mercedes, sr = librosa.load(mercedes_file)
sample_duration = 1 / sr
tot_samples = len(mercedes)
tot_samples
duration = 1 / sr * tot_samples

# Create your views here.
def SoundSpectrogram2(request):
    ipd.Audio(mercedes_file)
    plt.figure(figsize=(10, 8))
    plt.subplot(2, 1, 1)
    librosa.display.waveplot(mercedes, alpha=0.5)
    plt.ylim((-1, 1))
    plt.title("Mercedes X Class")

    fig = plt.gcf()
    # convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    return render(request, 'music_nation/gallery.html', {'data': uri})


raptor_file = "media/user_15/ford_raptor.wav"
raptor, sr = librosa.load(raptor_file)
sample_duration = 1 / sr
tot_samples = len(raptor)
tot_samples
duration = 1 / sr * tot_samples

# Create your views here.
def SoundSpectrogram3(request):
    ipd.Audio(raptor_file)
    plt.figure(figsize=(10, 8))
    plt.subplot(2, 1, 1)
    librosa.display.waveplot(raptor, alpha=0.5)
    plt.ylim((-1, 1))
    plt.title("Ford Raptor")

    fig = plt.gcf()
    # convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    return render(request, 'music_nation/gallery.html', {'data': uri})


everest_file = "media/user_15/Ford_everest.wav"
everest, sr = librosa.load(everest_file)
sample_duration = 1 / sr
tot_samples = len(everest)
tot_samples
duration = 1 / sr * tot_samples

# Create your views here.
def SoundSpectrogram4(request):
    ipd.Audio(everest_file)
    plt.figure(figsize=(10, 8))
    plt.subplot(2, 1, 1)
    librosa.display.waveplot(everest, alpha=0.5)
    plt.ylim((-1, 1))
    plt.title("Ford Everest")

    fig = plt.gcf()
    # convert graph into dtring buffer and then we convert 64 bit code into image
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    return render(request, 'music_nation/gallery.html', {'data': uri})
