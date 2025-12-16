import arcade
import random  # для извлечения случайной реплики персонажа


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Meowdex"

class Player:
    def __init__(self, nickname):
        self.nickname = nickname
        self.level = 0
        self.fish_cnt = 0
        self.streak = 0  # серия побед


class Character:
    def __init__(self, name, personality):
        self.name = name
        self.dialogues = '../characters/dialogues.json'  # путь до реплик определённого персонажа

    def get_dialogue(self, situation):
        pass  # возвращает случайную реплику для ситуации


class Word:
    def __init__(self, word, category, difficulty):
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
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)
        self.texture = arcade.load_texture("../../images/background/blue_shtori.jpg")

    def setup(self):
        pass

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(SCREEN_WIDTH // 2,
                                                                SCREEN_HEIGHT // 2,
                                                                SCREEN_WIDTH,
                                                                SCREEN_HEIGHT))



def main():
    game = MainWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()