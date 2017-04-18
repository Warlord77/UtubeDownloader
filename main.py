from pytube import YouTube
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder

Builder.load_string('''
<SR>:
    orientation: "vertical"
    TextInput:
        id: text_input
        hint_text: "Enter URL"
        font_size: "30dp"
        multiline: False
    Button:
        text: "Download"
        font_size:24
        on_release: root.on_our_btn_release(text_input.text)    


''')

class SR(BoxLayout):
    def on_our_btn_release(self, text_input):
        yt = YouTube(text_input)
        video = yt.get('mp4', '720p')
        video.download('/home/w77/kivyapp/utubedownloader/')


class Utube(App):

    def build(self):
        return SR()

if __name__ == '__main__':
   Utube().run()