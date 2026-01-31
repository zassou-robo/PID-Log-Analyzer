from src.calc.pid_calc import pid_calc
from src.plot.plot import plot_all
from src.display.display import MainWindow, QApplication, sys
from src.display.first_display import FirstDisplay

# グローバル参照を保持（ウィンドウがガベージコレクションされないようにするため）
main_window = None


def show_main_window(first_window):
    """初期画面から メインウィンドウに切り替える"""
    global main_window
    main_window = MainWindow()
    main_window.show()
    first_window.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 初期画面を表示
    first_window = FirstDisplay(lambda: show_main_window(first_window))
    first_window.show()
    
    sys.exit(app.exec())