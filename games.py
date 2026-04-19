from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton, MDFillRoundFlatButton
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp, sp
import random
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.text import LabelBase

LabelBase.register(
    name="Emoji",
    fn_regular="NotoColorEmoji-Regular.ttf"
)


# ---------- PREMIUM COLOR SCHEME ----------
class Colors:
    PRIMARY = "#6366F1"  # Indigo
    PRIMARY_LIGHT = "#818CF8"
    PRIMARY_DARK = "#4F46E5"
    SECONDARY = "#EC4899"  # Pink
    SECONDARY_LIGHT = "#F472B6"
    SECONDARY_DARK = "#DB2777"
    SUCCESS = "#10B981"  # Emerald
    SUCCESS_LIGHT = "#34D399"
    WARNING = "#F59E0B"  # Amber
    WARNING_LIGHT = "#FBBF24"
    DANGER = "#EF4444"  # Red
    DANGER_LIGHT = "#F87171"
    INFO = "#3B82F6"  # Blue
    INFO_LIGHT = "#60A5FA"
    BACKGROUND = "#F8FAFC"
    SURFACE = "#FFFFFF"
    SURFACE_VARIANT = "#F1F5F9"
    TEXT_PRIMARY = "#0F172A"
    TEXT_SECONDARY = "#64748B"
    TEXT_DISABLED = "#94A3B8"


# ---------- ANIMATED CARD ----------
class AnimatedCard(MDCard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.radius = [dp(20)]
        self.elevation = 4
        self.padding = [dp(20), dp(20)]
        self.md_bg_color = get_color_from_hex(Colors.SURFACE)


# ---------- MODERN BUTTON ----------
class ModernButton(MDFillRoundFlatButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.radius = [dp(12)]
        self.font_size = sp(16)
        self.size_hint_y = None
        self.height = dp(50)


# ---------- MAIN GAME MENU ----------
class GameScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(
            orientation="vertical",
            md_bg_color=get_color_from_hex(Colors.BACKGROUND)
        )
        
        # Header
        header = AnimatedCard(
            size_hint_y=None,
            height=dp(140),
            elevation=0
        )
        header.md_bg_color = get_color_from_hex(Colors.PRIMARY)
        
        header_layout = MDBoxLayout(orientation="vertical", spacing=dp(10))
        
        header_layout.add_widget(
            MDIcon(
                icon="gamepad-variant",
                font_size=sp(48),
                halign="center",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            )
        )
        
        header_layout.add_widget(
            MDLabel(
                text="Learning Games",
                halign="center",
                font_size=sp(28),
                bold=True,
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1)
            )
        )
        
        header_layout.add_widget(
            MDLabel(
                text="Learn while having fun!",
                halign="center",
                font_size=sp(14),
                theme_text_color="Custom",
                text_color=(1, 1, 1, 0.9)
            )
        )
        
        header.add_widget(header_layout)
        layout.add_widget(header)
        
        # Scrollable content
        scroll = ScrollView(bar_width=dp(4))
        content = MDBoxLayout(
            orientation="vertical",
            padding=[dp(20), dp(20)],
            spacing=dp(16),
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter('height'))
        
        games = [
            {
                "name": "Build a Sentence",
                "screen": "sentence",
                "icon": "format-list-bulleted",
                "description": "make correct sentences",
                "stats": "⭐ Level 1-3",
                "color": Colors.PRIMARY
            },
            {
                "name": "Build a Word",
                "screen": "word",
                "icon": "alphabetical",
                "description": "Test your grammar",
                "stats": "⭐ Level 1-5",
                "color": Colors.SECONDARY
            },
            {
                "name": "Color Challenge",
                "screen": "color",
                "icon": "palette",
                "description": "Match colors, not words!",
                "stats": "🎯 Endless Mode",
                "color": Colors.SUCCESS
            },
            {
                "name": "Memory Arrows",
                "screen": "direction",
                "icon": "compass",
                "description": "Remember and repeat",
                "stats": "🧠 Level 1-10",
                "color": Colors.WARNING
            }
        ]
        
        for game in games:
            card = AnimatedCard(
                size_hint=(1, None),
                height=dp(120),
                elevation=2
            )
            
            box = MDBoxLayout(spacing=dp(16))
            
            # Icon container
            icon_container = MDBoxLayout(
                size_hint=(None, None),
                size=(dp(70), dp(70)),
                md_bg_color=get_color_from_hex(game["color"]),
                radius=[dp(35)]
            )
            icon_container.add_widget(
                MDIcon(
                    icon=game["icon"],
                    font_size=sp(36),
                    halign="center",
                    valign="center",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(Colors.SURFACE)
                )
            )
            
            # Text container
            text_box = MDBoxLayout(orientation="vertical", spacing=dp(6))
            text_box.add_widget(
                MDLabel(
                    text=game["name"],
                    font_size=sp(18),
                    bold=True,
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
                )
            )
            text_box.add_widget(
                MDLabel(
                    text=game["description"],
                    font_size=sp(13),
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
                )
            )
            
            # Stats chip
            stats_chip = MDCard(
                size_hint=(None, None),
                size=(dp(100), dp(26)),
                radius=[dp(13)],
                md_bg_color=get_color_from_hex(game["color"]),
                elevation=0
            )
            stats_chip.add_widget(
                MDLabel(
                    text=game["stats"],
                    font_size=sp(11),
                    halign="center",
                    valign="center",
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1)
                )
            )
            text_box.add_widget(stats_chip)
            
            box.add_widget(icon_container)
            box.add_widget(text_box)
            
            # Play arrow
            play_icon = MDIcon(
                icon="chevron-right",
                font_size=sp(32),
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_DISABLED)
            )
            box.add_widget(play_icon)
            
            card.add_widget(box)
            card.bind(on_release=lambda x, s=game["screen"]: self.navigate_to_game(s))
            content.add_widget(card)
        
        scroll.add_widget(content)
        layout.add_widget(scroll)
        self.add_widget(layout)
    
    def navigate_to_game(self, screen_name):
        if self.manager:
            self.manager.current = screen_name



class DropSlot(AnimatedCard):
    word = StringProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(120), dp(60))
        self.elevation = 2
        self.chip = None
        self.md_bg_color = get_color_from_hex(Colors.SURFACE_VARIANT)
        
        self.empty_label = MDLabel(
            text="_____",
            halign="center",
            valign="center",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_DISABLED),
            font_style="Subtitle1",
            font_size=sp(16)
        )
        self.add_widget(self.empty_label)
        
        # Store the screen reference for coordinate conversion
        self.screen = None

    def set_word(self, chip):
        self.word = chip.word
        self.chip = chip
        # Convert to screen coordinates for positioning
        if hasattr(chip, 'parent') and chip.parent:
            # Remove from current parent
            chip.parent.remove_widget(chip)
        
        # Add to the screen's main layout (root) for free movement
        if self.screen and hasattr(self.screen, 'drag_layer'):
            self.screen.drag_layer.add_widget(chip)
        
        # Position the chip at the slot's position
        chip.pos = self.pos
        self.md_bg_color = get_color_from_hex(Colors.SUCCESS)
        self.empty_label.text = ""
        
        # Animate
        anim = Animation(elevation=8, duration=0.15) + \
               Animation(elevation=2, duration=0.15)
        anim.start(self)
        
        # Disable further dragging
        chip.disabled = True

    def clear(self):
        self.word = None
        if self.chip:
            if self.chip.parent:
                self.chip.parent.remove_widget(self.chip)
            self.chip = None
        self.md_bg_color = get_color_from_hex(Colors.SURFACE_VARIANT)
        self.empty_label.text = "_____"
        self.elevation = 2


class WordChip(MDCard, ButtonBehavior):
    def __init__(self, word, game, **kwargs):
        super().__init__(**kwargs)
        self.text = word
        self.word = word
        self.game = game
        self.size_hint = (None, None)
        self.size = (dp(120), dp(60))
        self.radius = [dp(12)]
        self.elevation = 3
        self.md_bg_color = get_color_from_hex(Colors.PRIMARY)
        self.drag_enabled = True
        self.original_parent = None
        self._touch_offset_x = 0
        self._touch_offset_y = 0
        
        self.label = MDLabel(
            text=word,
            halign="center",
            valign="center",
            font_size=sp(18),
            bold=True,
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.SURFACE)
        )
        self.add_widget(self.label)
        
        self.start_pos = (0, 0)
        self.bind(pos=self.update_start)
        
    def update_start(self, *args):
        if not self.disabled:
            self.start_pos = self.pos

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not self.disabled and self.drag_enabled:
            self._touch = touch
            # Calculate offset from touch point to widget center
            self._touch_offset_x = self.center_x - touch.x
            self._touch_offset_y = self.center_y - touch.y
            self.elevation = 12
            
            # Bring to front
            if self.parent:
                self.original_parent = self.parent
                self.parent.remove_widget(self)
                if hasattr(self.game, 'drag_layer'):
                    self.game.drag_layer.add_widget(self)
            
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if hasattr(self, "_touch") and touch is self._touch:
            # Move with offset to make dragging feel natural
            new_x = touch.x + self._touch_offset_x
            new_y = touch.y + self._touch_offset_y
            self.center_x = new_x
            self.center_y = new_y
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if hasattr(self, "_touch") and touch is self._touch:
            self.elevation = 3
            
            # Check if dropped on any slot
            dropped = False
            for slot in self.game.slots:
                if self.game._is_over_slot(self, slot) and not slot.word:
                    self.game.drop(self, slot)
                    dropped = True
                    break
            
            if not dropped:
                # Return to original position if not dropped on a valid slot
                self.go_back()
            
            # Remove from drag layer and return to original parent
            if hasattr(self, 'original_parent') and self.original_parent:
                if self.parent:
                    self.parent.remove_widget(self)
                if not dropped:
                    self.original_parent.add_widget(self)
                    self.go_back()
            
            delattr(self, "_touch")
            return True
        return super().on_touch_up(touch)

    def go_back(self):
        if self.start_pos:
            anim = Animation(pos=self.start_pos, duration=0.3, t='out_quad')
            anim.start(self)


class SentenceGameScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.correct = ["Do", "you", "have", "toast", "for", "breakfast?"]
        self.slots = []
        self.chips = []
        self.drag_layer = None
        self.build_ui()
        
    def build_ui(self):
        # Create main layout with FloatLayout for drag layer
        main_layout = FloatLayout()
        
        # Content layout (background)
        self.content_layout = MDBoxLayout(
            orientation="vertical",
            md_bg_color=get_color_from_hex(Colors.BACKGROUND)
        )
        
        # Create drag layer on top
        self.drag_layer = FloatLayout()
        
        # Header
        header = self.create_header("📝 Build a Sentence", Colors.PRIMARY)
        self.content_layout.add_widget(header)
        
        content = MDBoxLayout(
            orientation="vertical",
            padding=[dp(20), dp(20)],
            spacing=dp(20)
        )
        
        # Progress section
        progress_card = AnimatedCard(size_hint_y=None, height=dp(70), elevation=1)
        progress_layout = MDBoxLayout(orientation="vertical", spacing=dp(8))
        
        progress_layout.add_widget(
            MDLabel(
                text="Sentence Progress",
                font_size=sp(12),
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
            )
        )
        
        self.progress_bar = MDProgressBar(
            value=0,
            max=len(self.correct),
            size_hint_y=None,
            height=dp(8),
            color=get_color_from_hex(Colors.SUCCESS)
        )
        progress_layout.add_widget(self.progress_bar)
        progress_card.add_widget(progress_layout)
        content.add_widget(progress_card)
        
        # Word slots area
        slots_container = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(160)
        )
        
        slots_container.add_widget(
            MDLabel(
                text="🎯 Drop words here:",
                size_hint_y=None,
                height=dp(30),
                font_size=sp(14),
                bold=True,
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
            )
        )
        
        self.slot_box = MDBoxLayout(
            size_hint_y=None,
            height=dp(100),
            spacing=dp(12),
            padding=[dp(10), dp(5)]
        )
        
        self.slots = []
        for i in range(len(self.correct)):
            slot = DropSlot()
            slot.screen = self
            self.slot_box.add_widget(slot)
            self.slots.append(slot)
        
        slot_scroll = ScrollView(size_hint=(1, None), height=dp(110))
        slot_scroll.add_widget(self.slot_box)
        slots_container.add_widget(slot_scroll)
        content.add_widget(slots_container)
        
        # Words to drag area
        words_container = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(140)
        )
        
        words_container.add_widget(
            MDLabel(
                text="📖 Drag these words anywhere:",
                size_hint_y=None,
                height=dp(30),
                font_size=sp(14),
                bold=True,
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
            )
        )
        
        self.words_box = MDBoxLayout(
            size_hint_y=None,
            height=dp(80),
            spacing=dp(12),
            padding=[dp(10), dp(5)]
        )
        
        word_scroll = ScrollView(size_hint=(1, None), height=dp(90))
        word_scroll.add_widget(self.words_box)
        words_container.add_widget(word_scroll)
        content.add_widget(words_container)
        
        # Result
        self.result = MDCard(
            size_hint_y=None,
            height=dp(50),
            radius=[dp(12)],
            elevation=0,
            md_bg_color=get_color_from_hex(Colors.SURFACE_VARIANT)
        )
        self.result_label = MDLabel(
            text="",
            halign="center",
            valign="center",
            font_size=sp(16),
            theme_text_color="Custom"
        )
        self.result.add_widget(self.result_label)
        content.add_widget(self.result)
        
        # Control buttons
        buttons = MDBoxLayout(
            size_hint_y=None,
            height=dp(120),
            spacing=dp(12),
            orientation="vertical"
        )
        
        button_row = MDBoxLayout(spacing=dp(12), size_hint_y=None, height=dp(50))
        
        check_btn = ModernButton(
            text="✓ CHECK SENTENCE",
            md_bg_color=get_color_from_hex(Colors.SUCCESS),
            on_release=lambda x: self.check()
        )
        
        reset_btn = ModernButton(
            text="⟳ RESTART",
            md_bg_color=get_color_from_hex(Colors.WARNING),
            on_release=lambda x: self.reset()
        )
        
        button_row.add_widget(check_btn)
        button_row.add_widget(reset_btn)
        buttons.add_widget(button_row)
        
        # Hint button
        hint_btn = ModernButton(
            text="💡 SHOW HINT",
            md_bg_color=get_color_from_hex(Colors.INFO),
            text_color=get_color_from_hex(Colors.SURFACE),
            on_release=lambda x: self.show_hint()
        )
        buttons.add_widget(hint_btn)
        
        content.add_widget(buttons)
        
        # Add scrollview to content
        scroll_view = ScrollView()
        scroll_view.add_widget(content)
        self.content_layout.add_widget(scroll_view)
        
        # Add layouts to main FloatLayout
        main_layout.add_widget(self.content_layout)
        main_layout.add_widget(self.drag_layer)
        
        self.add_widget(main_layout)
        
        self.initialize_words()
    
    def create_header(self, title, color):
        header = AnimatedCard(
            size_hint_y=None,
            height=dp(80),
            elevation=0
        )
        header.md_bg_color = get_color_from_hex(color)
        
        header_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            padding=[dp(10), dp(10)]
        )
        
        back_btn = MDIconButton(
            icon="arrow-left",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            on_release=lambda x: self.go_back()
        )
        
        title_label = MDLabel(
            text=title,
            halign="center",
            font_size=sp(20),
            bold=True,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        
        header_layout.add_widget(back_btn)
        header_layout.add_widget(title_label)
        header_layout.add_widget(Widget(size_hint_x=None, width=dp(48)))
        
        header.add_widget(header_layout)
        return header
    
    def go_back(self):
        if self.manager:
            self.manager.current = "games"
    
    def initialize_words(self):
        self.words_box.clear_widgets()
        self.chips = []
        shuffled = self.correct[:]
        random.shuffle(shuffled)
        
        for w in shuffled:
            chip = WordChip(w, self)
            self.words_box.add_widget(chip)
            self.chips.append(chip)
    
    def drop(self, chip, target_slot):
        """Called when a chip is dropped on a slot"""
        # Check if this chip is already in a slot
        for s in self.slots:
            if s.chip == chip:
                chip.go_back()
                return
        
        # Place in slot
        target_slot.set_word(chip)
        self.update_progress()
    
    def _is_over_slot(self, chip, slot):
        """Check if chip is over a slot"""
        # Get widget positions in screen coordinates
        chip_pos = chip.to_window(chip.x, chip.y)
        slot_pos = slot.to_window(slot.x, slot.y)
        
        chip_center = (chip_pos[0] + chip.width / 2, chip_pos[1] + chip.height / 2)
        slot_center = (slot_pos[0] + slot.width / 2, slot_pos[1] + slot.height / 2)
        
        # Calculate distance
        distance = ((chip_center[0] - slot_center[0]) ** 2 + 
                   (chip_center[1] - slot_center[1]) ** 2) ** 0.5
        
        # If within 150 pixels, consider it dropped on the slot
        return distance < dp(150)
    
    def update_progress(self):
        filled = sum(1 for slot in self.slots if slot.word)
        self.progress_bar.value = filled
    
    def check(self):
        words = []
        empty_slots = []
        
        for i, slot in enumerate(self.slots):
            if not slot.word:
                empty_slots.append(i)
                words.append(None)
            else:
                words.append(slot.word)
        
        if empty_slots:
            self.show_result(f"❌ Fill all slots! ({len(empty_slots)} empty)", Colors.DANGER)
            return
        
        if words == self.correct:
            self.show_result("🎉 EXCELLENT! Perfect sentence! 🎉", Colors.SUCCESS)
            for slot in self.slots:
                if slot.chip:
                    slot.chip.disabled = True
            self.animate_success()
        else:
            mistake_positions = []
            for i, (user_word, correct_word) in enumerate(zip(words, self.correct)):
                if user_word != correct_word:
                    mistake_positions.append(i + 1)
            
            mistake_text = f"❌ Wrong at position(s): {mistake_positions}"
            self.show_result(mistake_text, Colors.DANGER)
            self.animate_error()
    
    def show_result(self, text, color):
        self.result_label.text = text
        self.result_label.text_color = get_color_from_hex(color)
        self.result.md_bg_color = get_color_from_hex(Colors.SURFACE_VARIANT)
        self.result.opacity = 1
        
        if hasattr(self, '_result_timer'):
            Clock.unschedule(self._result_timer)
        self._result_timer = Clock.schedule_once(lambda dt: self.clear_result(), 3)
    
    def clear_result(self):
        self.result_label.text = ""
    
    def animate_success(self):
        # Animate slots only (they have elevation property)
        for slot in self.slots:
            if slot.word:
                anim = Animation(elevation=8, duration=0.2) + Animation(elevation=2, duration=0.2)
                anim.start(slot)
    
    def animate_error(self):
        original_color = self.result.md_bg_color
        self.result.md_bg_color = get_color_from_hex(Colors.DANGER)
        Clock.schedule_once(lambda dt: setattr(self.result, 'md_bg_color', original_color), 0.3)
    
    def show_hint(self):
        dialog = MDDialog(
            title="💡 Hint",
            text=f"The sentence starts with '{self.correct[0]}' and ends with '{self.correct[-1]}'",
            buttons=[MDFlatButton(text="Got it!", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()
    
    def reset(self):
        # Clear all slots and return chips to words_box
        for slot in self.slots:
            if slot.chip:
                slot.chip.disabled = False
                slot.chip.drag_enabled = True
                # Remove from drag layer if there
                if slot.chip.parent:
                    slot.chip.parent.remove_widget(slot.chip)
                self.words_box.add_widget(slot.chip)
            slot.clear()
        
        self.result_label.text = ""
        self.progress_bar.value = 0
        self.initialize_words()



# ---------- MODERN BUTTON (исправленный) ----------
class ModernButton(MDFillRoundFlatButton):
    def __init__(self, **kwargs):
        # Удаляем bold из kwargs, если он там есть
        kwargs.pop('bold', None)
        super().__init__(**kwargs)
        self.radius = [dp(12)]
        self.font_size = sp(16)
        self.size_hint_y = None
        self.height = dp(50)


# ---------- DIRECTION GAME (оптимизированная версия) ----------
class DirectionGameScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine = DirectionGameEngine()
        self.timer_event = None
        self.build_ui()
        self.start_game()

    def build_ui(self):
        root = MDBoxLayout(
            orientation="vertical",
            md_bg_color=get_color_from_hex(Colors.BACKGROUND)
        )

        header = self.create_header("Memory Arrows", Colors.WARNING)
        root.add_widget(header)

        # Используем ScrollView чтобы весь контент был доступен
        scroll = ScrollView(bar_width=dp(3))
        
        content = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            padding=[dp(16), dp(12)],
            spacing=dp(10)
        )
        content.bind(minimum_height=content.setter('height'))
        
        # Stats card
        stats_card = AnimatedCard(size_hint_y=None, height=dp(65), elevation=2)
        stats_layout = MDBoxLayout(spacing=dp(10))
        
        self.level_label = MDLabel(
            text="Level: 1",
            halign="center",
            font_size=sp(13),
            bold=True,
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
        )
        
        self.score_label = MDLabel(
            text="Score: 0",
            halign="center",
            font_size=sp(13),
            bold=True,
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
        )
        
        self.time_label = MDLabel(
            text="Time: 15",
            halign="center",
            font_size=sp(13),
            bold=True,
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.WARNING)
        )
        
        stats_layout.add_widget(self.level_label)
        stats_layout.add_widget(self.score_label)
        stats_layout.add_widget(self.time_label)
        stats_card.add_widget(stats_layout)
        content.add_widget(stats_card)
        
        # Direction display (только текст направления)
        self.direction_card = AnimatedCard(
            size_hint=(1, None),
            height=dp(140),
            elevation=4
        )
        self.direction_card.md_bg_color = get_color_from_hex(Colors.PRIMARY_LIGHT)
        
        # Текст направления
        self.direction_text_label = MDLabel(
            text="RIGHT",
            halign="center",
            valign="center",
            font_size=sp(48),
            bold=True,
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.SURFACE)
        )
        self.direction_card.add_widget(self.direction_text_label)
        content.add_widget(self.direction_card)
        
        # Instruction
        content.add_widget(
            MDLabel(
                text="Press the matching direction button:",
                halign="center",
                size_hint_y=None,
                height=dp(20),
                font_size=sp(11),
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
            )
        )
        
        # Direction buttons - только стрелки внизу
        buttons_layout = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(200),
            spacing=dp(12)
        )
        
        # Верхний ряд (стрелка вверх)
        top_row = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(55),
            spacing=dp(15)
        )
        top_row.add_widget(Widget())
        top_row.add_widget(self.create_direction_button("arrow-up", "up", Colors.WARNING))
        top_row.add_widget(Widget())
        buttons_layout.add_widget(top_row)
        
        # Средний ряд (влево и вправо)
        middle_row = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(55),
            spacing=dp(20)
        )
        middle_row.add_widget(self.create_direction_button("arrow-left", "left", Colors.INFO))
        middle_row.add_widget(Widget())
        middle_row.add_widget(self.create_direction_button("arrow-right", "right", Colors.SUCCESS))
        buttons_layout.add_widget(middle_row)
        
        # Нижний ряд (стрелка вниз)
        bottom_row = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(55),
            spacing=dp(15)
        )
        bottom_row.add_widget(Widget())
        bottom_row.add_widget(self.create_direction_button("arrow-down", "down", Colors.SECONDARY))
        bottom_row.add_widget(Widget())
        buttons_layout.add_widget(bottom_row)
        
        content.add_widget(buttons_layout)
        
        # Result
        self.result_label = MDLabel(
            text="",
            halign="center",
            font_size=sp(12),
            size_hint_y=None,
            height=dp(25),
            theme_text_color="Custom"
        )
        content.add_widget(self.result_label)
        
        # Restart button
        restart_btn = ModernButton(
            text="RESTART",
            md_bg_color=get_color_from_hex(Colors.PRIMARY),
            size_hint_y=None,
            height=dp(40),
            on_release=lambda x: self.reset_game()
        )
        content.add_widget(restart_btn)
        
        scroll.add_widget(content)
        root.add_widget(scroll)
        self.add_widget(root)

    def create_header(self, title, color):
        header = AnimatedCard(
            size_hint_y=None,
            height=dp(55),
            elevation=0
        )
        header.md_bg_color = get_color_from_hex(color)
        
        header_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            padding=[dp(8), dp(8)]
        )
        
        back_btn = MDIconButton(
            icon="arrow-left",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            on_release=lambda x: self.go_back()
        )
        
        title_label = MDLabel(
            text=title,
            halign="center",
            font_size=sp(16),
            bold=True,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        
        header_layout.add_widget(back_btn)
        header_layout.add_widget(title_label)
        header_layout.add_widget(Widget(size_hint_x=None, width=dp(40)))
        
        header.add_widget(header_layout)
        return header

    def create_direction_button(self, icon_name, direction, color):
        """Создает кнопку направления с иконкой"""
        btn = MDIconButton(
            icon=icon_name,
            icon_size=sp(36),
            md_bg_color=get_color_from_hex(color),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint=(0.4, 1),
            on_release=lambda x, d=direction: self.on_press(d)
        )
        btn.radius = [dp(12)]
        return btn

    def go_back(self):
        if self.manager:
            if self.timer_event:
                Clock.unschedule(self.timer_event)
            self.manager.current = "games"

    def start_game(self):
        self.engine.generate()
        self.update_ui()
        if self.timer_event:
            Clock.unschedule(self.timer_event)
        self.timer_event = Clock.schedule_interval(self.timer, 1)

    def timer(self, dt):
        self.engine.time_left -= 1
        if self.engine.time_left <= 0:
            self.result_label.text = "TIME'S UP! Game Over!"
            self.result_label.text_color = get_color_from_hex(Colors.DANGER)
            self.reset_game()
            return
        self.update_ui()

    def on_press(self, direction):
        result = self.engine.check(direction)
        
        if result == "correct":
            self.result_label.text = "CORRECT!"
            self.result_label.text_color = get_color_from_hex(Colors.SUCCESS)
            self.animate_correct()
        elif result == "wrong":
            needed = self.engine.sequence[self.engine.index - 1] if self.engine.index > 0 else "?"
            self.result_label.text = f"Wrong! Needed: {needed.upper()}"
            self.result_label.text_color = get_color_from_hex(Colors.DANGER)
            self.animate_wrong()
            self.reset_game()
            return
        elif result == "level_complete":
            self.result_label.text = f"LEVEL {self.engine.level-1} COMPLETE! +5s!"
            self.result_label.text_color = get_color_from_hex(Colors.SUCCESS)
            self.animate_level_up()
            self.engine.generate()
        
        self.update_ui()
        Clock.schedule_once(lambda dt: self.clear_result(), 1.5)

    def clear_result(self):
        if "Game Over" not in self.result_label.text:
            self.result_label.text = ""

    def animate_correct(self):
        # Анимация правильного ответа
        anim = Animation(font_size=sp(56), duration=0.1) + Animation(font_size=sp(48), duration=0.1)
        anim.start(self.direction_text_label)

    def animate_wrong(self):
        # Анимация неправильного ответа
        original_color = self.direction_card.md_bg_color
        self.direction_card.md_bg_color = get_color_from_hex(Colors.DANGER)
        Clock.schedule_once(lambda dt: setattr(self.direction_card, 'md_bg_color', original_color), 0.3)

    def animate_level_up(self):
        # Анимация повышения уровня
        original_color = self.direction_card.md_bg_color
        self.direction_card.md_bg_color = get_color_from_hex(Colors.SUCCESS)
        Clock.schedule_once(lambda dt: setattr(self.direction_card, 'md_bg_color', original_color), 0.5)

    def update_ui(self):
        if self.engine.sequence and self.engine.index < len(self.engine.sequence):
            direction = self.engine.sequence[self.engine.index]
            
            # Обновляем текстовое направление
            direction_text = direction.upper()
            self.direction_text_label.text = direction_text
            
            # Обновляем цвета
            color_map = {"left": Colors.INFO, "right": Colors.SUCCESS, 
                        "up": Colors.WARNING, "down": Colors.SECONDARY}
            arrow_color = get_color_from_hex(color_map.get(direction, Colors.PRIMARY))
            self.direction_text_label.text_color = arrow_color

        self.level_label.text = f"Level: {self.engine.level}"
        self.score_label.text = f"Score: {self.engine.score}"
        self.time_label.text = f"Time: {self.engine.time_left}"
        
        if self.engine.time_left <= 5:
            self.time_label.text_color = get_color_from_hex(Colors.DANGER)
        else:
            self.time_label.text_color = get_color_from_hex(Colors.WARNING)

    def reset_game(self):
        if self.timer_event:
            Clock.unschedule(self.timer_event)
            self.timer_event = None
        self.engine = DirectionGameEngine()
        self.update_ui()
        self.start_game()


# ---------- MODERN BUTTON (исправленный) ----------
class ModernButton(MDFillRoundFlatButton):
    def __init__(self, **kwargs):
        # Удаляем bold из kwargs, если он там есть
        kwargs.pop('bold', None)
        super().__init__(**kwargs)
        self.radius = [dp(12)]
        self.font_size = sp(14)
        self.size_hint_y = None
        self.height = dp(45)


# ---------- WORD BUILDING GAME ----------
class WordGameScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.words = ["apple", "house", "school", "book", "computer", "phone", "table", "chair", "garden", "flower"]
        self.current_word = random.choice(self.words)
        self.selected = ""
        self.letter_buttons = []
        self.build_ui()
    
    def build_ui(self):
        root = MDBoxLayout(
            orientation="vertical",
            md_bg_color=get_color_from_hex(Colors.BACKGROUND)
        )
        
        header = self.create_header("🔤 Build a Word", Colors.SECONDARY)
        root.add_widget(header)
        
        content = MDBoxLayout(
            orientation="vertical",
            padding=[dp(20), dp(20)],
            spacing=dp(20)
        )
        
        # Hint card
        self.hint_card = AnimatedCard(
            size_hint=(1, None),
            height=dp(60),
            elevation=2
        )
        self.hint_card.md_bg_color = get_color_from_hex(Colors.INFO)
        
        self.hint_label = MDLabel(
            text=f"💡 Hint: {len(self.current_word)} letters",
            halign="center",
            valign="center",
            font_size=sp(16),
            bold=True,
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.SURFACE)
        )
        self.hint_card.add_widget(self.hint_label)
        content.add_widget(self.hint_card)
        
        # Current word display
        word_card = AnimatedCard(
            size_hint=(1, None),
            height=dp(120),
            elevation=3
        )
        word_card.md_bg_color = get_color_from_hex(Colors.PRIMARY_LIGHT)
        
        self.answer_label = MDLabel(
            text="",
            halign="center",
            valign="center",
            font_size=sp(48),
            bold=True,
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.SURFACE)
        )
        word_card.add_widget(self.answer_label)
        content.add_widget(word_card)
        
        # Letters section
        content.add_widget(
            MDLabel(
                text="📚 Available Letters:",
                size_hint_y=None,
                height=dp(30),
                font_size=sp(14),
                bold=True,
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
            )
        )
        
        self.letters_box = MDBoxLayout(
            size_hint_y=None,
            height=dp(120),
            spacing=dp(12),
            padding=[dp(10), dp(10)]
        )
        
        letters_scroll = ScrollView(size_hint=(1, None), height=dp(120))
        letters_scroll.add_widget(self.letters_box)
        content.add_widget(letters_scroll)
        
        # Result
        self.result_label = MDLabel(
            text="",
            halign="center",
            font_size=sp(16),
            size_hint_y=None,
            height=dp(40)
        )
        content.add_widget(self.result_label)
        
        # Buttons
        buttons = MDBoxLayout(
            size_hint_y=None,
            height=dp(120),
            spacing=dp(12),
            orientation="vertical"
        )
        
        button_row = MDBoxLayout(spacing=dp(12), size_hint_y=None, height=dp(50))
        
        check_btn = ModernButton(
            text="✓ CHECK",
            md_bg_color=get_color_from_hex(Colors.SUCCESS),
            on_release=lambda x: self.check()
        )
        
        clear_btn = ModernButton(
            text="🗑 CLEAR",
            md_bg_color=get_color_from_hex(Colors.WARNING),
            on_release=lambda x: self.clear_selection()
        )
        
        button_row.add_widget(check_btn)
        button_row.add_widget(clear_btn)
        buttons.add_widget(button_row)
        
        new_word_btn = ModernButton(
            text="🔄 NEW WORD",
            md_bg_color=get_color_from_hex(Colors.PRIMARY),
            on_release=lambda x: self.new_word()
        )
        buttons.add_widget(new_word_btn)
        
        content.add_widget(buttons)
        root.add_widget(content)
        self.add_widget(root)
        
        self.initialize_letters()
    
    def create_header(self, title, color):
        header = AnimatedCard(
            size_hint_y=None,
            height=dp(80),
            elevation=0
        )
        header.md_bg_color = get_color_from_hex(color)
        
        header_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            padding=[dp(10), dp(10)]
        )
        
        back_btn = MDIconButton(
            icon="arrow-left",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            on_release=lambda x: self.go_back()
        )
        
        title_label = MDLabel(
            text=title,
            halign="center",
            font_size=sp(20),
            bold=True,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        
        header_layout.add_widget(back_btn)
        header_layout.add_widget(title_label)
        header_layout.add_widget(Widget(size_hint_x=None, width=dp(48)))
        
        header.add_widget(header_layout)
        return header
    
    def go_back(self):
        if self.manager:
            self.manager.current = "games"
    
    def initialize_letters(self):
        self.letters_box.clear_widgets()
        self.letter_buttons = []
        letters = list(self.current_word)
        random.shuffle(letters)
        
        for letter in letters:
            btn = ModernButton(
                text=letter.upper(),
                font_size=sp(24),
                size_hint=(None, 1),
                width=dp(70),
                md_bg_color=get_color_from_hex(Colors.SECONDARY_LIGHT),
                on_release=lambda x, l=letter: self.add_letter(l)
            )
            self.letters_box.add_widget(btn)
            self.letter_buttons.append(btn)
    
    def add_letter(self, letter):
        self.selected += letter
        self.answer_label.text = self.selected.upper()
        self.animate_letter_add()
    
    def animate_letter_add(self):
        anim = Animation(font_size=sp(54), duration=0.1) + Animation(font_size=sp(48), duration=0.1)
        anim.start(self.answer_label)
    
    def clear_selection(self):
        self.selected = ""
        self.answer_label.text = ""
        self.result_label.text = ""
    
    def check(self):
        if self.selected.lower() == self.current_word:
            self.result_label.text = "🎉 PERFECT! Word built correctly! 🎉"
            self.result_label.text_color = get_color_from_hex(Colors.SUCCESS)
            self.animate_success()
            self.show_success_dialog()
        else:
            self.result_label.text = f"❌ Not quite right. Keep trying!"
            self.result_label.text_color = get_color_from_hex(Colors.DANGER)
            self.animate_error()
    
    def animate_success(self):
        # Animate the answer label instead
        anim = Animation(font_size=sp(54), duration=0.2) + Animation(font_size=sp(48), duration=0.2)
        anim.start(self.answer_label)
    
    def animate_error(self):
        original_color = self.result_label.text_color
        self.result_label.text_color = get_color_from_hex(Colors.DANGER)
        Clock.schedule_once(lambda dt: setattr(self.result_label, 'text_color', original_color), 1)
    
    def show_success_dialog(self):
        dialog = MDDialog(
            title="🎉 Congratulations!",
            text=f"You successfully built the word '{self.current_word.upper()}'!",
            buttons=[
                MDFlatButton(
                    text="NEW WORD",
                    text_color=get_color_from_hex(Colors.SUCCESS),
                    on_release=lambda x: self.new_word_and_close(dialog)
                ),
                MDFlatButton(
                    text="CLOSE",
                    on_release=lambda x: dialog.dismiss()
                ),
            ],
        )
        dialog.open()
    
    def new_word_and_close(self, dialog):
        dialog.dismiss()
        self.new_word()
    
    def new_word(self):
        self.current_word = random.choice(self.words)
        self.clear_selection()
        self.initialize_letters()
        self.hint_label.text = f"💡 Hint: {len(self.current_word)} letters"


# ---------- COLOR REACTION GAME ----------
class ColorGameScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.colors = {
            "RED": "#EF4444",
            "BLUE": "#3B82F6",
            "GREEN": "#10B981",
            "YELLOW": "#F59E0B",
            "PURPLE": "#8B5CF6"
        }
        self.color_names = list(self.colors.keys())
        self.score = 0
        self.streak = 0
        self.build_ui()
        self.new_round()
    
    def build_ui(self):
        root = MDBoxLayout(
            orientation="vertical",
            md_bg_color=get_color_from_hex(Colors.BACKGROUND)
        )
        
        header = self.create_header("🎨 Color Challenge", Colors.SUCCESS)
        root.add_widget(header)
        
        content = MDBoxLayout(
            orientation="vertical",
            padding=[dp(20), dp(20)],
            spacing=dp(20)
        )
        
        # Score card
        score_card = AnimatedCard(size_hint_y=None, height=dp(90), elevation=2)
        score_layout = MDBoxLayout(spacing=dp(20))
        
        self.score_label = MDLabel(
            text="Score: 0",
            halign="center",
            font_size=sp(20),
            bold=True,
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.SUCCESS)
        )
        
        self.streak_label = MDLabel(
            text="🔥 Streak: 0",
            halign="center",
            font_size=sp(20),
            bold=True,
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.WARNING)
        )
        
        score_layout.add_widget(self.score_label)
        score_layout.add_widget(self.streak_label)
        score_card.add_widget(score_layout)
        content.add_widget(score_card)
        
        # Colored word card
        self.word_card = AnimatedCard(
            size_hint=(1, None),
            height=dp(220),
            elevation=4
        )
        self.word_card.md_bg_color = get_color_from_hex(Colors.SURFACE)
        
        self.color_word = MDLabel(
            text="",
            halign="center",
            valign="center",
            font_size=sp(64),
            bold=True
        )
        self.word_card.add_widget(self.color_word)
        content.add_widget(self.word_card)
        
        # Instruction
        content.add_widget(
            MDLabel(
                text="🎯 Choose the COLOR of the text (not the word!)",
                halign="center",
                size_hint_y=None,
                height=dp(30),
                font_size=sp(14),
                bold=True,
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
            )
        )
        
        # Color buttons
        self.color_buttons_box = MDBoxLayout(
            size_hint_y=None,
            height=dp(80),
            spacing=dp(12),
            padding=[dp(10), dp(5)]
        )
        
        for color_name, color_hex in self.colors.items():
            btn = ModernButton(
                text=color_name,
                md_bg_color=get_color_from_hex(color_hex),
                on_release=lambda x, c=color_name: self.check_color(c)
            )
            self.color_buttons_box.add_widget(btn)
        
        content.add_widget(self.color_buttons_box)
        
        # Result
        self.result_label = MDLabel(
            text="",
            halign="center",
            font_size=sp(16),
            size_hint_y=None,
            height=dp(40)
        )
        content.add_widget(self.result_label)
        
        # Skip button
        skip_btn = ModernButton(
            text="⏭ SKIP",
            md_bg_color=get_color_from_hex(Colors.TEXT_DISABLED),
            on_release=lambda x: self.skip_round()
        )
        content.add_widget(skip_btn)
        
        root.add_widget(content)
        self.add_widget(root)
    
    def create_header(self, title, color):
        header = AnimatedCard(
            size_hint_y=None,
            height=dp(80),
            elevation=0
        )
        header.md_bg_color = get_color_from_hex(color)
        
        header_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            padding=[dp(10), dp(10)]
        )
        
        back_btn = MDIconButton(
            icon="arrow-left",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            on_release=lambda x: self.go_back()
        )
        
        title_label = MDLabel(
            text=title,
            halign="center",
            font_size=sp(20),
            bold=True,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        
        header_layout.add_widget(back_btn)
        header_layout.add_widget(title_label)
        header_layout.add_widget(Widget(size_hint_x=None, width=dp(48)))
        
        header.add_widget(header_layout)
        return header
    
    def go_back(self):
        if self.manager:
            self.manager.current = "games"
    
    def new_round(self):
        self.current_word = random.choice(self.color_names)
        self.current_color = random.choice(list(self.colors.values()))
        
        self.color_word.text = self.current_word
        self.color_word.color = get_color_from_hex(self.current_color)
        self.result_label.text = ""
    
    def skip_round(self):
        self.streak = 0
        self.streak_label.text = f"🔥 Streak: {self.streak}"
        self.new_round()
    
    def check_color(self, selected_color):
        correct_color = [name for name, hex_val in self.colors.items() 
                        if hex_val == self.current_color][0]
        
        if selected_color == correct_color:
            self.score += 1
            self.streak += 1
            self.score_label.text = f"Score: {self.score}"
            self.streak_label.text = f"🔥 Streak: {self.streak}"
            self.result_label.text = f"✅ CORRECT! +1 point (Streak: {self.streak})"
            self.result_label.text_color = get_color_from_hex(Colors.SUCCESS)
            self.animate_success()
            Clock.schedule_once(lambda dt: self.new_round(), 1)
        else:
            self.streak = 0
            self.streak_label.text = f"🔥 Streak: {self.streak}"
            self.result_label.text = f"❌ Wrong! The color was {correct_color}"
            self.result_label.text_color = get_color_from_hex(Colors.DANGER)
            self.animate_error()
    
    def animate_success(self):
        anim = Animation(font_size=sp(72), duration=0.15) + Animation(font_size=sp(64), duration=0.15)
        anim.start(self.color_word)
        
        # Animate score
        anim_score = Animation(font_size=sp(26), duration=0.15) + Animation(font_size=sp(20), duration=0.15)
        anim_score.start(self.score_label)
    
    def animate_error(self):
        original_color = self.word_card.md_bg_color
        self.word_card.md_bg_color = get_color_from_hex(Colors.DANGER)
        Clock.schedule_once(lambda dt: setattr(self.word_card, 'md_bg_color', original_color), 0.3)


# ---------- DIRECTION GAME ENGINE ----------
class DirectionGameEngine:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.time_left = 15
        self.sequence = []
        self.index = 0
    
    def generate(self):
        arrows = ["left", "right", "up", "down"]
        self.sequence = [random.choice(arrows) for _ in range(self.level + 2)]
        self.index = 0
    
    def check(self, direction):
        if direction == self.sequence[self.index]:
            self.index += 1
            self.score += 10
            
            if self.index >= len(self.sequence):
                self.level += 1
                self.time_left += 5
                return "level_complete"
            return "correct"
        return "wrong"
    
    def reset(self):
        self.__init__()
        self.generate()