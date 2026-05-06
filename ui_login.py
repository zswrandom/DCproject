import json
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from crop_avatar import CropWindow

USER_DATA_FILE = "user_data.json"
AVATAR_DIR = "avatars"

if not os.path.exists(AVATAR_DIR):
    os.makedirs(AVATAR_DIR)

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("登录 / 注册")
        self.setFixedSize(520, 550)
        self.setStyleSheet("background-color: #F8F9FA;")
        self.user_data = self.load_data()
        self.avatar_pix = None

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)

        title = QLabel("音视频会议系统")
        title.setFont(QFont("微软雅黑", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.user_edit = QLineEdit()
        self.user_edit.setPlaceholderText("用户名")
        self.user_edit.setStyleSheet("padding:12px; border-radius:10px; font-size:14px;")
        layout.addWidget(self.user_edit)

        self.pwd_edit = QLineEdit()
        self.pwd_edit.setPlaceholderText("密码")
        self.pwd_edit.setEchoMode(QLineEdit.Password)
        self.pwd_edit.setStyleSheet("padding:12px; border-radius:10px; font-size:14px;")
        layout.addWidget(self.pwd_edit)

        self.nick_edit = QLineEdit()
        self.nick_edit.setPlaceholderText("昵称")
        self.nick_edit.setStyleSheet("padding:12px; border-radius:10px; font-size:14px;")
        layout.addWidget(self.nick_edit)

        self.avatar_btn = QPushButton("选择头像并裁剪")
        self.avatar_btn.setStyleSheet("background:#673AB7; color:white; padding:10px; border-radius:10px;")
        self.avatar_btn.clicked.connect(self.choose_avatar)
        layout.addWidget(self.avatar_btn)

        btn_layout = QHBoxLayout()
        self.login_btn = QPushButton("登录")
        self.reg_btn = QPushButton("注册")
        self.login_btn.setStyleSheet("background:#2196F3; color:white; padding:12px; border-radius:10px; font-size:14px;")
        self.reg_btn.setStyleSheet("background:#4CAF50; color:white; padding:12px; border-radius:10px; font-size:14px;")
        btn_layout.addWidget(self.login_btn)
        btn_layout.addWidget(self.reg_btn)
        layout.addLayout(btn_layout)

        self.login_btn.clicked.connect(self.login)
        self.reg_btn.clicked.connect(self.register)
        self.setLayout(layout)
        self.current_user = None

    def load_data(self):
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_data(self):
        with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.user_data, f, indent=2, ensure_ascii=False)

    def choose_avatar(self):
        path, _ = QFileDialog.getOpenFileName(filter="Images (*.png *.jpg *.jpeg)")
        if path:
            cw = CropWindow(path)
            cw.cropped.connect(self.on_cropped)
            cw.exec_()

    def on_cropped(self, pix):
        self.avatar_pix = pix

    def login(self):
        u = self.user_edit.text().strip()
        p = self.pwd_edit.text().strip()
        if not u or not p:
            QMessageBox.warning(self, "提示", "用户名密码不能为空")
            return
        if u not in self.user_data or self.user_data[u]["pwd"] != p:
            QMessageBox.warning(self, "提示", "用户名或密码错误")
            return
        self.current_user = u
        self.accept()

    def register(self):
        u = self.user_edit.text().strip()
        p = self.pwd_edit.text().strip()
        n = self.nick_edit.text().strip()
        if not u or not p or not n:
            QMessageBox.warning(self, "提示", "信息不完整")
            return
        if u in self.user_data:
            QMessageBox.warning(self, "提示", "用户已存在")
            return

        path = os.path.join(AVATAR_DIR, f"{u}.png")
        if self.avatar_pix:
            self.avatar_pix.save(path)

        self.user_data[u] = {"pwd": p, "nick": n, "avatar": path}
        self.save_data()
        QMessageBox.information(self, "成功", "注册成功！请登录")