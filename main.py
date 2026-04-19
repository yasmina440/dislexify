from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.uix.image import AsyncImage
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.button import ButtonBehavior
from kivy.uix.screenmanager import FadeTransition
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.pickers import MDDatePicker
from kivy.animation import Animation
from kivy.utils import get_color_from_hex
from kivy.storage.jsonstore import JsonStore
import webbrowser
from task_screen import TaskScreen
from chat_screen import ChatScreen
from responsive import Responsive

# Хранилище данных пользователя
user_store = JsonStore('user_data.json')

# Создаем свой разделитель
class CustomDivider(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(1)
        self.md_bg_color = get_color_from_hex("#D0E8F2")

from tts import toggle
from games import (
    GameScreen,
    SentenceGameScreen,
    WordGameScreen,
    ColorGameScreen,
    DirectionGameScreen
)


# ---------- СТИЛИ (СИНЕ-ГОЛУБАЯ ГАММА) ----------
class Colors:
    # Основные синие цвета
    PRIMARY = "#2196F3"  # Material Blue
    PRIMARY_LIGHT = "#64B5F6"  # Light Blue
    PRIMARY_DARK = "#1976D2"  # Dark Blue
    
    # Акцентные цвета
    SECONDARY = "#00BCD4"  # Cyan
    SECONDARY_LIGHT = "#4DD0E1"  # Light Cyan
    
    # Функциональные цвета
    SUCCESS = "#4CAF50"  # Green
    WARNING = "#FF9800"  # Orange
    DANGER = "#F44336"  # Red
    
    # Фоновые цвета
    BACKGROUND = "#F0F8FF"  # Alice Blue
    SURFACE = "#FFFFFF"
    
    # Текстовые цвета
    TEXT_PRIMARY = "#1A237E"  # Dark Blue
    TEXT_SECONDARY = "#546E7A"  # Blue Grey
    
    # Градиенты для тестов
    DYSLEXIA_GRADIENT_START = "#42A5F5"  # Blue
    DYSLEXIA_GRADIENT_END = "#1E88E5"  # Darker Blue
    
    ADHD_GRADIENT_START = "#26C6DA"  # Cyan
    ADHD_GRADIENT_END = "#00ACC1"  # Darker Cyan

    @staticmethod
    def get_background():
        return get_color_from_hex(Colors.BACKGROUND)
    
    @staticmethod
    def get_surface():
        return get_color_from_hex(Colors.SURFACE)


# ---------- ЭКРАН РЕГИСТРАЦИИ ----------
class RegistrationScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.layout = MDBoxLayout(
            orientation="vertical",
            padding=[dp(20), dp(40), dp(20), dp(20)],
            spacing=dp(20),
            md_bg_color=get_color_from_hex(Colors.BACKGROUND)
        )
        
        # Заголовок
        title_card = MDCard(
            radius=[24],
            padding=dp(20),
            md_bg_color=get_color_from_hex(Colors.PRIMARY),
            size_hint_y=None,
            height=dp(70),
            elevation=3
        )
        
        title_card.add_widget(
            MDLabel(
                text="Create Account",
                halign="center",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                font_size="24sp",
                bold=True
            )
        )
        
        self.layout.add_widget(title_card)
        
        # Карточка с формой
        form_card = MDCard(
            radius=[24],
            padding=dp(20),
            spacing=dp(15),
            orientation="vertical",
            md_bg_color=get_color_from_hex(Colors.SURFACE),
            elevation=2
        )
        
        # Поле для имени
        self.name_field = MDTextField(
            hint_text="Name",
            helper_text="Enter your first name",
            helper_text_mode="on_focus",
            mode="rectangle",
            size_hint_y=None,
            height=dp(60),
            font_size="16sp"
        )
        form_card.add_widget(self.name_field)
        
        # Поле для фамилии
        self.surname_field = MDTextField(
            hint_text="Surname",
            helper_text="Enter your last name",
            helper_text_mode="on_focus",
            mode="rectangle",
            size_hint_y=None,
            height=dp(60),
            font_size="16sp"
        )
        form_card.add_widget(self.surname_field)
        
        # Поле для возраста
        self.age_field = MDTextField(
            hint_text="Age",
            helper_text="Enter your age",
            helper_text_mode="on_focus",
            mode="rectangle",
            size_hint_y=None,
            height=dp(60),
            font_size="16sp",
            input_filter="int"
        )
        form_card.add_widget(self.age_field)
        
        # Поле для даты рождения
        birthday_box = MDBoxLayout(
            orientation="vertical",
            spacing=dp(5),
            size_hint_y=None,
            height=dp(80)
        )
        
        birthday_label = MDLabel(
            text="Birthday Date",
            font_size="14sp",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_SECONDARY),
            size_hint_y=None,
            height=dp(20)
        )
        birthday_box.add_widget(birthday_label)
        
        self.birthday_btn = MDFlatButton(
            text="Select Date",
            size_hint=(1, None),
            height=dp(50),
            md_bg_color=get_color_from_hex(Colors.PRIMARY_LIGHT),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_size="16sp",
            on_release=self.show_date_picker
        )
        birthday_box.add_widget(self.birthday_btn)
        
        self.selected_date_label = MDLabel(
            text="",
            font_size="12sp",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_SECONDARY),
            halign="center"
        )
        birthday_box.add_widget(self.selected_date_label)
        
        form_card.add_widget(birthday_box)
        
        self.layout.add_widget(form_card)
        
        # Кнопка регистрации
        register_btn = MDRaisedButton(
            text="Register",
            size_hint=(1, None),
            height=dp(50),
            md_bg_color=get_color_from_hex(Colors.PRIMARY),
            font_size="18sp",
            pos_hint={"center_x": 0.5},
            on_release=self.register_user
        )
        self.layout.add_widget(register_btn)
        
        # Кнопка входа (если уже есть аккаунт)
        login_btn = MDFlatButton(
            text="Already have an account? Login",
            size_hint=(1, None),
            height=dp(40),
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.PRIMARY),
            font_size="14sp",
            on_release=lambda x: setattr(self.manager, "current", "home")
        )
        self.layout.add_widget(login_btn)
        
        # Сообщение об ошибке/успехе
        self.message_label = MDLabel(
            text="",
            halign="center",
            font_size="14sp",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.DANGER),
            size_hint_y=None,
            height=dp(40)
        )
        self.layout.add_widget(self.message_label)
        
        self.add_widget(self.layout)
        
        # Переменная для хранения выбранной даты
        self.selected_date = None
    
    def show_date_picker(self, instance):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_selected)
        date_dialog.open()
    
    def on_date_selected(self, instance, value, date_range):
        self.selected_date = value
        self.selected_date_label.text = f"Selected: {value.strftime('%d.%m.%Y')}"
        self.birthday_btn.text = value.strftime('%d.%m.%Y')
    
    def register_user(self, instance):
        name = self.name_field.text.strip()
        surname = self.surname_field.text.strip()
        age = self.age_field.text.strip()
        
        # Проверка заполнения полей
        if not name:
            self.message_label.text = "Please enter your name"
            return
        
        if not surname:
            self.message_label.text = "Please enter your surname"
            return
        
        if not age:
            self.message_label.text = "Please enter your age"
            return
        
        if not self.selected_date:
            self.message_label.text = "Please select your birthday date"
            return
        
        # Проверка возраста
        try:
            age_int = int(age)
            if age_int < 1 or age_int > 120:
                self.message_label.text = "Please enter a valid age (1-120)"
                return
        except ValueError:
            self.message_label.text = "Please enter a valid age number"
            return
        
        # Сохраняем данные пользователя
        user_data = {
            'name': name,
            'surname': surname,
            'age': age_int,
            'birthday': self.selected_date.strftime('%Y-%m-%d'),
            'is_registered': True
        }
        
        user_store.put('user', **user_data)
        
        self.message_label.text_color = get_color_from_hex(Colors.SUCCESS)
        self.message_label.text = "Registration successful!"
        
        # Переход на домашний экран
        Clock.schedule_once(lambda dt: setattr(self.manager, "current", "home"), 1)


# ---------- КНОПКА С ИЗОБРАЖЕНИЕМ ----------
class ClickableImage(ButtonBehavior, AsyncImage):
    def __init__(self, **kwargs):
        kwargs.pop('keep_ratio', None)
        kwargs.pop('allow_stretch', None)
        super().__init__(**kwargs)


# ---------- КАРТОЧКА ТЕСТА ----------
class TestCard(MDCard):
    def __init__(self, title, icon, color_start, color_end, screen_name, duration="10-15 min", **kwargs):
        super().__init__(**kwargs)
        self.screen_name = screen_name
        self.size_hint = (1, 1)
        self.radius = [24]
        self.md_bg_color = get_color_from_hex(color_start)
        self.ripple_behavior = True
        self.padding = dp(16)
        self.spacing = dp(12)
        self.orientation = "vertical"
        self.elevation = 3

        # Иконка в круге
        icon_bg = MDBoxLayout(
            size_hint=(None, None),
            size=(dp(56), dp(56)),
            pos_hint={"center_x": 0.5},
            md_bg_color=(1, 1, 1, 0.2),
            radius=[dp(28)]
        )
        
        icon_label = MDIcon(
            icon=icon,
            font_size="32sp",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            halign="center",
            valign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        icon_bg.add_widget(icon_label)

        # Заголовок
        title_label = MDLabel(
            text=title,
            font_size="16sp",
            bold=True,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            halign="center"
        )

        # Длительность
        duration_label = MDLabel(
            text=duration,
            font_size="11sp",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.8),
            halign="center"
        )

        self.add_widget(icon_bg)
        self.add_widget(title_label)
        self.add_widget(duration_label)

        self.bind(on_release=lambda x: self.go_to_screen())

    def go_to_screen(self):
        app = MDApp.get_running_app()
        app.sm.current = self.screen_name


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

        self.layout = MDBoxLayout(
            orientation="vertical",
            padding=[dp(20), dp(40), dp(20), dp(20)],
            spacing=dp(25),
            md_bg_color=get_color_from_hex(Colors.BACKGROUND)
        )

        # Верхняя панель
        top_panel = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(70),
            spacing=dp(10)
        )

        header_box = MDBoxLayout(size_hint_y=None, height=dp(30))

        self.progress_label = MDLabel(
            text=f"Question 1 of {len(self.questions)}",
            font_size="14sp",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
        )

        back_btn = MDIconButton(
            icon="close",
            pos_hint={"center_y": 0.5},
            theme_icon_color="Custom",
            icon_color=get_color_from_hex(Colors.TEXT_SECONDARY),
            on_release=lambda x: setattr(self.manager, "current", "home")
        )

        header_box.add_widget(self.progress_label)
        header_box.add_widget(back_btn)

        self.progress_bar = MDProgressBar(
            value=0,
            max=len(self.questions),
            size_hint_y=None,
            height=dp(5),
            color=get_color_from_hex(Colors.PRIMARY)
        )

        top_panel.add_widget(header_box)
        top_panel.add_widget(self.progress_bar)

        # Карточка с вопросом
        question_card = MDCard(
            size_hint=(1, None),
            height=dp(180),
            radius=[24],
            padding=dp(20),
            md_bg_color=get_color_from_hex(Colors.SURFACE),
            elevation=2
        )

        self.question_label = MDLabel(
            text=self.questions[0],
            halign="center",
            valign="middle",
            font_size="16sp",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
        )

        question_card.add_widget(self.question_label)

        # Шкала ответов
        scale_box = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(130),
            spacing=dp(10)
        )

        scale_label = MDLabel(
            text="How often does this happen?",
            halign="center",
            font_size="13sp",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
        )

        buttons_box = MDBoxLayout(
            spacing=dp(8),
            size_hint_y=None,
            height=dp(80)
        )

        # Иконки для эмоций
        emotions = [
            ("emoticon-sad", "Never", Colors.DANGER),
            ("emoticon-neutral", "Rarely", Colors.WARNING),
            ("emoticon", "Sometimes", "#90A4AE"),
            ("emoticon-happy", "Often", Colors.PRIMARY_LIGHT),
            ("emoticon-excited", "Always", Colors.PRIMARY)
        ]

        for i, (icon_name, text, color) in enumerate(emotions):
            btn_card = MDCard(
                size_hint=(0.2, 1),
                radius=[18],
                md_bg_color=get_color_from_hex(color),
                ripple_behavior=True
            )

            btn_layout = MDBoxLayout(
                orientation="vertical",
                padding=dp(5),
                spacing=dp(3)
            )

            emoji_icon = MDIcon(
                icon=icon_name,
                font_size="28sp",
                halign="center",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            )

            text_label = MDLabel(
                text=text,
                font_size="9sp",
                halign="center",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            )

            btn_layout.add_widget(emoji_icon)
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
            result = "Low likelihood of dyslexia"
            result_color = Colors.SUCCESS
            recommendation = "Continue practicing reading and writing skills."
            icon_name = "emoticon-happy"
        elif percent <= 60:
            result = "Moderate signs of dyslexia"
            result_color = Colors.WARNING
            recommendation = "Consider additional screening and targeted exercises."
            icon_name = "emoticon-neutral"
        else:
            result = "High likelihood of dyslexia"
            result_color = Colors.DANGER
            recommendation = "We recommend consulting with a specialist."
            icon_name = "emoticon-sad"

        self.layout.clear_widgets()

        result_card = MDCard(
            size_hint=(1, None),
            height=dp(380),
            radius=[24],
            padding=dp(25),
            spacing=dp(15),
            orientation="vertical",
            md_bg_color=get_color_from_hex(Colors.SURFACE),
            pos_hint={"center_y": 0.5},
            elevation=3
        )

        icon_label = MDIcon(
            icon=icon_name,
            font_size="56sp",
            theme_text_color="Custom",
            text_color=get_color_from_hex(result_color),
            halign="center"
        )

        percent_label = MDLabel(
            text=f"{percent}%",
            font_size="42sp",
            bold=True,
            halign="center",
            theme_text_color="Custom",
            text_color=get_color_from_hex(result_color)
        )

        result_label = MDLabel(
            text=result,
            font_size="18sp",
            bold=True,
            halign="center",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
        )

        recommendation_label = MDLabel(
            text=recommendation,
            font_size="13sp",
            halign="center",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
        )

        buttons_box = MDBoxLayout(
            spacing=dp(12),
            size_hint_y=None,
            height=dp(45)
        )

        home_btn = MDFlatButton(
            text="Back to Home",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.PRIMARY),
            on_release=lambda x: setattr(self.manager, "current", "home")
        )

        retake_btn = MDRaisedButton(
            text="Retake Test",
            md_bg_color=get_color_from_hex(Colors.PRIMARY),
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
            spacing=dp(25),
            md_bg_color=get_color_from_hex(Colors.BACKGROUND)
        )

        top_panel = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(70),
            spacing=dp(10)
        )

        header_box = MDBoxLayout(size_hint_y=None, height=dp(30))

        self.progress_label = MDLabel(
            text=f"Question 1 of {len(self.questions)}",
            font_size="14sp",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
        )

        back_btn = MDIconButton(
            icon="close",
            theme_icon_color="Custom",
            icon_color=get_color_from_hex(Colors.TEXT_SECONDARY),
            on_release=lambda x: setattr(self.manager, "current", "home")
        )

        header_box.add_widget(self.progress_label)
        header_box.add_widget(back_btn)

        self.progress_bar = MDProgressBar(
            value=0,
            max=len(self.questions),
            size_hint_y=None,
            height=dp(5),
            color=get_color_from_hex(Colors.SECONDARY)
        )

        top_panel.add_widget(header_box)
        top_panel.add_widget(self.progress_bar)

        question_card = MDCard(
            size_hint=(1, None),
            height=dp(180),
            radius=[24],
            padding=dp(20),
            md_bg_color=get_color_from_hex(Colors.SURFACE),
            elevation=2
        )

        self.question_label = MDLabel(
            text=self.questions[0],
            halign="center",
            valign="middle",
            font_size="16sp",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
        )

        question_card.add_widget(self.question_label)

        scale_box = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(130),
            spacing=dp(10)
        )

        scale_label = MDLabel(
            text="How often does this happen?",
            halign="center",
            font_size="13sp",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
        )

        buttons_box = MDBoxLayout(spacing=dp(8), size_hint_y=None, height=dp(80))

        emotions = [
            ("emoticon-sad", "Never", Colors.DANGER),
            ("emoticon-neutral", "Rarely", Colors.WARNING),
            ("emoticon", "Sometimes", "#90A4AE"),
            ("emoticon-happy", "Often", Colors.SECONDARY_LIGHT),
            ("emoticon-excited", "Always", Colors.SECONDARY)
        ]

        for i, (icon_name, text, color) in enumerate(emotions):
            btn_card = MDCard(
                size_hint=(0.2, 1),
                radius=[18],
                md_bg_color=get_color_from_hex(color),
                ripple_behavior=True
            )

            btn_layout = MDBoxLayout(orientation="vertical", padding=dp(5), spacing=dp(3))

            emoji_icon = MDIcon(
                icon=icon_name,
                font_size="28sp",
                halign="center",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            )

            text_label = MDLabel(
                text=text,
                font_size="9sp",
                halign="center",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            )

            btn_layout.add_widget(emoji_icon)
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
            icon_name = "emoticon-happy"
        elif percent <= 60:
            result = "Moderate signs of ADHD"
            result_color = Colors.WARNING
            recommendation = "Some ADHD traits are present. Monitor your symptoms."
            icon_name = "emoticon-neutral"
        else:
            result = "High likelihood of ADHD"
            result_color = Colors.DANGER
            recommendation = "Consider consulting a healthcare professional."
            icon_name = "emoticon-sad"

        self.layout.clear_widgets()

        result_card = MDCard(
            size_hint=(1, None),
            height=dp(380),
            radius=[24],
            padding=dp(25),
            spacing=dp(15),
            orientation="vertical",
            md_bg_color=get_color_from_hex(Colors.SURFACE),
            pos_hint={"center_y": 0.5},
            elevation=3
        )

        icon_label = MDIcon(
            icon=icon_name,
            font_size="56sp",
            theme_text_color="Custom",
            text_color=get_color_from_hex(result_color),
            halign="center"
        )

        percent_label = MDLabel(
            text=f"{percent}%",
            font_size="42sp",
            bold=True,
            halign="center",
            theme_text_color="Custom",
            text_color=get_color_from_hex(result_color)
        )

        result_label = MDLabel(
            text=result,
            font_size="18sp",
            bold=True,
            halign="center",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
        )

        recommendation_label = MDLabel(
            text=recommendation,
            font_size="13sp",
            halign="center",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
        )

        buttons_box = MDBoxLayout(spacing=dp(12), size_hint_y=None, height=dp(45))

        home_btn = MDFlatButton(
            text="Back to Home",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.SECONDARY),
            on_release=lambda x: setattr(self.manager, "current", "home")
        )

        retake_btn = MDRaisedButton(
            text="Retake Test",
            md_bg_color=get_color_from_hex(Colors.SECONDARY),
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

        title_card = MDCard(
            radius=[24],
            padding=dp(20),
            md_bg_color=get_color_from_hex(Colors.PRIMARY),
            size_hint_y=None,
            height=dp(70),
            elevation=3
        )

        title_card.add_widget(
            MDLabel(
                text="What is Dyslexia?",
                halign="center",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                font_size="24sp",
                bold=True
            )
        )

        text_card = MDCard(
            radius=[24],
            padding=dp(20),
            md_bg_color=get_color_from_hex(Colors.SURFACE),
            size_hint_y=None,
            elevation=2
        )

        text_scroll = ScrollView(size_hint=(1, None), height=dp(220))
        
        self.text_label = MDLabel(
            text=self.full_text,
            halign="left",
            font_size="14sp",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_PRIMARY),
            size_hint_y=None
        )
        self.text_label.bind(texture_size=self.text_label.setter('size'))
        
        text_scroll.add_widget(self.text_label)
        text_card.add_widget(text_scroll)

        image_card = MDCard(
            radius=[24],
            size_hint_y=None,
            height=dp(180),
            elevation=2
        )

        image_card.add_widget(
            AsyncImage(
                source="https://barcelona.guttmann.com/sites/default/files/styles/article_image/public/2023-02/shutterstock_2174662661.jpg"
            )
        )

        self.listen_btn = MDIconButton(
            icon="volume-high",
            pos_hint={"center_x": 0.5},
            theme_icon_color="Custom",
            icon_color=get_color_from_hex(Colors.PRIMARY),
            size_hint=(None, None),
            size=(dp(56), dp(56))
        )

        self.listen_btn.bind(on_release=self.on_listen)

        back_btn = MDRaisedButton(
            text="Back to Home",
            pos_hint={"center_x": 0.5},
            size_hint_x=0.5,
            md_bg_color=get_color_from_hex(Colors.PRIMARY),
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
        
        Window.bind(on_resize=self.on_window_resize)
        
        self.build_ui()
    
    def on_window_resize(self, window, width, height):
        Clock.schedule_once(lambda dt: self.build_ui(), 0.1)
    
    def get_user_name(self):
        """Получить имя пользователя из хранилища"""
        try:
            if user_store.exists('user'):
                user_data = user_store.get('user')
                return user_data.get('name', '')
        except:
            pass
        return ''
    
    def build_ui(self):
        self.clear_widgets()
        
        main = MDBoxLayout(
            orientation="vertical",
            md_bg_color=get_color_from_hex(Colors.BACKGROUND)
        )
        
        # Верхняя панель с названием приложения
        header = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(70),
            padding=[dp(20), dp(12)],
            md_bg_color=get_color_from_hex(Colors.SURFACE),
            spacing=dp(10)
        )
        
        # Логотип и название
        logo_box = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint_x=0.7
        )
        
        # Логотип в круге
        logo_bg = MDBoxLayout(
            size_hint=(None, None),
            size=(dp(40), dp(40)),
            md_bg_color=get_color_from_hex(Colors.PRIMARY_LIGHT),
            radius=[dp(20)]
        )
        
        logo_icon = MDIcon(
            icon="brain",
            font_size="22sp",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        logo_bg.add_widget(logo_icon)
        
        app_title = MDLabel(
            text="DISLEXIFY",
            font_size="22sp",
            bold=True,
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.PRIMARY)
        )
        
        logo_box.add_widget(logo_bg)
        logo_box.add_widget(app_title)
        
        header.add_widget(logo_box)
        
        # Кнопка профиля/регистрации
        user_name = self.get_user_name()
        if user_name:
            profile_btn = MDIconButton(
                icon="account-circle",
                pos_hint={"center_y": 0.5},
                theme_icon_color="Custom",
                icon_color=get_color_from_hex(Colors.PRIMARY),
                on_release=lambda x: self.show_user_profile()
            )
        else:
            profile_btn = MDIconButton(
                icon="login",
                pos_hint={"center_y": 0.5},
                theme_icon_color="Custom",
                icon_color=get_color_from_hex(Colors.PRIMARY),
                on_release=lambda x: setattr(self.manager, "current", "registration")
            )
        header.add_widget(profile_btn)
        
        main.add_widget(header)
        
        scroll = ScrollView()
        content = MDBoxLayout(
            orientation="vertical",
            padding=dp(Responsive.get_padding(18)),
            spacing=dp(Responsive.get_padding(18)),
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter("height"))
        
        # Приветствие с именем пользователя
        greeting_box = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(40)
        )
        
        user_name = self.get_user_name()
        if user_name:
            greeting_text = f"Hello, {user_name}! "
        else:
            greeting_text = "Hello! "
        
        greeting = MDLabel(
            text=greeting_text,
            font_size=f"{Responsive.get_font_size(26)}sp",
            bold=True,
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
        )
        greeting_box.add_widget(greeting)
        content.add_widget(greeting_box)
        
        # Если пользователь не зарегистрирован, показываем карточку с предложением
        if not user_name:
            register_card = MDCard(
                size_hint=(1, None),
                height=dp(80),
                radius=[24],
                md_bg_color=get_color_from_hex(Colors.PRIMARY_LIGHT),
                ripple_behavior=True,
                padding=dp(18),
                spacing=dp(12),
                elevation=2
            )
            
            register_box = MDBoxLayout(spacing=dp(12))
            
            register_icon = MDIcon(
                icon="account-plus",
                font_size="28sp",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            )
            
            register_text_box = MDBoxLayout(orientation="vertical", spacing=dp(3))
            
            register_text_box.add_widget(
                MDLabel(
                    text="Create your profile",
                    font_size="16sp",
                    bold=True,
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1)
                )
            )
            
            register_text_box.add_widget(
                MDLabel(
                    text="Get personalized recommendations",
                    font_size="12sp",
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 0.9)
                )
            )
            
            register_box.add_widget(register_icon)
            register_box.add_widget(register_text_box)
            register_card.add_widget(register_box)
            
            register_card.bind(on_release=lambda x: setattr(self.manager, "current", "registration"))
            content.add_widget(register_card)
        
        # Информационная карточка
        info_card = MDCard(
            size_hint=(1, None),
            height=dp(Responsive.get_card_height(95)),
            radius=[24],
            md_bg_color=get_color_from_hex(Colors.PRIMARY),
            ripple_behavior=True,
            padding=dp(Responsive.get_padding(18)),
            spacing=dp(12),
            elevation=3
        )
        
        info_box = MDBoxLayout(spacing=dp(12))
        
        info_icon_bg = MDBoxLayout(
            size_hint=(None, None),
            size=(dp(48), dp(48)),
            md_bg_color=(1, 1, 1, 0.2),
            radius=[dp(24)]
        )
        
        info_icon = MDIcon(
            icon="book-open-page-variant",
            font_size="28sp",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        info_icon_bg.add_widget(info_icon)
        
        info_text_box = MDBoxLayout(orientation="vertical", spacing=dp(3))
        
        info_text_box.add_widget(
            MDLabel(
                text="What is dyslexia?",
                font_size=f"{Responsive.get_font_size(16)}sp",
                bold=True,
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            )
        )
        
        info_text_box.add_widget(
            MDLabel(
                text="Learn about symptoms and support",
                font_size=f"{Responsive.get_font_size(12)}sp",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 0.9)
            )
        )
        
        info_box.add_widget(info_icon_bg)
        info_box.add_widget(info_text_box)
        info_card.add_widget(info_box)
        
        info_card.bind(on_release=lambda x: setattr(self.manager, "current", "info"))
        content.add_widget(info_card)
        
        # Заголовок тестов
        tests_title = MDLabel(
            text="Take a Test",
            font_size=f"{Responsive.get_font_size(20)}sp",
            bold=True,
            size_hint_y=None,
            height=dp(Responsive.get_font_size(32)),
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
        )
        content.add_widget(tests_title)
        
        # Карточки тестов - ВСЕГДА ГОРИЗОНТАЛЬНО
        tests_box = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(12),
            size_hint_y=None,
            height=dp(155)
        )
        
        # Тест на дислексию
        dyslexia_card = TestCard(
            title="Dyslexia\nScreening",
            icon="book-open-outline",
            color_start=Colors.DYSLEXIA_GRADIENT_START,
            color_end=Colors.DYSLEXIA_GRADIENT_END,
            screen_name="dyslexia"
        )
        
        # Тест на ADHD
        adhd_card = TestCard(
            title="ADHD\nScreening",
            icon="brain",
            color_start=Colors.ADHD_GRADIENT_START,
            color_end=Colors.ADHD_GRADIENT_END,
            screen_name="adhd"
        )
        
        tests_box.add_widget(dyslexia_card)
        tests_box.add_widget(adhd_card)
        
        content.add_widget(tests_box)
        
        # Видео
        video_title = MDLabel(
            text="Watch & Learn",
            font_size=f"{Responsive.get_font_size(20)}sp",
            bold=True,
            size_hint_y=None,
            height=dp(Responsive.get_font_size(32)),
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
        )
        content.add_widget(video_title)
        
        video_card = MDCard(
            size_hint=(1, None),
            height=dp(Responsive.get_card_height(180)),
            radius=[24],
            elevation=3
        )
        
        video = ClickableImage(
            source="https://img.youtube.com/vi/zafiGBrFkRM/0.jpg",
            size_hint=(1, 1)
        )
        
        video_card.add_widget(video)
        
        video.bind(on_release=lambda x: webbrowser.open("https://www.youtube.com/watch?v=zafiGBrFkRM"))
        content.add_widget(video_card)
        
        # Отступ снизу
        content.add_widget(MDBoxLayout(size_hint_y=None, height=dp(10)))
        
        scroll.add_widget(content)
        main.add_widget(scroll)
        self.add_widget(main)
    
    def show_user_profile(self):
        """Показать профиль пользователя"""
        try:
            if user_store.exists('user'):
                user_data = user_store.get('user')
                
                # Создаем диалог с информацией о пользователе
                from kivymd.uix.dialog import MDDialog
                from kivymd.uix.button import MDFlatButton
                
                content = MDBoxLayout(
                    orientation="vertical",
                    spacing=dp(10),
                    padding=dp(20),
                    size_hint_y=None,
                    height=dp(200)
                )
                
                content.add_widget(MDLabel(
                    text=f"Name: {user_data.get('name', '')}",
                    font_size="16sp",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
                ))
                
                content.add_widget(MDLabel(
                    text=f"Surname: {user_data.get('surname', '')}",
                    font_size="16sp",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
                ))
                
                content.add_widget(MDLabel(
                    text=f"Age: {user_data.get('age', '')}",
                    font_size="16sp",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
                ))
                
                content.add_widget(MDLabel(
                    text=f"Birthday: {user_data.get('birthday', '')}",
                    font_size="16sp",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
                ))
                
                dialog = MDDialog(
                    title="Your Profile",
                    type="custom",
                    content_cls=content,
                    buttons=[
                        MDFlatButton(
                            text="CLOSE",
                            on_release=lambda x: dialog.dismiss()
                        ),
                        MDRaisedButton(
                            text="LOGOUT",
                            md_bg_color=get_color_from_hex(Colors.DANGER),
                            on_release=lambda x: self.logout(dialog)
                        ),
                    ],
                )
                dialog.open()
        except:
            pass
    
    def logout(self, dialog):
        """Выйти из аккаунта"""
        try:
            user_store.delete('user')
        except:
            pass
        dialog.dismiss()
        self.build_ui()


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
        self.sm.add_widget(RegistrationScreen(name="registration"))
        self.sm.add_widget(HomeScreen(name="home"))
        self.sm.add_widget(GameScreen(name="games"))
        self.sm.add_widget(TaskScreen(name="tasks"))
        self.sm.add_widget(ChatScreen(name="chat"))
        self.sm.add_widget(InfoScreen(name="info"))
        self.sm.add_widget(DyslexiaTestScreen(name="dyslexia"))
        self.sm.add_widget(ADHDTestScreen(name="adhd"))
        self.sm.add_widget(SentenceGameScreen(name="sentence"))
        self.sm.add_widget(WordGameScreen(name="word"))
        self.sm.add_widget(ColorGameScreen(name="color"))
        self.sm.add_widget(DirectionGameScreen(name="direction"))

        # Проверяем, зарегистрирован ли пользователь
        try:
            if not user_store.exists('user'):
                self.sm.current = "registration"
            else:
                self.sm.current = "home"
        except:
            self.sm.current = "registration"

        root.add_widget(self.sm)

        # Нижняя навигационная панель
        bottom_bar = MDBoxLayout(
            size_hint_y=None,
            height=dp(65),
            md_bg_color=get_color_from_hex(Colors.SURFACE),
            padding=[dp(10), 0],
            spacing=dp(10)
        )

        def switch_screen(screen_name):
            self.sm.current = screen_name

        nav_buttons = [
            ("home", "Home", "home"),
            ("checkbox-marked-outline", "Tasks", "tasks"),
            ("gamepad-variant", "Games", "games"),
            ("head-cog", "AI", "chat"),
        ]

        for icon, text, screen_name in nav_buttons:
            btn_box = MDBoxLayout(
                orientation="vertical",
                size_hint=(1, 1),
                padding=[0, dp(5)]
            )

            btn = MDIconButton(
                icon=icon,
                pos_hint={"center_x": 0.5},
                theme_icon_color="Custom",
                icon_color=get_color_from_hex(Colors.TEXT_SECONDARY),
                on_release=lambda x, s=screen_name: switch_screen(s)
            )

            label = MDLabel(
                text=text,
                halign="center",
                font_size="11sp",
                size_hint_y=None,
                height=dp(18),
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