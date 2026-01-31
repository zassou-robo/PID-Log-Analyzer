import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QRadioButton,
    QPushButton,
    QLabel,
)
from PySide6.QtCore import Slot

class MainWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("ログ可視化モード/シミュレーションモード切替")

    layout = QVBoxLayout(self)

    self.radio_a = QRadioButton("ログ可視化モード")
    self.radio_b = QRadioButton("シミュレーションモード")

        # 初期状態
    self.radio_a.setChecked(True)

        # 実行ボタン
    self.exec_button = QPushButton("実行")

        # 結果表示
    self.result_label = QLabel("未実行")

    layout.addWidget(self.radio_a)
    layout.addWidget(self.radio_b)
    layout.addWidget(self.exec_button)
    layout.addWidget(self.result_label)

    self.exec_button.clicked.connect(self.on_execute)

  @Slot()
  def on_execute(self):
    if self.radio_a.isChecked():
      self.process_a()
    elif self.radio_b.isChecked():
      self.process_b()

  def process_a(self):
      # Aモードの処理
      self.result_label.setText("Aモードの処理を実行しました")
      print("Aモードの処理")

  def process_b(self):
      # Bモードの処理
      self.result_label.setText("Bモードの処理を実行しました")
      print("Bモードの処理")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())