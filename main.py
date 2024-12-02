import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QMessageBox
from PyQt5.QtCore import Qt

test = 1

# moving with [h, j, k, l]

class Game15(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Игра в 15'
        self.size = 400
        self.grid_size = 4
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, self.size, self.size)
        self.layout = QGridLayout()
        self.buttons = []

        numbers = list(range(1, self.grid_size * self.grid_size)) + [None]
        if not test:
            random.shuffle(numbers)
        i = numbers.index(None)
        self.empty_pos = (i//4, i%4)

        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                number = numbers[i * self.grid_size + j]
                button = QPushButton(str(number) if number is not None else '')
                button.setFixedSize(100, 100)
                button.setStyleSheet("font-size: 24px;")
                self.layout.addWidget(button, i, j)
                row.append(button)
            self.buttons.append(row)

        self.setLayout(self.layout)

    def keyPressEvent(self, event):
        # if event.key() == Qt.Key_Up:
        if event.key() == 75:
            self.move_to_empty((self.empty_pos[0] + 1, self.empty_pos[1]))
        # elif event.key() == Qt.Key_Down:
        elif event.key() == 74:
            self.move_to_empty((self.empty_pos[0] - 1, self.empty_pos[1]))
        # elif event.key() == Qt.Key_Left:
        elif event.key() == 72:
            self.move_to_empty((self.empty_pos[0], self.empty_pos[1] + 1))
        # elif event.key() == Qt.Key_Right:
        elif event.key() == 76:
            self.move_to_empty((self.empty_pos[0], self.empty_pos[1] - 1))
        if self.check_win():
            QMessageBox.information(self, 'Поздравляем!', 'Вы выиграли!')
            exit(0)

    def move_to_empty(self, pos):
        if 0 <= pos[0] < self.grid_size and 0 <= pos[1] < self.grid_size:
            if self.is_adjacent(pos, self.empty_pos):
                self.swap_buttons(pos, self.empty_pos)
                self.empty_pos = pos

    def get_button_position(self, button):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.buttons[i][j] == button:
                    return (i, j)

    def is_adjacent(self, pos1, pos2):
        return (abs(pos1[0] - pos2[0]) == 1 and pos1[1] == pos2[1]) or \
               (pos1[0] == pos2[0] and abs(pos1[1] - pos2[1]) == 1)

    def swap_buttons(self, pos1, pos2):
        button1 = self.buttons[pos1[0]][pos1[1]]
        button2 = self.buttons[pos2[0]][pos2[1]]

        self.buttons[pos1[0]][pos1[1]] = button2
        self.buttons[pos2[0]][pos2[1]] = button1

        self.layout.addWidget(button1, pos2[0], pos2[1])
        self.layout.addWidget(button2, pos1[0], pos1[1])

        b1 = button1.text()
        b2 = button2.text()
        button1.setText(b1)
        button2.setText(b2)

    def check_win(self):
        count = 1
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if i == self.grid_size - 1 and j == self.grid_size - 1:
                    return True
                if self.buttons[i][j].text() != str(count):
                    return False
                count += 1
        return True

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game15()
    game.show()
    sys.exit(app.exec_())

