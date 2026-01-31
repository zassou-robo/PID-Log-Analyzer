import sys
import os
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
)
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QFont, QColor, QPixmap, QImage
from PySide6.QtWidgets import QScrollArea


class FirstDisplay(QWidget):
    def __init__(self, main_window_callback=None):
        super().__init__()
        self.main_window_callback = main_window_callback
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("PID_Log_Analyzer - スタート画面")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #ffffff;")  # 白背景を明示
        
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # ===== ロゴエリア =====
        logo_frame = QFrame()
        logo_frame.setStyleSheet("border: none; background-color: transparent;")  # 枠を非表示にして背景を透明に
        logo_layout = QVBoxLayout(logo_frame)
        logo_layout.setContentsMargins(0, 0, 0, 0)  # 余白を削除
        
        logo_label = QLabel()
        # プロジェクトルートを基準にしたパスを構築
        logo_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "pictures", "PID_Log_Analyzer_logo.png")
        logo_pixmap = QPixmap(logo_path)
        
        # ロゴが読み込めたかチェック
        if not logo_pixmap.isNull():
            # 画像を読み込めた場合 - 正方形サイズ（150×150）で拡大縮小
            logo_pixmap = logo_pixmap.scaledToWidth(150, Qt.TransformationMode.SmoothTransformation)
            # 正方形にするため、不足している高さを追加
            if logo_pixmap.height() < 150:
                logo_pixmap = logo_pixmap.scaledToHeight(150, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(logo_pixmap)
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            logo_label.setMinimumHeight(150)
            logo_label.setMaximumHeight(150)
        else:
            # 画像を読み込めなかった場合はテキストを表示
            logo_label.setText("ロゴ\nPID_Log_Analyzer")
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            logo_label.setMinimumHeight(150)
            logo_label.setMaximumHeight(150)
            logo_font = QFont()
            logo_font.setPointSize(24)
            logo_font.setBold(True)
            logo_label.setFont(logo_font)
            logo_label.setStyleSheet("color: #666666;")
        
        logo_layout.addWidget(logo_label)
        main_layout.addWidget(logo_frame)

        # ===== タイトルと説明 =====
        title_label = QLabel("PID制御ログ可視化・シミュレーションツール")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        description_label = QLabel(
            "このアプリケーションは、ロボットの PID 制御を支援するためのツールです。\n"
            "ロボコンなどで PID 制御のログを可視化したり、"
            "ゲイン値を調整してシミュレーションを行えます。"
        )
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setWordWrap(True)
        description_font = QFont()
        description_font.setPointSize(11)
        description_label.setFont(description_font)
        description_label.setStyleSheet("color: #333333;")  # テキスト色を明示
        main_layout.addWidget(description_label)

        # ===== 利用方法 =====
        usage_title = QLabel("利用方法")
        usage_title_font = QFont()
        usage_title_font.setPointSize(13)
        usage_title_font.setBold(True)
        usage_title.setFont(usage_title_font)
        usage_title.setStyleSheet("color: #333333;")  # テキスト色を明示
        main_layout.addWidget(usage_title)

        usage_content = QLabel(
            "【ログ可視化モード】\n"
            "  • CSVファイルから PID 制御のログを読み込みます\n"
            "  • グラフで応答時間、出力、定常偏差などを可視化します\n"
            "  • ロボットの制御性能を分析できます\n\n"
            "【シミュレーションモード】\n"
            "  • 目標値とゲイン値 (P, I, D) を入力します\n"
            "  • ログなしでシミュレーションを実行できます\n"
            "  • ゲイン調整の目安として活用できます"
        )
        usage_content.setWordWrap(True)
        usage_font = QFont()
        usage_font.setPointSize(10)
        usage_content.setFont(usage_font)
        usage_content.setStyleSheet("background-color: #f5f5f5; color: #333333; padding: 15px; border-radius: 5px;")
        main_layout.addWidget(usage_content)

        # ===== スペーサー =====
        main_layout.addStretch()

        # ===== 開始ボタン =====
        start_button = QPushButton("開始")
        start_button.setMinimumHeight(50)
        start_font = QFont()
        start_font.setPointSize(14)
        start_font.setBold(True)
        start_button.setFont(start_font)
        start_button.setStyleSheet(
            "QPushButton {"
            "  background-color: #4CAF50;"
            "  color: white;"
            "  border: none;"
            "  border-radius: 5px;"
            "  padding: 10px;"
            "}"
            "QPushButton:hover {"
            "  background-color: #45a049;"
            "}"
            "QPushButton:pressed {"
            "  background-color: #3d8b40;"
            "}"
        )
        start_button.clicked.connect(self.on_start_clicked)
        main_layout.addWidget(start_button)

    @Slot()
    def on_start_clicked(self):
        """開始ボタンがクリックされた時の処理"""
        if self.main_window_callback:
            self.main_window_callback()
        else:
            # コールバックがない場合は画面を閉じる
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FirstDisplay()
    window.show()
    sys.exit(app.exec())
