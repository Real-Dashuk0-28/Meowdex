import arcade
import random
import time

SCREEN_TITLE = "Meowdex"


class Player:
    def __init__(self, nickname):
        self.nickname = nickname
        self.level = 0
        self.fish_cnt = 0
        self.streak = 0


class Character:
    def __init__(self, name):
        self.name = name
        self.dialogues = '../characters/dialogues.json'

    def get_dialogue(self, situation):
        pass


class Word:
    def __init__(self, word, difficulty):
        self.word = word.upper()
        self.difficulty = difficulty
        self.length = len(word)


class GameRound:
    def __init__(self, hidden_words, max_attempts):
        self.hidden_words = hidden_words
        self.max_attempts = max_attempts
        self.current_attempt = 0
        self.attempts_history = []
        self.is_completed = False
        self.result = None


class GameManager:
    def __init__(self):
        self.current_player = None
        self.game_mode = None
        self.current_difficulty = None


class Keyboard:
    def __init__(self):
        self.keys = [
            ['Й', 'Ц', 'У', 'К', 'Е', 'Н', 'Г', 'Ш', 'Щ', 'З', 'Х', 'Ъ'],
            ['Ф', 'Ы', 'В', 'А', 'П', 'Р', 'О', 'Л', 'Д', 'Ж', 'Э'],
            ['ENTER', 'Я', 'Ч', 'С', 'М', 'И', 'Т', 'Ь', 'Б', 'Ю', 'BACKSPACE']
        ]


class WordGrid:
    def __init__(self, row, col, cell_size):
        self.row = row
        self.col = col
        self.cell_size = cell_size
        self.grid = [[None for _ in range(col)] for _ in range(row)]


class MainView(arcade.View):
    """Основное меню"""

    def __init__(self):
        super().__init__()

        # Загружаем текстуры
        self.background_texture = arcade.load_texture("../../images/background/blue_shtori.jpg")
        self.logo_texture = arcade.load_texture("../../images/logo/logo.png")
        self.play_btn_texture = arcade.load_texture("../../images/button/play_btn.png")
        self.rating_btn_texture = arcade.load_texture("../../images/button/rating_btn.png")
        self.settings_btn_texture = arcade.load_texture("../../images/button/settings_btn.png")
        self.exit_btn_texture = arcade.load_texture("../../images/button/exit_btn.png")

        self.buttons_hover = {
            "play": False,
            "rating": False,
            "settings": False,
            "exit": False
        }

        # Анимационные переменные
        self.animation_timer = 0.0
        self.animating = False
        self.animation_progress = 0.0
        self.animation_duration = 0.8
        self.button_positions = []
        self.button_targets = []

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.animating = False
        self.animation_progress = 0.0
        self.animation_timer = 0.0

    def on_draw(self):
        self.clear()

        # Рисуем задний фон
        if (self.window.width / self.window.height) > (self.background_texture.width / self.background_texture.height):
            draw_width = self.background_texture.width * (self.window.height / self.background_texture.height)
            draw_height = self.window.height
        else:
            draw_width = self.window.width
            draw_height = self.background_texture.height * (self.window.width / self.background_texture.width)

        # Затемнение фона при анимации
        if self.animating:
            darken_alpha = int(150 * self.animation_progress)
            arcade.draw_texture_rect(self.background_texture,
                                     arcade.rect.XYWH(self.window.width // 2,
                                                      self.window.height // 2,
                                                      draw_width,
                                                      draw_height))
            arcade.draw_rectangle_filled(self.window.width // 2,
                                         self.window.height // 2,
                                         self.window.width,
                                         self.window.height,
                                         (0, 0, 0, darken_alpha))
        else:
            arcade.draw_texture_rect(self.background_texture,
                                     arcade.rect.XYWH(self.window.width // 2,
                                                      self.window.height // 2,
                                                      draw_width,
                                                      draw_height))

        # Логотип
        logo_height = self.window.height / 3
        logo_width = self.logo_texture.width * (logo_height / self.logo_texture.height)
        logo_y = self.window.height - (logo_height // 2)

        logo_alpha = 255
        if self.animating:
            logo_alpha = int(255 * (1 - self.animation_progress))

        arcade.draw_texture_rect(self.logo_texture,
                                 arcade.rect.XYWH(self.window.width // 2,
                                                  logo_y,
                                                  logo_width,
                                                  logo_height),
                                 alpha=logo_alpha)

        btn_height = self.window.height / 10
        start_y = self.window.height // 1.8
        spacing = btn_height * 1.2

        # Список кнопок
        buttons = [
            (self.play_btn_texture, "play"),
            (self.rating_btn_texture, "rating"),
            (self.settings_btn_texture, "settings"),
            (self.exit_btn_texture, "exit")
        ]

        # Рисуем кнопки с учетом анимации
        for i, (texture, btn_type) in enumerate(buttons):
            btn_width = texture.width * (btn_height / texture.height)

            if self.animating:
                if i < len(self.button_positions):
                    start_pos = self.button_positions[i]
                    target_pos = self.button_targets[i]
                    current_y = start_pos + (target_pos - start_pos) * self.animation_progress
                    alpha = int(255 * (1 - self.animation_progress))
                    arcade.draw_texture_rect(texture,
                                             arcade.rect.XYWH(self.window.width // 2,
                                                              current_y,
                                                              btn_width,
                                                              btn_height),
                                             alpha=alpha)
            else:
                btn_y = start_y - (i * spacing)
                if self.buttons_hover[btn_type]:
                    arcade.draw_rectangle_filled(self.window.width // 2, btn_y,
                                                 btn_width * 1.1, btn_height * 1.1,
                                                 arcade.color.GOLDEN_BROWN + (100,))
                arcade.draw_texture_rect(texture,
                                         arcade.rect.XYWH(self.window.width // 2,
                                                          btn_y,
                                                          btn_width,
                                                          btn_height))

    def on_update(self, delta_time):
        if self.animating:
            self.animation_timer += delta_time
            self.animation_progress = self.animation_timer / self.animation_duration

            if self.animation_progress >= 1.0:
                level_view = LevelView()
                self.window.show_view(level_view)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.animating:
            return

        btn_height = self.window.height / 10
        start_y = self.window.height // 1.8
        spacing = btn_height * 1.2

        buttons = ["play", "rating", "settings", "exit"]
        for i, btn_type in enumerate(buttons):
            btn_y = start_y - (i * spacing)
            btn_width = self.play_btn_texture.width * (btn_height / self.play_btn_texture.height)

            if (self.window.width // 2 - btn_width // 2 < x < self.window.width // 2 + btn_width // 2 and
                    btn_y - btn_height // 2 < y < btn_y + btn_height // 2):
                self.buttons_hover[btn_type] = True
            else:
                self.buttons_hover[btn_type] = False

    def on_mouse_press(self, x, y, button, modifiers):
        if self.animating:
            return

        if button == arcade.MOUSE_BUTTON_LEFT:
            btn_height = self.window.height / 10
            start_y = self.window.height // 1.8
            spacing = btn_height * 1.2

            buttons = ["play", "rating", "settings", "exit"]
            for i, btn_type in enumerate(buttons):
                btn_y = start_y - (i * spacing)
                btn_width = self.play_btn_texture.width * (btn_height / self.play_btn_texture.height)

                if (self.window.width // 2 - btn_width // 2 < x < self.window.width // 2 + btn_width // 2 and
                        btn_y - btn_height // 2 < y < btn_y + btn_height // 2):

                    if btn_type == "play":
                        self.animating = True
                        self.animation_timer = 0.0
                        self.animation_progress = 0.0

                        self.button_positions = []
                        self.button_targets = []
                        for j in range(len(buttons)):
                            btn_y_pos = start_y - (j * spacing)
                            self.button_positions.append(btn_y_pos)
                            if j % 2 == 0:
                                target_y = -100
                            else:
                                target_y = self.window.height + 100
                            self.button_targets.append(target_y)
                    elif btn_type == "exit":
                        self.window.close()
                    else:
                        print(f"Нажата кнопка: {btn_type}")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)
        elif key == arcade.key.ESCAPE and self.window.fullscreen:
            self.window.set_fullscreen(False)


class LevelView(arcade.View):

    def __init__(self):
        super().__init__()

        # Загружаем текстуры
        try:
            self.background_texture = arcade.load_texture("../../images/background/blue_shtori_dark.jpg")
        except:
            self.background_texture = arcade.load_texture("../../images/background/blue_shtori.jpg")

        # Загружаем текстуры цепей
        try:
            self.chains1_texture = arcade.load_texture("../../images/background/chains1.png")
            self.chains2_texture = arcade.load_texture("../../images/background/chains2.png")
            self.chains_loaded = True
        except:
            print("Текстуры цепей не найдены. Цепи не будут отображаться.")
            self.chains_loaded = False

        # Загружаем текстуры кнопок уровней
        self.level1_btn = arcade.load_texture("../../images/button/level1_btn.png")
        self.level2_btn = arcade.load_texture("../../images/button/level2_btn.png")
        self.level3_btn = arcade.load_texture("../../images/button/level3_btn.png")
        self.back_btn = arcade.load_texture("../../images/button/exit_btn.png")

        self.buttons_hover = {
            "level1": False,
            "level2": False,
            "level3": False,
            "back": False
        }

        # Анимационные переменные
        self.buttons_appear_start = 0.0
        self.buttons_appear_progress = 0.0
        self.buttons_appear_duration = 0.5

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.buttons_appear_start = time.time()
        self.buttons_appear_progress = 0.0

    def on_draw(self):
        self.clear()

        # Рисуем затемненный фон
        if (self.window.width / self.window.height) > (self.background_texture.width / self.background_texture.height):
            draw_width = self.background_texture.width * (self.window.height / self.background_texture.height)
            draw_height = self.window.height
        else:
            draw_width = self.window.width
            draw_height = self.background_texture.height * (self.window.width / self.background_texture.width)

        arcade.draw_texture_rect(self.background_texture,
                                 arcade.rect.XYWH(self.window.width // 2,
                                                  self.window.height // 2,
                                                  draw_width,
                                                  draw_height))

        # Рисуем цепи
        if self.chains_loaded:
            chain_height = self.window.height * 0.9

            # Левая цепь
            left_chain_width = self.chains1_texture.width * (chain_height / self.chains1_texture.height)
            arcade.draw_texture_rect(self.chains1_texture,
                                     arcade.rect.XYWH(100,
                                                      self.window.height // 2,
                                                      left_chain_width,
                                                      chain_height),
                                     alpha=200)

            # Правая цепь
            right_chain_width = self.chains2_texture.width * (chain_height / self.chains2_texture.height)
            arcade.draw_texture_rect(self.chains2_texture,
                                     arcade.rect.XYWH(self.window.width - 100,
                                                      self.window.height // 2,
                                                      right_chain_width,
                                                      chain_height),
                                     alpha=200)

        # Рисуем кнопки уровней ГОРИЗОНТАЛЬНО в центре экрана
        btn_height = self.window.height / 6
        btn_width = self.level1_btn.width * (btn_height / self.level1_btn.height)
        spacing = btn_width * 1.2
        center_x = self.window.width // 2
        center_y = self.window.height // 2

        # Список кнопок для горизонтального расположения
        level_buttons = [
            (self.level1_btn, "level1", center_x - spacing),
            (self.level2_btn, "level2", center_x),
            (self.level3_btn, "level3", center_x + spacing)
        ]

        # Рисуем кнопки уровней
        for texture, btn_type, btn_x in level_buttons:
            scale = self.buttons_appear_progress
            alpha = int(255 * self.buttons_appear_progress)

            if self.buttons_hover[btn_type] and self.buttons_appear_progress >= 1.0:
                arcade.draw_rectangle_filled(btn_x, center_y,
                                             btn_width * 1.1, btn_height * 1.1,
                                             arcade.color.GOLDEN_BROWN + (100,))

            if scale > 0:
                arcade.draw_texture_rect(texture,
                                         arcade.rect.XYWH(btn_x,
                                                          center_y,
                                                          btn_width * scale,
                                                          btn_height * scale),
                                         alpha=alpha)

        # Кнопка "Назад"
        back_btn_height = self.window.height / 12
        back_btn_y = back_btn_height * 1.2
        back_btn_width = self.back_btn.width * (back_btn_height / self.back_btn.height)

        back_scale = 1.0
        back_alpha = 255
        if self.buttons_appear_progress < 1.0:
            back_progress = max(0, (self.buttons_appear_progress - 0.3) * 1.4)
            back_scale = back_progress
            back_alpha = int(255 * back_progress)

        if self.buttons_hover["back"] and self.buttons_appear_progress >= 1.0:
            arcade.draw_rectangle_filled(self.window.width // 2, back_btn_y,
                                         back_btn_width * 1.1 * back_scale, back_btn_height * 1.1 * back_scale,
                                         arcade.color.GRAY + (100,))

        if back_scale > 0:
            arcade.draw_texture_rect(self.back_btn,
                                     arcade.rect.XYWH(self.window.width // 2,
                                                      back_btn_y,
                                                      back_btn_width * back_scale,
                                                      back_btn_height * back_scale),
                                     alpha=back_alpha)

    def on_update(self, delta_time):
        """Обновление анимации появления кнопок"""
        elapsed_time = time.time() - self.buttons_appear_start
        self.buttons_appear_progress = min(1.0, elapsed_time / self.buttons_appear_duration)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.buttons_appear_progress < 1.0:
            return

        btn_height = self.window.height / 6
        btn_width = self.level1_btn.width * (btn_height / self.level1_btn.height)
        spacing = btn_width * 1.2
        center_x = self.window.width // 2
        center_y = self.window.height // 2

        # Кнопки уровней
        level_buttons = ["level1", "level2", "level3"]
        for i, btn_type in enumerate(level_buttons):
            btn_x = center_x + (i - 1) * spacing
            if (btn_x - btn_width // 2 < x < btn_x + btn_width // 2 and
                    center_y - btn_height // 2 < y < center_y + btn_height // 2):
                self.buttons_hover[btn_type] = True
            else:
                self.buttons_hover[btn_type] = False

        # Кнопка "Назад"
        back_btn_height = self.window.height / 12
        back_btn_y = back_btn_height * 1.2
        back_btn_width = self.back_btn.width * (back_btn_height / self.back_btn.height)

        if (self.window.width // 2 - back_btn_width // 2 < x < self.window.width // 2 + back_btn_width // 2 and
                back_btn_y - back_btn_height // 2 < y < back_btn_y + back_btn_height // 2):
            self.buttons_hover["back"] = True
        else:
            self.buttons_hover["back"] = False

    def on_mouse_press(self, x, y, button, modifiers):
        if self.buttons_appear_progress < 1.0:
            return

        if button == arcade.MOUSE_BUTTON_LEFT:
            btn_height = self.window.height / 6
            btn_width = self.level1_btn.width * (btn_height / self.level1_btn.height)
            spacing = btn_width * 1.2
            center_x = self.window.width // 2
            center_y = self.window.height // 2

            # Проверка нажатия на кнопки уровней
            level_buttons = ["level1", "level2", "level3"]
            for i, btn_type in enumerate(level_buttons):
                btn_x = center_x + (i - 1) * spacing
                if (btn_x - btn_width // 2 < x < btn_x + btn_width // 2 and
                        center_y - btn_height // 2 < y < center_y + btn_height // 2):
                    print(f"Выбран уровень: {btn_type}")
                    # Здесь будет переход к игре на выбранном уровне

            # Проверка нажатия на кнопку "Назад"
            back_btn_height = self.window.height / 12
            back_btn_y = back_btn_height * 1.2
            back_btn_width = self.back_btn.width * (back_btn_height / self.back_btn.height)

            if (self.window.width // 2 - back_btn_width // 2 < x < self.window.width // 2 + back_btn_width // 2 and
                    back_btn_y - back_btn_height // 2 < y < back_btn_y + back_btn_height // 2):
                main_view = MainView()
                self.window.show_view(main_view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            main_view = MainView()
            self.window.show_view(main_view)


class MainWindow(arcade.Window):
    """Главное окно приложения"""

    def __init__(self, title):
        super().__init__(800, 600, title, resizable=True)

    def setup(self):
        main_view = MainView()
        self.show_view(main_view)


def main():
    game = MainWindow(SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()