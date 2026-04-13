from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDIconButton
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.scrollview import ScrollView
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.chip import MDChip
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.properties import (
    StringProperty, BooleanProperty, NumericProperty
)
from kivy.uix.widget import Widget
from functools import partial


class Colors:
    """Цветовая схема"""
    PRIMARY = "#4A90E2"
    PRIMARY_DARK = "#357ABD"
    PRIMARY_LIGHT = "#7FB0F0"
    SUCCESS = "#51CF66"
    DANGER = "#FF6B6B"
    WARNING = "#FFD43B"
    SURFACE = "#FFFFFF"
    SURFACE_VARIANT = "#F8F9FA"
    BACKGROUND = "#F0F2F5"
    TEXT_PRIMARY = "#212529"
    TEXT_SECONDARY = "#6C757D"
    TEXT_HINT = "#A0A0A0"
    DIVIDER = "#E0E0E0"


class ReadingProgressIndicator(MDBoxLayout):
    """Индикатор прогресса чтения"""
    max_pages = NumericProperty(10)
    current_page = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = dp(5)
        self.padding = [dp(10), dp(5)]
        self.size_hint_y = None
        self.height = dp(40)
        
        self.progress_label = MDLabel(
            text=f"Page {self.current_page}/{self.max_pages}",
            font_size="12sp",
            halign="center",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
        )
        
        self.progress_bar = MDProgressBar(
            value=0,
            max=self.max_pages,
            size_hint_y=None,
            height=dp(4),
            color=get_color_from_hex(Colors.PRIMARY),
            back_color=get_color_from_hex(Colors.DIVIDER)
        )
        
        self.add_widget(self.progress_label)
        self.add_widget(self.progress_bar)
        
        self.bind(current_page=self.update_progress)
        self.bind(max_pages=self.update_progress)
    
    def update_progress(self, *args):
        self.progress_bar.value = self.current_page
        self.progress_bar.max = self.max_pages
        self.progress_label.text = f"Page {self.current_page}/{self.max_pages}"


class AchievementBadge(MDCard):
    """Бейдж достижения"""
    title = StringProperty("")
    icon = StringProperty("trophy")
    is_unlocked = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(80), dp(100))
        self.radius = [15]
        self.padding = dp(10)
        self.md_bg_color = get_color_from_hex(Colors.SURFACE_VARIANT if not self.is_unlocked else Colors.SUCCESS)
        self.orientation = "vertical"
        self.spacing = dp(5)
        
        icon_layout = MDRelativeLayout(size_hint_y=0.6)
        icon = MDIcon(
            icon=self.icon,
            font_size="30sp",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_HINT if not self.is_unlocked else Colors.SURFACE),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        icon_layout.add_widget(icon)
        
        title_label = MDLabel(
            text=self.title,
            font_size="10sp",
            halign="center",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_HINT if not self.is_unlocked else Colors.SURFACE),
            size_hint_y=0.3
        )
        
        self.add_widget(icon_layout)
        self.add_widget(title_label)


class ReadingStatsCard(MDCard):
    """Карточка статистики чтения"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(180)
        self.radius = [20]
        self.padding = dp(20)
        self.spacing = dp(15)
        self.md_bg_color = get_color_from_hex(Colors.SURFACE)
        self.orientation = "vertical"
        
        title = MDLabel(
            text="Reading Statistics",
            font_size="18sp",
            bold=True,
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
        )
        self.add_widget(title)
        
        stats_grid = MDGridLayout(
            cols=3,
            spacing=dp(15),
            size_hint_y=0.8
        )
        
        stats = [
            {"icon": "book-open-variant", "value": "12", "label": "Books Read"},
            {"icon": "clock-outline", "value": "45m", "label": "Total Time"},
            {"icon": "star", "value": "850", "label": "Points"}
        ]
        
        for stat in stats:
            stat_box = MDBoxLayout(
                orientation="vertical",
                spacing=dp(5),
                md_bg_color=get_color_from_hex(Colors.SURFACE_VARIANT),
                radius=[15],
                padding=[dp(10), dp(15)]
            )
            
            icon = MDIcon(
                icon=stat["icon"],
                font_size="24sp",
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.PRIMARY)
            )
            
            value = MDLabel(
                text=stat["value"],
                font_size="20sp",
                bold=True,
                halign="center",
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
            )
            
            label = MDLabel(
                text=stat["label"],
                font_size="11sp",
                halign="center",
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
            )
            
            stat_box.add_widget(icon)
            stat_box.add_widget(value)
            stat_box.add_widget(label)
            stats_grid.add_widget(stat_box)
        
        self.add_widget(stats_grid)


class TaskScreen(MDScreen):
    """Улучшенный экран заданий"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.state = "menu"
        self.time = 0
        self.font_size = 18
        self.line_spacing = 1.5
        self.timer_event = None
        self.user_points = 850
        self.user_level = 3
        self.current_page = 1
        self.total_pages = 1
        
        # Данные книг
        self.books_data = {
            "Being a good classmate": {
                "level": "Level 3",
                "category": "School Life",
                "author": "British Council",
                "description": "Learn how to be a good classmate.",
                "estimated_time": "5 min",
                "pages": [
                    "Good classmates are kind and helpful. They share things and help each other.",
                    "Being a good classmate makes school better.",
                    "They say kind words and include everyone in games."
                ],
                "text": "Good classmates are kind and helpful. They share things and help each other. Being a good classmate makes school better. They say kind words and include everyone in games.",
                "questions": [
                    {
                        "q": "Good classmates are rude.",
                        "type": "tf",
                        "answer": False
                    },
                    {
                        "q": "What should a good classmate do?",
                        "type": "mc",
                        "options": ["Be rude", "Help others", "Ignore others"],
                        "answer": "Help others"
                    }
                ]
            },
            "School trip": {
                "level": "Level 2",
                "category": "Adventure",
                "author": "British Council",
                "description": "Join a fun school trip to the zoo.",
                "estimated_time": "3 min",
                "pages": [
                    "The class went on a trip to the zoo. They saw lions and tigers.",
                    "Everyone was excited. They had a picnic lunch."
                ],
                "text": "The class went on a trip to the zoo. They saw lions and tigers. Everyone was excited. They had a picnic lunch.",
                "questions": [
                    {
                        "q": "They went to a museum.",
                        "type": "tf",
                        "answer": False
                    },
                    {
                        "q": "What did they see at the zoo?",
                        "type": "mc",
                        "options": ["Fish", "Lions and tigers", "Birds"],
                        "answer": "Lions and tigers"
                    }
                ]
            },
            "The Mystery of the Missing Homework": {
                "level": "Level 4",
                "category": "Mystery",
                "author": "British Council",
                "description": "Solve the mystery of the missing homework.",
                "estimated_time": "7 min",
                "pages": [
                    "Tom couldn't find his homework anywhere. He had done it last night, but now it was gone!",
                    "He searched his bag, his desk, and even asked his mom. No one had seen it.",
                    "At school, his friend Mia noticed Tom was worried. 'What's wrong?' she asked.",
                    "They found the homework in his sister's toy box."
                ],
                "text": "Tom couldn't find his homework anywhere. He had done it last night, but now it was gone! He searched his bag, his desk, and even asked his mom. No one had seen it. At school, his friend Mia noticed Tom was worried. They found the homework in his sister's toy box.",
                "questions": [
                    {
                        "q": "What did Tom lose?",
                        "type": "mc",
                        "options": ["His book", "His homework", "His lunch"],
                        "answer": "His homework"
                    },
                    {
                        "q": "Who helped Tom?",
                        "type": "mc",
                        "options": ["His mom", "His friend Mia", "His teacher"],
                        "answer": "His friend Mia"
                    }
                ]
            }
        }
        
        self.load_user_data()
        self.build_menu()
    
    def load_user_data(self):
        """Загрузить данные пользователя"""
        self.user_stats = {
            "total_books_read": 12,
            "total_time": 45,
            "points": 850,
            "level": 3
        }
    
    def build_menu(self):
        """Построить главное меню"""
        self.clear_widgets()
        self.state = "menu"
        
        main_layout = MDBoxLayout(
            orientation="vertical",
            md_bg_color=get_color_from_hex(Colors.BACKGROUND)
        )
        
        # Шапка
        header = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(80),
            padding=[dp(20), dp(10)],
            md_bg_color=get_color_from_hex(Colors.PRIMARY)
        )
        
        header.add_widget(
            MDLabel(
                text="Reading Practice",
                font_size="24sp",
                bold=True,
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            )
        )
        
        main_layout.add_widget(header)
        
        # Скролл
        scroll = ScrollView(bar_width=dp(4))
        
        content = MDBoxLayout(
            orientation="vertical",
            padding=[dp(20), dp(10)],
            spacing=dp(20),
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter("height"))
        
        # Приветственная карточка
        welcome_card = MDCard(
            size_hint=(1, None),
            height=dp(100),
            radius=[25],
            padding=dp(20),
            md_bg_color=get_color_from_hex(Colors.SURFACE),
            orientation="vertical",
            spacing=dp(10)
        )
        
        welcome_card.add_widget(
            MDLabel(
                text="Continue Your Reading Journey! 📚",
                font_size="20sp",
                bold=True,
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
            )
        )
        
        welcome_card.add_widget(
            MDLabel(
                text=f"You've read {self.user_stats['total_books_read']} books this month!",
                font_size="14sp",
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
            )
        )
        
        content.add_widget(welcome_card)
        
        # Статистика
        stats_card = ReadingStatsCard()
        content.add_widget(stats_card)
        
        # Достижения
        achievements_section = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(140)
        )
        
        achievements_section.add_widget(
            MDLabel(
                text="Recent Achievements",
                font_size="18sp",
                bold=True,
                size_hint_y=None,
                height=dp(30),
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
            )
        )
        
        achievements_scroll = ScrollView(
            do_scroll_x=True,
            do_scroll_y=False,
            size_hint_y=None,
            height=dp(100)
        )
        
        achievements_box = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            padding=[0, dp(5)],
            size_hint_x=None
        )
        achievements_box.bind(minimum_width=achievements_box.setter("width"))
        
        sample_achievements = [
            {"title": "First Book", "icon": "book", "unlocked": True},
            {"title": "Perfect Score", "icon": "trophy", "unlocked": True},
            {"title": "7 Day Streak", "icon": "fire", "unlocked": True},
            {"title": "Speed Reader", "icon": "clock-fast", "unlocked": False}
        ]
        
        for achievement in sample_achievements:
            badge = AchievementBadge(
                title=achievement["title"],
                icon=achievement["icon"],
                is_unlocked=achievement["unlocked"]
            )
            achievements_box.add_widget(badge)
        
        achievements_scroll.add_widget(achievements_box)
        achievements_section.add_widget(achievements_scroll)
        content.add_widget(achievements_section)
        
        # Заголовок книг
        content.add_widget(
            MDLabel(
                text="Available Stories",
                font_size="20sp",
                bold=True,
                size_hint_y=None,
                height=dp(40),
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
            )
        )
        
        # Карточки книг
        for book_name, book_data in self.books_data.items():
            card = MDCard(
                size_hint=(1, None),
                height=dp(120),
                radius=[20],
                padding=dp(15),
                spacing=dp(15),
                md_bg_color=get_color_from_hex(Colors.SURFACE),
                ripple_behavior=True
            )
            
            # Иконка книги
            icon_box = MDBoxLayout(
                size_hint=(None, 1),
                width=dp(70),
                md_bg_color=get_color_from_hex(Colors.PRIMARY_LIGHT),
                radius=[15]
            )
            
            icon_box.add_widget(
                MDIcon(
                    icon="book-open-variant",
                    font_size="40sp",
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1),
                    pos_hint={"center_x": 0.5, "center_y": 0.5}
                )
            )
            
            # Информация
            info_box = MDBoxLayout(
                orientation="vertical",
                spacing=dp(5)
            )
            
            info_box.add_widget(
                MDChip(
                    text=book_data.get("category", "General"),
                    size_hint=(None, None),
                    height=dp(25),
                    width=dp(80),
                    md_bg_color=get_color_from_hex(Colors.PRIMARY_LIGHT),
                    text_color=(1, 1, 1, 1)
                )
            )
            
            info_box.add_widget(
                MDLabel(
                    text=book_name,
                    font_size="16sp",
                    bold=True,
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
                )
            )
            
            info_box.add_widget(
                MDLabel(
                    text=book_data.get("level", "Level 1"),
                    font_size="12sp",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
                )
            )
            
            card.add_widget(icon_box)
            card.add_widget(info_box)
            
            card.bind(on_release=lambda x, b=book_name: self.open_book(b))
            content.add_widget(card)
        
        content.add_widget(Widget(size_hint_y=None, height=dp(20)))
        
        scroll.add_widget(content)
        main_layout.add_widget(scroll)
        
        # Кнопка назад
        back_btn = MDBoxLayout(
            size_hint_y=None,
            height=dp(70),
            padding=[dp(20), dp(10)]
        )
        
        back_btn.add_widget(
            MDFlatButton(
                text="Back to Home",
                on_release=lambda x: setattr(self.manager, "current", "home") if self.manager else None
            )
        )
        
        main_layout.add_widget(back_btn)
        
        self.add_widget(main_layout)
    
    def open_book(self, book):
        """Открыть книгу"""
        self.clear_widgets()
        self.state = "reading"
        self.time = 0
        self.current_book = book
        self.current_page = 1
        
        book_data = self.books_data[book]
        self.text = book_data["text"]
        self.questions = book_data["questions"]
        self.pages = book_data.get("pages", [self.text])
        self.total_pages = len(self.pages)
        
        main = MDBoxLayout(
            orientation="vertical",
            md_bg_color=get_color_from_hex(Colors.BACKGROUND)
        )
        
        # Верхняя панель
        top_bar = MDBoxLayout(
            size_hint_y=None,
            height=dp(60),
            padding=[dp(15), dp(5)],
            spacing=dp(10),
            md_bg_color=get_color_from_hex(Colors.SURFACE)
        )
        
        back_btn = MDIconButton(
            icon="arrow-left",
            on_release=lambda x: self.build_menu()
        )
        
        book_info = MDBoxLayout(
            orientation="vertical",
            spacing=dp(2),
            size_hint_x=0.5
        )
        
        book_info.add_widget(
            MDLabel(
                text=book,
                font_size="16sp",
                bold=True,
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
            )
        )
        
        self.timer_label = MDLabel(
            text="00:00",
            halign="right",
            size_hint_x=0.3,
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
        )
        
        top_bar.add_widget(back_btn)
        top_bar.add_widget(book_info)
        top_bar.add_widget(self.timer_label)
        
        main.add_widget(top_bar)
        
        # Прогресс
        self.reading_progress = ReadingProgressIndicator(
            current_page=self.current_page,
            max_pages=self.total_pages
        )
        main.add_widget(self.reading_progress)
        
        # Область чтения
        reading_area = MDBoxLayout(
            orientation="vertical",
            padding=[dp(20), dp(10)]
        )
        
        self.text_scroll = ScrollView(bar_width=dp(4))
        
        self.text_container = MDBoxLayout(
            orientation="vertical",
            spacing=dp(15),
            size_hint_y=None,
            padding=[0, 0, dp(10), 0]
        )
        self.text_container.bind(minimum_height=self.text_container.setter("height"))
        
        self.display_current_page()
        
        self.text_scroll.add_widget(self.text_container)
        reading_area.add_widget(self.text_scroll)
        
        # Навигация по страницам
        nav_box = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(50),
            padding=[dp(20), dp(5)],
            spacing=dp(10)
        )
        
        prev_btn = MDIconButton(
            icon="chevron-left",
            on_release=self.previous_page,
            disabled=self.current_page == 1
        )
        
        self.page_indicator = MDLabel(
            text=f"{self.current_page}/{self.total_pages}",
            halign="center",
            size_hint_x=0.6
        )
        
        next_btn = MDIconButton(
            icon="chevron-right",
            on_release=self.next_page,
            disabled=self.current_page == self.total_pages
        )
        
        nav_box.add_widget(prev_btn)
        nav_box.add_widget(self.page_indicator)
        nav_box.add_widget(next_btn)
        
        reading_area.add_widget(nav_box)
        main.add_widget(reading_area)
        
        # Кнопка продолжить
        actions_bar = MDBoxLayout(
            size_hint_y=None,
            height=dp(70),
            padding=[dp(20), dp(10)],
            spacing=dp(10)
        )
        
        continue_btn = MDRaisedButton(
            text="Continue to Questions",
            on_release=self.open_questions
        )
        
        actions_bar.add_widget(continue_btn)
        main.add_widget(actions_bar)
        
        self.add_widget(main)
        
        if self.timer_event:
            Clock.unschedule(self.timer_event)
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)
    
    def display_current_page(self):
        """Отобразить текущую страницу"""
        self.text_container.clear_widgets()
        
        if self.current_page <= len(self.pages):
            page_text = self.pages[self.current_page - 1]
            
            text_label = MDLabel(
                text=page_text,
                font_size=str(self.font_size) + "sp",
                line_height=self.line_spacing,
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_PRIMARY),
                size_hint_y=None,
                halign="left",
                valign="top"
            )
            text_label.bind(texture_size=text_label.setter("size"))
            
            self.text_container.add_widget(text_label)
            self.reading_progress.current_page = self.current_page
    
    def previous_page(self, instance):
        """Предыдущая страница"""
        if self.current_page > 1:
            self.current_page -= 1
            self.display_current_page()
            self.page_indicator.text = f"{self.current_page}/{self.total_pages}"
    
    def next_page(self, instance):
        """Следующая страница"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.display_current_page()
            self.page_indicator.text = f"{self.current_page}/{self.total_pages}"
    
    def update_timer(self, dt):
        """Обновить таймер"""
        self.time += 1
        m = self.time // 60
        s = self.time % 60
        self.timer_label.text = f"{m:02d}:{s:02d}"
    
    def open_questions(self, instance):
        """Открыть вопросы"""
        if self.timer_event:
            Clock.unschedule(self.timer_event)
            self.timer_event = None
        
        self.clear_widgets()
        self.state = "questions"
        
        main = MDBoxLayout(
            orientation="vertical",
            md_bg_color=get_color_from_hex(Colors.BACKGROUND)
        )
        
        header = MDBoxLayout(
            size_hint_y=None,
            height=dp(70),
            padding=[dp(20), dp(15)],
            md_bg_color=get_color_from_hex(Colors.PRIMARY)
        )
        
        header.add_widget(
            MDLabel(
                text="Check Your Understanding",
                font_size="24sp",
                bold=True,
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            )
        )
        
        main.add_widget(header)
        
        scroll = ScrollView()
        content = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(20),
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter("height"))
        
        self.question_widgets = []
        
        for i, q in enumerate(self.questions):
            q_card = MDCard(
                size_hint=(1, None),
                height=dp(150 if q["type"] == "mc" else 120),
                radius=[20],
                padding=dp(20),
                spacing=dp(10),
                orientation="vertical",
                md_bg_color=get_color_from_hex(Colors.SURFACE)
            )
            
            q_card.add_widget(
                MDLabel(
                    text=f"Question {i + 1}",
                    font_size="14sp",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
                )
            )
            
            q_card.add_widget(
                MDLabel(
                    text=q["q"],
                    font_size="16sp",
                    bold=True,
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
                )
            )
            
            if q["type"] == "tf":
                tf_box = MDBoxLayout(spacing=dp(20), size_hint_y=None, height=dp(40))
                
                true_box = MDBoxLayout(spacing=dp(5), size_hint_x=0.5)
                true_cb = MDCheckbox(group=f"q{i}", size_hint=(None, None), size=(dp(30), dp(30)))
                true_box.add_widget(true_cb)
                true_box.add_widget(MDLabel(text="True"))
                
                false_box = MDBoxLayout(spacing=dp(5), size_hint_x=0.5)
                false_cb = MDCheckbox(group=f"q{i}", size_hint=(None, None), size=(dp(30), dp(30)))
                false_box.add_widget(false_cb)
                false_box.add_widget(MDLabel(text="False"))
                
                tf_box.add_widget(true_box)
                tf_box.add_widget(false_box)
                q_card.add_widget(tf_box)
                
                self.question_widgets.append({
                    "type": "tf",
                    "question": q,
                    "widgets": [true_cb, false_cb]
                })
            
            else:
                dropdown_btn = MDFlatButton(
                    text="Choose an answer",
                    size_hint_y=None,
                    height=dp(40)
                )
                
                # Создаем меню заранее
                menu_items = []
                for opt in q["options"]:
                    menu_items.append({
                        "text": opt,
                        "on_release": lambda x=opt, btn=dropdown_btn: setattr(btn, 'text', x)
                    })
                
                menu = MDDropdownMenu(
                    caller=dropdown_btn,
                    items=menu_items,
                    width_mult=4
                )
                
                # Исправленная привязка - используем lambda без аргументов
                dropdown_btn.bind(on_release=lambda x, m=menu: m.open())
                
                q_card.add_widget(dropdown_btn)
                
                self.question_widgets.append({
                    "type": "mc",
                    "question": q,
                    "widgets": [dropdown_btn]
                })
            
            content.add_widget(q_card)
        
        scroll.add_widget(content)
        main.add_widget(scroll)
        
        submit_btn = MDBoxLayout(
            size_hint_y=None,
            height=dp(80),
            padding=[dp(20), dp(15)]
        )
        
        submit_btn.add_widget(
            MDRaisedButton(
                text="Submit Answers",
                font_size="16sp",
                on_release=self.show_results
            )
        )
        
        main.add_widget(submit_btn)
        
        self.add_widget(main)
    
    def show_results(self, instance):
        """Показать результаты"""
        self.clear_widgets()
        self.state = "results"
        
        score = 0
        total = len(self.questions)
        
        for widget_data in self.question_widgets:
            q = widget_data["question"]
            is_correct = False
            
            if q["type"] == "tf":
                true_cb, false_cb = widget_data["widgets"]
                user_answer = True if true_cb.active else (False if false_cb.active else None)
                is_correct = user_answer == q["answer"]
            else:
                btn = widget_data["widgets"][0]
                user_answer = btn.text if btn.text != "Choose an answer" else None
                is_correct = user_answer == q["answer"]
            
            if is_correct:
                score += 1
        
        main = MDBoxLayout(
            orientation="vertical",
            md_bg_color=get_color_from_hex(Colors.BACKGROUND)
        )
        
        percentage = (score / total) * 100 if total > 0 else 0
        color = Colors.SUCCESS if percentage >= 60 else Colors.WARNING
        
        header = MDBoxLayout(
            size_hint_y=None,
            height=dp(140),
            padding=[dp(20), dp(20)],
            md_bg_color=get_color_from_hex(color),
            orientation="vertical",
            spacing=dp(10)
        )
        
        header.add_widget(
            MDLabel(
                text="Reading Complete!",
                font_size="28sp",
                bold=True,
                halign="center",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            )
        )
        
        header.add_widget(
            MDLabel(
                text=f"Score: {score}/{total}",
                font_size="42sp",
                bold=True,
                halign="center",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            )
        )
        
        header.add_widget(
            MDLabel(
                text=f"Time: {self.timer_label.text}",
                font_size="16sp",
                halign="center",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 0.9)
            )
        )
        
        main.add_widget(header)
        
        actions = MDBoxLayout(
            size_hint_y=None,
            height=dp(80),
            padding=[dp(20), dp(10)],
            spacing=dp(10)
        )
        
        actions.add_widget(
            MDFlatButton(
                text="Choose Another Story",
                on_release=lambda x: self.build_menu()
            )
        )
        
        actions.add_widget(
            MDRaisedButton(
                text="Read Again",
                on_release=lambda x: self.open_book(self.current_book)
            )
        )
        
        main.add_widget(actions)
        
        self.add_widget(main)