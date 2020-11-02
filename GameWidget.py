import sys

import PySide2
from PySide2.QtGui import *
from PySide2.QtMultimedia import QSound
from PySide2.QtWidgets import *
from PySide2.QtCore import *

from Chessman import Chessman
from MyButton import MyButton


class GameWidget(QWidget):
    # 返回
    goback_signal = Signal()
    # 开始
    start_signal = Signal()
    # 悔棋
    regret_signal = Signal()
    # 认输
    lose_signal = Signal()
    # 落子
    position_signal = Signal(tuple)


    def __init__(self,parent=None):

        super(GameWidget,self).__init__( parent = parent)

        self.setWindowTitle('我的五子棋')

        self.setWindowIcon(QIcon('source/icon.icon'))

        # 设置背景图片
        p = QPalette(self.palette())  # 获得当前的调色板
        brush = QBrush(QImage('source/游戏界面.png'))
        p.setBrush(QPalette.Background, brush)  # 设置调色板
        self.setPalette(p)  # 给窗口设置调色板

        self.setFixedSize(QImage('source/游戏界面.png').size())

        self.start_button = MyButton(self, 'source/开始按钮_hover.png', 'source/开始按钮_normal.png', 'source/开始按钮_press.png')
        self.start_button.move(650,200)
        self.start_button.clicked_signal.connect(self.start_signal)

        self.goback_button = MyButton(self,'source/返回按钮_hover.png','source/返回按钮_normal.png','source/返回按钮_press.png')
        self.goback_button.move(660,60)
        self.goback_button.clicked_signal.connect(self.goback_signal)

        self.regret_button = MyButton(self, 'source/悔棋按钮_hover.png', 'source/悔棋按钮_normal.png', 'source/悔棋按钮_press.png')
        self.regret_button.move(650,300)
        self.regret_button.clicked_signal.connect(self.regret_signal)

        self.lose_button = MyButton(self, 'source/认输按钮_hover.png', 'source/认输按钮_normal.png', 'source/认输按钮_press.png')
        self.lose_button.move(650,400)
        self.lose_button.clicked_signal.connect(self.lose_signal)

        # 落子标识
        self.focus_point = QLabel(self)
        self.focus_point.setPixmap(QPixmap('source/标识.png'))
        self.focus_point.hide() # 隐藏

        # 获胜
        self.win_lbl = QLabel(self)
        # self.win_lbl.setPixmap((QPixmap('source/黑棋获胜.png')))
        self.win_lbl.hide()

        # 存储棋盘上的棋子
        self.chessman_list = []

    # 重置棋盘
    def reset(self):
        for i in range(len(self.chessman_list))[::-1]:# 下标逆序
            self.chessman_list[i].close() # 关闭棋子显示
            del self.chessman_list[i] # 删除棋子
        self.focus_point.hide()
        self.win_lbl.hide()

    # 处理鼠标释放时间
    def mouseReleaseEvent(self, event:PySide2.QtGui.QMouseEvent):
        coord_x = event.x() # 获得鼠标X坐标
        coord_y = event.y() # 获得鼠标Y坐标
        # print('zuobiao{} {}'.format(coord_x,coord_y))
        # 坐标转换位置
        pos = self.reverse_to_position((coord_x,coord_y))
        # 如果位置有效，发送落子信号
        if pos is None:
            return
        else:
            self.position_signal.emit(pos)

    # 将落子位置转化为坐标
    def reverse_to_coordinate(self,position):
        # 落子范围（0-18）
        x = 50 + position[0] * 30
        y = 50 + position[1] * 30

        return (x,y)

    # 将坐标转化为落子位置
    def reverse_to_position(self,coordinate:tuple):
        # 判断落子位置是否有效
        # 棋盘落子范围：左>35,上>35,右>590+15,下>590+15
        x = coordinate[0]
        y = coordinate[1]
        if x <= 35 or x >= 590+15 or y <= 35 or y >= 590+15:
            return
        # 将坐标转化为落子位置
        # 思路：相对于35坐标，向右偏移 x 个30的宽度
        pos_x = (x - 35) // 30
        pos_y = (y - 35) // 30
        return (pos_x,pos_y)

    # 落子
    def down_chess(self,position,color):
        # position 落子位置
        # color 落子颜色

        # 构建一个棋子
        chessman = Chessman(color,self)

        coord = QPoint(*self.reverse_to_coordinate(position))#QPoint 传两个参数，但是position只是一个元组，所以用*展开元组
        # 将位置转换成坐标
        chessman.move(coord)

        chessman.show()
        chessman.raise_()

        # 落子后构造声音
        QSound.play('source/luozisheng.wav')

        # 将棋子放到当前在棋子列表中
        self.chessman_list.append(chessman)
        # 显示棋子标识
        self.focus_point.move(coord.x()-15,coord.y()-15)# 用x()代替 int x，及用（） 代替int
        # 显示标识
        self.focus_point.show()
        # 让标识在上层显示
        self.focus_point.raise_()

    # 悔棋
    def goback(self):

        # 棋盘没有棋子，返回函数
        if len(self.chessman_list) == 0:
            return
        else:
            # 获得最后一个棋子
            chessman = self.chessman_list.pop()
            # 从界面上删除棋子
            chessman.close()
            # 销毁棋子对象
            del chessman
            # 隐藏标识
            # self.focus_point.move(chessman-15)
            self.focus_point.hide()

    # 显示获胜结果
    def show_win(self,color):

        if color == 'White':
            self.win_lbl.setPixmap(QPixmap('source/白棋胜利.png'))
            self.win_lbl.raise_()
        else:
            self.win_lbl.setPixmap(QPixmap('source/黑棋胜利.png'))
            self.win_lbl.raise_()
        self.win_lbl.move(50,50)
        self.win_lbl.show()



if __name__ == '__main__':
    app = QApplication([])
    w = GameWidget()


    def print_position(position):
        print(position)
        w.down_chess(position,'black')
    w.regret_signal.connect(w.goback)
    w.start_signal.connect(w.reset)

    w.position_signal.connect(print_position)
    # w.show_win('white')
    # w.down_chess((15,15),'black')
    w.show()
    sys.exit(app.exec_())