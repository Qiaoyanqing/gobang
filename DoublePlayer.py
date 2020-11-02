import sys

from PySide2.QtCore import QObject, Signal
from PySide2.QtWidgets import QApplication

from GameCore import GameCore
from GameWidget import GameWidget


class DoublePlayer(QObject):

    exit_clicked = Signal()

    def __init__(self):
        super(DoublePlayer, self).__init__()
        self.game_widget = GameWidget()
        self.game_core = GameCore()
        self.current_color = 'Black'  # 当前落子颜色
        self.is_active = False  # 游戏状态，是否进行中
        self.history = []  # 记录落子位置
        # 绑定游戏窗口信号 到 游戏逻辑处理函数
        self.game_widget.start_signal.connect(self.start_game)
        self.game_widget.goback_signal.connect(self.stop_game)
        self.game_widget.goback_signal.connect(self.exit_menu)

        self.game_widget.regret_signal.connect(self.regret_game)
        self.game_widget.lose_signal.connect(self.lose_game)
        self.game_widget.position_signal.connect(self.down_chess)

    def start_game(self):
        self.init_game()
        self.is_active = True
        self.game_widget.show()

    def exit_menu(self):
        self.game_widget.hide()

    def get_reverse_color(self, color: str):
        '''
        功能函数，获得相反颜色
        '''
        if color == 'Black':
            return 'White'
        else:
            return 'Black'

    def switch_color(self):
        '''
        切换当前棋子颜色
        :return:
        '''
        self.current_color = self.get_reverse_color(self.current_color)



    def stop_game(self):
        self.exit_clicked.emit()

    def init_game(self):
        '''
        对游戏进行初始化
        :return:
        '''
        self.game_widget.reset()# 调用GameWidget的reset方法重置棋盘，从而达到对界面初始化的目的
        self.game_core.init_game()# 初始化棋盘
        self.history.clear()
        self.current_color = 'Black'

    def down_chess(self,position):
        res = self.game_core.down_chessman(position[0],position[1],self.current_color)

        # 判断游戏状态，如果游戏状态为False，返回
        if self.is_active is False:
            return
        # 判断落子是否成功
        if res is None:
            return
        # 添加落子记录
        self.history.append(position)
        # 如果落子成功，在界面上显示棋子
        self.game_widget.down_chess(position,self.current_color)
        # 判断是否获胜
        if res == 'Down':
            # 继续游戏切换颜色
            self.switch_color()
            return
        self.game_win(res)

    def game_win(self,color):
        self.is_active = False # 游戏状态为False
        self.game_widget.show_win(color) # 显示获胜

    def lose_game(self):
        if self.is_active is False:
            return
        self.is_active = False
        self.game_widget.show_win(self.get_reverse_color(self.current_color))

    def regret_game(self):
        if self.is_active  is False:
            return

        # 如果棋盘中的棋子少于1个，不能悔棋
        if len(self.history) < 1:
            return
        # 撤销两个棋子
        # for i in range(2):
        position = self.history.pop()
        res = self.game_core.regret(*position)
        if res is False:
            return
        self.switch_color()
        self.game_widget.goback()



if __name__ == '__main__':
    app = QApplication([])
    game = DoublePlayer()
    game.start_game()
    sys.exit(app.exec_())# 进入死循环