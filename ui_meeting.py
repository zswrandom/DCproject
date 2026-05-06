import random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class MeetingUI(QMainWindow):
    def __init__(self, user, data):
        super().__init__()
        self.current_user = user
        self.user_data = data
        self.setWindowTitle("会议系统")
        self.setFixedSize(1200, 800)

        central = QWidget()
        self.setCentralWidget(central)
        self.main_layout = QVBoxLayout(central)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(15)

        self.page_home = self.create_home()
        self.page_meeting = self.create_meeting()
        self.main_layout.addWidget(self.page_home)
        self.main_layout.addWidget(self.page_meeting)
        self.page_meeting.setVisible(False)

    def create_home(self):
        w = QWidget()
        w.setStyleSheet("background-color: #F7F9FA;")
        layout = QVBoxLayout(w)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(40)

        top_layout = QHBoxLayout()
        info = self.user_data[self.current_user]

        avatar_lb = QLabel()
        avatar_lb.setFixedSize(100, 100)
        avatar_lb.setAlignment(Qt.AlignCenter)
        try:
            pix = QPixmap(info['avatar'])
            avatar_lb.setPixmap(pix.scaled(100,100,Qt.KeepAspectRatio,Qt.SmoothTransformation))
        except:
            avatar_lb.setText(info['nick'][0] if info['nick'] else "头")
            avatar_lb.setStyleSheet("""
                background-color: #42A5F5;
                color: white;
                border-radius: 50px;
                border: 3px solid white;
                font-size: 32px;
                font-weight: bold;
            """)

        nick_lb = QLabel(info['nick'])
        nick_lb.setFont(QFont("微软雅黑", 18, QFont.Bold))
        nick_lb.setStyleSheet("""
            color: #2C3E50;
            border: 1px solid #DCDFE6;
            border-radius: 10px;
            padding: 8px 14px;
        """)

        top_layout.addWidget(avatar_lb)
        top_layout.addSpacing(20)
        top_layout.addWidget(nick_lb)
        top_layout.addStretch()
        layout.addLayout(top_layout)

        btn_layout = QVBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)
        btn_layout.setSpacing(25)

        btn_join = QPushButton("加入会议")
        btn_quick = QPushButton("快速会议")

        btn_join.setFixedSize(280, 80)
        btn_quick.setFixedSize(280, 80)
        btn_join.setFont(QFont("微软雅黑", 16, QFont.Bold))
        btn_quick.setFont(QFont("微软雅黑", 16, QFont.Bold))

        btn_join.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 40px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        btn_quick.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 40px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)

        btn_layout.addWidget(btn_join)
        btn_layout.addWidget(btn_quick)
        layout.addLayout(btn_layout)
        layout.addStretch()

        btn_join.clicked.connect(lambda: self.switch_page(True))
        btn_quick.clicked.connect(self.quick_meeting)
        return w

    def create_meeting(self):
        w = QWidget()
        layout = QVBoxLayout(w)
        bar = QHBoxLayout()
        bar.addWidget(QLabel("房间号"))
        self.room_edit = QLineEdit()
        bar.addWidget(self.room_edit)
        bar.addWidget(QLabel("昵称"))
        self.name_edit = QLineEdit(self.user_data[self.current_user]['nick'])
        bar.addWidget(self.name_edit)
        back = QPushButton("返回主页")
        back.clicked.connect(lambda: self.switch_page(False))
        bar.addWidget(back)
        bar.addStretch()
        layout.addLayout(bar)

        video = QFrame()
        video.setStyleSheet("border:1px solid #ddd; border-radius:10px;")
        layout.addWidget(video, stretch=1)

        ctrl = QHBoxLayout()
        for t in ["摄像头", "麦克风", "共享"]:
            b = QPushButton(t)
            b.setFixedSize(150,50)
            ctrl.addWidget(b)
        layout.addLayout(ctrl)
        return w

    def switch_page(self, to_meet):
        self.page_home.setVisible(not to_meet)
        self.page_meeting.setVisible(to_meet)

    def quick_meeting(self):
        self.switch_page(True)
        self.room_edit.setText(str(random.randint(100000,999999)))