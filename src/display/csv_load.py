import csv
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QCoreApplication

def load_csv_file(parent=None):
    """
    ファイルダイアログからCSVファイルを選択して読み込む
    
    Returns:
        tuple: (time_history, goal_history, actual_history) または (None, None, None) キャンセル時
    """
    file_dialog = QFileDialog()
    file_path, _ = file_dialog.getOpenFileName(
        parent,
        "CSVファイルを選択",
        "",
        "CSV Files (*.csv);;All Files (*)"
    )
    
    if not file_path:
        return None, None, None
    
    try:
        time_history = []
        goal_history = []
        actual_history = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            # ヘッダー行をスキップ
            next(reader, None)
            
            for row in reader:
                if len(row) >= 3:
                    time_history.append(float(row[0]))
                    goal_history.append(float(row[1]))
                    actual_history.append(float(row[2]))
        
        return time_history, goal_history, actual_history
    
    except Exception as e:
        raise Exception(f"CSVファイルの読み込みに失敗しました: {str(e)}")
