import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QRadioButton,
    QPushButton,
    QLabel,
    QLineEdit,
)
from PySide6.QtCore import Slot
from src.display.display_funcs import funcs
from src.calc.pid_calc import pid_calc
from src.plot.plot import plot_all
from src.display.csv_load import load_csv_file

class MainWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("ログ可視化モード/シミュレーションモード切替")

    layout = QVBoxLayout(self)

    self.radio_a = QRadioButton("ログ可視化モード　csvファイルを読み込みグラフ描画をします")
    self.radio_b = QRadioButton("シミュレーションモード　ゲインと目標値をもとにシミュレーションを行います")

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

    # シミュレーションモード用のテキストボックス
    self.sim_widget = QWidget()
    self.sim_layout = QVBoxLayout(self.sim_widget)
    
    # 目標値入力
    self.label_goal = QLabel("目標値:")
    self.textbox_goal = QLineEdit()
    self.textbox_goal.setPlaceholderText("目標値を入力してください")
    self.sim_layout.addWidget(self.label_goal)
    self.sim_layout.addWidget(self.textbox_goal)
    
    # ゲイン値入力
    self.label_gain = QLabel("ゲイン値 (P, I, D):")
    self.textbox_gain = QLineEdit()
    self.textbox_gain.setPlaceholderText("例: 0.2, 0.1, 0.0 (P値, I値, D値)")
    self.sim_layout.addWidget(self.label_gain)
    self.sim_layout.addWidget(self.textbox_gain)
    
    # シミュレーション結果表示
    # self.label_result = QLabel("シミュレーション結果:")
    # self.textbox_result = QLineEdit()
    # self.textbox_result.setReadOnly(True)
    # self.textbox_result.setPlaceholderText("シミュレーション実行後に結果が表示されます")
    # self.sim_layout.addWidget(self.label_result)
    # self.sim_layout.addWidget(self.textbox_result)
    
    self.sim_widget.hide()
    layout.addWidget(self.sim_widget)

    self.exec_button.clicked.connect(self.on_execute)
    self.radio_a.toggled.connect(self.on_mode_changed)
    self.radio_b.toggled.connect(self.on_mode_changed)

  @Slot()
  def on_mode_changed(self):
    if self.radio_b.isChecked():
      self.sim_widget.show()
    else:
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