from django.urls import path, include, re_path
from . import views as music_nation_views
from django.contrib.auth.views import LoginView, LogoutView
from . import views

import mysql.connector
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="django"
)

cursor = mydb.cursor()
sql = '''SELECT id, spectrogram, file from file_viewer'''
cursor.execute(sql)
result = cursor.fetchall();

app_name = 'music_nation'
urlpatterns = [

    path('', views.Showemp),
    path('showform', views.showform),
    path('showgallery', views.showgallery),
    path('showspec', views.showspec),
    # path('SoundSpectrogram', views.SoundSpectrogram),
    path('SoundSpectrogram0', views.SoundSpectrogram0),
    path('SoundSpectrogram1', views.SoundSpectrogram1),
    path('SoundSpectrogram2', views.SoundSpectrogram2),
    path('SoundSpectrogram3', views.SoundSpectrogram3),
    path('SoundSpectrogram4', views.SoundSpectrogram4),
    path('SoundSpectrogram5', views.SoundSpectrogram5),
    # path('SoundSpectrogram1', views.SoundSpectrogram),

    #home /
    path('', music_nation_views.home, name='home'),

    #profile_detail /@username/
    path('@<str:username>/', music_nation_views.profile_detail, name='profile_detail'),

    #add new album /@username/add
    path('@<str:username>/add/', music_nation_views.add_album, name='add_album'),

    #album's detail page /@username/album/album_name
    path('@<str:username>/album/<str:album>/', music_nation_views.album_detail, name='album_detail'),

    # login the user /login/
    path('login/', LoginView.as_view(template_name='music_nation/user_login.html'), name="login"),

    # signUp new user /signup/
    path('signup/', music_nation_views.signup, name='signup'),

    #delete album /@username/album/album_name/delete
    path('@<str:username>/album/<str:album>/delete/', music_nation_views.delete_album, name='delete_album'),

    #add songs to the albums
    path('@<str:username>/album/<str:album>/add/', music_nation_views.add_song, name='add_song'),

    #logout the current user
    path('logout/', LogoutView.as_view(), name='logout'),

]

#path('link', view, name='', kwargs={})
#re_path(r'regex', view, name='', kwargs={})