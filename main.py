from src.calc.pid_calc import pid_calc
from src.plot.plot import plot_all
from src.display.display import MainWindow,QApplication,sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())