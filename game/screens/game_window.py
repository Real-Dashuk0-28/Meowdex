import arcade
import random  # для извлечения случайной реплики персонажа


SCREEN_TITLE = "Meowdex"

class Player:
    def __init__(self, nickname):
        self.nickname = nickname
        self.level = 0
        self.fish_cnt = 0
        self.streak = 0  # серия побед


class Character:
    def __init__(self, name):
        self.name = name
        self.dialogues = '../characters/dialogues.json'  # путь до реплик определённого персонажа

    def get_dialogue(self, situation):
        pass  # возвращает случайную реплику для ситуации


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


class MainWindow(arcade.Window):
    def __init__(self, title):
        self.background_texture = arcade.load_texture("../../images/background/blue_shtori.jpg")
        texture_width = self.background_texture.width
        texture_height = self.background_texture.height

        super().__init__(texture_width, texture_height, title, resizable=True)

        # сохраняем исходные размеры картинки
        self.texture_width = texture_width
        self.texture_height = texture_height

        self.logo_texture = arcade.load_texture("../../images/logo/logo.png")

        self.play_btn_texture = arcade.load_texture("../../images/button/play_btn.png")
        self.rating_btn_texture = arcade.load_texture("../../images/button/rating_btn.png")
        self.settings_btn_texture = arcade.load_texture("../../images/button/settings_btn.png")
        self.exit_btn_texture = arcade.load_texture("../../images/button/exit_btn.png")

    def setup(self):
        pass

    def on_draw(self):
        self.clear()

        # окно ШИРЕ заднего фона
        if (self.width / self.height) > (self.texture_width / self.texture_height):
            draw_width = self.texture_width * (self.height / self.texture_height)
            draw_height = self.height
        # окно УЖЕ заднего фона
        else:
            draw_width = self.width
            draw_height = self.texture_height * (self.width / self.texture_width)

        # рисуем задний фон
        arcade.draw_texture_rect(self.background_texture,
                                 arcade.rect.XYWH(self.width // 2,
                                                  self.height // 2,
                                                  draw_width,
                                                  draw_height))

        # высота логотипа - 1/3 высоты экрана
        logo_height = self.height / 3
        logo_width = self.logo_texture.width * (logo_height / self.logo_texture.height)
        logo_y = self.height - (logo_height // 2)

        # рисуем логотип
        arcade.draw_texture_rect(self.logo_texture,
                                 arcade.rect.XYWH(self.width // 2,
                                                  logo_y,
                                                  logo_width,
                                                  logo_height))

        btn_height = self.height / 10
        start_y = self.height // 1.8  # позиция первой кнопки
        spacing = btn_height * 1.2  # расстояние между кнопками

        # список текстур кнопок
        buttons = (self.play_btn_texture,
                   self.rating_btn_texture,
                   self.settings_btn_texture,
                   self.exit_btn_texture)

        # рисуем все кнопки
        for i, texture in enumerate(buttons):
            # сохраняем пропорции кнопки
            btn_width = texture.width * (btn_height / texture.height)

            # вычисляем позицию y для каждой кнопки
            # первая кнопка на start_y, каждая следующая ниже
            btn_y = start_y - (i * spacing)

            # отрисовка
            arcade.draw_texture_rect(texture,
                                     arcade.rect.XYWH(self.width // 2,
                                                      btn_y,
                                                      btn_width,
                                                      btn_height))

    def on_key_press(self, key, modifiers):
        # переключение полноэкранного режима по нажатию F11/Escape
        if key == arcade.key.F11:
            # self.fullscreen - св-во arcade, которое показывает текущий режим
            # set_fullscreen() - метод для изменения режима
            self.set_fullscreen(not self.fullscreen)

        elif key == arcade.key.ESCAPE and self.fullscreen:
            self.set_fullscreen(False)


def main():
    game = MainWindow(SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()