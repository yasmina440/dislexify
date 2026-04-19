from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp

from ai import get_ai_response


class ChatScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = MDBoxLayout(orientation="vertical")

        # ---------- история ----------
        self.scroll = MDScrollView()
        self.chat_box = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            padding=dp(10),
            spacing=dp(15)
        )

        self.scroll.add_widget(self.chat_box)
        self.layout.add_widget(self.scroll)

        # ---------- input ----------
        input_box = MDBoxLayout(
            size_hint_y=None,
            height=dp(60),
            padding=dp(10),
            spacing=dp(10)
        )

        self.input = MDTextField(
            hint_text="Write a message...",
            multiline=False,
            on_text_validate=self.send_message
        )

        send_btn = MDIconButton(
            icon="send",
            on_release=self.send_message
        )

        input_box.add_widget(self.input)
        input_box.add_widget(send_btn)

        self.layout.add_widget(input_box)

        self.add_widget(self.layout)

    def add_message(self, text, is_user=False):
        msg = MDLabel(
            text=("🧑 Ты: " if is_user else "🤖 AI: ") + text,
            adaptive_height=True
        )
        self.chat_box.add_widget(msg)

    def send_message(self, *args):
        text = self.input.text.strip()
        if not text:
            return

        self.add_message(text, True)

        self.input.text = ""
        self.input.focus = True
        
        response = get_ai_response(text)
        self.add_message(response, False)