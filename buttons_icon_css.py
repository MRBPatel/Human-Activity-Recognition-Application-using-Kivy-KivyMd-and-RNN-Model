from kivy.factory import Factory
from kivy.graphics import Color, RoundedRectangle
from kivy.lang import Builder
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image


class RoundedButton(BoxLayout, Button):
    def __init__(self, **kwargs) -> None:
        super(RoundedButton, self).__init__()
        self.canvas.clear()
        self._image = None
        self._args = {'normal': (230 / 255, 184 / 255, 26 / 255, 1), 'down': (0, .7, .7, 1)}
        self._color = Color()
        self._color.rgba = self._args['normal']
        self._rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[10])
        self.canvas.add(self._color)
        self.canvas.add(self._rect)

    def _set_background(self, color):
        if color:
            self._color.rgba = color

    def on_click(self, state):
        self._set_background(self._args.get(state))

    def _set_args(self, value):
        """ set initial args for Button as dict
            # >>>@param:value -> python dict containing args for button
                                @required ('pos', 'size')
                                @optional ('normal', 'down', 'radius')
        """
        for key, val in value.items():
            self._args[key] = val

        self._color.rgba = self._args.get("normal")
        self._rect.pos = value['pos']
        self._rect.size = value['size']
        self._rect.radius = value.get("radius", [10])

    args = property(lambda arg: None, _set_args)

    @property
    def icon_source(self):
        if self._image:
            return self._image.source

    @icon_source.setter
    def icon_source(self, value):
        """ set image source in case Circle Button is using icon"""
        if self._image is None:

            self._image = Image()
            self._image.size_hint_y = 0.70
            self._image.source = value
            self.ids.lbl.size_hint_y = 0.3
            self.ids.lbl.text = self.text
            self.text = ""
            self.add_widget(self._image)

        else:
            self._image.source = value


Builder.load_string("""
<LabelButton@Button+ButtonBehavior>:
    size_hint_y:1
    size_hint_x:None
    width:50
    background_color:0,0,0,0
    color:(57/255.0,177/255.0,204/255.0,255/255.0)
    font_size:16
    bold:True
""")


class IconClick(BoxLayout, Button, ButtonBehavior):
    def __init__(self, **kwargs) -> None:
        super(IconClick, self).__init__()
        background_normal = ''
        self.canvas.clear()
        self._image = None
        self._args = {'normal': (29 / 255.0, 26 / 255.0, 69 / 255.0, 1), 'down': (0, .7, .7, 1)}
        self._color = Color()
        self._color.rgba = self._args['normal']
        self._rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[5])
        self.canvas.add(self._color)
        self.canvas.add(self._rect)

    def _set_bg_color(self, color):
        if color:
            self._color.rgba = color

    def on_click(self, state):
        self.background_normal = ""
        self._set_bg_color(self._args.get(state))

    def _set_args(self, value):
        """
        Getting value from main.kv file with id which is responsible
        for shape and color of button.
        """
        for key, val in value.items():
            self._args[key] = val

        self._color.rgba = self._args.get("normal")
        self._rect.pos = value['pos']
        self._rect.size = value['size']
        self._rect.radius = value.get("radius", [5])

    args = property(lambda arg: None, _set_args)

    @property
    def icon_source(self):
        if self._image:
            return self._image.source

    @icon_source.setter
    def icon_source(self, value):
        if self._image is None:
            self.text = ""
            self._image = Image()
            self._image.size_hint_y = 1
            self._image.source = value
            self.add_widget(self._image)

        else:
            self._image.source = value


Builder.load_string(
    """
<RowButton@BoxLayout+Button>:
    orientation:"horizontal"
    background_color: 0,0,0,0
    text_size:self.size
    bold: True
    font_size:14
    size_hint_y:None
    height:30
    color:(1,1,1,1)
    valign:'middle'
    halign:'center'
    canvas.before:
        Color:
            rgba: (0.92,0.96,0.97,.9) if self.state=='normal' else (0.2,.7,.7,1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [0]
"""
)


class RowButton(BoxLayout, Button):
    def __init__(self, **kwargs) -> None:
        super(RowButton, self).__init__()


Factory.register("IconClick", IconClick)
Factory.register("RoundedButton", RoundedButton)