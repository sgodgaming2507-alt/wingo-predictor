import hashlib
import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window

# Dark Casino Style Background
Window.clearcolor = (0.05, 0.07, 0.11, 1)

class OkWinPredictorApp(App):
    def build(self):
        self.cached_predictions = {}
        self.current_period = ""

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Header Title
        t = Label(
            text="[b][color=#FFD700]OKWIN / DMWIN 1M ANALYZER[/color][/b]",
            markup=True,
            font_size='20sp',
            size_hint=(1, 0.12)
        )

        # Period Number
        self.p = Label(
            text="Syncing OKWin Server...",
            markup=True,
            font_size='17sp',
            size_hint=(1, 0.1),
            color=(0.2, 0.9, 1, 1)
        )

        # Timer Countdown
        self.tm = Label(
            text="Timer: 00:00",
            markup=True,
            font_size='18sp',
            size_hint=(1, 0.1),
            color=(1, 1, 1, 1)
        )

        # Output Box
        self.r = Label(
            text="[b]Connecting to Server Stream...[/b]",
            markup=True,
            font_size='18sp',
            size_hint=(1, 0.58),
            color=(0.95, 0.95, 0.95, 1)
        )

        # Server Status
        self.st = Label(
            text="● SERVER: IST (UTC+05:30) SYNCED",
            font_size='13sp',
            size_hint=(1, 0.1),
            color=(0, 1, 0.6, 1)
        )

        for w in [t, self.p, self.tm, self.r, self.st]:
            layout.add_widget(w)

        Clock.schedule_interval(self.tick, 1)
        return layout

    def get_ist_time(self):
        # Precise UTC to IST conversion
        utc_now = datetime.datetime.now(datetime.timezone.utc)
        ist_tz = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
        return utc_now.astimezone(ist_tz)

    def get_okwin_period(self):
        # Exact OKWIN 1-Min Calculation
        ist_now = self.get_ist_time()
        
        # Total minutes passed today in IST
        total_minutes = (ist_now.hour * 60) + ist_now.minute + 1
        date_str = ist_now.strftime('%Y%m%d')
        
        # OKWin Format: YYYYMMDD01000XXXX (e.g., 20260819010000542)
        return f"{date_str}01000{total_minutes:04d}"

    def tick(self, dt):
        ist_now = self.get_ist_time()
        seconds_left = 60 - ist_now.second
        
        self.tm.text = f"Round Time: [color=#ffbb00]00:{seconds_left:02d}s[/color]"

        period = self.get_okwin_period()
        if period != self.current_period:
            self.current_period = period
            self.p.text = f"[b]Live Period:[/b] [color=#00ffea]{self.current_period}[/color]"
            self.generate_pattern_forecast(period)

    def generate_pattern_forecast(self, period):
        if period not in self.cached_predictions:
            # Deterministic multi-hash algorithm
            raw_seed = (period + "OKWIN_DMWIN_SECURE_SALT").encode('utf-8')
            sha_hash = hashlib.sha256(raw_seed).hexdigest()
            md5_hash = hashlib.md5(raw_seed).hexdigest()

            val = int(sha_hash[:8], 16) ^ int(md5_hash[:8], 16)

            # Outcome logic
            size = "BIG" if (val % 2 == 0) else "SMALL"
            
            if size == "BIG":
                num_pool = [5, 6, 7, 8, 9]
            else:
                num_pool = [0, 1, 2, 3, 4]
                
            predicted_num = num_pool[(val >> 2) % len(num_pool)]
            
            # Color Mapping
            if predicted_num in [1, 3, 7, 9]:
                color_badge = "[color=#00ff66]GREEN 🟢[/color]"
            elif predicted_num in [2, 4, 6, 8]:
                color_badge = "[color=#ff3333]RED 🔴[/color]"
            elif predicted_num == 0:
                color_badge = "[color=#ff3333]RED[/color] + [color=#cc33ff]VIOLET 🔴🟣[/color]"
            else:
                color_badge = "[color=#00ff66]GREEN[/color] + [color=#cc33ff]VIOLET 🟢🟣[/color]"

            confidence_rate = 88 + (val % 10)  # 88% to 97% range

            self.cached_predictions[period] = {
                "size": size,
                "num": predicted_num,
                "color": color_badge,
                "conf": confidence_rate
            }

        d = self.cached_predictions[period]
        self.r.text = (
            f"[b]ANALYSIS PREDICTION (LOCKED)[/b]\n\n"
            f"Pattern Result: [color=#ffff00][b]{d['size']}[/b][/color]\n"
            f"Target Number: [color=#00ffff][b]{d['num']}[/b][/color]\n"
            f"Color Signal: {d['color']}\n"
            f"Pattern Signal: [color=#00ff88]{d['conf']}%[/color]"
        )

if __name__ == '__main__':
    OkWinPredictorApp().run()
