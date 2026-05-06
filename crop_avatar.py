from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class CropWindow(QDialog):
    cropped = pyqtSignal(QPixmap)

    def __init__(self, path):
        super().__init__()
        self.setWindowTitle("裁剪头像")
        self.setFixedSize(800, 650)  # 固定窗口大小，底部有足够空间放按钮
        self.setStyleSheet("background-color: #1E1E1E;")

        # 核心参数
        self.original_pix = QPixmap(path)
        self.scale_factor = 1.0
        self.min_scale = 0.5
        self.max_scale = 4.0
        self.crop_radius = 200  # 固定裁剪圆半径（头像大小）
        self.dragging = False
        self.last_pos = QPoint()

        # 1. 创建场景和视图（关键：加滚动条）
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setDragMode(QGraphicsView.NoDrag)  # 手动控制拖拽
        self.view.setStyleSheet("border: none; background: transparent;")
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # 需要时显示滚动条
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # 2. 加载图片
        self.pix_item = QGraphicsPixmapItem(self.original_pix)
        self.scene.addItem(self.pix_item)

        # 3. 初始缩放：让图片刚好适应视图，留一点边距
        self.view.fitInView(self.pix_item, Qt.KeepAspectRatio)
        self.scale_factor = self.view.transform().m11()  # 获取当前缩放比例

        # 4. 绘制微信同款圆形遮罩
        self.overlay_item = self._create_overlay()
        self.scene.addItem(self.overlay_item)

        # 5. 按钮布局（确保在窗口底部，绝对可见）
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(30)
        btn_layout.setAlignment(Qt.AlignCenter)  # 居中

        self.confirm_btn = QPushButton("完成")
        self.cancel_btn = QPushButton("取消")

        # 微信同款样式
        self.confirm_btn.setFixedSize(130, 50)
        self.confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #07C160;
                color: white;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #06AE56;
            }
        """)

        self.cancel_btn.setFixedSize(130, 50)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                border-radius: 25px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)

        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.confirm_btn)

        # 6. 主布局（垂直排列，视图在上，按钮在下）
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        main_layout.addWidget(self.view)
        main_layout.addLayout(btn_layout)  # 按钮固定在最底部

        # 7. 绑定事件
        self.confirm_btn.clicked.connect(self._do_crop)
        self.cancel_btn.clicked.connect(self.reject)
        self.view.wheelEvent = self._wheel_event
        self.view.mousePressEvent = self._mouse_press
        self.view.mouseMoveEvent = self._mouse_move
        self.view.mouseReleaseEvent = self._mouse_release

    def _create_overlay(self):
        """创建微信同款圆形遮罩（中间透明，四周半透明）"""
        overlay = QPixmap(self.view.size())
        overlay.fill(Qt.transparent)
        painter = QPainter(overlay)
        painter.setRenderHint(QPainter.Antialiasing)

        # 1. 绘制半透明黑色背景
        painter.fillRect(overlay.rect(), QColor(0, 0, 0, 150))

        # 2. 绘制中间透明圆形区域
        center = overlay.rect().center()
        painter.setCompositionMode(QPainter.CompositionMode_Clear)
        painter.drawEllipse(center, self.crop_radius, self.crop_radius)

        # 3. 绘制白色圆形边框
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        painter.setPen(QPen(Qt.white, 3))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(center, self.crop_radius, self.crop_radius)

        painter.end()
        return QGraphicsPixmapItem(overlay)

    def _wheel_event(self, event):
        """滚轮缩放：锚点在鼠标位置"""
        delta = event.angleDelta().y()
        factor = 1.15 if delta > 0 else 0.85
        new_scale = self.scale_factor * factor

        if self.min_scale <= new_scale <= self.max_scale:
            self.scale_factor = new_scale
            self.view.scale(factor, factor)

            # 缩放后重新移动遮罩到中心
            self.overlay_item.setPos(0, 0)
            self.overlay_item = self._create_overlay()
            self.scene.addItem(self.overlay_item)

        event.accept()

    def _mouse_press(self, event):
        """开始拖拽"""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.last_pos = event.pos()
        super().mousePressEvent(event)

    def _mouse_move(self, event):
        """移动画面"""
        if self.dragging:
            delta = event.pos() - self.last_pos
            self.view.horizontalScrollBar().setValue(
                self.view.horizontalScrollBar().value() - delta.x()
            )
            self.view.verticalScrollBar().setValue(
                self.view.verticalScrollBar().value() - delta.y()
            )
            self.last_pos = event.pos()
        super().mouseMoveEvent(event)

    def _mouse_release(self, event):
        """结束拖拽"""
        self.dragging = False
        super().mouseReleaseEvent(event)

    def _do_crop(self):
        """最终裁剪：截取中间圆形区域"""
        # 1. 获取视图中心和当前缩放比例
        view_center = self.view.viewport().rect().center()
        scene_center = self.view.mapToScene(view_center)

        # 2. 计算裁剪区域在原图的大小
        actual_radius = self.crop_radius / self.scale_factor

        # 3. 截取正方形区域
        src_rect = QRectF(
            scene_center.x() - actual_radius,
            scene_center.y() - actual_radius,
            actual_radius * 2,
            actual_radius * 2
        )

        # 4. 复制并生成圆形头像
        cropped_pix = self.original_pix.copy(src_rect.toRect())

        circle_pix = QPixmap(cropped_pix.size())
        circle_pix.fill(Qt.transparent)

        painter = QPainter(circle_pix)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setClipRegion(QRegion(QRect(0, 0, circle_pix.width(), circle_pix.height()), QRegion.Ellipse))
        painter.drawPixmap(0, 0, cropped_pix)
        painter.end()

        self.cropped.emit(circle_pix)
        self.accept()