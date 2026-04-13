from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivymd.uix.button import MDIconButton
from kivy.uix.image import AsyncImage
from kivy.core.window import Window
from kivy.clock import Clock
import webbrowser
from kivy.uix.button import ButtonBehavior
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.screenmanager import MDScreenManager
from task_screen import TaskScreen

from tts import toggle

from games import (
    GameScreen,
    SentenceGameScreen,
    WordGameScreen,
    ColorGameScreen,
    DirectionGameScreen
)

class DyslexiaTestScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.questions = [
            "It seems to me that the letters or words are moving across the page.",
            "Sometimes when I read I skip words or lines.",
            "I often confuse directions such as left and right.",
            "Long paragraphs create a feeling of clutter.",
            "I find it harder to read from a screen than from paper.",
            "I have difficulty remembering names of people or places.",
            "People tell me I repeat the same things.",
            "I often misplace things.",
            "I have difficulty spelling irregular words.",
            "I often reread to understand.",
            "I focus more on the big picture than details.",
            "Noise makes it hard to focus.",
            "I work best with structured routine.",
            "I need extra time for writing tasks.",
            "I struggle to process lots of information quickly.",
            "I confuse similar-looking words.",
            "I lose track mid-task.",
            "I struggle remembering multiple instructions.",
            "I feel mentally exhausted after reading/writing.",
            "I think of creative solutions.",
            "I avoid reading out loud.",
            "I often make spelling mistakes.",
            "I struggle distinguishing similar sounds.",
            "I add extra letters when writing.",
            "I write words by ear.",
            "I understand better when text is read aloud.",
            "I make mistakes even knowing rules.",
            "I struggle breaking words into sounds."
        ]

        self.answers = []
        self.current_q = 0

        self.layout = MDBoxLayout(orientation="vertical", padding=20, spacing=20)
        
        self.progress = MDLabel(
            text=f"1/{len(self.questions)}",
            halign="center"
        )

        self.question_label = MDLabel(
            text=self.questions[0],
            halign="center"
        )

        # КНОПКИ
        self.buttons = MDBoxLayout(spacing=10, size_hint_y=None, height=80)

        colors = [
            (1, 0, 0, 1),
            (1, 0.5, 0, 1),
            (1, 1, 1, 1),
            (0, 0.5, 1, 1),
            (0, 1, 0, 1)
        ]

        for i, color in enumerate(colors):
            btn = MDIconButton(
                icon="circle",
                theme_text_color="Custom",
                text_color=color,
                on_release=lambda x, val=i: self.select_answer(val)
            )
            self.buttons.add_widget(btn)

        self.layout.add_widget(self.progress)
        self.layout.add_widget(self.question_label)
        self.layout.add_widget(self.buttons)

        self.add_widget(self.layout)

    def select_answer(self, value):
        self.answers.append(value)
        self.current_q += 1

        if self.current_q < len(self.questions):
            self.question_label.text = self.questions[self.current_q]
            self.progress.text = f"{self.current_q+1}/{len(self.questions)}"
        else:
            self.show_result()

    def show_result(self):
        score = sum(self.answers)
        percent = int((score / (len(self.questions)*4)) * 100)

        if percent <= 30:
            result = "Dyslexia is not indicated. Try improving study techniques."
        elif percent <= 60:
            result = "Possible dyslexia traits. Pay attention to reading and writing skills."
        else:
            result = "Strong signs of dyslexia. Consider consulting a specialist."

        self.layout.clear_widgets()

        self.layout.add_widget(
            MDLabel(
                text=f"Result: {percent}%\n\n{result}",
                halign="center"
            )
        )

class ADHDTestScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.questions = [
            "I tend to leave things unfinished because I get bored or distracted",
            "I often have difficulty getting things in order",
            "I find it hard to regulate my energy level",
            "I often feel nervous or anxious",
            "I avoid tasks that require a lot of thinking",
            "I have little interest in doing things",
            "I have difficulty relaxing",
            "I get frustrated easily",
            "I struggle with repetitive work",
            "I have trouble waiting my turn",
            "I struggle with multi-step processes",
            "I feel overwhelmed with many tasks",
            "I struggle to prioritize tasks",
            "I can't track responsibilities well",
            "I feel urge to act immediately",
            "I avoid social events",
            "I hyper-focus on one thing",
            "I feel I work harder than others",
            "I have trouble sleeping",
            "I get overwhelmed by choices",
            "I struggle to differentiate tasks",
            "I react emotionally to stress",
            "I interrupt conversations",
            "I interrupt others speaking"
        ]

        self.answers = []
        self.current_q = 0

        self.layout = MDBoxLayout(orientation="vertical", padding=20, spacing=20)

        self.progress = MDLabel(
            text="1/24",
            halign="center",
            font_size=18
        )

        self.question_label = MDLabel(
            text=self.questions[0],
            halign="center"
        )

        # КРУГИ
        self.buttons = MDBoxLayout(spacing=10, size_hint_y=None, height=80)

        colors = [
            (1, 0, 0, 1),
            (1, 0.5, 0, 1),
            (1, 1, 1, 1),
            (0, 0.5, 1, 1),
            (0, 1, 0, 1)
        ]

        for i, color in enumerate(colors):
            btn = MDIconButton(
                icon="circle",
                theme_text_color="Custom",
                text_color=color,
                on_release=lambda x, val=i: self.select_answer(val)
            )
            self.buttons.add_widget(btn)

        self.layout.add_widget(self.progress)
        self.layout.add_widget(self.question_label)
        self.layout.add_widget(self.buttons)

        self.add_widget(self.layout)

    def select_answer(self, value):
        self.answers.append(value)
        self.current_q += 1

        if self.current_q < len(self.questions):
            self.update_question()
        else:
            self.show_result()

    def update_question(self):
        self.question_label.text = self.questions[self.current_q]
        self.progress_label.text = f"Question {self.current_q + 1} of {len(self.questions)}"
        self.progress_bar.value = self.current_q + 1

    def show_result(self):
        score = sum(self.answers)
        percent = int((score / (len(self.questions)*4)) * 100)

        if percent <= 30:
            result = "No significant signs of ADHD"
        elif percent <= 60:
            result = "Moderate signs of ADHD"
        else:
            result = "Strong signs of ADHD"

        self.layout.clear_widgets()

        self.layout.add_widget(
            MDLabel(
                text=f"Result: {percent}%\n\n{result}",
                halign="center"
            )
        )


# ---------------- OTHER SCREENS ----------------
class TaskScreen(MDScreen):
    pass

class ClickableImage(ButtonBehavior, AsyncImage):
    pass

class HomeScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main = MDBoxLayout(orientation="vertical")

        scroll = ScrollView()
        content = MDBoxLayout(
            orientation="vertical",
            padding=20,
            spacing=20,
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter("height"))

        # ---------- TITLE ----------
        title_app = MDLabel(
            text="Dislexify",
            halign="center",
            font_size=32,
            theme_text_color="Custom",
            text_color=(0.2, 0.6, 1, 1)
        )

        content.add_widget(title_app)

        # ---------- INFO CARD ----------
        info_card = MDCard(
            size_hint=(1, None),
            height=dp(130),
            radius=[20],
            md_bg_color=(0.9, 0.94, 1, 1),
            ripple_behavior=True
        )

        info_box = MDBoxLayout(padding=15, spacing=15)

        info_icon = MDIcon(icon="book-open-page-variant", font_size=40)

        title = MDLabel(
            text="What is dyslexia?",
            halign="center",
            font_size=24
        )

        info_box.add_widget(info_icon)
        info_box.add_widget(title)
        info_card.add_widget(info_box)

        info_card.bind(on_release=lambda x: setattr(self.manager, "current", "info"))

        # ---------- TESTS TITLE ----------
        tests_title = MDLabel(
            text="Tests",
            halign="center",
            font_size=22
        )

        # ---------- TEST CARDS ----------
        tests_box = MDBoxLayout(
            size_hint_y=None,
            height=dp(120),
            spacing=10
        )

        # --- Dyslexia Test ---
        dys_card = MDCard(
            size_hint=(0.5, 1),
            md_bg_color=(0.8, 0.9, 1, 1),
            ripple_behavior=True,
            radius=[15]
        )

        dys_card.add_widget(
            MDLabel(text="Dyslexia Test", halign="center")
        )

        dys_card.bind(on_release=lambda x: setattr(self.manager, "current", "dyslexia"))

        # --- ADHD Test ---
        adhd_card = MDCard(
            size_hint=(0.5, 1),
            md_bg_color=(0.2, 0.4, 1, 1),
            ripple_behavior=True,
            radius=[15]
        )

        adhd_card.add_widget(
            MDLabel(text="ADHD Test", halign="center", theme_text_color="Custom", text_color=(1,1,1,1))
        )

        adhd_card.bind(on_release=lambda x: setattr(self.manager, "current", "adhd"))

        video = ClickableImage(
            source="https://img.youtube.com/vi/zafiGBrFkRM/0.jpg",
            size_hint_y=None,
            height=dp(200)
        )

        video.bind(on_release=lambda x: webbrowser.open(
            "https://www.youtube.com/watch?v=zafiGBrFkRM"
        ))

        content.add_widget(video)

        # ---------- ADD ----------
        tests_box.add_widget(dys_card)
        tests_box.add_widget(adhd_card)

        content.add_widget(info_card)
        content.add_widget(tests_title)
        content.add_widget(tests_box)

        scroll.add_widget(content)
        main.add_widget(scroll)
        self.add_widget(main)

class InfoScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.full_text = """Dyslexia is the most common learning disability. It is characterized by difficulties with reading, spelling and decoding.

People with dyslexia may read slowly, confuse words, or need more time to process information. However, they are often very creative and think differently.

Dyslexia is not related to intelligence — many successful people have it."""

        self.is_playing = False

        scroll = ScrollView()

        layout = MDBoxLayout(
            orientation="vertical",
            padding=20,
            spacing=20,
            size_hint_y=None
        )
        layout.bind(minimum_height=layout.setter("height"))

        # ---------- TITLE ----------
        title_card = MDCard(
            radius=[20],
            padding=15,
            md_bg_color=(0.2, 0.6, 1, 1),
            size_hint_y=None,
            height=dp(80)
        )

        title_card.add_widget(
            MDLabel(
                text="What is Dyslexia?",
                halign="center",
                theme_text_color="Custom",
                text_color=(1,1,1,1),
                font_size=30
            )
        )

        # ---------- TEXT WRAPPER ----------
        text_box = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            padding=dp(10),
        )

# ---------- TEXT ----------
        self.text_label = MDLabel(
            text=self.full_text,
            halign="left",
            size_hint_y=None,
            adaptive_height=True,
        )

        text_box.add_widget(self.text_label)

        text_card = MDCard(
            radius=[20],
            padding=15,
            md_bg_color=(0.95, 0.95, 0.95, 1),
            size_hint_y=None
        )

        text_card.add_widget(text_box)

        def update_height_and_width(*args):
            width = text_card.width - dp(30)
            self.text_label.text_size = (width, None)

            self.text_label.texture_update()
            self.text_label.height = self.text_label.texture_size[1]

            text_box.height = self.text_label.height + dp(20)
            text_card.height = text_box.height + dp(30)

        text_card.bind(width=update_height_and_width)

        Clock.schedule_once(lambda dt: update_height_and_width())

        # ---------- IMAGE ----------
        image_card = MDCard(
            radius=[20],
            size_hint_y=None,
            height=dp(220)
        )

        image_card.add_widget(
            AsyncImage(
                source="https://barcelona.guttmann.com/sites/default/files/styles/article_image/public/2023-02/shutterstock_2174662661.jpg"
            )
        )

        # ---------- BUTTON ----------
        listen_btn = MDIconButton(
            icon="volume-high",
            pos_hint={"center_x": 0.5},
            theme_icon_color="Custom",
            icon_color=(0.2, 0.6, 1, 1),
            size_hint=(None, None),
            size=(dp(60), dp(60))
        )

        def on_listen(instance):
            if self.is_playing:
                toggle("")
                self.is_playing = False
                instance.icon = "volume-high"
                return

            self.is_playing = True
            instance.icon = "pause"

            def on_end():
                self.is_playing = False
                instance.icon = "volume-high"

            toggle(
                self.full_text,
                on_word=self.highlight_word,
                on_end=on_end
            )

        listen_btn.bind(on_release=on_listen)

        # ---------- BACK ----------
        back_btn = MDRaisedButton(
            text="← Back",
            pos_hint={"center_x": 0.5},
            on_release=lambda x: setattr(self.manager, "current", "home")
        )

        # ---------- ADD ----------
        layout.add_widget(title_card)
        layout.add_widget(text_card)
        layout.add_widget(image_card)
        layout.add_widget(listen_btn)
        layout.add_widget(back_btn)

        scroll.add_widget(layout)
        self.add_widget(scroll)

    def highlight_word(self, word):
        words = self.full_text.split()
        new_text = []

        for w in words:
            if w.strip(".,!?") == word.strip(".,!?"):
                new_text.append(f"[color=ff3333]{w}[/color]")
            else:
                new_text.append(w)

        self.text_label.markup = True
        self.text_label.text = " ".join(new_text)

# ---------------- MAIN APP ----------------
class MainApp(MDApp):

    def build(self):
        self.theme_cls.material_style = "M3"

        Window.clearcolor = (0.92, 0.97, 1, 1)

        root = BoxLayout(orientation="vertical")

        self.sm = MDScreenManager()

        self.sm.add_widget(HomeScreen(name="home"))
        self.sm.add_widget(TaskScreen(name="task"))
        self.sm.add_widget(GameScreen(name="game"))
        self.sm.add_widget(InfoScreen(name="info"))
        self.sm.add_widget(DyslexiaTestScreen(name="dyslexia"))
        self.sm.add_widget(ADHDTestScreen(name="adhd"))
        self.sm.add_widget(SentenceGameScreen(name="sentence"))
        self.sm.add_widget(WordGameScreen(name="word"))
        self.sm.add_widget(ColorGameScreen(name="color"))
        self.sm.add_widget(DirectionGameScreen(name="direction"))

        root.add_widget(self.sm)

        # ---------- BOTTOM BAR ----------
        bottom_bar = BoxLayout(size_hint_y=None, height=dp(70))

        def switch(screen):
            self.sm.current = screen

        def make_btn(icon, screen):
            return MDIconButton(
                icon="home",
                icon_size="40sp",
                font_size="32sp",
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                on_release=lambda x: switch(screen)
            )

        bottom_bar.add_widget(make_btn("home", "home"))
        bottom_bar.add_widget(make_btn("checkbox-marked-outline", "tasks"))
        bottom_bar.add_widget(make_btn("gamepad-variant", "game"))

        root.add_widget(bottom_bar)

        return root


if __name__ == "__main__":
    MainApp().run()