from __future__ import unicode_literals
import youtube_dl
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.lang import Builder
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
from kivy.uix.scrollview import ScrollView
from kivy.factory import Factory
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.uix.videoplayer import VideoPlayer
from progress import ProgressBehavior
import threading 

class ProgressButton(ProgressBehavior,Button):
    pass
    

Builder.load_string('''
<Burfee>
    size_hint: 1, None
    height: dp(45)
    Label
        text: root.text
    ProgressButton
        text: 'download'
        progress: float(root.progress[0:-1])/100
        progress_color: 1, 0, 0, 0.5
        on_release: root.start_download(root.url)
        size_hint: 0.2 ,1

    Button
        text: 'pause'
        size_hint: 0.1 , 1


<SR>:
    orientation: "vertical"
    BoxLayout:
        size_hint: 1, .2
        TextInput:
            id: text_input
            hint_text: "Enter KeyWord"
            font_size: "30dp"
            multiline: False
            size_hint_x: 0.8 
        Button:
            text: "Search"
            font_size:24
            size_hint_x: 0.5
            on_release: root.on_btn_release(text_input.text)
    ScrollView:
        GridLayout:
            cols: 1
            size_hint: 1, None
            height: self.minimum_height
            id: grid
    
  
''')


class Burfee(BoxLayout):
    text = StringProperty('')
    url = StringProperty('')
    progress = StringProperty('0%')

    def play(self, url):
        video= VideoPlayer(source= 'http://www.youtube.com/watch?v='+ url, state='play')
        print 'http://www.youtube.com/watch?v='+ url

    def on_status(self, progress):
        print progress, '<<'
        if progress['status'] == 'downloading':
            self.progress = progress['_percent_str']

    def bar(self,pbar):
    	b =  float(progress)
        self.pbar =  b/100

    def start_download(self, url):
        # 1) hook our function into progress_hooks
        threading.Thread(target=self.download, args=(url,)).start()
    

    def download(self, url):
        ydl_opts= {'progress_hooks': [self.on_status]}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['http://www.youtube.com/watch?v='+ url])
        print 'http://www.youtube.com/watch?v='+ url
        

    


    

class SR(BoxLayout):

    def youtube_search(self, options):
        DEVELOPER_KEY = "AIzaSyDhHcCDOIhkaHh4gD7xlAmK3vr-GI-4Iiw "
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                        developerKey=DEVELOPER_KEY)

        search_response = youtube.search().list(
            q=options,
            part="id,snippet",
            # maxResults=options.max_results
        ).execute()

        videos = []
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                videos.append(
                    {search_result["snippet"]["title"]:  
                                           search_result["id"]["videoId"]})
        print videos
        for video in videos:
            key = video.keys()[0]
            self.ids.grid.add_widget(Burfee(
                text=key,
                url=video[key]))


    def on_btn_release(self, text_input):
        to_search = text_input
        try:
            self.youtube_search(to_search)
        except HttpError, e:
            print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)


class Utube(App):
    '''
    '''

    def build(self):
        return SR()

if __name__ == '__main__':
    Utube().run()

    #Button
    #text: 'play'
    #on_release:  root.play(root.url)
    #size_hint: 0.2 , 1