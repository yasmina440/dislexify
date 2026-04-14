from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton, MDFillRoundFlatButton
from kivymd.uix.progressbar import MDProgressBar
from kivy.metrics import dp
import random
from kivy.uix.button import Button
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


# ---------- PROFESSIONAL COLOR SCHEME ----------
class Colors:
    PRIMARY = "#6366F1"
    PRIMARY_LIGHT = "#818CF8"
    PRIMARY_DARK = "#4F46E5"
    SECONDARY = "#EC4899"
    SECONDARY_LIGHT = "#F472B6"
    SECONDARY_DARK = "#DB2777"
    SUCCESS = "#10B981"
    WARNING = "#F59E0B"
    DANGER = "#EF4444"
    INFO = "#3B82F6"
    BACKGROUND = "#F9FAFB"
    SURFACE = "#FFFFFF"
    SURFACE_VARIANT = "#F3F4F6"
    TEXT_PRIMARY = "#111827"
    TEXT_SECONDARY = "#6B7280"
    TEXT_DISABLED = "#9CA3AF"
    GRADIENT_DYSLEXIA = ["#667EEA", "#764BA2"]
    GRADIENT_ADHD = ["#F093FB", "#F5576C"]
    GRADIENT_AUTISM = ["#4FACFE", "#00F2FE"]
    SHADOW_LIGHT = "#E5E7EB"
    SHADOW_MEDIUM = "#D1D5DB"
    SHADOW_DARK = "#9CA3AF"


# ---------- ENHANCED CARD ----------
class ModernCard(MDCard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.radius = [dp(16)]
        self.elevation = 2
        self.md_bg_color = get_color_from_hex(Colors.SURFACE)
        self.padding = [dp(16), dp(16), dp(16), dp(16)]
        self.ripple_behavior = True


# ---------- ENHANCED DROP SLOT ----------
class DropSlot(MDCard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(130), dp(60))
        self.radius = [dp(12)]
        self.elevation = 1
        self.word = None
        self.chip = None
        self.md_bg_color = get_color_from_hex(Colors.SURFACE_VARIANT)
        
        self.empty_label = MDLabel(
            text="____",
            halign="center",
            valign="center",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_DISABLED),
            font_style="Subtitle1"
        )
        self.add_widget(self.empty_label)

    def set_word(self, chip):
        self.word = chip.word
        self.chip = chip
        chip.pos = self.pos
        self.md_bg_color = get_color_from_hex(Colors.SUCCESS)
        self.empty_label.text = ""
        
        anim = Animation(elevation=4, duration=0.15) + \
               Animation(elevation=2, duration=0.15)
        anim.start(self)

    def clear(self):
        self.word = None
        if self.chip:
            self.chip = None
        self.md_bg_color = get_color_from_hex(Colors.SURFACE_VARIANT)
        self.empty_label.text = "____"
        self.elevation = 1


# ---------- ENHANCED WORD CHIP ----------
class WordChip(Button):
    def __init__(self, word, game, **kwargs):
        super().__init__(**kwargs)
        self.text = word
        self.word = word
        self.game = game
        self.size_hint = (None, None)
        self.size = (dp(130), dp(60))
        
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.color = get_color_from_hex(Colors.SURFACE)
        self.font_size = '18sp'
        self.bold = True
        
        self.start_pos = (0, 0)
        self.bind(pos=self.update_start)
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.update_graphics()
        
    def update_graphics(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*get_color_from_hex(Colors.PRIMARY))
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(12)]
            )

    def update_start(self, *args):
        self.start_pos = self.pos

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self._touch = touch
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if hasattr(self, "_touch") and touch is self._touch:
            self.center_x = touch.x
            self.center_y = touch.y
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if hasattr(self, "_touch") and touch is self._touch:
            self.game.drop(self)
            delattr(self, "_touch")
            return True
        return super().on_touch_up(touch)

    def go_back(self):
        anim = Animation(pos=self.start_pos, duration=0.3, t='out_quad')
        anim.start(self)


# ---------- MAIN GAME MENU ----------
class GameScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.layout = MDBoxLayout(
            orientation="vertical",
            md_bg_color=get_color_from_hex(Colors.BACKGROUND)
        )
        
        header = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(120),
            padding=[dp(20), dp(30), dp(20), dp(20)],
            md_bg_color=get_color_from_hex(Colors.SURFACE)
        )
        
        header.add_widget(
            MDLabel(
                text="🎮 Learning Through Games",
                halign="center",
                font_size="32sp",
                bold=True,
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
            )
        )
        
        header.add_widget(
            MDLabel(
                text="Choose a game to develop your skills",
                halign="center",
                font_size="16sp",
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
            )
        )
        
        self.layout.add_widget(header)
        
        scroll = ScrollView()
        content = MDBoxLayout(
            orientation="vertical",
            padding=[dp(20), dp(10), dp(20), dp(20)],
            spacing=dp(16),
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter('height'))
        
        games = [
            {
                "name": "Build a Sentence",
                "screen": "sentence",
                "icon": "format-list-bulleted",
                "description": "Arrange words to form a correct sentence",
                "color": Colors.PRIMARY,
                "stats": "Level 1-3"
            },
            {
                "name": "Build a Word",
                "screen": "word",
                "icon": "alphabetical",
                "description": "Form a word from scrambled letters",
                "color": Colors.SECONDARY,
                "stats": "Level 1-5"
            },
            {
                "name": "Color Reaction",
                "screen": "color",
                "icon": "palette",
                "description": "Name the color of the word, not its meaning",
                "color": Colors.SUCCESS,
                "stats": "Endless"
            },
            {
                "name": "Direction Arrows",
                "screen": "direction",
                "icon": "compass",
                "description": "Remember and repeat the sequence",
                "color": Colors.WARNING,
                "stats": "Level 1-10"
            }
        ]
        
        for game in games:
            card = ModernCard(
                size_hint=(1, None),
                height=dp(110)
            )
            
            box = MDBoxLayout(spacing=dp(16))
            
            icon_container = MDBoxLayout(
                size_hint=(None, None),
                size=(dp(60), dp(60)),
                md_bg_color=get_color_from_hex(game["color"]),
                radius=[dp(30)]
            )
            icon_container.add_widget(
                MDIcon(
                    icon=game["icon"],
                    font_size="32sp",
                    halign="center",
                    valign="center",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(Colors.SURFACE)
                )
            )
            
            text_box = MDBoxLayout(orientation="vertical", spacing=dp(4))
            text_box.add_widget(
                MDLabel(
                    text=game["name"],
                    font_size="18sp",
                    bold=True,
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
                )
            )
            text_box.add_widget(
                MDLabel(
                    text=game["description"],
                    font_size="14sp",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
                )
            )
            text_box.add_widget(
                MDLabel(
                    text=game["stats"],
                    font_size="12sp",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex(game["color"])
                )
            )
            
            box.add_widget(icon_container)
            box.add_widget(text_box)
            
            card.add_widget(box)
            card.bind(on_release=lambda x, s=game["screen"]: self.navigate_to_game(s))
            content.add_widget(card)
        
        scroll.add_widget(content)
        self.layout.add_widget(scroll)
        self.add_widget(self.layout)
    
    def navigate_to_game(self, screen_name):
        if self.manager:
            self.manager.current = screen_name


# ---------- FIXED SENTENCE BUILDING GAME (Working Drag & Drop) ----------
class SentenceGameScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.correct = ["Do", "you", "have", "toast", "for", "breakfast?"]
        self.slots = []
        self.chips = []
        self.dragging_chip = None
        self.build_modern_ui()
        
    def build_modern_ui(self):
        root = MDBoxLayout(
            orientation="vertical",
            md_bg_color=get_color_from_hex(Colors.BACKGROUND)
        )
        
        header = self.create_header("📝 Build a Sentence")
        root.add_widget(header)
        
        content = MDBoxLayout(
            orientation="vertical",
            padding=[dp(20), dp(20), dp(20), dp(20)],
            spacing=dp(20)
        )
        
        # Progress
        progress_box = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(40),
            spacing=dp(5)
        )
        
        self.progress_bar = MDProgressBar(
            value=0,
            max=len(self.correct),
            size_hint_y=None,
            height=dp(8),
            color=get_color_from_hex(Colors.PRIMARY)
        )
        
        progress_box.add_widget(
            MDLabel(
                text="Progress",
                font_size="12sp",
                theme_text_color="Custom",
                text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
            )
        )
        progress_box.add_widget(self.progress_bar)
        content.add_widget(progress_box)
        
        # Word slots area
        slots_container = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(160)
        )
        
        slots_label = MDLabel(
            text="Drop words here:",
            size_hint_y=None,
            height=dp(30),
            font_size="14sp",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
        )
        slots_container.add_widget(slots_label)
        
        self.slot_box = MDBoxLayout(
            size_hint_y=None,
            height=dp(100),
            spacing=dp(12),
            padding=[dp(10), dp(5)]
        )
        
        self.slots = []
        for i in range(len(self.correct)):
            slot = DropSlot()
            slot.bind(pos=self.on_slot_pos_change)
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
            height=dp(120)
        )
        
        words_label = MDLabel(
            text="Drag these words:",
            size_hint_y=None,
            height=dp(30),
            font_size="14sp",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
        )
        words_container.add_widget(words_label)
        
        self.words_box = MDBoxLayout(
            size_hint_y=None,
            height=dp(70),
            spacing=dp(12),
            padding=[dp(10), dp(5)]
        )
        
        word_scroll = ScrollView(size_hint=(1, None), height=dp(80))
        word_scroll.add_widget(self.words_box)
        words_container.add_widget(word_scroll)
        content.add_widget(words_container)
        
        # Result
        self.result = MDLabel(
            text="",
            halign="center",
            font_size="18sp",
            size_hint_y=None,
            height=dp(50),
            theme_text_color="Custom"
        )
        content.add_widget(self.result)
        
        # Control buttons
        buttons = MDBoxLayout(
            size_hint_y=None,
            height=dp(60),
            spacing=dp(12)
        )
        
        buttons.add_widget(
            MDFillRoundFlatButton(
                text="Check Sentence",
                font_size="16sp",
                md_bg_color=get_color_from_hex(Colors.PRIMARY),
                on_release=lambda x: self.check()
            )
        )
        
        buttons.add_widget(
            MDFillRoundFlatButton(
                text="Restart",
                font_size="16sp",
                md_bg_color=get_color_from_hex(Colors.SURFACE_VARIANT),
                text_color=get_color_from_hex(Colors.TEXT_SECONDARY),
                on_release=lambda x: self.reset()
            )
        )
        
        content.add_widget(buttons)
        root.add_widget(content)
        self.add_widget(root)
        
        self.initialize_words()
    
    def on_slot_pos_change(self, instance, value):
        """Update chip positions when slots move"""
        pass
    
    def create_header(self, title):
        header = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(70),
            padding=[dp(20), dp(10), dp(20), dp(10)],
            md_bg_color=get_color_from_hex(Colors.SURFACE)
        )
        
        back_btn = MDIconButton(
            icon="arrow-left",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_PRIMARY),
            on_release=lambda x: self.go_back()
        )
        
        title_label = MDLabel(
            text=title,
            halign="center",
            font_size="20sp",
            bold=True,
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
        )
        
        header.add_widget(back_btn)
        header.add_widget(title_label)
        header.add_widget(Widget(size_hint_x=None, width=dp(48)))
        
        return header
    
    def go_back(self):
        if self.manager:
            self.manager.current = "games"
    
    def initialize_words(self):
        self.words_box.clear_widgets()
        shuffled = self.correct[:]
        random.shuffle(shuffled)
        
        for w in shuffled:
            chip = WordChip(w, self)
            self.words_box.add_widget(chip)
            self.chips.append(chip)
    
    def drop(self, chip):
        """Called when a chip is dropped"""
        # Find which slot the chip is over
        target_slot = None
        for slot in self.slots:
            if self._is_over_slot(chip, slot) and not slot.word:
                target_slot = slot
                break
        
        if target_slot:
            # Check if this chip is already in a slot
            for s in self.slots:
                if s.chip == chip:
                    return
            
            # Remove from current parent (words_box or another slot)
            if chip.parent:
                chip.parent.remove_widget(chip)
            
            # Place in slot
            target_slot.set_word(chip)
            self.update_progress()
        else:
            # Return to original position if not dropped on a valid slot
            chip.go_back()
    
    def _is_over_slot(self, chip, slot):
        """Check if chip is over a slot"""
        # Get center positions
        chip_center = (chip.center_x, chip.center_y)
        slot_center = (slot.center_x, slot.center_y)
        
        # Calculate distance
        distance = ((chip_center[0] - slot_center[0]) ** 2 + 
                   (chip_center[1] - slot_center[1]) ** 2) ** 0.5
        
        # If within 100 pixels, consider it dropped on the slot
        return distance < dp(100)
    
    def update_progress(self):
        filled = sum(1 for slot in self.slots if slot.word)
        self.progress_bar.value = filled
    
    def check(self):
        # Get words from slots in order
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
        
        # Check if the sentence is correct
        if words == self.correct:
            self.show_result("🎉 Excellent! Perfect sentence!", Colors.SUCCESS)
            # Disable dragging on success
            for slot in self.slots:
                if slot.chip:
                    slot.chip.disabled = True
        else:
            # Show where the mistake is
            mistake_positions = []
            for i, (user_word, correct_word) in enumerate(zip(words, self.correct)):
                if user_word != correct_word:
                    mistake_positions.append(i + 1)
            
            mistake_text = f"❌ Wrong at position(s): {mistake_positions}"
            self.show_result(mistake_text, Colors.DANGER)
    
    def show_result(self, text, color):
        self.result.text = text
        self.result.text_color = get_color_from_hex(color)
        
        self.result.opacity = 0
        anim = Animation(opacity=1, duration=0.3)
        anim.start(self.result)
        Clock.schedule_once(lambda dt: self.clear_result(), 3)
    
    def clear_result(self):
        anim = Animation(opacity=0, duration=0.3)
        anim.start(self.result)
        Clock.schedule_once(lambda dt: setattr(self.result, 'text', ''), 0.3)
    
    def reset(self):
        # Clear all slots and return chips to words_box
        for slot in self.slots:
            if slot.chip:
                chip = slot.chip
                slot.clear()
                # Re-enable chip
                chip.disabled = False
                # Add back to words_box
                self.words_box.add_widget(chip)
                # Animate to new position
                Clock.schedule_once(lambda dt, c=chip: c.go_back(), 0.1)
            slot.clear()
        
        self.result.text = ""
        self.progress_bar.value = 0


# ---------- FIXED DIRECTION ARROWS GAME (Text-based) ----------
class DirectionGameScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine = GameEngine()
        self.timer_event = None
        self._pulsing = False
        self.build_modern_ui()
        self.start_game()

    def build_modern_ui(self):
        root = MDBoxLayout(
            orientation="vertical",
            md_bg_color=get_color_from_hex(Colors.BACKGROUND)
        )

        header = self.create_header("🧭 Direction Arrows")
        root.add_widget(header)

        content = MDBoxLayout(
            orientation="vertical",
            padding=[dp(20), dp(20), dp(20), dp(20)],
            spacing=dp(20)
        )

        # Info panel
        info_card = ModernCard(
            size_hint=(1, None),
            height=dp(80),
            md_bg_color=get_color_from_hex(Colors.SURFACE)
        )

        info_box = MDBoxLayout(spacing=dp(20))

        self.level_label = MDLabel(
            text="Level: 1",
            halign="center",
            font_size="16sp",
            bold=True,
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
        )

        self.score_label = MDLabel(
            text="Score: 0",
            halign="center",
            font_size="16sp",
            bold=True,
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
        )

        self.time_label = MDLabel(
            text="Time: 15",
            halign="center",
            font_size="16sp",
            bold=True,
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.WARNING)
        )

        info_box.add_widget(self.level_label)
        info_box.add_widget(self.score_label)
        info_box.add_widget(self.time_label)

        info_card.add_widget(info_box)
        content.add_widget(info_card)

        # Instruction text
        instruction_label = MDLabel(
            text="Press the button that matches the DIRECTION WORD below:",
            halign="center",
            size_hint_y=None,
            height=dp(30),
            font_size="14sp",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
        )
        content.add_widget(instruction_label)

        # Direction text display (instead of icon)
        self.direction_card = ModernCard(
            size_hint=(1, None),
            height=dp(150),
            md_bg_color=get_color_from_hex(Colors.PRIMARY_LIGHT)
        )

        self.direction_text = MDLabel(
            text="RIGHT",
            halign="center",
            valign="center",
            font_size="56sp",
            bold=True,
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.SURFACE)
        )
        self.direction_card.add_widget(self.direction_text)
        content.add_widget(self.direction_card)

        # Hint
        hint_label = MDLabel(
            text="👇 Press the matching direction button 👇",
            halign="center",
            size_hint_y=None,
            height=dp(30),
            font_size="12sp",
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_SECONDARY)
        )
        content.add_widget(hint_label)

        # Direction buttons with arrows only
        buttons_grid = MDBoxLayout(
            size_hint_y=None,
            height=dp(250),
            spacing=dp(12),
            padding=[dp(20), dp(10)]
        )

        # Left column
        left_col = MDBoxLayout(orientation="vertical", spacing=dp(12))
        left_col.add_widget(Widget())
        left_col.add_widget(self.create_direction_button("←", "left"))
        left_col.add_widget(Widget())

        # Center column
        center_col = MDBoxLayout(orientation="vertical", spacing=dp(12))
        center_col.add_widget(self.create_direction_button("↑", "up"))
        center_col.add_widget(self.create_direction_button("↓", "down"))

        # Right column
        right_col = MDBoxLayout(orientation="vertical", spacing=dp(12))
        right_col.add_widget(Widget())
        right_col.add_widget(self.create_direction_button("→", "right"))
        right_col.add_widget(Widget())

        buttons_grid.add_widget(left_col)
        buttons_grid.add_widget(center_col)
        buttons_grid.add_widget(right_col)

        content.add_widget(buttons_grid)

        # Result
        self.result_label = MDLabel(
            text="",
            halign="center",
            font_size="18sp",
            size_hint_y=None,
            height=dp(40)
        )
        content.add_widget(self.result_label)

        # Restart button
        restart_btn = MDFillRoundFlatButton(
            text="Restart Game",
            size_hint_y=None,
            height=dp(50),
            md_bg_color=get_color_from_hex(Colors.SURFACE_VARIANT),
            text_color=get_color_from_hex(Colors.TEXT_SECONDARY),
            on_release=lambda x: self.reset_game()
        )
        content.add_widget(restart_btn)

        root.add_widget(content)
        self.add_widget(root)

    def create_header(self, title):
        header = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(70),
            padding=[dp(20), dp(10), dp(20), dp(10)],
            md_bg_color=get_color_from_hex(Colors.SURFACE)
        )

        back_btn = MDIconButton(
            icon="arrow-left",
            on_release=lambda x: self.go_back()
        )

        title_label = MDLabel(
            text=title,
            halign="center",
            font_size="20sp",
            bold=True
        )

        header.add_widget(back_btn)
        header.add_widget(title_label)
        header.add_widget(Widget(size_hint_x=None, width=dp(48)))

        return header

    def go_back(self):
        if self.manager:
            if self.timer_event:
                Clock.unschedule(self.timer_event)
            self.manager.current = "games"

    def create_direction_button(self, icon, direction):
        """Create a button with only an arrow (no text)."""
        btn = MDFillRoundFlatButton(
            text=icon,
            font_size="48sp",
            size_hint=(1, 1),
            md_bg_color=get_color_from_hex(Colors.PRIMARY),
            on_release=lambda x, d=direction: self.on_press(d)
        )
        return btn

    def start_game(self):
        self.engine.generate()
        self.update_ui()

        if self.timer_event:
            Clock.unschedule(self.timer_event)

        self.timer_event = Clock.schedule_interval(self.timer, 1)

    def timer(self, dt):
        self.engine.time_left -= 1

        if self.engine.time_left <= 0:
            self.result_label.text = "⏰ Time's up! Game Over!"
            self.result_label.text_color = get_color_from_hex(Colors.DANGER)
            self.reset_game()
            return

        self.update_ui()

    def on_press(self, direction):
        result = self.engine.check(direction)

        if result == "correct":
            self.result_label.text = "✅ Correct!"
            self.result_label.text_color = get_color_from_hex(Colors.SUCCESS)
            self.animate_correct()

        elif result == "wrong":
            needed = self.engine.sequence[self.engine.index]
            self.result_label.text = f"❌ Wrong! You pressed {direction.upper()}, but needed {needed}"
            self.result_label.text_color = get_color_from_hex(Colors.DANGER)
            self.animate_wrong()
            self.reset_game()
            return

        elif result == "level_complete":
            self.result_label.text = f"🎉 Level {self.engine.level-1} Complete! +5 seconds!"
            self.result_label.text_color = get_color_from_hex(Colors.SUCCESS)
            self.animate_level_up()
            self.engine.generate()

        self.update_ui()
        Clock.schedule_once(lambda dt: self.clear_result_if_not_game_over(), 1)

    def clear_result_if_not_game_over(self):
        if "Game Over" not in self.result_label.text:
            self.result_label.text = ""

    def animate_correct(self):
        anim = Animation(font_size="64sp", duration=0.1) + \
               Animation(font_size="56sp", duration=0.1)
        anim.start(self.direction_text)

    def animate_wrong(self):
        # Animate background color of the direction card instead of text color
        original_color = self.direction_card.md_bg_color
        anim = Animation(md_bg_color=get_color_from_hex(Colors.DANGER), duration=0.2) + \
               Animation(md_bg_color=original_color, duration=0.2)
        anim.start(self.direction_card)

    def animate_level_up(self):
        self.direction_card.md_bg_color = get_color_from_hex(Colors.SUCCESS)
        Clock.schedule_once(lambda dt: setattr(self.direction_card, 'md_bg_color',
                                              get_color_from_hex(Colors.PRIMARY_LIGHT)), 0.5)

    def update_ui(self):
        if self.engine.sequence and self.engine.index < len(self.engine.sequence):
            direction = self.engine.sequence[self.engine.index]
            self.direction_text.text = direction.upper()

            color_map = {
                "left": Colors.INFO,
                "right": Colors.SUCCESS,
                "up": Colors.WARNING,
                "down": Colors.SECONDARY
            }
            self.direction_text.text_color = get_color_from_hex(color_map.get(direction, Colors.PRIMARY))

        self.level_label.text = f"Level: {self.engine.level}"
        self.score_label.text = f"Score: {self.engine.score}"
        self.time_label.text = f"Time: {self.engine.time_left}"

        if self.engine.time_left <= 5:
            self.time_label.text_color = get_color_from_hex(Colors.DANGER)
            if not self._pulsing:
                self._pulsing = True
                self.pulse_time_label()
        else:
            self.time_label.text_color = get_color_from_hex(Colors.WARNING)
            self._pulsing = False

    def pulse_time_label(self):
        if self._pulsing:
            anim = Animation(opacity=0.5, duration=0.5) + Animation(opacity=1, duration=0.5)
            anim.repeat = True
            anim.start(self.time_label)

    def reset_game(self):
        if self.timer_event:
            Clock.unschedule(self.timer_event)
            self.timer_event = None

        self.engine.reset()
        self.update_ui()
        self.result_label.text = ""
        self._pulsing = False
        self.start_game()


# ---------- WORD BUILDING GAME ----------
class WordGameScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.words = ["apple", "house", "school", "book", "computer"]
        self.current_word = random.choice(self.words)
        self.selected = ""
        self.build_modern_ui()
    
    def build_modern_ui(self):
        root = MDBoxLayout(
            orientation="vertical",
            md_bg_color=get_color_from_hex(Colors.BACKGROUND)
        )
        
        header = self.create_header("🔤 Build a Word")
        root.add_widget(header)
        
        content = MDBoxLayout(
            orientation="vertical",
            padding=[dp(20), dp(20), dp(20), dp(20)],
            spacing=dp(20)
        )
        
        # Current word card
        word_card = ModernCard(
            size_hint=(1, None),
            height=dp(120),
            md_bg_color=get_color_from_hex(Colors.PRIMARY_LIGHT)
        )
        
        self.answer_label = MDLabel(
            text="",
            halign="center",
            font_size="48sp",
            bold=True,
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.SURFACE)
        )
        word_card.add_widget(self.answer_label)
        content.add_widget(word_card)
        
        # Letters
        self.letters_box = MDBoxLayout(
            size_hint_y=None,
            height=dp(100),
            spacing=dp(12),
            padding=[dp(10), dp(10)]
        )
        
        letters_scroll = ScrollView(size_hint=(1, None), height=dp(100))
        letters_scroll.add_widget(self.letters_box)
        content.add_widget(letters_scroll)
        
        # Result
        self.result_label = MDLabel(
            text="",
            halign="center",
            font_size="18sp",
            size_hint_y=None,
            height=dp(40)
        )
        content.add_widget(self.result_label)
        
        # Buttons
        buttons = MDBoxLayout(
            size_hint_y=None,
            height=dp(60),
            spacing=dp(12)
        )
        
        buttons.add_widget(
            MDFillRoundFlatButton(
                text="Check",
                md_bg_color=get_color_from_hex(Colors.SECONDARY),
                on_release=lambda x: self.check()
            )
        )
        
        buttons.add_widget(
            MDFillRoundFlatButton(
                text="Clear",
                md_bg_color=get_color_from_hex(Colors.SURFACE_VARIANT),
                text_color=get_color_from_hex(Colors.TEXT_SECONDARY),
                on_release=lambda x: self.clear_selection()
            )
        )
        
        buttons.add_widget(
            MDFillRoundFlatButton(
                text="New Word",
                md_bg_color=get_color_from_hex(Colors.SURFACE_VARIANT),
                text_color=get_color_from_hex(Colors.TEXT_SECONDARY),
                on_release=lambda x: self.new_word()
            )
        )
        
        content.add_widget(buttons)
        root.add_widget(content)
        self.add_widget(root)
        
        self.initialize_letters()
    
    def create_header(self, title):
        header = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(70),
            padding=[dp(20), dp(10), dp(20), dp(10)],
            md_bg_color=get_color_from_hex(Colors.SURFACE)
        )
        
        back_btn = MDIconButton(
            icon="arrow-left",
            on_release=lambda x: self.go_back()
        )
        
        title_label = MDLabel(
            text=title,
            halign="center",
            font_size="20sp",
            bold=True
        )
        
        header.add_widget(back_btn)
        header.add_widget(title_label)
        header.add_widget(Widget(size_hint_x=None, width=dp(48)))
        
        return header
    
    def go_back(self):
        if self.manager:
            self.manager.current = "games"
    
    def initialize_letters(self):
        self.letters_box.clear_widgets()
        letters = list(self.current_word)
        random.shuffle(letters)
        
        for letter in letters:
            btn = MDFillRoundFlatButton(
                text=letter.upper(),
                font_size="20sp",
                size_hint=(None, 1),
                width=dp(70),
                md_bg_color=get_color_from_hex(Colors.SECONDARY_LIGHT),
                on_release=lambda x, l=letter: self.add_letter(l)
            )
            self.letters_box.add_widget(btn)
    
    def add_letter(self, letter):
        self.selected += letter
        self.answer_label.text = self.selected.upper()
    
    def clear_selection(self):
        self.selected = ""
        self.answer_label.text = ""
        self.result_label.text = ""
    
    def check(self):
        if self.selected.lower() == self.current_word:
            self.result_label.text = "🎉 Correct! Excellent!"
            self.result_label.text_color = get_color_from_hex(Colors.SUCCESS)
        else:
            self.result_label.text = f"❌ Incorrect! The word was {self.current_word}"
            self.result_label.text_color = get_color_from_hex(Colors.DANGER)
    
    def new_word(self):
        self.current_word = random.choice(self.words)
        self.clear_selection()
        self.initialize_letters()


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
        self.build_modern_ui()
        self.new_round()
    
    def build_modern_ui(self):
        root = MDBoxLayout(
            orientation="vertical",
            md_bg_color=get_color_from_hex(Colors.BACKGROUND)
        )
        
        header = self.create_header("🎨 Color Reaction")
        root.add_widget(header)
        
        content = MDBoxLayout(
            orientation="vertical",
            padding=[dp(20), dp(20), dp(20), dp(20)],
            spacing=dp(20)
        )
        
        # Score
        self.score_label = MDLabel(
            text="Score: 0",
            halign="center",
            font_size="18sp",
            size_hint_y=None,
            height=dp(30),
            bold=True,
            theme_text_color="Custom",
            text_color=get_color_from_hex(Colors.TEXT_PRIMARY)
        )
        content.add_widget(self.score_label)
        
        # Colored word card
        self.word_card = ModernCard(
            size_hint=(1, None),
            height=dp(200),
            md_bg_color=get_color_from_hex(Colors.SURFACE)
        )
        
        self.color_word = MDLabel(
            text="",
            halign="center",
            valign="center",
            font_size="64sp",
            bold=True
        )
        self.word_card.add_widget(self.color_word)
        content.add_widget(self.word_card)
        
        # Input field
        self.input_field = TextInput(
            size_hint_y=None,
            height=dp(60),
            multiline=False,
            font_size="20sp",
            padding=[dp(15), dp(15)],
            background_color=get_color_from_hex(Colors.SURFACE),
            foreground_color=get_color_from_hex(Colors.TEXT_PRIMARY),
            hint_text="Enter the COLOR of the text (not the word)",
            hint_text_color=get_color_from_hex(Colors.TEXT_DISABLED)
        )
        content.add_widget(self.input_field)
        
        # Result
        self.result_label = MDLabel(
            text="",
            halign="center",
            font_size="18sp",
            size_hint_y=None,
            height=dp(40)
        )
        content.add_widget(self.result_label)
        
        # Buttons
        buttons = MDBoxLayout(
            size_hint_y=None,
            height=dp(60),
            spacing=dp(12)
        )
        
        buttons.add_widget(
            MDFillRoundFlatButton(
                text="Check",
                md_bg_color=get_color_from_hex(Colors.SUCCESS),
                on_release=lambda x: self.check()
            )
        )
        
        buttons.add_widget(
            MDFillRoundFlatButton(
                text="Skip",
                md_bg_color=get_color_from_hex(Colors.SURFACE_VARIANT),
                text_color=get_color_from_hex(Colors.TEXT_SECONDARY),
                on_release=lambda x: self.new_round()
            )
        )
        
        content.add_widget(buttons)
        root.add_widget(content)
        self.add_widget(root)
    
    def create_header(self, title):
        header = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(70),
            padding=[dp(20), dp(10), dp(20), dp(10)],
            md_bg_color=get_color_from_hex(Colors.SURFACE)
        )
        
        back_btn = MDIconButton(
            icon="arrow-left",
            on_release=lambda x: self.go_back()
        )
        
        title_label = MDLabel(
            text=title,
            halign="center",
            font_size="20sp",
            bold=True
        )
        
        header.add_widget(back_btn)
        header.add_widget(title_label)
        header.add_widget(Widget(size_hint_x=None, width=dp(48)))
        
        return header
    
    def go_back(self):
        if self.manager:
            self.manager.current = "games"
    
    def new_round(self):
        self.current_word = random.choice(self.color_names)
        self.current_color = random.choice(list(self.colors.values()))
        
        self.color_word.text = self.current_word
        self.color_word.color = get_color_from_hex(self.current_color)
        self.input_field.text = ""
        self.result_label.text = ""
    
    def check(self):
        user_answer = self.input_field.text.strip().upper()
        correct_color = [name for name, hex_val in self.colors.items() 
                        if hex_val == self.current_color][0]
        
        if user_answer == correct_color:
            self.score += 1
            self.score_label.text = f"Score: {self.score}"
            self.result_label.text = "✅ Correct! +1"
            self.result_label.text_color = get_color_from_hex(Colors.SUCCESS)
            Clock.schedule_once(lambda dt: self.new_round(), 1)
        else:
            self.result_label.text = f"❌ Incorrect! Correct answer: {correct_color}"
            self.result_label.text_color = get_color_from_hex(Colors.DANGER)


# ---------- DIRECTION ARROWS GAME ----------
class GameEngine:
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