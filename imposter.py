# -*- coding: utf-8 -*-
"""Игра «Кто импостер?» — Kivy-приложение для Android."""

import random
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import platform

if platform in ("android", "ios"):
    Window.fullscreen = "auto"
else:
    Window.size = (400, 700)

# 50 наборов: (общее слово, слово импостера) — слова объединяет что-то общее
WORD_SETS = [
    ("Человек-паук", "Дедпул"),
    ("Кот", "Тигр"),
    ("Кока-кола", "Квас"),
    ("Пицца", "Пирог"),
    ("Москва", "Санкт-Петербург"),
    ("Айфон", "Самсунг"),
    ("Самолёт", "Вертолёт"),
    ("Футбол", "Хоккей"),
    ("Море", "Океан"),
    ("Лето", "Весна"),
    ("Шоколад", "Зефир"),
    ("Собака", "Волк"),
    ("Роза", "Ромашка"),
    ("Кино", "Театр"),
    ("Поезд", "Трамвай"),
    ("Золото", "Серебро"),
    ("Дед Мороз", "Снегурочка"),
    ("Пушкин", "Толстой"),
    ("Шахматы", "Шашки"),
    ("Банан", "Яблоко"),
    ("Микроволновка", "Духовка"),
    ("Носок", "Перчатка"),
    ("Дельфин", "Акула"),
    ("Земля", "Марс"),
    ("Кофе", "Чай"),
    ("Гитара", "Балалайка"),
    ("Тетрадь", "Блокнот"),
    ("Зима", "Осень"),
    ("Пингвин", "Тюлень"),
    ("Карандаш", "Ручка"),
    ("Батон", "Багет"),
    ("Крокодил", "Аллигатор"),
    ("Молоко", "Кефир"),
    ("Треугольник", "Круг"),
    ("Мороженое", "Пирожное"),
    ("Велосипед", "Самокат"),
    ("Балерина", "Фигурист"),
    ("Дуб", "Берёза"),
    ("Пчела", "Оса"),
    ("Диван", "Кресло"),
    ("Снег", "Дождь"),
    ("Оркестр", "Хор"),
    ("Доллар", "Евро"),
    ("Зонт", "Плащ"),
    ("Жираф", "Зебра"),
    ("Уха", "Борщ"),
    ("Лиса", "Шакал"),
    ("Телевизор", "Монитор"),
    ("Утка", "Гусь"),
    ("Наручные часы", "Будильник"),
]

MAX_PLAYERS = 8
MIN_PLAYERS = 2

BG = (0.12, 0.12, 0.16, 1)
ACCENT = (0.95, 0.45, 0.15, 1)
CARD = (0.20, 0.20, 0.26, 1)


def base_button(text, color=ACCENT, height=dp(56), font_size=22):
    return Button(
        text=text,
        background_normal="",
        background_color=color,
        font_size=font_size,
        size_hint=(1, None),
        height=height,
        bold=True,
        color=(1, 1, 1, 1),
    )


class MenuScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = BoxLayout(orientation="vertical", padding=dp(30), spacing=dp(20))
        layout.add_widget(Label(text="КТО ИМПОСТЕР?", font_size=34,
                                size_hint=(1, 0.4), color=(1, 1, 1, 1)))
        layout.add_widget(Label(text="Одно слово для всех.\nОдно — для импостера.",
                                font_size=16, size_hint=(1, 0.2),
                                color=(0.8, 0.8, 0.85, 1)))
        play = base_button("Играть")
        play.bind(on_press=self.go_setup)
        layout.add_widget(play)
        layout.add_widget(Label(size_hint=(1, 1)))
        self.add_widget(layout)

    def go_setup(self, *a):
        self.manager.current = "setup"


class PlayerRow(BoxLayout):
    def __init__(self, setup_screen, **kw):
        super().__init__(orientation="horizontal", size_hint=(1, None),
                         height=dp(52), spacing=dp(8), **kw)
        self.input = TextInput(multiline=False, hint_text="Имя игрока",
                               font_size=18, background_color=CARD,
                               foreground_color=(1, 1, 1, 1),
                               cursor_color=(1, 1, 1, 1), write_tab=False)
        self.add_widget(self.input)
        del_btn = Button(text="✕", size_hint=(None, 1), width=dp(48),
                         background_normal="",
                         background_color=(0.6, 0.2, 0.2, 1),
                         bold=True, font_size=18)
        del_btn.bind(on_press=lambda *a: setup_screen.remove_row(self))
        self.add_widget(del_btn)


class SetupScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.rows = []
        layout = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))

        # Верх: кнопка «Играть» — появляется, когда игроков >= 2 и все имена вписаны
        self.play_btn = base_button("Играть", height=dp(54))
        self.play_btn.bind(on_press=self.start_game)
        self.play_btn.opacity = 0
        self.play_btn.disabled = True
        self.play_btn.size_hint_y = None
        self.play_btn.height = 0  # место займёт только когда появится
        layout.add_widget(self.play_btn)

        # Середина: список игроков
        self.container = GridLayout(cols=1, size_hint_y=None, spacing=dp(8))
        self.container.bind(minimum_height=self.container.setter("height"))
        scroll = ScrollView(bar_width=dp(4))
        scroll.add_widget(self.container)
        layout.add_widget(scroll)

        # Низ: кнопка «+»
        self.add_btn = base_button("+ Добавить игрока")
        self.add_btn.bind(on_press=self.add_row)
        layout.add_widget(self.add_btn)

        self.add_widget(layout)
        self.add_row()  # стартовая строка

    def add_row(self, *a):
        if len(self.rows) >= MAX_PLAYERS:
            return
        row = PlayerRow(self)
        # при вводе имени — обновляем видимость кнопки «Играть»
        row.input.bind(text=lambda instance, value: self.refresh())
        self.rows.append(row)
        self.container.add_widget(row)
        self.refresh()

    def remove_row(self, row):
        if row in self.rows:
            self.rows.remove(row)
            self.container.remove_widget(row)
            self.refresh()

    def refresh(self, *a):
        filled = [r.input.text.strip() for r in self.rows]
        ready = len(filled) >= MIN_PLAYERS and all(filled)
        self.play_btn.opacity = 1 if ready else 0
        self.play_btn.disabled = not ready
        self.play_btn.height = dp(54) if ready else 0
        self.add_btn.disabled = len(self.rows) >= MAX_PLAYERS
        self.add_btn.background_color = (ACCENT if not self.add_btn.disabled
                                         else (0.4, 0.4, 0.4, 1))

    def start_game(self, *a):
        names = [r.input.text.strip() for r in self.rows]
        if len(names) < MIN_PLAYERS or not all(names):
            return
        app = App.get_running_app()
        app.start_new_game(names)
        self.manager.current = "game"

    def on_pre_enter(self, *a):
        self.refresh()


class GameScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.names = []
        self.idx = 0
        layout = BoxLayout(orientation="vertical", padding=dp(24), spacing=dp(20))

        # Имя игрока сверху
        self.name_label = Label(text="", font_size=26, size_hint=(1, 0.12),
                                color=(1, 1, 1, 1))
        layout.add_widget(self.name_label)

        # Центр: закрытая «карточка» со словом
        center = BoxLayout(size_hint=(1, 0.55))
        self.card = Button(text="Нажми, чтобы увидеть слово",
                           background_normal="", background_color=CARD,
                           font_size=18, color=(0.85, 0.85, 0.9, 1))
        self.card.bind(on_press=self.reveal)
        center.add_widget(self.card)
        layout.add_widget(center)

        self.word_label = Label(text="", font_size=30, size_hint=(1, 0.12),
                                color=(1, 1, 1, 1))
        layout.add_widget(self.word_label)

        # Кнопка «Следующий игрок» (после вскрытия) / «Выйти» (после последнего)
        self.next_btn = base_button("Передать следующему игроку")
        self.next_btn.bind(on_press=self.next_player)
        self.next_btn.opacity = 0
        self.next_btn.disabled = True
        layout.add_widget(self.next_btn)

        self.quit_btn = base_button("Выйти в меню")
        self.quit_btn.bind(on_press=self.go_menu)
        self.quit_btn.opacity = 0
        self.quit_btn.disabled = True
        layout.add_widget(self.quit_btn)

        layout.add_widget(Label(size_hint=(1, 0.05)))
        self.add_widget(layout)

    def on_pre_enter(self, *a):
        self.names = App.get_running_app().names
        self.idx = 0
        self.show_player()

    def show_player(self):
        name = self.names[self.idx]
        self.name_label.text = f"Игрок {self.idx + 1} из {len(self.names)}: {name}"
        self.word_label.text = ""
        self.card.text = "Нажми, чтобы увидеть слово"
        self.card.disabled = False
        self.card.background_color = CARD
        self.next_btn.opacity = 0
        self.next_btn.disabled = True
        self.quit_btn.opacity = 0
        self.quit_btn.disabled = True

    def reveal(self, *a):
        app = App.get_running_app()
        if app.is_impostor(self.idx):
            self.card.text = "ТЫ ИМПОСТЕР!"
            self.card.background_color = (0.75, 0.15, 0.15, 1)
            self.word_label.text = f"Твоё слово: {app.current_pair[1]}"
            self.word_label.color = (1, 0.6, 0.6, 1)
        else:
            self.card.text = "Ты в команде"
            self.card.background_color = (0.15, 0.55, 0.25, 1)
            self.word_label.text = f"Твоё слово: {app.current_pair[0]}"
            self.word_label.color = (0.7, 1, 0.75, 1)
        self.card.disabled = True
        if self.idx < len(self.names) - 1:
            self.next_btn.opacity = 1
            self.next_btn.disabled = False
        else:
            self.quit_btn.opacity = 1
            self.quit_btn.disabled = False

    def next_player(self, *a):
        self.idx += 1
        self.show_player()

    def go_menu(self, *a):
        self.manager.current = "menu"


class ImposterApp(App):
    title = "Кто импостер?"

    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MenuScreen(name="menu"))
        self.sm.add_widget(SetupScreen(name="setup"))
        self.sm.add_widget(GameScreen(name="game"))
        return self.sm

    def start_new_game(self, names):
        self.names = names
        self.pair = random.choice(WORD_SETS)
        # Один случайный игрок — импостер
        self.impostor_idx = random.randrange(len(names))

    def is_impostor(self, idx):
        return idx == self.impostor_idx

    @property
    def current_pair(self):
        return self.pair


if __name__ == "__main__":
    ImposterApp().run()
