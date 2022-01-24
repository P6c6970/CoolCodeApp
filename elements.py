from kivy.properties import BooleanProperty
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem
from kivymd.uix.textfield import MDTextFieldRound


class MDTextFieldRoundPas(MDTextFieldRound):
    password_mode = BooleanProperty(True)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.icon_right:
                icon_x = (self.width + self.x) - (self._lbl_icon_right.texture_size[1])
                icon_y = self.center[1] - self._lbl_icon_right.texture_size[1] / 2

                # not a complete bounding box test, but should be sufficient
                if touch.pos[0] > icon_x and touch.pos[1] > icon_y:
                    if self.password_mode:
                        self.icon_right = 'eye'
                        self.password_mode = False
                        self.password = self.password_mode
                    else:
                        self.icon_right = 'eye-off'
                        self.password_mode = True
                        self.password = self.password_mode

                    # try to adjust cursor position
                    cursor = self.cursor
                    self.cursor = (0, 0)
        return super(MDTextFieldRound, self).on_touch_down(touch)


class OneLineListItemAligned(OneLineListItem):
    def __init__(self, **kwargs):
        super(OneLineListItemAligned, self).__init__(**kwargs)
        self.ids._lbl_primary.halign = "center"

class MyMDCard(MDCard):
    pass