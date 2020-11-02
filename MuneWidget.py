import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from MyButton import MyButton


class MenuWidget(QWidget):

    # 定义三个信号用于控制人机对战、双人对战和联机对战
    single_clicked = Signal()
    double_clicked = Signal()
    network_clicked = Signal()

    def __init__(self):
        super().__init__()

        # 设置标题
        self.setWindowTitle('我的五子棋')
        # 窗口固定大小
        self.setFixedSize(760, 650)
        # print('111')
        # 设置背景
        p = QPalette(self.palette())  # 获得当前的调色板
        # print('333')
        brush = QBrush(QImage('source/五子棋界面.png'))
        # print('222')
        p.setBrush(QPalette.Background, brush)  # 设置调色板
        self.setPalette(p)  # 给窗口设置调色板

        # 单人模式按钮
        self.single_btn = MyButton(self,'source/人机对战_hover.png','source/人机对战_normal.png','source/人机对战_press.png')
        self.single_btn.move(250,300)
        self.single_btn.show()
        self.single_btn.clicked_signal.connect(self.single_clicked) # 绑定按钮点击信号，当单击对战按钮被点击时，发送single_clicked信号

        # 双人模式
        self.double_btn = MyButton(self,'source/双人对战_hover.png', 'source/双人对战_normal.png', 'source/双人对战_press.png')
        self.double_btn.move(250, 400)
        self.double_btn.show()
        self.double_btn.clicked_signal.connect(self.double_clicked)

        # 联机模式
        self.network_btn = MyButton(self,'source/联机对战_hover.png', 'source/联机对战_normal.png', 'source/联机对战_press.png')
        self.network_btn.move(250, 500)
        self.network_btn.show()
        self.network_btn.clicked_signal.connect(self.network_clicked)

# if __name__ == '__main__':
#     app = QApplication([])
#
#     label1 = QLabel('单机')
#     label2 = QLabel('双人')
#     label3 = QLabel('联机')
#
#     w = MenuWidget()
#
#     w.single_clicked.connect(label1.show)
#     w.double_clicked.connect(label2.show)
#     w.network_clicked.connect(label3.show)
#
#     w.show()
#     sys.exit(app.exec_())