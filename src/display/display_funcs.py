from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QRadioButton,
    QPushButton,
    QLabel,
)
import PySide6.QtWidgets as Qw

class funcs(Qw.QMainWindow):
    def text_box(self):
      self.tb_log = Qw.QTextEdit('',self)
      self.tb_log.setGeometry(10,40,620,170)
      self.tb_log.setPlaceholderText('(ここに実行ログを表示します)')