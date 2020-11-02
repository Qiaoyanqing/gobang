import sys

from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QWidget, QApplication, QLabel, QFrame, QGridLayout, QPushButton


class CalWidget(QWidget):#自定义窗口类，继承QWidget（相当于继承一个空面板）

    def __init__(self):
        #调用父类的构造函数进行初始化
        super().__init__()
        self.setWindowTitle('我的计算器')#从父类继承的方法
        self.resize(600,400)

        self.pre_text = ''#记录上一次的按钮信息
        self.op = ''#记录操作符
        self.num = '' #记录第一个操作数

        # 构造按钮布局
        layout = QGridLayout()

        self.content_text = QLabel('0',self)
        # 设置字体
        font = QFont()
        font.setPointSize(30)
        self.content_text.setFont(font)
        self.content_text.setAlignment(Qt.AlignRight)#对齐方式
        self.content_text.setMaximumHeight(50)#最大高度

        # 设置边框
        self.content_text.setFrameStyle(QFrame.Box)
        layout.addWidget(self.content_text,0,0,1,4)# 行坐标 列坐标  跨行 跨列 默认为1

        # 定义按钮
        btn_list = [
            ('AC',(2,0)),('+/-',(2,1)),('%',(2,2)),('/',(2,3)), #AC 行坐标为2，列坐标为0（及第三行第一列）跨1行，跨一列
            ('7', (3,0)),('8',(3,1)),('9',(3,2)),('*',(3,3)),
            ('4', (4,0)),('5',(4,1)),('6',(4,2)),('-',(4,3)),
            ('1', (5,0)),('2',(5,1)),('3',(5,2)),('+',(5,3)),
            ('0', (6,0,1,2)),('.',(6,2)),('=',(6,3))#0 第七行，第一列，跨一行两列
        ]
        # 添加按钮
        for btn in btn_list:
            new_btn = QPushButton(btn[0],self)
            new_btn.setMinimumHeight(30)#固定高度
            new_btn.setFont(font)
            # 绑定信号处理函数
            new_btn.clicked.connect(self.dealBtnClicked)
            # 按钮添加到布局中
            layout.addWidget(new_btn,*btn[1])

        self.setLayout(layout)

    def dealBtnClicked(self):
        '''
        处理按钮点击
        :return:
        '''
        sender = self.sender()#获取信号的发出对象

        print('{} sss'.format(sender.text()))
        text = sender.text()

        if text == 'AC':
            self.content_text.setText('0')
        elif text.isdigit():
            if self.pre_text.isdigit()or self.pre_text == '.':
                cur_text = self.content_text.text()
                self.content_text.setText(cur_text + text)
            else:
                self.content_text.setText(text)

        elif text == '.':
            cur_text = self.content_text.text()
            if '.' not in cur_text:
                self.content_text.setText(cur_text + text)
                # self.content_text.repaint()
        elif text in ['+','-','*','/']:
            self.op = text#记录第一个运算符
            self.num = self.content_text.text()#记录当前内容  作为第一个操作数
        elif text == '=':
            num2 = self.content_text.text()#当前内容是第二个操作数
            if self.op =='+':
                result = float(self.num) + float(num2)
            elif self.op =='-':
                result = float(self.num) - float(num2)
            elif self.op =='*':
                result = float(self.num) * float(num2)
            elif self.op =='/':
                result = float(self.num) / float(num2)
            self.content_text.setText(str(result))#设置label显示结果

        elif text == '+/-':
            #先获取当前的label内容
            cur_text = self.content_text.text()
            cur_text = str(- float(cur_text))
            #设置label的内容
            self.content_text.setText(cur_text)
            # self.content_text.repaint()
        elif text == '%':
            cur_text = self.content_text.text()
            cur_text = str(float(cur_text)/100)
            self.content_text.setText(cur_text)
            # self.content_text.repaint()
        self.content_text.repaint()  # 重新绘制组件 作用：强制刷新
        self.pre_text = text# 更新记录上一次点击的按钮

if __name__ =="__main__":
    app = QApplication([])

    w = CalWidget()
    w.show()
    sys.exit(app.exec_())