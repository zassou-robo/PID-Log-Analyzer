import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QRadioButton,
    QPushButton,
    QLabel,
    QLineEdit,
    QFrame,
)
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QFont
from src.display.display_funcs import funcs
from src.calc.pid_calc import pid_calc
from src.plot.plot import plot_all
from src.display.csv_load import load_csv_file

class MainWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("PID_Log_Analyzer - モード選択")
    self.setGeometry(100, 100, 800, 700)
    
    # スタイルシート（統一デザイン）
    self.setStyleSheet(
        "QWidget { background-color: #ffffff; }"
        "QLabel { color: #333333; }"
        "QRadioButton { color: #333333; font-size: 11pt; }"
    )

    layout = QVBoxLayout(self)
    layout.setSpacing(15)
    layout.setContentsMargins(40, 30, 40, 30)

    # ===== タイトル =====
    title_label = QLabel("PID 制御ログ解析")
    title_font = QFont()
    title_font.setPointSize(18)
    title_font.setBold(True)
    title_label.setFont(title_font)
    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(title_label)

    # ===== モード選択説明 =====
    mode_desc = QLabel("以下のモードを選択して実行してください")
    mode_desc_font = QFont()
    mode_desc_font.setPointSize(11)
    mode_desc.setFont(mode_desc_font)
    mode_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(mode_desc)

    # ===== モード選択フレーム =====
    mode_frame = QFrame()
    mode_frame.setStyleSheet("border: 1px solid #ddd; border-radius: 5px; padding: 15px;")
    mode_layout = QVBoxLayout(mode_frame)
    mode_layout.setSpacing(15)

    # モードA フレーム
    self.mode_a_frame = QFrame()
    self.mode_a_frame.setStyleSheet(
        "QFrame { border: 2px solid #4CAF50; border-radius: 5px; padding: 10px; background-color: #f1f8f4; }"
    )
    mode_a_layout = QVBoxLayout(self.mode_a_frame)
    mode_a_layout.setSpacing(5)
    mode_a_layout.setContentsMargins(10, 10, 10, 10)
    
    self.radio_a = QRadioButton("ログ可視化モード")
    radio_a_font = QFont()
    radio_a_font.setPointSize(11)
    radio_a_font.setBold(True)
    self.radio_a.setFont(radio_a_font)
    radio_a_desc = QLabel("CSVファイルを読み込み、PID制御のログをグラフで可視化します")
    radio_a_desc.setStyleSheet("color: #666666; font-size: 9pt;")
    
    mode_a_layout.addWidget(self.radio_a)
    mode_a_layout.addWidget(radio_a_desc)
    mode_layout.addWidget(self.mode_a_frame)

    # モードB フレーム
    self.mode_b_frame = QFrame()
    self.mode_b_frame.setStyleSheet(
        "QFrame { border: 2px solid #cccccc; border-radius: 5px; padding: 10px; background-color: #ffffff; }"
    )
    mode_b_layout = QVBoxLayout(self.mode_b_frame)
    mode_b_layout.setSpacing(5)
    mode_b_layout.setContentsMargins(10, 10, 10, 10)
    
    self.radio_b = QRadioButton("シミュレーションモード")
    radio_b_font = QFont()
    radio_b_font.setPointSize(11)
    radio_b_font.setBold(True)
    self.radio_b.setFont(radio_b_font)
    radio_b_desc = QLabel("ゲインと目標値を入力し、シミュレーションを実行します")
    radio_b_desc.setStyleSheet("color: #666666; font-size: 9pt;")

    # 初期状態
    self.radio_a.setChecked(True)

    mode_b_layout.addWidget(self.radio_b)
    mode_b_layout.addWidget(radio_b_desc)
    mode_layout.addWidget(self.mode_b_frame)
    
    layout.addWidget(mode_frame)

    # ===== シミュレーションモード用のテキストボックス =====
    self.sim_widget = QWidget()
    self.sim_layout = QVBoxLayout(self.sim_widget)
    self.sim_layout.setSpacing(10)

    sim_frame = QFrame()
    sim_frame.setStyleSheet("border: 1px solid #ddd; border-radius: 5px; padding: 15px;")
    sim_frame_layout = QVBoxLayout(sim_frame)
    sim_frame_layout.setSpacing(10)
    
    # シミュレーション設定タイトル
    sim_title = QLabel("シミュレーション設定")
    sim_title_font = QFont()
    sim_title_font.setPointSize(12)
    sim_title_font.setBold(True)
    sim_title.setFont(sim_title_font)
    sim_frame_layout.addWidget(sim_title)
    
    # 目標値入力
    self.label_goal = QLabel("目標値:")
    goal_font = QFont()
    goal_font.setPointSize(10)
    self.label_goal.setFont(goal_font)
    self.textbox_goal = QLineEdit()
    self.textbox_goal.setPlaceholderText("例: 10.5")
    self.textbox_goal.setMinimumHeight(35)
    self.textbox_goal.setStyleSheet(
        "QLineEdit { border: 1px solid #ccc; border-radius: 4px; padding: 5px; }"
    )
    sim_frame_layout.addWidget(self.label_goal)
    sim_frame_layout.addWidget(self.textbox_goal)
    
    # ゲイン値入力
    self.label_gain = QLabel("ゲイン値 (P, I, D):")
    gain_font = QFont()
    gain_font.setPointSize(10)
    self.label_gain.setFont(gain_font)
    self.textbox_gain = QLineEdit()
    self.textbox_gain.setPlaceholderText("例: 0.2, 0.1, 0.0")
    self.textbox_gain.setMinimumHeight(35)
    self.textbox_gain.setStyleSheet(
        "QLineEdit { border: 1px solid #ccc; border-radius: 4px; padding: 5px; }"
    )
    sim_frame_layout.addWidget(self.label_gain)
    sim_frame_layout.addWidget(self.textbox_gain)
    
    self.sim_layout.addWidget(sim_frame)
    self.sim_widget.hide()
    layout.addWidget(self.sim_widget)

    layout.addStretch()

    # ===== 実行ボタン =====
    self.exec_button = QPushButton("実行")
    self.exec_button.setMinimumHeight(45)
    exec_font = QFont()
    exec_font.setPointSize(12)
    exec_font.setBold(True)
    self.exec_button.setFont(exec_font)
    self.exec_button.setStyleSheet(
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
    layout.addWidget(self.exec_button)

    # ===== 結果表示 =====
    self.result_label = QLabel("未実行")
    result_font = QFont()
    result_font.setPointSize(10)
    self.result_label.setFont(result_font)
    self.result_label.setWordWrap(True)
    self.result_label.setStyleSheet(
        "QLabel { background-color: #f5f5f5; padding: 10px; border-radius: 4px; }"
    )
    layout.addWidget(self.result_label)

    self.exec_button.clicked.connect(self.on_execute)
    self.radio_a.toggled.connect(self.on_mode_changed)
    self.radio_b.toggled.connect(self.on_mode_changed)

  @Slot()
  def on_mode_changed(self):
    if self.radio_b.isChecked():
      # モードB選択時
      self.mode_a_frame.setStyleSheet(
          "QFrame { border: 2px solid #cccccc; border-radius: 5px; padding: 10px; background-color: #ffffff; }"
      )
      self.mode_b_frame.setStyleSheet(
          "QFrame { border: 2px solid #4CAF50; border-radius: 5px; padding: 10px; background-color: #f1f8f4; }"
      )
      self.sim_widget.show()
    else:
      # モードA選択時
      self.mode_a_frame.setStyleSheet(
          "QFrame { border: 2px solid #4CAF50; border-radius: 5px; padding: 10px; background-color: #f1f8f4; }"
      )
      self.mode_b_frame.setStyleSheet(
          "QFrame { border: 2px solid #cccccc; border-radius: 5px; padding: 10px; background-color: #ffffff; }"
      )
      self.sim_widget.hide()

  @Slot()
  def on_execute(self):
    if self.radio_a.isChecked():
      self.process_a()
    elif self.radio_b.isChecked():
      self.process_b()

  def process_a(self):
      # Aモードの処理
      try:
          time_history, goal_history, actual_history = load_csv_file(self)
          
          if time_history is None:
              self.result_label.setText("キャンセルされました。")
              return
          
          # グラフを描画
          plot_all(time_history, goal_history, actual_history)
          self.result_label.setText(f"ログを可視化しました。（{len(time_history)}データポイント）")
          
      except Exception as e:
          self.result_label.setText(f"エラー: {str(e)}")

  def process_b(self):
      # Bモードの処理
      try:
          # 入力値を取得
          goal = float(self.textbox_goal.text())
          gain_str = self.textbox_gain.text()
          gains = [float(x.strip()) for x in gain_str.split(',')]
          p_gain, i_gain, d_gain = gains[0], gains[1], gains[2]
          
          # シミュレーション実行
          time_step = 0.01
          simulation_time = 100
          
          actual = 0
          pre_error = 0
          time_history = []
          goal_history = []
          actual_history = []
          
          for i in range(simulation_time):
              error = goal - actual
              output = pid_calc(error, pre_error, time_step, p_gain, i_gain, d_gain)
              actual += output
              
              time_history.append(i * time_step)
              goal_history.append(goal)
              actual_history.append(actual)
              
              pre_error = error
          
          # 最終結果を表示
          final_actual = actual_history[-1]
          steady_state_error = goal - final_actual
          
          result_text = f"シミュレーション完了 | 目標値: {goal} | 最終値: {final_actual:.2f} | 定常偏差: {steady_state_error:.2f}"
          self.result_label.setText(result_text)
          
          # グラフを描画
          plot_all(time_history, goal_history, actual_history)
          
      except ValueError:
          self.result_label.setText("エラー: 入力値が正しくありません。数値を入力してください。")
      except IndexError:
          self.result_label.setText("エラー: ゲイン値は3つ必要です（P, I, D をカンマ区切りで入力）")


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())