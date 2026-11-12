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

# 150 наборов «слова»: (общее слово, слово импостера)
WORD_SETS = [
    ("Кот", "Тигр"),
    ("Кока-кола", "Пепси"),
    ("Пицца", "Паста"),
    ("Айфон", "Самсунг"),
    ("Самолёт", "Вертолёт"),
    ("Футбол", "Хоккей"),
    ("Лето", "Весна"),
    ("Шоколад", "Зефир"),
    ("Собака", "Волк"),
    ("Роза", "Тюльпан"),
    ("Кино", "Театр"),
    ("Поезд", "Трамвай"),
    ("Золото", "Серебро"),
    ("Дед Мороз", "Снегурочка"),
    ("Анна Каренина", "Война и мир"),
    ("Шахматы", "Шашки"),
    ("Банан", "Яблоко"),
    ("Микроволновка", "Духовка"),
    ("Носок", "Перчатка"),
    ("Кофе", "Чай"),
    ("Гитара", "Балалайка"),
    ("Тетрадь", "Блокнот"),
    ("Зима", "Осень"),
    ("Карандаш", "Ручка"),
    ("Батон", "Багет"),
    ("Молоко", "Кефир"),
    ("Мороженое", "Пирожное"),
    ("Велосипед", "Самокат"),
    ("Балерина", "Фигурист"),
    ("Пчела", "Оса"),
    ("Диван", "Кресло"),
    ("Снег", "Дождь"),
    ("Оркестр", "Хор"),
    ("Доллар", "Евро"),
    ("Зонт", "Плащ"),
    ("Суп", "Борщ"),
    ("Телевизор", "Монитор"),
    ("Утка", "Гусь"),
    ("Наручные часы", "Будильник"),
    ("Лиса", "Шакал"),
    ("Дельфин", "Акула"),
    ("Крокодил", "Аллигатор"),
    ("Жираф", "Зебра"),
    ("Дуб", "Берёза"),
    ("Шум", "Гром"),
    ("Блузка", "Юбка"),
    ("Телефон", "Наушники"),
    ("Морковь", "Свёкла"),
    ("Торт", "Пирог"),
    ("Аквариум", "Клетка"),
    ("Лодка", "Яхта"),
    ("Стихи", "Песня"),
    ("Книга", "Журнал"),
    ("Ножницы", "Нож"),
    ("Лестница", "Лифт"),
    ("Зеркало", "Окно"),
    ("Молоток", "Гвоздь"),
    ("Малина", "Клубника"),
    ("Такси", "Автобус"),
    ("Рюкзак", "Чемодан"),
    ("Очки", "Контактные линзы"),
    ("Пианино", "Скрипка"),
    ("Свадьба", "Юбилей"),
    ("Учитель", "Тренер"),
    ("Курица", "Индейка"),
    ("Гриб", "Трава"),
    ("Соль", "Перец"),
    ("Клюква", "Брусника"),
    ("Смех", "Улыбка"),
    ("Тень", "Свет"),
    ("Свеча", "Лампа"),
    ("Дым", "Туман"),
    ("Кроссовки", "Ботинки"),
    ("Ужин", "Обед"),
    ("Ложка", "Вилка"),
    ("Подушка", "Одеяло"),
    ("Град", "Иней"),
    ("Портфель", "Сумка"),
    ("Масло", "Маргарин"),
    ("Яичница", "Омлет"),
    ("Гречка", "Рис"),
    ("Макароны", "Лапша"),
    ("Сметана", "Сливки"),
    ("Сахар", "Мёд"),
    ("Чипсы", "Сухарики"),
    ("Жвачка", "Мармелад"),
    ("Компот", "Морс"),
    ("Сок", "Нектар"),
    ("Квас", "Лимонад"),
    ("Пельмени", "Вареники"),
    ("Суши", "Роллы"),
    ("Салат", "Винегрет"),
    ("Сон", "Дрёма"),
    ("Радость", "Счастье"),
    ("Грусть", "Тоска"),
    ("Страх", "Ужас"),
    ("Шёпот", "Крик"),
    ("Барабан", "Бубен"),
    ("Опера", "Балет"),
    ("Мультфильм", "Сериал"),
    ("Радио", "Подкаст"),
    ("Фото", "Видео"),
    ("Селфи", "Портрет"),
    ("Палитра", "Холст"),
    ("Конструктор", "Мозаика"),
    ("Кукла", "Неваляшка"),
    ("Юла", "Волчок"),
    ("Мяч", "Обруч"),
    ("Скакалка", "Бадминтон"),
    ("Йога", "Пилатес"),
    ("Ролики", "Скейтборд"),
    ("Лыжи", "Сноуборд"),
    ("Коньки", "Санки"),
    ("Рыбалка", "Охота"),
    ("Грибы", "Ягоды"),
    ("Ромашка", "Хризантема"),
    ("Одуванчик", "Мать-и-мачеха"),
    ("Кактус", "Алоэ"),
    ("Тополь", "Осина"),
    ("Ель", "Пихта"),
    ("Барсук", "Крот"),
    ("Бобёр", "Ондатра"),
    ("Ёж", "Дикобраз"),
    ("Хомяк", "Морская свинка"),
    ("Попугай", "Канарейка"),
    ("Голубь", "Скворец"),
    ("Страус", "Эму"),
    ("Кенгуру", "Валлаби"),
    ("Панда", "Коала"),
    ("Леопард", "Гепард"),
    ("Слон", "Носорог"),
    ("Антилопа", "Газель"),
    ("Верблюд", "Лама"),
    ("Кит", "Косатка"),
    ("Медуза", "Осьминог"),
    ("Краб", "Креветка"),
    ("Морж", "Нерпа"),
    ("Корабль", "Паром"),
    ("Художник", "Скульптор"),
    ("Певец", "Музыкант"),
    ("Врач", "Медсестра"),
    ("Пожарный", "Спасатель"),
    ("Полицейский", "Шериф"),
    ("Моряк", "Пират"),
    ("Король", "Царь"),
    ("Рыцарь", "Самурай"),
    ("Дракон", "Змей Горыныч"),
    ("Ведьма", "Колдун"),
    ("Робот", "Дрон"),
]

# 100 наборов «места»: (общее место, место импостера)
WORD_SETS_PLACES = [
    ("Москва", "Санкт-Петербург"),
    ("Море", "Океан"),
    ("Пирамида", "Колизей"),
    ("Эйфелева башня", "Пизанская башня"),
    ("Лувр", "Эрмитаж"),
    ("Байкал", "Ладожское озеро"),
    ("Волга", "Днепр"),
    ("Амазонка", "Нил"),
    ("Эверест", "Эльбрус"),
    ("Сахара", "Гоби"),
    ("Америка", "Австралия"),
    ("Токио", "Сеул"),
    ("Париж", "Лондон"),
    ("Рим", "Афины"),
    ("Нью-Йорк", "Чикаго"),
    ("Кремль", "Вестминстерский дворец"),
    ("Венеция", "Амстердам"),
    ("Метро", "Автовокзал"),
    ("Кухня", "Балкон"),
    ("Дачный участок", "Огород"),
    ("Пляж", "Бассейн"),
    ("Деревня", "Город"),
    ("Гостиница", "Хостел"),
    ("Аптека", "Больница"),
    ("Школа", "Университет"),
    ("Детский сад", "Ясли"),
    ("Парк", "Сквер"),
    ("Зоопарк", "Дельфинарий"),
    ("Баня", "Сауна"),
    ("Кинотеатр", "Драмтеатр"),
    ("Стадион", "Каток"),
    ("Аквапарк", "Ледовый дворец"),
    ("Библиотека", "Книжный магазин"),
    ("Музей", "Галерея"),
    ("Рынок", "Супермаркет"),
    ("Бар", "Паб"),
    ("Кофейня", "Чайхана"),
    ("Автобусная остановка", "Троллейбусная остановка"),
    ("Аэропорт", "Вокзал"),
    ("Порт", "Пристань"),
    ("Маяк", "Ветряная мельница"),
    ("Замок", "Крепость"),
    ("Собор", "Церковь"),
    ("Мечеть", "Пагода"),
    ("Оранжерея", "Теплица"),
    ("Сад", "Лесопарк"),
    ("Гараж", "Ангар"),
    ("Спальня", "Прихожая"),
    ("Ванная", "Душевая"),
    ("Подвал", "Чердак"),
    ("Гора", "Холм"),
    ("Вулкан", "Гейзер"),
    ("Пустыня", "Степь"),
    ("Тайга", "Джунгли"),
    ("Тундра", "Лесотундра"),
    ("Река", "Ручей"),
    ("Водопад", "Родник"),
    ("Озеро", "Пруд"),
    ("Болото", "Топь"),
    ("Остров", "Полуостров"),
    ("Мыс", "Скала"),
    ("Пещера", "Грот"),
    ("Каньон", "Овраг"),
    ("Долина", "Ущелье"),
    ("Кратер", "Воронка"),
    ("Северный полюс", "Южный полюс"),
    ("Экватор", "Тропики"),
    ("Африка", "Евразия"),
    ("Антарктида", "Арктика"),
    ("Гренландия", "Исландия"),
    ("Швейцария", "Австрия"),
    ("Япония", "Китай"),
    ("Бразилия", "Аргентина"),
    ("Сочи", "Кисловодск"),
    ("Красная площадь", "Таймс-сквер"),
    ("Статуя Свободы", "Родина-мать"),
    ("Египет", "Мексика"),
    ("Аляска", "Камчатка"),
    ("Хабаровск", "Владивосток"),
    ("Екатеринбург", "Челябинск"),
    ("Казань", "Самара"),
    ("Новосибирск", "Омск"),
    ("Шереметьево", "Домодедово"),
    ("Ботанический сад", "Дендрарий"),
    ("Кемпинг", "Турбаза"),
    ("Спортзал", "Фитнес-клуб"),
    ("Прачечная", "Химчистка"),
    ("Парикмахерская", "Салон красоты"),
    ("Ресторан", "Столовая"),
    ("Ювелирный магазин", "Ломбард"),
    ("Заброшенный дом", "Недострой"),
    ("Бухта", "Лагуна"),
    ("Причал", "Пирс"),
    ("Тропа", "Дорожка"),
    ("Перрон", "Платформа"),
    ("Шоссе", "Проспект"),
    ("Переулок", "Тупик"),
    ("Площадь", "Бульвар"),
    ("Двор", "Аллея"),
    ("Цирк", "Зоопарк"),
]

MAX_PLAYERS = 8
MIN_PLAYERS = 2

ACCENT = (0.95, 0.45, 0.15, 1)
CARD = (0.20, 0.20, 0.26, 1)
GREY = (0.4, 0.4, 0.4, 1)
BLUE = (0.25, 0.45, 0.75, 1)
GREEN = (0.15, 0.55, 0.25, 1)
RED = (0.75, 0.15, 0.15, 1)


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
        self.mode = "words"  # выбранный режим по умолчанию
        layout = BoxLayout(orientation="vertical", padding=dp(30), spacing=dp(20))

        layout.add_widget(Label(text="КТО ИМПОСТЕР?", font_size=34,
                                size_hint=(1, 0.35), color=(1, 1, 1, 1)))
        layout.add_widget(Label(text="Одно слово для всех.\nОдно — для импостера.",
                                font_size=16, size_hint=(1, 0.15),
                                color=(0.8, 0.8, 0.85, 1)))

        play = base_button("Играть")
        play.bind(on_press=self.go_setup)
        layout.add_widget(play)

        layout.add_widget(Label(text="Режим:", font_size=20,
                                size_hint=(1, 0.08), color=(1, 1, 1, 1)))
        mode_row = BoxLayout(size_hint=(1, None), height=dp(52), spacing=dp(12))
        self.mode_places = base_button("1 — Места", color=GREY,
                                       height=dp(52), font_size=20)
        self.mode_words = base_button("2 — Слова", color=ACCENT,
                                      height=dp(52), font_size=20)
        self.mode_places.bind(on_press=self.pick_places)
        self.mode_words.bind(on_press=self.pick_words)
        mode_row.add_widget(self.mode_places)
        mode_row.add_widget(self.mode_words)
        layout.add_widget(mode_row)

        layout.add_widget(Label(size_hint=(1, 1)))
        self.add_widget(layout)

    def pick_places(self, *a):
        self.mode = "places"
        self.mode_places.background_color = ACCENT
        self.mode_words.background_color = GREY

    def pick_words(self, *a):
        self.mode = "words"
        self.mode_words.background_color = ACCENT
        self.mode_places.background_color = GREY

    def go_setup(self, *a):
        app = App.get_running_app()
        app.mode = self.mode
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
        del_btn = Button(text="X", size_hint=(None, 1), width=dp(48),
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

        # Верх: справа кнопка «Перемешать»
        top = BoxLayout(size_hint=(1, None), height=dp(44), spacing=dp(8))
        top.add_widget(Label(size_hint=(1, 1)))  # распорка слева
        self.shuffle_btn = Button(text="Перемешать", background_normal="",
                                  background_color=BLUE, font_size=16,
                                  bold=True, color=(1, 1, 1, 1),
                                  size_hint=(None, 1), width=dp(140))
        self.shuffle_btn.bind(on_press=self.shuffle_players)
        top.add_widget(self.shuffle_btn)
        layout.add_widget(top)

        # Выбор: знаете ли вы, кто импостер
        layout.add_widget(Label(text="Импостер знает, кто он?", font_size=18,
                                size_hint=(1, None), height=dp(24),
                                color=(1, 1, 1, 1)))
        know_row = BoxLayout(size_hint=(1, None), height=dp(48), spacing=dp(12))
        self.know_btn = base_button("1 — Знать", color=ACCENT,
                                    height=dp(48), font_size=18)
        self.not_know_btn = base_button("2 — Не знать", color=GREY,
                                        height=dp(48), font_size=18)
        self.know_btn.bind(on_press=self.pick_know)
        self.not_know_btn.bind(on_press=self.pick_not_know)
        know_row.add_widget(self.know_btn)
        know_row.add_widget(self.not_know_btn)
        layout.add_widget(know_row)

        # Середина: список игроков
        self.container = GridLayout(cols=1, size_hint_y=None, spacing=dp(8))
        self.container.bind(minimum_height=self.container.setter("height"))
        scroll = ScrollView(bar_width=dp(4))
        scroll.add_widget(self.container)
        layout.add_widget(scroll)

        # Низ: кнопка «Играть», под ней «Добавить игрока»
        self.play_btn = base_button("Играть", height=dp(54))
        self.play_btn.bind(on_press=self.start_game)
        self.play_btn.opacity = 0
        self.play_btn.disabled = True
        self.play_btn.size_hint_y = None
        self.play_btn.height = 0
        layout.add_widget(self.play_btn)

        self.add_btn = base_button("+ Добавить игрока")
        self.add_btn.bind(on_press=self.add_row)
        layout.add_widget(self.add_btn)

        self.add_widget(layout)
        self.add_row()

    def pick_know(self, *a):
        App.get_running_app().know = "know"
        self.know_btn.background_color = ACCENT
        self.not_know_btn.background_color = GREY

    def pick_not_know(self, *a):
        App.get_running_app().know = "not_know"
        self.not_know_btn.background_color = ACCENT
        self.know_btn.background_color = GREY

    def add_row(self, *a):
        if len(self.rows) >= MAX_PLAYERS:
            return
        row = PlayerRow(self)
        row.input.bind(text=lambda instance, value: self.refresh())
        self.rows.append(row)
        self.container.add_widget(row)
        self.refresh()

    def remove_row(self, row):
        if row in self.rows:
            self.rows.remove(row)
            self.container.remove_widget(row)
            self.refresh()

    def shuffle_players(self, *a):
        names = [r.input.text.strip() for r in self.rows]
        if len(names) < 2:
            return
        random.shuffle(names)
        for row, name in zip(self.rows, names):
            row.input.text = name

    def refresh(self, *a):
        filled = [r.input.text.strip() for r in self.rows]
        ready = len(filled) >= MIN_PLAYERS and all(filled)
        self.play_btn.opacity = 1 if ready else 0
        self.play_btn.disabled = not ready
        self.play_btn.height = dp(54) if ready else 0
        self.add_btn.disabled = len(self.rows) >= MAX_PLAYERS
        self.add_btn.background_color = ACCENT if not self.add_btn.disabled else GREY
        self.shuffle_btn.disabled = len(self.rows) < 2
        self.shuffle_btn.background_color = BLUE if not self.shuffle_btn.disabled else GREY

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
        self.idx = 0
        layout = BoxLayout(orientation="vertical", padding=dp(24), spacing=dp(20))

        self.name_label = Label(text="", font_size=26, size_hint=(1, 0.12),
                                color=(1, 1, 1, 1))
        layout.add_widget(self.name_label)

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
        if app.know == "know":
            # Импостер знает, кто он: у него красная карточка и надпись
            if app.is_impostor(self.idx):
                self.card.text = "ТЫ ИМПОСТЕР!"
                self.card.background_color = RED
                self.word_label.text = f"Твоё слово: {app.current_pair[1]}"
                self.word_label.color = (1, 0.6, 0.6, 1)
            else:
                self.card.text = "Ты в команде"
                self.card.background_color = GREEN
                self.word_label.text = f"Твоё слово: {app.current_pair[0]}"
                self.word_label.color = (0.7, 1, 0.75, 1)
        else:
            # Импостер не знает, кто он: все видят только слово, без подсказок
            self.card.text = "Твоё слово готово"
            self.card.background_color = CARD
            word = app.current_pair[1] if app.is_impostor(self.idx) else app.current_pair[0]
            self.word_label.text = f"Твоё слово: {word}"
            self.word_label.color = (1, 1, 1, 1)
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
        self.mode = "words"        # режим: words / places
        self.know = "know"         # знать / не знать
        self.sm = ScreenManager()
        self.sm.add_widget(MenuScreen(name="menu"))
        self.sm.add_widget(SetupScreen(name="setup"))
        self.sm.add_widget(GameScreen(name="game"))
        return self.sm

    def start_new_game(self, names):
        self.names = names
        sets = WORD_SETS_PLACES if self.mode == "places" else WORD_SETS
        self.pair = random.choice(sets)
        self.impostor_idx = random.randrange(len(names))

    def is_impostor(self, idx):
        return idx == self.impostor_idx

    @property
    def current_pair(self):
        return self.pair


if __name__ == "__main__":
    ImposterApp().run()
