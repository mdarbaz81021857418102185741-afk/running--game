from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Ellipse, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from random import randint


class RunnerGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.player_size = dp(48)
        self.player_x = dp(70)
        self.player_y = dp(55)
        self.velocity_y = 0
        self.gravity = -dp(1500)
        self.jump_power = dp(650)

        self.obstacles = []
        self.spawn_timer = 1
        self.score = 0
        self.speed = dp(360)
        self.game_over = False

        self.score_label = Label(
            text="Score: 0",
            font_size=dp(22),
            bold=True,
            size_hint=(None, None),
            size=(dp(180), dp(50))
        )
        self.add_widget(self.score_label)

        self.message = Label(
            text="TAP TO JUMP",
            font_size=dp(28),
            bold=True,
            halign="center",
            valign="middle",
            size_hint=(1, None),
            height=dp(80)
        )
        self.add_widget(self.message)

        self.bind(size=self.layout_ui, pos=self.layout_ui)
        Clock.schedule_interval(self.update, 1 / 60)

    @property
    def ground_y(self):
        return dp(55)

    def layout_ui(self, *args):
        self.score_label.pos = (dp(16), self.height - dp(60))
        self.message.pos = (0, self.height / 2 - dp(40))

    def jump(self):
        if self.game_over:
            self.reset_game()
            return

        if self.player_y <= self.ground_y + dp(2):
            self.velocity_y = self.jump_power
            self.message.text = ""

    def on_touch_down(self, touch):
        self.jump()
        return True

    def reset_game(self):
        self.obstacles.clear()
        self.score = 0
        self.speed = dp(360)
        self.spawn_timer = 1
        self.velocity_y = 0
        self.player_x = dp(70)
        self.player_y = self.ground_y
        self.game_over = False
        self.message.text = "TAP TO JUMP"
        self.draw()

    def spawn_obstacle(self):
        self.obstacles.append({
            "x": self.width + dp(20),
            "y": self.ground_y,
            "w": dp(randint(30, 50)),
            "h": dp(randint(45, 90))
        })

    def update(self, dt):
        if self.width <= 0 or self.height <= 0:
            return

        if self.game_over:
            self.draw()
            return

        self.velocity_y += self.gravity * dt
        self.player_y += self.velocity_y * dt

        if self.player_y <= self.ground_y:
            self.player_y = self.ground_y
            self.velocity_y = 0

        self.spawn_timer -= dt

        if self.spawn_timer <= 0:
            self.spawn_obstacle()
            self.spawn_timer = randint(8, 15) / 10

        for obstacle in self.obstacles:
            obstacle["x"] -= self.speed * dt

        self.obstacles = [
            o for o in self.obstacles
            if o["x"] + o["w"] > 0
        ]

        self.score += dt * 10
        self.speed = min(dp(700), dp(360) + self.score * dp(1.5))
        self.score_label.text = f"Score: {int(self.score)}"

        px1 = self.player_x + dp(7)
        px2 = self.player_x + self.player_size - dp(7)
        py1 = self.player_y + dp(5)
        py2 = self.player_y + self.player_size - dp(5)

        for o in self.obstacles:
            ox1 = o["x"]
            ox2 = o["x"] + o["w"]
            oy1 = o["y"]
            oy2 = o["y"] + o["h"]

            if px1 < ox2 and px2 > ox1 and py1 < oy2 and py2 > oy1:
                self.game_over = True
                self.message.text = "GAME OVER\nTAP TO RESTART"
                break

        self.draw()

    def draw(self):
        self.canvas.clear()

        with self.canvas:
            Color(0.08, 0.16, 0.30, 1)
            Rectangle(pos=(0, 0), size=self.size)

            Color(1, 0.9, 0.55, 1)
            Ellipse(
                pos=(self.width - dp(90), self.height - dp(120)),
                size=(dp(55), dp(55))
            )

            Color(0.12, 0.55, 0.20, 1)
            Rectangle(
                pos=(0, 0),
                size=(self.width, self.ground_y)
            )

            Color(0.65, 0.45, 0.20, 1)
            Rectangle(
                pos=(0, 0),
                size=(self.width, dp(12))
            )

            Color(0.95, 0.25, 0.15, 1)
            RoundedRectangle(
                pos=(self.player_x, self.player_y),
                size=(self.player_size, self.player_size),
                radius=[dp(10)]
            )

            Color(1, 1, 1, 1)
            Ellipse(
                pos=(
                    self.player_x + dp(28),
                    self.player_y + dp(30)
                ),
                size=(dp(8), dp(8))
            )

            Color(0.15, 0.8, 0.35, 1)

            for o in self.obstacles:
                RoundedRectangle(
                    pos=(o["x"], o["y"]),
                    size=(o["w"], o["h"]),
                    radius=[dp(5)]
                )


class RunningGameApp(App):

    title = "Running Game"

    def build(self):
        return RunnerGame()


if __name__ == "__main__":
    RunningGameApp().run()
