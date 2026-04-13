from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.uix.image import AsyncImage
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.button import ButtonBehavior
from kivy.uix.screenmanager import FadeTransition
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.progressbar import MDProgressBar
from kivy.animation import Animation
from kivy.utils import get_color_from_hex
import webbrowser
from task_screen import TaskScreen

# Создаем свой разделитель (MDDivider отсутствует в старых версиях)
class CustomDivider(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(1)
        self.md_bg_color = get_color_from_hex("#E0E0E0")

from tts import toggle
from games import (
    GameScreen,
    SentenceGameScreen,
    WordGameScreen,
    ColorGameScreen,
    DirectionGameScreen
)


# ---------- СТИЛИ ----------
class Colors:
    PRIMARY = "#4A90E2"
    PRIMARY_LIGHT = "#7FB0F0"
    PRIMARY_DARK = "#2C5F9E"
    SECONDARY = "#FF6B6B"
    SECONDARY_LIGHT = "#FF9B9B"
    SUCCESS = "#51CF66"
    WARNING = "#FFD43B"
    DANGER = "#FF6B6B"
    BACKGROUND = "#F8F9FA"
    SURFACE = "#FFFFFF"
    TEXT_PRIMARY = "#212529"
    TEXT_SECONDARY = "#6C757D"
    DYSLEXIA_GRADIENT_START = "#667EEA"
    DYSLEXIA_GRADIENT_END = "#764BA2"
    ADHD_GRADIENT_START = "#F093FB"
    ADHD_GRADIENT_END = "#F5576C"


# ---------- КНОПКА С ИЗОБРАЖЕНИЕМ ----------
class ClickableImage(ButtonBehavior, AsyncImage):
    def __init__(self, **kwargs):
        kwargs.pop('keep_ratio', None)
        kwargs.pop('allow_stretch', None)
        super().__init__(**kwargs)


# ---------- КАРТОЧКА ТЕСТА (С РАБОЧЕЙ АНИМАЦИЕЙ) ----------
class TestCard(MDCard):
    def __init__(self, title, icon, color_start, color_end, screen_name, duration="10-15 min", **kwargs):
        super().__init__(**kwargs)
        self.screen_name = screen_name
        self.size_hint = (1, None)
        self.height = dp(140)
        self.radius = [20]
        self.md_bg_color = get_color_from_hex(color_start)
        self.ripple_behavior = True
        self.padding = dp(20)
        self.spacing = dp(10)
        self.orientation = "vertical"

        # Иконка
        icon_label = MDIcon(
            icon=icon,
            font_size="48sp",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            halign="center"
        )

        # Заголовок
        title_label = MDLabel(
            text=title,
            font_size="22sp",
            bold=True,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            halign="center"
        )

        # Длительность
        duration_label = MDLabel(
            text=duration,
            font_size="14sp",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.8),
            halign="center"
        )

        self.add_widget(icon_label)
        self.add_widget(title_label)
        self.add_widget(duration_label)

        # Привязываем переход на экран
        self.bind(on_release=lambda x: self.go_to_screen())

    def go_to_screen(self):
        app = MDApp.get_running_app()
        app.sm.current = self.screen_name

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # Анимация уменьшения
            anim = Animation(height=dp(135), duration=0.1)
            anim.start(self)
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            # Анимация возврата
            anim = Animation(height=dp(140), duration=0.1)
            anim.start(self)
        return super().on_touch_up(touch)


# ---------- ЭКРАН ТЕСТА НА ДИСЛЕКСИЮ (УЛУЧШЕННЫЙ) ----------
# ---------- ЭКРАН ТЕСТА НА ДИСЛЕКСИЮ ----------
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

        # Основной layout
        self.layout = MDBoxLayout(
            orientation="vertical",
            padding=[dp(20), dp(40), dp(20), dp(20)],
            spacing=dp(30),
            md_bg_color=get_color_from_hex(Colors.BACKGROUND)
        )

        # Верхняя панель с прогрессом
        top_panel = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(80),
            spacing=dp(10)
        )

        # Заголовок и счетчик
        header_box = MDBoxLayout(
            size_hint_y=None,
            height=dp(30)
        )

        self.progress_label = MDLabel(
            text=f"Question 1 of {len(self.questions)}",
            font_size="16sp",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
        )

        back_btn = MDIconButton(
            icon="close",
            pos_hint={"center_y": 0.5},
            on_release=lambda x: setattr(self.manager, "current", "home")
        )

        header_box.add_widget(self.progress_label)
        header_box.add_widget(back_btn)

        # Прогресс-бар
        self.progress_bar = MDProgressBar(
            value=0,
            max=len(self.questions),
            size_hint_y=None,
            height=dp(6),
            color=get_color_from_hex(Colors.PRIMARY)
        )

        top_panel.add_widget(header_box)
        top_panel.add_widget(self.progress_bar)

        # Карточка с вопросом
        question_card = MDCard(
            size_hint=(1, None),
            height=dp(200),
            radius=[20],
            padding=dp(20),
            md_bg_color=get_color_from_hex(Colors.SURFACE),
            elevation=2
        )

        self.question_label = MDLabel(
            text=self.questions[0],
            halign="center",
            valign="middle",
            font_size="18sp",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
        )

        question_card.add_widget(self.question_label)

        # Шкала ответов с эмодзи
        scale_box = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(120),
            spacing=dp(10)
        )

        scale_label = MDLabel(
            text="How often does this happen?",
            halign="center",
            font_size="14sp",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
        )

        # Кнопки с эмодзи
        buttons_box = MDBoxLayout(
            spacing=dp(10),
            size_hint_y=None,
            height=dp(70)
        )

        emotions = [
            ("😡", "Never", Colors.DANGER),
            ("😕", "Rarely", Colors.WARNING),
            ("😐", "Sometimes", "#ADB5BD"),
            ("🙂", "Often", Colors.PRIMARY),
            ("😍", "Always", Colors.SUCCESS)
        ]

        for i, (emoji, text, color) in enumerate(emotions):
            btn_card = MDCard(
                size_hint=(0.2, 1),
                radius=[15],
                md_bg_color=get_color_from_hex(color),
                ripple_behavior=True
            )

            btn_layout = MDBoxLayout(
                orientation="vertical",
                padding=dp(5)
            )

            emoji_label = MDLabel(
                text=emoji,
                font_size="28sp",
                halign="center",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            )

            text_label = MDLabel(
                text=text,
                font_size="10sp",
                halign="center",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            )

            btn_layout.add_widget(emoji_label)
            btn_layout.add_widget(text_label)
            btn_card.add_widget(btn_layout)

            btn_card.bind(on_release=lambda x, val=i: self.select_answer(val))
            buttons_box.add_widget(btn_card)

        scale_box.add_widget(scale_label)
        scale_box.add_widget(buttons_box)

        # Добавляем всё в layout
        self.layout.add_widget(top_panel)
        self.layout.add_widget(question_card)
        self.layout.add_widget(scale_box)

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
        percent = int((score / (len(self.questions) * 4)) * 100)

        if percent <= 30:
            result = "Low likelihood of dyslexia"
            result_color = Colors.SUCCESS
            recommendation = "Continue practicing reading and writing skills."
        elif percent <= 60:
            result = "Moderate signs of dyslexia"
            result_color = Colors.WARNING
            recommendation = "Consider additional screening and targeted exercises."
        else:
            result = "High likelihood of dyslexia"
            result_color = Colors.DANGER
            recommendation = "We recommend consulting with a specialist."

        self.layout.clear_widgets()

        # Карточка результата
        result_card = MDCard(
            size_hint=(1, None),
            height=dp(400),
            radius=[20],
            padding=dp(30),
            spacing=dp(20),
            orientation="vertical",
            md_bg_color=get_color_from_hex(Colors.SURFACE),
            pos_hint={"center_y": 0.5}
        )

        # Иконка результата
        icon = "check-circle" if percent <= 30 else "alert-circle"
        icon_label = MDIcon(
            icon=icon,
            font_size="64sp",
            theme_text_color="Custom",
            text_color=get_color_from_hex(result_color),
            halign="center"
        )

        # Процент
        percent_label = MDLabel(
            text=f"{percent}%",
            font_size="48sp",
            bold=True,
            halign="center",
            theme_text_color="Custom",
            text_color=get_color_from_hex(result_color)
        )

        # Результат
        result_label = MDLabel(
            text=result,
            font_size="20sp",
            bold=True,
            halign="center",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
        )

        # Рекомендация
        recommendation_label = MDLabel(
            text=recommendation,
            font_size="14sp",
            halign="center",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
        )

        # Кнопки
        buttons_box = MDBoxLayout(
            spacing=dp(15),
            size_hint_y=None,
            height=dp(50)
        )

        home_btn = MDFlatButton(
            text="Back to Home",
            on_release=lambda x: setattr(self.manager, "current", "home")
        )

        retake_btn = MDRaisedButton(
            text="Retake Test",
            on_release=lambda x: self.retake_test()
        )

        buttons_box.add_widget(home_btn)
        buttons_box.add_widget(retake_btn)

        result_card.add_widget(icon_label)
        result_card.add_widget(percent_label)
        result_card.add_widget(result_label)
        result_card.add_widget(CustomDivider())
        result_card.add_widget(recommendation_label)
        result_card.add_widget(buttons_box)

        self.layout.add_widget(result_card)

    def retake_test(self):
        self.answers = []
        self.current_q = 0
        self.layout.clear_widgets()
        self.__init__()
        self.manager.current = "dyslexia"


# ---------- ЭКРАН ТЕСТА НА ADHD ----------
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

        self.layout = MDBoxLayout(
            orientation="vertical",
            padding=[dp(20), dp(40), dp(20), dp(20)],
            spacing=dp(30),
            md_bg_color=get_color_from_hex(Colors.BACKGROUND)
        )

        # Верхняя панель
        top_panel = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(80),
            spacing=dp(10)
        )

        header_box = MDBoxLayout(size_hint_y=None, height=dp(30))

        self.progress_label = MDLabel(
            text=f"Question 1 of {len(self.questions)}",
            font_size="16sp",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
        )

        back_btn = MDIconButton(
            icon="close",
            on_release=lambda x: setattr(self.manager, "current", "home")
        )

        header_box.add_widget(self.progress_label)
        header_box.add_widget(back_btn)

        self.progress_bar = MDProgressBar(
            value=0,
            max=len(self.questions),
            size_hint_y=None,
            height=dp(6),
            color=get_color_from_hex(Colors.SECONDARY)
        )

        top_panel.add_widget(header_box)
        top_panel.add_widget(self.progress_bar)

        # Карточка вопроса
        question_card = MDCard(
            size_hint=(1, None),
            height=dp(200),
            radius=[20],
            padding=dp(20),
            md_bg_color=get_color_from_hex(Colors.SURFACE),
            elevation=2
        )

        self.question_label = MDLabel(
            text=self.questions[0],
            halign="center",
            valign="middle",
            font_size="18sp",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
        )

        question_card.add_widget(self.question_label)

        # Шкала ответов
        scale_box = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(120),
            spacing=dp(10)
        )

        scale_label = MDLabel(
            text="How often does this happen?",
            halign="center",
            font_size="14sp",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
        )

        buttons_box = MDBoxLayout(spacing=dp(10), size_hint_y=None, height=dp(70))

        emotions = [
            ("😡", "Never", Colors.DANGER),
            ("😕", "Rarely", Colors.WARNING),
            ("😐", "Sometimes", "#ADB5BD"),
            ("🙂", "Often", Colors.SECONDARY),
            ("😍", "Always", Colors.SUCCESS)
        ]

        for i, (emoji, text, color) in enumerate(emotions):
            btn_card = MDCard(
                size_hint=(0.2, 1),
                radius=[15],
                md_bg_color=get_color_from_hex(color),
                ripple_behavior=True
            )

            btn_layout = MDBoxLayout(orientation="vertical", padding=dp(5))

            emoji_label = MDLabel(
                text=emoji,
                font_size="28sp",
                halign="center",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            )

            text_label = MDLabel(
                text=text,
                font_size="10sp",
                halign="center",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            )

            btn_layout.add_widget(emoji_label)
            btn_layout.add_widget(text_label)
            btn_card.add_widget(btn_layout)

            btn_card.bind(on_release=lambda x, val=i: self.select_answer(val))
            buttons_box.add_widget(btn_card)

        scale_box.add_widget(scale_label)
        scale_box.add_widget(buttons_box)

        self.layout.add_widget(top_panel)
        self.layout.add_widget(question_card)
        self.layout.add_widget(scale_box)

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
        percent = int((score / (len(self.questions) * 4)) * 100)

        if percent <= 30:
            result = "Low likelihood of ADHD"
            result_color = Colors.SUCCESS
            recommendation = "Your responses suggest minimal ADHD symptoms."
        elif percent <= 60:
            result = "Moderate signs of ADHD"
            result_color = Colors.WARNING
            recommendation = "Some ADHD traits are present. Monitor your symptoms."
        else:
            result = "High likelihood of ADHD"
            result_color = Colors.DANGER
            recommendation = "Consider consulting a healthcare professional."

        self.layout.clear_widgets()

        result_card = MDCard(
            size_hint=(1, None),
            height=dp(400),
            radius=[20],
            padding=dp(30),
            spacing=dp(20),
            orientation="vertical",
            md_bg_color=get_color_from_hex(Colors.SURFACE),
            pos_hint={"center_y": 0.5}
        )

        icon_label = MDIcon(
            icon="check-circle" if percent <= 30 else "alert-circle",
            font_size="64sp",
            theme_text_color="Custom",
            text_color=get_color_from_hex(result_color),
            halign="center"
        )

        percent_label = MDLabel(
            text=f"{percent}%",
            font_size="48sp",
            bold=True,
            halign="center",
            theme_text_color="Custom",
            text_color=get_color_from_hex(result_color)
        )

        result_label = MDLabel(
            text=result,
            font_size="20sp",
            bold=True,
            halign="center",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
        )

        recommendation_label = MDLabel(
            text=recommendation,
            font_size="14sp",
            halign="center",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
        )

        buttons_box = MDBoxLayout(spacing=dp(15), size_hint_y=None, height=dp(50))

        home_btn = MDFlatButton(
            text="Back to Home",
            on_release=lambda x: setattr(self.manager, "current", "home")
        )

        retake_btn = MDRaisedButton(
            text="Retake Test",
            on_release=lambda x: self.retake_test()
        )

        buttons_box.add_widget(home_btn)
        buttons_box.add_widget(retake_btn)

        result_card.add_widget(icon_label)
        result_card.add_widget(percent_label)
        result_card.add_widget(result_label)
        result_card.add_widget(CustomDivider())
        result_card.add_widget(recommendation_label)
        result_card.add_widget(buttons_box)

        self.layout.add_widget(result_card)

    def retake_test(self):
        self.answers = []
        self.current_q = 0
        self.layout.clear_widgets()
        self.__init__()
        self.manager.current = "adhd"


# ---------- ИНФОРМАЦИОННЫЙ ЭКРАН ----------
class InfoScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.full_text = """Dyslexia is the most common learning disability. It is characterized by difficulties with reading, spelling and decoding.

People with dyslexia may read slowly, confuse words, or need more time to process information. However, they are often very creative and think differently.

Dyslexia is not related to intelligence — many successful people have it."""

        self.is_playing = False
        self.original_text = self.full_text

        scroll = ScrollView()

        layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(20),
            size_hint_y=None,
            md_bg_color=get_color_from_hex(Colors.BACKGROUND)
        )
        layout.bind(minimum_height=layout.setter("height"))

        # Заголовок
        title_card = MDCard(
            radius=[20],
            padding=dp(20),
            md_bg_color=get_color_from_hex(Colors.PRIMARY),
            size_hint_y=None,
            height=dp(80)
        )

        title_card.add_widget(
            MDLabel(
                text="What is Dyslexia?",
                halign="center",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                font_size="28sp",
                bold=True
            )
        )

        # Карточка с текстом
        text_card = MDCard(
            radius=[20],
            padding=dp(20),
            md_bg_color=get_color_from_hex(Colors.SURFACE),
            size_hint_y=None
        )

        self.text_label = MDLabel(
            text=self.full_text,
            halign="left",
            font_size="16sp",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
        )

        text_card.add_widget(self.text_label)

        # Изображение
        image_card = MDCard(
            radius=[20],
            size_hint_y=None,
            height=dp(200)
        )

        image_card.add_widget(
            AsyncImage(
                source="https://barcelona.guttmann.com/sites/default/files/styles/article_image/public/2023-02/shutterstock_2174662661.jpg"
            )
        )

        # Кнопка прослушивания
        self.listen_btn = MDIconButton(
            icon="volume-high",
            pos_hint={"center_x": 0.5},
            theme_icon_color="Custom",
            icon_color=get_color_from_hex(Colors.PRIMARY),
            size_hint=(None, None),
            size=(dp(64), dp(64))
        )

        self.listen_btn.bind(on_release=self.on_listen)

        # Кнопка назад
        back_btn = MDRaisedButton(
            text="Back to Home",
            pos_hint={"center_x": 0.5},
            size_hint_x=0.5,
            on_release=lambda x: setattr(self.manager, "current", "home")
        )

        layout.add_widget(title_card)
        layout.add_widget(text_card)
        layout.add_widget(image_card)
        layout.add_widget(self.listen_btn)
        layout.add_widget(back_btn)

        scroll.add_widget(layout)
        self.add_widget(scroll)

    def on_listen(self, instance):
        if self.is_playing:
            toggle("")
            self.is_playing = False
            instance.icon = "volume-high"
        # Возвращаем исходный текст
            self.text_label.text = self.original_text
            self.text_label.markup = False
            return

        self.is_playing = True
        instance.icon = "pause"

        def on_end():
            self.is_playing = False
            instance.icon = "volume-high"
            self.text_label.text = self.original_text
            self.text_label.markup = False

        toggle(self.full_text, on_word=self.highlight_word, on_end=on_end)

    def highlight_word(self, word):
        words = self.full_text.split()
        new_text = []

        for w in words:
            clean_w = w.strip(".,!?")
            if clean_w == word.strip(".,!?"):
                new_text.append(f"[color={Colors.DANGER}]{w}[/color]")
            else:
                new_text.append(w)

        self.text_label.markup = True
        self.text_label.text = " ".join(new_text)


# ---------- ДОМАШНИЙ ЭКРАН ----------
class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main = MDBoxLayout(
            orientation="vertical",
            md_bg_color=get_color_from_hex(Colors.BACKGROUND)
        )

        scroll = ScrollView()
        content = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(20),
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter("height"))

        # Приветствие
        greeting = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(60)
        )

        greeting.add_widget(
            MDLabel(
                text="Hello! 👋",
                font_size="28sp",
                bold=True,
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
            )
        )

        content.add_widget(greeting)

        # Информационная карточка
        info_card = MDCard(
            size_hint=(1, None),
            height=dp(120),
            radius=[20],
            md_bg_color=get_color_from_hex(Colors.PRIMARY_LIGHT),
            ripple_behavior=True,
            padding=dp(20),
            spacing=dp(15)
        )

        info_box = MDBoxLayout(spacing=dp(15))

        info_icon = MDIcon(
            icon="book-open-page-variant",
            font_size="40sp",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )

        info_text_box = MDBoxLayout(orientation="vertical", spacing=dp(5))

        info_text_box.add_widget(
            MDLabel(
                text="What is dyslexia?",
                font_size="20sp",
                bold=True,
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            )
        )

        info_text_box.add_widget(
            MDLabel(
                text="Learn about symptoms and support",
                font_size="14sp",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 0.9)
            )
        )

        info_box.add_widget(info_icon)
        info_box.add_widget(info_text_box)
        info_card.add_widget(info_box)

        info_card.bind(on_release=lambda x: setattr(self.manager, "current", "info"))

        content.add_widget(info_card)

        # Заголовок тестов
        tests_title = MDLabel(
            text="Take a Test",
            font_size="22sp",
            bold=True,
            size_hint_y=None,
            height=dp(40),
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
        )

        content.add_widget(tests_title)

        # Карточки тестов
        tests_box = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(15),
            size_hint_y=None,
            height=dp(160)
        )

        tests_box.add_widget(
            TestCard(
                title="Dyslexia\nScreening",
                icon="book-open-outline",
                color_start=Colors.DYSLEXIA_GRADIENT_START,
                color_end=Colors.DYSLEXIA_GRADIENT_END,
                screen_name="dyslexia"
            )
        )

        tests_box.add_widget(
            TestCard(
                title="ADHD\nScreening",
                icon="brain",
                color_start=Colors.ADHD_GRADIENT_START,
                color_end=Colors.ADHD_GRADIENT_END,
                screen_name="adhd"
            )
        )

        content.add_widget(tests_box)

        # Видео
        video_title = MDLabel(
            text="Watch & Learn",
            font_size="22sp",
            bold=True,
            size_hint_y=None,
            height=dp(40),
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
        )

        content.add_widget(video_title)

        video = ClickableImage(
            source="https://img.youtube.com/vi/zafiGBrFkRM/0.jpg",
            size_hint_y=None,
            height=dp(200)
        )

        video.bind(on_release=lambda x: webbrowser.open("https://www.youtube.com/watch?v=zafiGBrFkRM"))

        content.add_widget(video)

        scroll.add_widget(content)
        main.add_widget(scroll)
        self.add_widget(main)



# ---------- ГЛАВНОЕ ПРИЛОЖЕНИЕ ----------
class MainApp(MDApp):
    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"

        Window.clearcolor = get_color_from_hex(Colors.BACKGROUND)

        root = MDBoxLayout(orientation="vertical")

        self.sm = MDScreenManager()
        self.sm.transition = FadeTransition(duration=0.3)

    # Добавляем все экраны
        self.sm.add_widget(HomeScreen(name="home"))
        self.sm.add_widget(GameScreen(name="games"))
        self.sm.add_widget(TaskScreen(name="tasks"))
        self.sm.add_widget(InfoScreen(name="info"))
        self.sm.add_widget(DyslexiaTestScreen(name="dyslexia"))
        self.sm.add_widget(ADHDTestScreen(name="adhd"))
        self.sm.add_widget(SentenceGameScreen(name="sentence"))
        self.sm.add_widget(WordGameScreen(name="word"))
        self.sm.add_widget(ColorGameScreen(name="color"))
        self.sm.add_widget(DirectionGameScreen(name="direction"))

        root.add_widget(self.sm)

    # Нижняя навигационная панель
        bottom_bar = MDBoxLayout(
            size_hint_y=None,
            height=dp(70),
            md_bg_color=get_color_from_hex(Colors.SURFACE),
            padding=[dp(10), 0],
            spacing=dp(10)
        )

        btn = MDIconButton(
            icon="checkbox-marked-outline",
            on_release=lambda x: switch_screen("tasks")
        )

        def switch_screen(screen_name):
            self.sm.current = screen_name

    # Создаем кнопки навигации
        nav_buttons = [
            ("home", "Home", "home"),
            ("checkbox-marked-outline", "Tasks", "tasks"),
            ("gamepad-variant", "Games", "games")
        ]

        for icon, text, screen_name in nav_buttons:  # Исправлено: теперь 3 элемента
            btn_box = MDBoxLayout(
                orientation="vertical",
                size_hint=(1, 1),
                padding=[0, dp(5)]
            )

            btn = MDIconButton(
                icon=icon,
                pos_hint={"center_x": 0.5},
                on_release=lambda x, s=screen_name: switch_screen(s)
            )

            label = MDLabel(
                text=text,
                halign="center",
                font_size="12sp",
                size_hint_y=None,
                height=dp(20),
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
            )

            btn_box.add_widget(btn)
            btn_box.add_widget(label)
            bottom_bar.add_widget(btn_box)

        root.add_widget(bottom_bar)

        return root


if __name__ == "__main__":
    MainApp().run()