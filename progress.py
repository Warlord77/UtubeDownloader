'''
Progress Behavior
-----------------

Displays progress on top of a widget::


usage::

<ProgressButton@ProgressBhavior+Button>

'''

from kivy.properties import NumericProperty, ListProperty

from kivy.lang import Builder


class ProgressBehavior(object):

    progress  = NumericProperty(0)
    ''' Current progress status to be displayed on top of a widget.
    0 = 0%, 1 = 100%
    '''

    progress_color = ListProperty([0, 1, 0, .05])
    ''' Current Color to be used for progress
    '''

Builder.load_string('''
<ProgressBehavior>
    canvas.after:
        Color:
            rgba: self.progress_color
        Rectangle:
            pos: self.pos
            size: self.progress*self.width, self.height
        Color:
            rgba: 1, 1, 1, 1
''')


if __name__ == '__main__':
    from kivy.app import App
    from kivy.uix.button import Button

    class ProgressButton(ProgressBehavior, Button):
        pass

    class ProgressApp(App):
        def build(self):
            return ProgressButton()
        def on_start(self):
            from kivy.animation import Animation
            Animation(progress=1, d=5).start(self.root)
    ProgressApp().run()