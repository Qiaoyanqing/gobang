
import sys
from PySide2.QtCore import QObject
from PySide2.QtWidgets import QApplication

from DoublePlayer import DoublePlayer
from MuneWidget import MenuWidget
from SinglePlayer import SinglePlayer


class Main(QObject):

    def __init__(self):
        super().__init__()
        self.menu_widget = MenuWidget()

        # 绑定菜单按钮点击信号
        self.menu_widget.single_clicked.connect(self.start_single_player)
        self.menu_widget.double_clicked.connect(self.start_double_player)
        self.menu_widget.network_clicked.connect(self.start_network_player)


        self.double_player = DoublePlayer()
        self.double_player.exit_clicked.connect(self.start_program)

        self.single_player = SinglePlayer()
        self.single_player.exit_clicked.connect(self.start_program)
        # self.network_player = NetworkPlayer()

    def start_program(self):
        self.menu_widget.show()
        # self.menu_widget.hide()

    def start_single_player(self):
        self.single_player.start_game()
        # 隐藏主菜单
        self.menu_widget.hide()

    def start_double_player(self):

        self.double_player.start_game()
        # 隐藏主菜单
        self.menu_widget.hide()

    def start_network_player(self):
        pass

if __name__ == '__main__':
    app = QApplication([])
    main = Main()
    main.start_program()
    sys.exit(app.exec_())