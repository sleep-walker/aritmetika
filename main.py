# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
import random

RANGE=11


class AritmetikaLayout(Widget):
    pass

class Aritmetika(App):
    result = 0
    x = 0
    y = 0
    op = 1
    good = 0
    bad = 0

    def reset_state(self, _):
        self.good = 0
        self.bad = 0
        self.op = 1
        self.x = 0
        self.y = 0
        self.result = 0
        self.new_exercise()

    def setup_gui(self):
        self.textbox = TextInput(size_hint_y=.2, multiline=False, font_size=70)
        self.textbox.bind(on_text_validate=self.check_answer)
        self.q_label = Label(text='7 - 4\n', font_size=70)
        self.layout = BoxLayout(orientation='vertical')

        self.score_layout = BoxLayout(size_hint_y=.1, orientation='horizontal')
        self.g_label = Label(text='', font_size=30, markup=True)
        self.b_label = Label(text='', font_size=30, markup=True)
        self.reset_button = Button(text="Reset")
        self.reset_button.bind(on_press=self.reset_state)
        self.score_layout.add_widget(self.g_label)
        self.score_layout.add_widget(self.b_label)
        self.score_layout.add_widget(self.reset_button)

        self.layout.add_widget(self.score_layout)
        self.layout.add_widget(self.q_label)
        self.layout.add_widget(self.textbox)
        return self.layout

    def sign(self):
        if self.op == 1:
            return '+'
        else:
            return '-'

    def set_focus_to_textinput(self, _):
        self.textbox.focus = True

    def redraw(self):
        self.g_label.text = '[color=#00ff00]Správně:[/color] %d' % self.good
        self.b_label.text = '[color=#ff0000]Špatně:[/color] %d' % self.bad
        self.q_label.text = "%d %s %d" % (self.x, self.sign(), self.y)
        Clock.schedule_once(self.set_focus_to_textinput, 0.1)

    def validate_exercise(self):
        if self.x == self.y:
            return False
        if self.x * self.y == 0:
            return False
        if self.result == 1 or self.result == 0:
            return False
        return True

    def new_exercise(self):
        if random.randint(0, 1):
            self.op = -1
        else:
            self.op = 1

        self.x = random.randrange(RANGE)
        self.y = random.randrange(RANGE)

        if self.op == -1 and self.x < self.y:
            tmp = self.x
            self.x = self.y
            self.y = tmp

        self.result = self.x + self.op * self.y
        if not self.validate_exercise():
            self.new_exercise()
        self.redraw()

    def check_answer(self, *args):
        ans = self.textbox.text
        if ans:
            if int(ans) == self.result:
                self.good += 1
                self.textbox.text = ""
                self.new_exercise()
                return True
            else:
                self.bad += 1
                self.redraw()
                return False

    def build(self):
        layout = self.setup_gui()
        self.new_exercise()
        return layout

if __name__ == '__main__':
    Aritmetika().run()

