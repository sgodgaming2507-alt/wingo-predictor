import json, os, datetime, hashlib
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window

Window.clearcolor = (0.08, 0.09, 0.12, 1)

class PredictorApp(App):
    def build(self):
        self.locked_predictions = {}
        self.current_period = ""

        layout = BoxLayout(orientation='vertical', padding=20, spacing=12)

        t = Label(text="[b]WINGO LIVE PREDICTOR[/b]", markup=True, font_size='22sp', size_hint=(1, 0.12), color=(1, 0.84, 0, 1))
        self.p = Label(text="Period: Syncing...", markup=True, font_size='18sp', size_hint=(1, 0.08), color=(0, 1, 0.7, 1))
        self.tm = Label(text="Timer: 00:00", font_size='18sp', size_hint=(1, 0.08), color=(1, 1, 1, 1))
        self.r = Label(text="[b]Waiting for Period...[/b]", markup=True, font_size='19sp', size_hint=(1, 0.5), color=(1, 1, 1, 1))
        
        for w in [t, self.p, self.tm, self.r]:
            layout.add_widget(w)

        Clock.schedule_interval(self.tick, 1)
        return layout

    def get_period(self):
        now = datetime.datetime.now()
        minutes_passed = (now.hour * 60) + now.minute + 1
        return f"{now.strftime('%Y%m%d')}1000{minutes_passed:04d}"

    def tick(self, dt):
        now = datetime.datetime.now()
        seconds_left = 60 - now.second
        self.tm.text = f"Timer: 00:{seconds_left:02d}"

        period = self.get_period()
        if period != self.current_period:
            self.current_period = period
            self.p.text = f"[b]Period:[/b] {self.current_period}"
            self.calc_prediction(period)

    def calc_prediction(self, period):
        p_hash = int(hashlib.md5(period.encode('utf-8')).hexdigest(), 16)
        size = "BIG" if (p_hash % 2 == 0) else "SMALL"
        nums = [5, 6, 7, 8, 9] if size == "BIG" else [0, 1, 2, 3, 4]
        num = nums[(p_hash >> 2) % len(nums)]
        
        if num in [1, 3, 7, 9]: color = "GREEN 🟢"
        elif num in [2, 4, 6, 8]: color = "RED 🔴"
        elif num == 0: color = "RED + VIOLET 🔴🟣"
        else: color = "GREEN + VIOLET 🟢🟣"

        self.r.text = (f"[b]PREDICTION[/b]\n\n"
                       f"Result: [color=#ffff00]{size}[/color]\n"
                       f"Number: [color=#00e1ff]{num}[/color]\n"
                       f"Color: {color}")

if __name__ == '__main__':
    PredictorApp().run()
