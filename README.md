# Vehicle_Sound_Wav_File_Analyzer Documentation
1) Download the zipped file 'Software_Engineering_Mini_Project'
2) Unzipped the file 
3) open file 'utm' > 'music' > 'music' > 'music_nation'
4) All the important file are inside the file 'music_nation'
5) Inside 'templates' > 'music_nation' , the html files are kept inside.
6) Inside 'static' > 'music_nation', the image used in user interface are kept inside.
7) Wav file used had been taken out due to upload limit of github. It was originally stored inside 'media' > 'user_15'.
8) Database are shown in Table 1, Table 2, Table 3 and Table 4.

youtube link: https://www.youtube.com/watch?v=Ay3O7nQjfc4

# Architecture 
1) MVC architecture: Model View Controller +Database

# Features Explanation
1) Recording Features, the script is in homepage.html
a) As explain in video, user click on the record button and record their voice.
b) User download the reordings wav file, it is available.

2) Add wav file to the database, database setting are set inside the models.py(calling information from data base), settings.py(connect to database), database used is mySQL.
a) Click the upload button.
b) Select the wav file wish to upload.
c) Name the file in the database.
d) Press submit.
e) refresh the server, the database will update the wav file uploaded.

3) Sound Analyzer features (written in views.py, gallery.html, SoundSpectogram.html)  
a) User can view in Gallery once the wav file uploaded.
b) There is a table of list with the wav file uploaded.
c) Press play button to hear the sound, press show spectogram to show the spectogram.
d) The spectogram shown is only the time domain sound waveform (it is actually not the frequency domain spectogram).

4) Specifications Viewing (written in models.py, settings.py, mySQL, ShowSpec.html)
a) Back to the homepage 
b) Press the show specification button.
c) The specification table will show the specifications of the vehicle which have their sounds in gallery. For details can look at Table 1, Table 2, Table 3, and Table 4.
