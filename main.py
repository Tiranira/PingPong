import time

from kivy._clock import ClockEvent
from kivy.app import App
from kivy.graphics import Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
import random

class FinishTable(Widget):
    text = StringProperty()
    start_new_game = ClockEvent(None, 0, 0, 0, 0)


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1 
            ball.velocity = vel.x, vel.y + offset

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(self.velocity) + self.pos


class PongGame(Widget):
    win = NumericProperty(0)
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    score_player = ObjectProperty(None)
    event = ClockEvent(None, 0, 0, 0, 0)
    finish = ClockEvent(None, 0, 0, 0, 0)
    start_new_game = ClockEvent(None, 0, 0, 0, 0)
    def first_start(self):
        self.add_widget(Label(font_size=70, center_x=self.width * 3 / 4, top=self.top - 50, text=str(self.player1.score)))

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def start(self):
        self.event = Clock.schedule_interval(self.update, 0.5 / 60.0)
        self.finish = Clock.create_trigger(self.finished)
        self.start_new_game = Clock.create_trigger(self.new_game_button)

    def create_new_game(self):
        self.add_widget(self.ball)
        self.add_widget(self.player1)
        self.add_widget(self.player2)
        self.canvas.add(Rectangle(pos=(self.center_x - 5, 0), size=(10, self.height)))
        self.add_widget(Label(font_size=70, center_x=self.width / 4, top=self.top - 50, text=str(self.player2.score)))
        self.add_widget(Label(font_size=70, center_x=self.width * 3 / 4, top=self.top - 50, text=str(self.player1.score)))
        self.serve_ball()

    def rewrite_game(self):
        self.add_widget(self.ball)
        self.add_widget(self.player1)
        self.add_widget(self.player2)
        self.add_widget(Label(font_size=70, center_x=self.width / 4, top=self.top - 50, text=str(self.player2.score)))
        self.add_widget(Label(font_size=70, center_x=self.width * 3 / 4, top=self.top - 50, text=str(self.player1.score)))



    def finished(self, dt):
        self.player1.center_y = self.center_y
        self.player2.center_y = self.center_y
        self.player1.score = 0
        self.player2.score = 0
        fin = FinishTable()
        if self.win == 1:
            fin.text = "Win player 1"
        elif self.win == 2:
            fin.text = "Win player 2"
        self.clear_widgets()
        self.canvas.clear()
        fin.start_new_game = self.start_new_game
        self.add_widget(fin)

    def new_game_button(self, dt):
        self.clear_widgets()
        self.create_new_game()
        self.start()

    def update(self, dt):

        ball_stat = self.ball.pos
        self.clear_widgets()
        self.rewrite_game()
        self.ball.pos = ball_stat
        self.player2.center_y = self.ball.y - 95
        self.ball.move()

        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # went of to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            if self.player2.score == 2:
                self.win = 2
                self.event.cancel()
                return self.finish()
            self.serve_ball(vel=(4, 0))
        if self.ball.right > self.width:
            self.player1.score += 1
            if self.player1.score == 2:
                self.win = 1
                self.event.cancel()
                return self.finish()
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        # if touch.x > self.width - self.width / 3:
        #     self.player2.center_y = touch.y



class PongApp(App):
    # def __int__(self):
    #     super().__int__()
    #     self.label = Label(text="Win")

    def build(self):
        box = BoxLayout()
        game = PongGame()
        game.serve_ball()
        game.start()
        box.add_widget(game)

        return box


if __name__ == '__main__':
    PongApp().run()
