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

Builder.load_string('''
<Burfee>
    size_hint: 1, None
    height: dp(45)
    text: ''
    Label
        text: root.text
    Button
        text: 'download'
        on_release: root.download(root.url)
    Button
        text: 'play'
        on_release:  root.play(root.url)

<SR>:
    orientation: "vertical"
    Label:
        text:'Enter Keyword'
        text_size: self.size
        font_size: 24
        halign: 'left'
        valign: 'center'
    TextInput:
        id: text_input
        hint_text: "Enter KeyWord"
        font_size: "30dp"
        multiline: False
    Button:
        text: "Search"
        font_size:24
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

    def play(self, url):
        print 'play url', url

    def download(self, url):
        print 'download url', url


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
        str= ""

        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                           search_result["id"]["videoId"]))
                str = str + search_result["snippet"]["title"] +\
                    " http://www.youtube.com/watch?v=" + \
                    search_result["id"]["videoId"] + "\n"
        
        for i in str.split('\n'):
            print i
            self.ids.grid.add_widget(Burfee(text=i))


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
