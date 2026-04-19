from kivy.metrics import dp
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

class Responsive:
    """Класс для адаптивного дизайна"""
    
    @staticmethod
    def get_screen_size():
        """Получить размер экрана"""
        return Window.width, Window.height
    
    @staticmethod
    def is_small_screen():
        """Проверить, является ли экран маленьким (телефон)"""
        return Window.width < 600
    
    @staticmethod
    def is_tablet():
        """Проверить, является ли экран планшетом"""
        return 600 <= Window.width < 1200
    
    @staticmethod
    def is_desktop():
        """Проверить, является ли экран десктопом"""
        return Window.width >= 1200
    
    @staticmethod
    def get_font_size(base_size):
        """Адаптивный размер шрифта"""
        if Responsive.is_small_screen():
            return base_size - 2
        elif Responsive.is_tablet():
            return base_size
        else:
            return base_size + 2
    
    @staticmethod
    def get_padding(base_padding):
        """Адаптивный отступ"""
        if Responsive.is_small_screen():
            return base_padding - 5
        return base_padding
    
    @staticmethod
    def get_card_height(base_height):
        """Адаптивная высота карточки"""
        if Responsive.is_small_screen():
            return base_height - 20
        return base_height
    
    @staticmethod
    def get_grid_cols():
        """Адаптивное количество колонок в сетке"""
        if Responsive.is_small_screen():
            return 1
        elif Responsive.is_tablet():
            return 2
        else:
            return 3

# Импортируем в main.py