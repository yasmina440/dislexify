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
from kivymd.uix.slider import MDSlider
from kivy.metrics import dp, sp
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.properties import (
    StringProperty, BooleanProperty, NumericProperty, ListProperty,
    ObjectProperty
)
from kivy.uix.widget import Widget
from kivy.core.window import Window
from functools import partial
from responsive import Responsive


class Colors:
    """Color scheme based on British Council design"""
    PRIMARY = "#0066CC"
    PRIMARY_DARK = "#004C99"
    PRIMARY_LIGHT = "#4D94FF"
    SECONDARY = "#FF6B00"
    SUCCESS = "#28A745"
    DANGER = "#DC3545"
    WARNING = "#FFC107"
    SURFACE = "#FFFFFF"
    SURFACE_VARIANT = "#F8F9FA"
    BACKGROUND = "#F5F7FA"
    TEXT_PRIMARY = "#2C3E50"
    TEXT_SECONDARY = "#6C757D"
    TEXT_HINT = "#95A5A6"
    DIVIDER = "#E9ECEF"


class ResponsiveMixin:
    """Mixin for responsive sizing"""
    
    def get_responsive_height(self, base_height):
        """Get responsive height based on screen size"""
        screen_height = Window.height
        if screen_height < 600:  # Small phone
            return dp(base_height * 0.8)
        elif screen_height < 800:  # Medium phone
            return dp(base_height)
        else:  # Large phone
            return dp(base_height * 1.1)
    
    def get_responsive_width(self, base_width):
        """Get responsive width based on screen size"""
        screen_width = Window.width
        if screen_width < 360:  # Small phone
            return dp(base_width * 0.85)
        elif screen_width < 480:  # Medium phone
            return dp(base_width)
        else:  # Large phone
            return dp(base_width * 1.15)
    
    def get_responsive_font(self, base_size):
        """Get responsive font size"""
        screen_width = Window.width
        if screen_width < 360:
            return sp(base_size * 0.8)
        elif screen_width < 480:
            return sp(base_size)
        else:
            return sp(base_size * 1.1)
    
    def get_responsive_padding(self, base_padding):
        """Get responsive padding"""
        scale = min(Window.width / 360, 1.2)
        return dp(base_padding * scale)
    
    def get_responsive_spacing(self, base_spacing):
        """Get responsive spacing"""
        scale = min(Window.width / 360, 1.2)
        return dp(base_spacing * scale)


class WordSpacingControlPanel(MDBoxLayout, ResponsiveMixin):
    """Панель управления межсловным интервалом"""
    word_spacing = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = self.get_responsive_height(90)
        self.padding = [self.get_responsive_padding(15), self.get_responsive_padding(5)]
        self.spacing = self.get_responsive_spacing(5)
        self.md_bg_color = get_color_from_hex(Colors.SURFACE)
        
        # Заголовок панели
        title = MDLabel(
            text="Расстояние между словами",
            font_size=f"{self.get_responsive_font(14)}sp",
            bold=True,
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_PRIMARY),
            size_hint_y=None,
            height=self.get_responsive_height(25)
        )
        self.add_widget(title)
        
        # Слайдер для межсловного интервала
        spacing_box = MDBoxLayout(
            orientation="horizontal",
            spacing=self.get_responsive_spacing(10),
            size_hint_y=None,
            height=self.get_responsive_height(40)
        )
        
        spacing_icon_small = MDIcon(
            icon="arrow-expand-horizontal",
            font_size=f"{self.get_responsive_font(18)}sp",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
        )
        spacing_box.add_widget(spacing_icon_small)
        
        self.spacing_slider = MDSlider(
            min=0,
            max=10,
            value=self.word_spacing,
            step=1,
            size_hint_x=0.8,
            color=get_color_from_hex(Colors.PRIMARY),
            thumb_color_active=get_color_from_hex(Colors.PRIMARY),
            track_color_active=get_color_from_hex(Colors.PRIMARY_LIGHT)
        )
        self.spacing_slider.bind(value=self.on_word_spacing_change)
        spacing_box.add_widget(self.spacing_slider)
        
        spacing_icon_large = MDIcon(
            icon="arrow-expand-horizontal",
            font_size=f"{self.get_responsive_font(22)}sp",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
        )
        spacing_box.add_widget(spacing_icon_large)
        
        self.add_widget(spacing_box)
        
        # Подсказка с текущим значением
        self.hint_label = MDLabel(
            text=f"Текущий интервал: {int(self.word_spacing)}",
            font_size=f"{self.get_responsive_font(11)}sp",
            halign="center",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_HINT),
            size_hint_y=None,
            height=self.get_responsive_height(20)
        )
        self.add_widget(self.hint_label)
    
    def on_word_spacing_change(self, instance, value):
        self.word_spacing = int(value)
        self.hint_label.text = f"Текущий интервал: {int(self.word_spacing)}"


class ReadingProgressIndicator(MDBoxLayout, ResponsiveMixin):
    """Reading progress indicator - responsive"""
    max_pages = NumericProperty(10)
    current_page = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = self.get_responsive_spacing(5)
        self.padding = [
            self.get_responsive_padding(20),
            self.get_responsive_padding(10)
        ]
        self.size_hint_y = None
        self.height = self.get_responsive_height(50)
        
        self.progress_label = MDLabel(
            text=f"Page {self.current_page} of {self.max_pages}",
            font_size=f"{self.get_responsive_font(14)}sp",
            halign="center",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_SECONDARY),
            size_hint_y=None,
            height=self.get_responsive_height(25)
        )
        
        self.progress_bar = MDProgressBar(
            value=0,
            max=self.max_pages,
            size_hint_y=None,
            height=self.get_responsive_height(6),
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
        self.progress_label.text = f"Page {self.current_page} of {self.max_pages}"


class AchievementBadge(MDCard, ResponsiveMixin):
    """Achievement badge - responsive"""
    title = StringProperty("")
    icon = StringProperty("trophy")
    is_unlocked = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        
        # Responsive size based on screen width
        card_width = self.get_responsive_width(85)
        card_height = self.get_responsive_height(105)
        self.size = (card_width, card_height)
        
        self.radius = [self.get_responsive_padding(15)]
        self.padding = self.get_responsive_padding(8)
        self.elevation = 2
        self.md_bg_color = get_color_from_hex(
            Colors.SURFACE_VARIANT if not self.is_unlocked else Colors.SUCCESS
        )
        
        layout = MDBoxLayout(
            orientation="vertical",
            spacing=self.get_responsive_spacing(8),
            padding=[0, self.get_responsive_padding(5)]
        )
        
        icon = MDIcon(
            icon=self.icon,
            font_size=f"{self.get_responsive_font(32)}sp",
            theme_text_color="Custom",
            text_color=get_color_from_hex(
                Colors.TEXT_HINT if not self.is_unlocked else Colors.SURFACE
            ),
            halign="center"
        )
        
        title_label = MDLabel(
            text=self.title,
            font_size=f"{self.get_responsive_font(11)}sp",
            halign="center",
            theme_text_color="Custom",
            text_color=get_color_from_hex(
                Colors.TEXT_HINT if not self.is_unlocked else Colors.SURFACE
            ),
            size_hint_y=None,
            height=self.get_responsive_height(30),
            max_lines=2,
            shorten=True,
            shorten_from='right'
        )
        
        layout.add_widget(icon)
        layout.add_widget(title_label)
        self.add_widget(layout)


class ReadingStatsCard(MDCard, ResponsiveMixin):
    """Reading statistics card - responsive compact design"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = self.get_responsive_height(160)
        self.radius = [self.get_responsive_padding(20)]
        self.padding = [
            self.get_responsive_padding(16),
            self.get_responsive_padding(16),
            self.get_responsive_padding(16),
            self.get_responsive_padding(12)
        ]
        self.spacing = self.get_responsive_spacing(12)
        self.elevation = 2
        self.md_bg_color = get_color_from_hex(Colors.SURFACE)
        self.orientation = "vertical"
        
        # Title
        title = MDLabel(
            text="Your Reading Stats",
            font_size=f"{self.get_responsive_font(18)}sp",
            bold=True,
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_PRIMARY),
            size_hint_y=None,
            height=self.get_responsive_height(30),
            padding=[0, 0, 0, self.get_responsive_padding(5)]
        )
        self.add_widget(title)
        
        # Stats container
        stats_container = MDBoxLayout(
            orientation="horizontal",
            spacing=self.get_responsive_spacing(12),
            size_hint_y=None,
            height=self.get_responsive_height(95)
        )
        
        stats = [
            {"icon": "book-open-variant", "value": "12", "label": "Stories"},
            {"icon": "clock-outline", "value": "45m", "label": "Reading"},
            {"icon": "star", "value": "850", "label": "Points"}
        ]
        
        for stat in stats:
            stat_card = MDCard(
                size_hint=(1, 1),
                radius=[self.get_responsive_padding(12)],
                padding=[
                    self.get_responsive_padding(5),
                    self.get_responsive_padding(8)
                ],
                md_bg_color=get_color_from_hex(Colors.SURFACE_VARIANT),
                elevation=0
            )
            
            stat_layout = MDBoxLayout(
                orientation="vertical",
                spacing=self.get_responsive_spacing(4),
                padding=[0, self.get_responsive_padding(2)]
            )
            
            # Icon
            icon = MDIcon(
                icon=stat["icon"],
                font_size=f"{self.get_responsive_font(20)}sp",
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.PRIMARY),
                halign="center",
                size_hint_y=None,
                height=self.get_responsive_height(25)
            )
            stat_layout.add_widget(icon)
            
            # Value
            value_label = MDLabel(
                text=stat["value"],
                font_size=f"{self.get_responsive_font(18)}sp",
                bold=True,
                halign="center",
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_PRIMARY),
                size_hint_y=None,
                height=self.get_responsive_height(25)
            )
            stat_layout.add_widget(value_label)
            
            # Label
            desc_label = MDLabel(
                text=stat["label"],
                font_size=f"{self.get_responsive_font(10)}sp",
                halign="center",
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_SECONDARY),
                size_hint_y=None,
                height=self.get_responsive_height(20),
                max_lines=1,
                shorten=True,
                shorten_from='right'
            )
            stat_layout.add_widget(desc_label)
            
            stat_card.add_widget(stat_layout)
            stats_container.add_widget(stat_card)
        
        self.add_widget(stats_container)


class TaskScreen(MDScreen, ResponsiveMixin):
    """Enhanced reading practice screen - fully responsive for phones"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.state = "menu"
        self.time = 0
        self.font_size = 22  # Увеличенный базовый размер шрифта
        self.word_spacing = 0
        self.line_spacing = 1.6
        self.timer_event = None
        self.user_points = 850
        self.user_level = 3
        self.current_page = 1
        self.total_pages = 1
        self.current_book = None
        self.current_text_label = None
        
        # Bind to window resize events
        Window.bind(on_resize=self.on_window_resize)
        
        # Stories data
        self.books_data = {
            "Being a good classmate": {
                "level": "Level 3",
                "category": "School",
                "author": "British Council",
                "description": "What do you know about being a good classmate?",
                "estimated_time": "5 min",
                "pages": [
                    "Good classmates are kind and helpful. They share things and help each other with school work.",
                    "When someone is sad, a good classmate tries to help them feel better. They say kind words and include everyone in games.",
                    "Being a good classmate makes school a happier place for everyone. You can be a good classmate too!"
                ],
                "questions": [
                    {"q": "Good classmates are unkind to others.", "type": "tf", "answer": False},
                    {"q": "What should a good classmate do?", "type": "mc", 
                     "options": ["Ignore others", "Help and share", "Be mean"], "answer": "Help and share"},
                    {"q": "A good classmate includes everyone in games.", "type": "tf", "answer": True}
                ]
            },
            "School trip": {
                "level": "Level 2",
                "category": "Adventure",
                "author": "British Council",
                "description": "Read about a fun school trip to the zoo.",
                "estimated_time": "3 min",
                "pages": [
                    "Last week, our class went on a school trip to the city zoo. Everyone was very excited!",
                    "We saw lots of amazing animals - lions, tigers, elephants and playful monkeys.",
                    "At lunch time, we sat on the grass and had a picnic. It was the best day ever!"
                ],
                "questions": [
                    {"q": "The class went to a museum.", "type": "tf", "answer": False},
                    {"q": "What animals did they see at the zoo?", "type": "mc",
                     "options": ["Fish and birds", "Lions and tigers", "Dogs and cats"], "answer": "Lions and tigers"}
                ]
            },
            "The Mystery of the Missing Homework": {
                "level": "Level 4",
                "category": "Mystery",
                "author": "British Council",
                "description": "Can you solve the mystery of the missing homework?",
                "estimated_time": "7 min",
                "pages": [
                    "Tom couldn't find his homework anywhere. He had finished it carefully last night, but now it was completely gone!",
                    "He looked in his school bag, under his bed, and even in the kitchen. 'Mum, have you seen my homework?' he asked.",
                    "His mum shook her head. 'Sorry Tom, I haven't seen it. Did you check your little sister's room?'",
                    "Tom ran to Lily's room. There it was! His homework was in her toy box. Lily had wanted the paper for drawing!"
                ],
                "questions": [
                    {"q": "What did Tom lose?", "type": "mc",
                     "options": ["His lunch box", "His homework", "His pencil case"], "answer": "His homework"},
                    {"q": "Who had taken Tom's homework?", "type": "mc",
                     "options": ["His mum", "His sister Lily", "His friend"], "answer": "His sister Lily"},
                    {"q": "Tom found his homework under his bed.", "type": "tf", "answer": False}
                ]
            }
        }
        
        self.load_user_data()
        self.build_menu()
    
    def on_window_resize(self, window, width, height):
        """Handle window resize for orientation changes"""
        Clock.schedule_once(lambda dt: self.rebuild_current_state(), 0.1)
    
    def rebuild_current_state(self):
        """Rebuild current state after orientation change"""
        if self.state == "menu":
            self.build_menu()
        elif self.state == "reading" and self.current_book:
            self.open_book(self.current_book)
        elif self.state == "questions":
            self.open_questions(None)
        elif self.state == "results":
            self.show_results(None)
    
    def load_user_data(self):
        """Load user data"""
        self.user_stats = {
            "total_books_read": 12,
            "total_time": 45,
            "points": 850,
            "level": 3
        }
    
    def build_menu(self):
        """Build main menu - responsive"""
        self.clear_widgets()
        self.state = "menu"
        
        # Stop timer if running
        if self.timer_event:
            Clock.unschedule(self.timer_event)
            self.timer_event = None
        
        main_layout = MDBoxLayout(
            orientation="vertical",
            md_bg_color=get_color_from_hex(Colors.BACKGROUND)
        )
        
        # Header - responsive height
        header_height = self.get_responsive_height(130)
        header_padding = [
            self.get_responsive_padding(25),
            self.get_responsive_padding(15)
        ]
        
        header = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=header_height,
            padding=header_padding,
            md_bg_color=get_color_from_hex(Colors.PRIMARY)
        )
        
        header.add_widget(
            MDLabel(
                text="Reading Practice",
                font_size=f"{self.get_responsive_font(28)}sp",
                bold=True,
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            )
        )
        
        main_layout.add_widget(header)
        
        # Scroll view
        scroll = ScrollView(bar_width=self.get_responsive_padding(4))
        
        content = MDBoxLayout(
            orientation="vertical",
            padding=[self.get_responsive_padding(20), self.get_responsive_padding(15)],
            spacing=self.get_responsive_spacing(20),
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter("height"))
        
        # Welcome card
        welcome_card = MDCard(
            size_hint=(1, None),
            height=self.get_responsive_height(110),
            radius=[self.get_responsive_padding(20)],
            padding=self.get_responsive_padding(20),
            elevation=2,
            md_bg_color=get_color_from_hex(Colors.SURFACE),
            orientation="vertical",
            spacing=self.get_responsive_spacing(8)
        )
        
        welcome_card.add_widget(
            MDLabel(
                text="📚 Continue Your Reading Journey!",
                font_size=f"{self.get_responsive_font(20)}sp",
                bold=True,
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_PRIMARY),
                size_hint_y=None,
                height=self.get_responsive_height(35)
            )
        )
        
        welcome_card.add_widget(
            MDLabel(
                text=f"You've read {self.user_stats['total_books_read']} stories this month. Keep it up!",
                font_size=f"{self.get_responsive_font(14)}sp",
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_SECONDARY),
                size_hint_y=None,
                height=self.get_responsive_height(40)
            )
        )
        
        content.add_widget(welcome_card)
        
        # Statistics
        stats_card = ReadingStatsCard()
        content.add_widget(stats_card)
        
        # Achievements section
        achievements_height = self.get_responsive_height(150)
        achievements_section = MDBoxLayout(
            orientation="vertical",
            spacing=self.get_responsive_spacing(12),
            size_hint_y=None,
            height=achievements_height
        )
        
        achievements_section.add_widget(
            MDLabel(
                text="Your Achievements",
                font_size=f"{self.get_responsive_font(18)}sp",
                bold=True,
                size_hint_y=None,
                height=self.get_responsive_height(30),
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
            )
        )
        
        achievements_scroll = ScrollView(
            do_scroll_x=True,
            do_scroll_y=False,
            size_hint_y=None,
            height=self.get_responsive_height(110)
        )
        
        achievements_box = MDBoxLayout(
            orientation="horizontal",
            spacing=self.get_responsive_spacing(12),
            padding=[0, self.get_responsive_padding(5)],
            size_hint_x=None
        )
        achievements_box.bind(minimum_width=achievements_box.setter("width"))
        
        sample_achievements = [
            {"title": "First Story", "icon": "book-open-variant", "unlocked": True},
            {"title": "Perfect Score", "icon": "trophy", "unlocked": True},
            {"title": "7 Day Streak", "icon": "fire", "unlocked": True},
            {"title": "Bookworm", "icon": "book-multiple", "unlocked": False},
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
        
        # Stories header
        content.add_widget(
            MDLabel(
                text="Choose a Story",
                font_size=f"{self.get_responsive_font(20)}sp",
                bold=True,
                size_hint_y=None,
                height=self.get_responsive_height(40),
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
            )
        )
        
        # Story cards
        for book_name, book_data in self.books_data.items():
            card_height = self.get_responsive_height(130)
            
            card = MDCard(
                size_hint=(1, None),
                height=card_height,
                radius=[self.get_responsive_padding(20)],
                padding=self.get_responsive_padding(15),
                spacing=self.get_responsive_spacing(15),
                elevation=2,
                md_bg_color=get_color_from_hex(Colors.SURFACE),
                ripple_behavior=True,
                orientation="horizontal"
            )
            
            # Book icon
            icon_width = self.get_responsive_width(80)
            icon_box = MDBoxLayout(
                size_hint=(None, 1),
                width=icon_width,
                md_bg_color=get_color_from_hex(Colors.PRIMARY_LIGHT),
                radius=[self.get_responsive_padding(15)]
            )
            
            icon_box.add_widget(
                MDIcon(
                    icon="book-open-page-variant",
                    font_size=f"{self.get_responsive_font(40)}sp",
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1),
                    pos_hint={"center_x": 0.5, "center_y": 0.5}
                )
            )
            
            # Info section
            info_box = MDBoxLayout(
                orientation="vertical",
                spacing=self.get_responsive_spacing(8)
            )
            
            # Level chip
            chip_container = MDBoxLayout(
                size_hint_y=None,
                height=self.get_responsive_height(28)
            )
            
            level_chip = MDChip(
                text=book_data.get("level", "Level 1"),
                size_hint=(None, None),
                height=self.get_responsive_height(28),
                md_bg_color=get_color_from_hex(Colors.SECONDARY),
                text_color=(1, 1, 1, 1)
            )
            level_chip.bind(width=level_chip.setter("width"))
            
            chip_container.add_widget(level_chip)
            info_box.add_widget(chip_container)
            
            info_box.add_widget(
                MDLabel(
                    text=book_name,
                    font_size=f"{self.get_responsive_font(16)}sp",
                    bold=True,
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(Colors.TEXT_PRIMARY),
                    size_hint_y=None,
                    height=self.get_responsive_height(25)
                )
            )
            
            info_box.add_widget(
                MDLabel(
                    text=book_data.get("description", "")[:50] + "...",
                    font_size=f"{self.get_responsive_font(12)}sp",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(Colors.TEXT_SECONDARY),
                    size_hint_y=None,
                    height=self.get_responsive_height(40)
                )
            )
            
            info_box.add_widget(
                MDLabel(
                    text=f" {book_data.get('estimated_time', '5 min')}",
                    font_size=f"{self.get_responsive_font(11)}sp",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(Colors.PRIMARY),
                    size_hint_y=None,
                    height=self.get_responsive_height(20)
                )
            )
            
            card.add_widget(icon_box)
            card.add_widget(info_box)
            
            card.bind(on_release=lambda x, b=book_name: self.open_book(b))
            content.add_widget(card)
        
        # Spacer
        content.add_widget(Widget(size_hint_y=None, height=self.get_responsive_padding(20)))
        
        scroll.add_widget(content)
        main_layout.add_widget(scroll)
        
        # Back button
        back_btn_container = MDBoxLayout(
            size_hint_y=None,
            height=self.get_responsive_height(70),
            padding=[self.get_responsive_padding(20), self.get_responsive_padding(10)]
        )
        
        back_btn_container.add_widget(
            MDFlatButton(
                text="← Back to Home",
                font_size=f"{self.get_responsive_font(16)}sp",
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.PRIMARY),
                on_release=lambda x: self.go_back_home()
            )
        )
        
        main_layout.add_widget(back_btn_container)
        
        self.add_widget(main_layout)
    
    def go_back_home(self):
        """Navigate back to home screen"""
        if self.manager:
            if hasattr(self.manager, 'has_screen') and self.manager.has_screen('home'):
                self.manager.current = 'home'
            else:
                if self.manager.screens:
                    self.manager.current = self.manager.screens[0].name
    
    def open_book(self, book):
        """Open a book for reading - responsive"""
        self.clear_widgets()
        self.state = "reading"
        self.time = 0
        self.current_book = book
        self.current_page = 1
        
        book_data = self.books_data[book]
        self.pages = book_data.get("pages", [])
        self.total_pages = len(self.pages)
        self.questions = book_data.get("questions", [])
        
        main = MDBoxLayout(
            orientation="vertical",
            md_bg_color=get_color_from_hex(Colors.BACKGROUND)
        )
        
        # Top bar
        top_bar = MDBoxLayout(
            size_hint_y=None,
            height=self.get_responsive_height(60),
            padding=[self.get_responsive_padding(10), self.get_responsive_padding(10)],
            spacing=self.get_responsive_spacing(10),
            md_bg_color=get_color_from_hex(Colors.SURFACE)
        )
        
        back_btn = MDIconButton(
            icon="arrow-left",
            on_release=lambda x: self.build_menu()
        )
        
        book_info = MDBoxLayout(
            orientation="vertical",
            spacing=self.get_responsive_spacing(2),
            size_hint_x=0.6
        )
        
        book_info.add_widget(
            MDLabel(
                text=book,
                font_size=f"{self.get_responsive_font(16)}sp",
                bold=True,
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_PRIMARY),
                size_hint_y=None,
                height=self.get_responsive_height(25)
            )
        )
        
        book_info.add_widget(
            MDLabel(
                text=self.books_data[book].get("level", ""),
                font_size=f"{self.get_responsive_font(12)}sp",
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_SECONDARY),
                size_hint_y=None,
                height=self.get_responsive_height(20)
            )
        )
        
        self.timer_label = MDLabel(
            text="00:00",
            halign="right",
            size_hint_x=0.3,
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_SECONDARY),
            font_size=f"{self.get_responsive_font(14)}sp"
        )
        
        top_bar.add_widget(back_btn)
        top_bar.add_widget(book_info)
        top_bar.add_widget(self.timer_label)
        
        main.add_widget(top_bar)
        
        # Progress indicator
        self.reading_progress = ReadingProgressIndicator(
            current_page=self.current_page,
            max_pages=self.total_pages
        )
        main.add_widget(self.reading_progress)
        
        # Reading area
        reading_area = MDBoxLayout(
            orientation="vertical",
            padding=[self.get_responsive_padding(20), self.get_responsive_padding(10)]
        )
        
        self.text_scroll = ScrollView(bar_width=self.get_responsive_padding(4))
        
        self.text_container = MDBoxLayout(
            orientation="vertical",
            spacing=self.get_responsive_spacing(15),
            size_hint_y=None,
            padding=[0, 0, self.get_responsive_padding(10), 0]
        )
        self.text_container.bind(minimum_height=self.text_container.setter("height"))
        
        self.display_current_page()
        
        self.text_scroll.add_widget(self.text_container)
        reading_area.add_widget(self.text_scroll)
        
        # Page navigation
        nav_box = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=self.get_responsive_height(50),
            padding=[self.get_responsive_padding(20), self.get_responsive_padding(5)],
            spacing=self.get_responsive_spacing(10)
        )
        
        self.prev_btn = MDIconButton(
            icon="chevron-left",
            on_release=self.previous_page,
            disabled=self.current_page == 1
        )
        
        self.page_indicator = MDLabel(
            text=f"{self.current_page} / {self.total_pages}",
            halign="center",
            size_hint_x=0.6,
            font_size=f"{self.get_responsive_font(14)}sp"
        )
        
        self.next_btn = MDIconButton(
            icon="chevron-right",
            on_release=self.next_page,
            disabled=self.current_page == self.total_pages
        )
        
        nav_box.add_widget(self.prev_btn)
        nav_box.add_widget(self.page_indicator)
        nav_box.add_widget(self.next_btn)
        
        reading_area.add_widget(nav_box)
        main.add_widget(reading_area)
        
        # Word Spacing Control Panel
        self.word_spacing_panel = WordSpacingControlPanel(
            word_spacing=self.word_spacing
        )
        self.word_spacing_panel.spacing_slider.bind(value=self.on_word_spacing_change)
        main.add_widget(self.word_spacing_panel)
        
        # Continue button
        actions_bar = MDBoxLayout(
            size_hint_y=None,
            height=self.get_responsive_height(70),
            padding=[self.get_responsive_padding(20), self.get_responsive_padding(10)],
            spacing=self.get_responsive_spacing(10)
        )
        
        continue_btn = MDRaisedButton(
            text="Go to Questions →",
            font_size=f"{self.get_responsive_font(16)}sp",
            md_bg_color=get_color_from_hex(Colors.PRIMARY),
            on_release=self.open_questions
        )
        
        actions_bar.add_widget(continue_btn)
        main.add_widget(actions_bar)
        
        self.add_widget(main)
        
        # Start timer
        if self.timer_event:
            Clock.unschedule(self.timer_event)
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)
    
    def on_word_spacing_change(self, instance, value):
        """Обработчик изменения межсловного интервала"""
        self.word_spacing = int(value)
        if hasattr(self, 'word_spacing_panel'):
            self.word_spacing_panel.word_spacing = int(value)
        self.display_current_page()
    
    def display_current_page(self):
        """Display current page content"""
        self.text_container.clear_widgets()
        
        if self.current_page <= len(self.pages):
            page_text = self.pages[self.current_page - 1]
            
            # Форматируем текст с межсловным интервалом
            if self.word_spacing > 0:
                words = page_text.split(' ')
                spacer = ' ' * (self.word_spacing + 1)
                formatted_text = spacer.join(words)
            else:
                formatted_text = page_text
            
            # Используем увеличенный размер шрифта
            base_font_size = self.font_size
            responsive_font = self.get_responsive_font(base_font_size)
            
            # Создаем label с текстом
            text_label = MDLabel(
                text=formatted_text,
                font_size=f"{responsive_font}sp",
                line_height=self.line_spacing,
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_PRIMARY),
                size_hint_y=None,
                halign="left",
                valign="top",
                padding=[0, self.get_responsive_padding(10), 0, self.get_responsive_padding(10)]
            )
            
            self.current_text_label = text_label
            
            text_label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1] + self.get_responsive_padding(20)))
            
            self.text_container.add_widget(text_label)
            self.reading_progress.current_page = self.current_page
            
            # Update navigation buttons
            if hasattr(self, 'prev_btn'):
                self.prev_btn.disabled = self.current_page == 1
            if hasattr(self, 'next_btn'):
                self.next_btn.disabled = self.current_page == self.total_pages
            if hasattr(self, 'page_indicator'):
                self.page_indicator.text = f"{self.current_page} / {self.total_pages}"
    
    def previous_page(self, instance):
        """Go to previous page"""
        if self.current_page > 1:
            self.current_page -= 1
            self.display_current_page()
    
    def next_page(self, instance):
        """Go to next page"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.display_current_page()
    
    def update_timer(self, dt):
        """Update reading timer"""
        self.time += 1
        m = self.time // 60
        s = self.time % 60
        self.timer_label.text = f"{m:02d}:{s:02d}"
    
    def open_questions(self, instance):
        """Open questions section - responsive"""
        if self.timer_event:
            Clock.unschedule(self.timer_event)
            self.timer_event = None
        
        self.clear_widgets()
        self.state = "questions"
        
        main = MDBoxLayout(
            orientation="vertical",
            md_bg_color=get_color_from_hex(Colors.BACKGROUND)
        )
        
        # Header
        header = MDBoxLayout(
            size_hint_y=None,
            height=self.get_responsive_height(80),
            padding=[self.get_responsive_padding(20), self.get_responsive_padding(20)],
            md_bg_color=get_color_from_hex(Colors.PRIMARY)
        )
        
        header.add_widget(
            MDLabel(
                text="Check Your Understanding",
                font_size=f"{self.get_responsive_font(22)}sp",
                bold=True,
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            )
        )
        
        main.add_widget(header)
        
        # Scroll view for questions
        scroll = ScrollView(bar_width=self.get_responsive_padding(4))
        content = MDBoxLayout(
            orientation="vertical",
            padding=self.get_responsive_padding(20),
            spacing=self.get_responsive_spacing(20),
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter("height"))
        
        self.question_widgets = []
        
        for i, q in enumerate(self.questions):
            # Динамическая высота карточки в зависимости от типа вопроса
            if q["type"] == "mc":
                # Для multiple choice: базовая высота + высота для каждого варианта
                options_count = len(q.get("options", []))
                card_height = self.get_responsive_height(130 + options_count * 45)
            else:
                card_height = self.get_responsive_height(140)
            
            q_card = MDCard(
                size_hint=(1, None),
                height=card_height,
                radius=[self.get_responsive_padding(20)],
                padding=self.get_responsive_padding(20),
                spacing=self.get_responsive_spacing(12),
                orientation="vertical",
                elevation=2,
                md_bg_color=get_color_from_hex(Colors.SURFACE)
            )
            
            # Question number
            q_card.add_widget(
                MDLabel(
                    text=f"Question {i + 1} of {len(self.questions)}",
                    font_size=f"{self.get_responsive_font(13)}sp",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(Colors.PRIMARY),
                    size_hint_y=None,
                    height=self.get_responsive_height(25)
                )
            )
            
            # Question text
            q_card.add_widget(
                MDLabel(
                    text=q["q"],
                    font_size=f"{self.get_responsive_font(16)}sp",
                    bold=True,
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(Colors.TEXT_PRIMARY),
                    size_hint_y=None,
                    height=self.get_responsive_height(40)
                )
            )
            
            if q["type"] == "tf":
                tf_box = MDBoxLayout(
                    spacing=self.get_responsive_spacing(30),
                    size_hint_y=None,
                    height=self.get_responsive_height(40)
                )
                
                true_box = MDBoxLayout(spacing=self.get_responsive_spacing(8), size_hint_x=0.5)
                true_cb = MDCheckbox(
                    group=f"q{i}",
                    size_hint=(None, None),
                    size=(self.get_responsive_width(35), self.get_responsive_height(35))
                )
                true_box.add_widget(true_cb)
                true_box.add_widget(MDLabel(text="True", font_size=f"{self.get_responsive_font(15)}sp"))
                
                false_box = MDBoxLayout(spacing=self.get_responsive_spacing(8), size_hint_x=0.5)
                false_cb = MDCheckbox(
                    group=f"q{i}",
                    size_hint=(None, None),
                    size=(self.get_responsive_width(35), self.get_responsive_height(35))
                )
                false_box.add_widget(false_cb)
                false_box.add_widget(MDLabel(text="False", font_size=f"{self.get_responsive_font(15)}sp"))
                
                tf_box.add_widget(true_box)
                tf_box.add_widget(false_box)
                q_card.add_widget(tf_box)
                
                self.question_widgets.append({
                    "type": "tf",
                    "question": q,
                    "widgets": [true_cb, false_cb]
                })
            
            else:  # Multiple choice с радиокнопками
                # Контейнер для вариантов ответов
                options_container = MDBoxLayout(
                    orientation="vertical",
                    spacing=self.get_responsive_spacing(8),
                    size_hint_y=None,
                    height=self.get_responsive_height(len(q["options"]) * 45)
                )
                
                # Список для хранения чекбоксов этого вопроса
                option_checkboxes = []
                
                for opt_idx, opt in enumerate(q["options"]):
                    option_box = MDBoxLayout(
                        orientation="horizontal",
                        spacing=self.get_responsive_spacing(10),
                        size_hint_y=None,
                        height=self.get_responsive_height(40)
                    )
                    
                    # Радиокнопка (кружок) для выбора варианта
                    checkbox = MDCheckbox(
                        group=f"q{i}_mc",  # Группируем по вопросу
                        size_hint=(None, None),
                        size=(self.get_responsive_width(35), self.get_responsive_height(35))
                    )
                    option_checkboxes.append(checkbox)
                    
                    # Текст варианта ответа
                    option_label = MDLabel(
                        text=opt,
                        font_size=f"{self.get_responsive_font(14)}sp",
                        theme_text_color="Custom",
                        text_color=get_color_from_hex(Colors.TEXT_PRIMARY),
                        size_hint_y=None,
                        height=self.get_responsive_height(40)
                    )
                    
                    option_box.add_widget(checkbox)
                    option_box.add_widget(option_label)
                    options_container.add_widget(option_box)
                
                q_card.add_widget(options_container)
                
                self.question_widgets.append({
                    "type": "mc",
                    "question": q,
                    "widgets": option_checkboxes,
                    "options": q["options"]
                })
            
            content.add_widget(q_card)
        
        scroll.add_widget(content)
        main.add_widget(scroll)
        
        # Submit button
        submit_container = MDBoxLayout(
            size_hint_y=None,
            height=self.get_responsive_height(80),
            padding=[self.get_responsive_padding(20), self.get_responsive_padding(15)]
        )
        
        submit_btn = MDRaisedButton(
            text="Check Answers",
            font_size=f"{self.get_responsive_font(16)}sp",
            md_bg_color=get_color_from_hex(Colors.PRIMARY),
            on_release=self.show_results
        )
        
        submit_container.add_widget(submit_btn)
        main.add_widget(submit_container)
        
        self.add_widget(main)
    
    def set_dropdown_text(self, button, text):
        """Set dropdown button text"""
        button.text = text
    
    def show_results(self, instance):
        """Show quiz results - responsive"""
        self.clear_widgets()
        self.state = "results"
        
        score = 0
        total = len(self.questions)
        
        for widget_data in self.question_widgets:
            q = widget_data["question"]
            is_correct = False
            
            if q["type"] == "tf":
                true_cb, false_cb = widget_data["widgets"]
                if true_cb.active:
                    user_answer = True
                elif false_cb.active:
                    user_answer = False
                else:
                    user_answer = None
                is_correct = user_answer == q["answer"]
            else:  # Multiple choice с радиокнопками
                checkboxes = widget_data["widgets"]
                options = widget_data["options"]
                selected_option = None
                
                # Находим выбранный вариант
                for idx, cb in enumerate(checkboxes):
                    if cb.active:
                        selected_option = options[idx]
                        break
                
                is_correct = selected_option == q["answer"]
            
            if is_correct:
                score += 1
        
        main = MDBoxLayout(
            orientation="vertical",
            md_bg_color=get_color_from_hex(Colors.BACKGROUND)
        )
        
        percentage = (score / total) * 100 if total > 0 else 0
        color = Colors.SUCCESS if percentage >= 60 else Colors.WARNING
        
        # Result header
        header_height = self.get_responsive_height(160)
        header = MDBoxLayout(
            size_hint_y=None,
            height=header_height,
            padding=[self.get_responsive_padding(20), self.get_responsive_padding(20)],
            md_bg_color=get_color_from_hex(color),
            orientation="vertical",
            spacing=self.get_responsive_spacing(10)
        )
        
        header.add_widget(
            MDLabel(
                text="🎉 Well Done!" if percentage >= 60 else "📚 Keep Practicing!",
                font_size=f"{self.get_responsive_font(28)}sp",
                bold=True,
                halign="center",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                size_hint_y=None,
                height=self.get_responsive_height(45)
            )
        )
        
        header.add_widget(
            MDLabel(
                text=f"Your Score: {score}/{total}",
                font_size=f"{self.get_responsive_font(36)}sp",
                bold=True,
                halign="center",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                size_hint_y=None,
                height=self.get_responsive_height(50)
            )
        )
        
        header.add_widget(
            MDLabel(
                text=f"Reading Time: {self.timer_label.text}",
                font_size=f"{self.get_responsive_font(16)}sp",
                halign="center",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 0.9),
                size_hint_y=None,
                height=self.get_responsive_height(30)
            )
        )
        
        main.add_widget(header)
        
        # Result message
        message_card = MDCard(
            size_hint=(1, None),
            height=self.get_responsive_height(120),
            radius=[self.get_responsive_padding(20)],
            padding=self.get_responsive_padding(20),
            spacing=self.get_responsive_spacing(10),
            orientation="vertical",
            elevation=2,
            md_bg_color=get_color_from_hex(Colors.SURFACE),
            pos_hint={"center_x": 0.5}
        )
        
        if percentage >= 80:
            message = "Excellent! You understood the story very well!"
            points_earned = 50
        elif percentage >= 60:
            message = "Good job! You understood most of the story."
            points_earned = 30
        else:
            message = "Try reading the story again to understand it better."
            points_earned = 10
        
        message_card.add_widget(
            MDLabel(
                text=message,
                font_size=f"{self.get_responsive_font(16)}sp",
                halign="center",
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_PRIMARY),
                size_hint_y=None,
                height=self.get_responsive_height(40)
            )
        )
        
        message_card.add_widget(
            MDLabel(
                text=f"+{points_earned} points earned!",
                font_size=f"{self.get_responsive_font(18)}sp",
                bold=True,
                halign="center",
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.SUCCESS),
                size_hint_y=None,
                height=self.get_responsive_height(35)
            )
        )
        
        main.add_widget(message_card)
        
        # Action buttons
        actions = MDBoxLayout(
            size_hint_y=None,
            height=self.get_responsive_height(90),
            padding=[self.get_responsive_padding(20), self.get_responsive_padding(15)],
            spacing=self.get_responsive_spacing(15)
        )
        
        actions.add_widget(
            MDFlatButton(
                text="Choose Another Story",
                font_size=f"{self.get_responsive_font(15)}sp",
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.PRIMARY),
                on_release=lambda x: self.build_menu()
            )
        )
        
        actions.add_widget(
            MDRaisedButton(
                text="Read Again",
                font_size=f"{self.get_responsive_font(15)}sp",
                md_bg_color=get_color_from_hex(Colors.PRIMARY),
                on_release=lambda x: self.open_book(self.current_book)
            )
        )
        
        main.add_widget(actions)
        
        self.add_widget(main)