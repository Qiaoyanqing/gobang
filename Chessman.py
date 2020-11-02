import sys

import PySide2
from PySide2.QtCore import QPoint
from PySide2.QtWidgets import QLabel, QApplication
from PySide2.QtGui import QPixmap

class Chessman(QLabel):

    def __init__(self,color = 'black',parent = None):
        super().__init__(parent = parent)
        self.color = color
        self.pic = QPixmap('source/黑子.png')
        if color != 'Black':
            self.pic = QPixmap('source/白子.png')
        self.setPixmap(self.pic)

        self.x = 0
        self.y = 0

    def move(self, point:PySide2.QtCore.QPoint):
        # 调用父类的move方法实现棋子移动
        # 让棋子（及棋子的图片）的中心点移动到坐标位置
        # 但是默认是让棋子的左上角移动到坐标位置
        # 这里棋子的大小为30X30
        super().move(point.x()-15,point.y()-15)

    def set_index(self, x, y):
        self.x = x# 横坐标
        self.y = y# 纵坐标

if __name__ == '__main__':
    app = QApplication([])
    b = Chessman('Black')
    b.move(QPoint(200,300))
    white = Chessman('White')
    white.move(QPoint(100,200))
    white.show()
    b.show()
    sys.exit(app.exec_())