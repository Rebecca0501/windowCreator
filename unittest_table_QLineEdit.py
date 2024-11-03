from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidget, 
                           QTableWidgetItem, QLineEdit)
from PyQt6.QtGui import QIntValidator  # 修正：從 QtGui 導入 QIntValidator
from PyQt6.QtCore import Qt
import sys

class CustomLineEdit(QLineEdit):
    def __init__(self, placeholder_text="", validator=None):
        super().__init__()
        self.setPlaceholderText(placeholder_text)
        if validator:
            self.setValidator(validator)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTableWidget with LineEdit Example")
        self.resize(800, 400)

        # 創建表格
        self.table = QTableWidget(self)
        self.setCentralWidget(self.table)
        
        # 設置表格的行數和列數
        self.table.setRowCount(4)
        self.table.setColumnCount(4)
        
        # 設置表頭
        self.table.setHorizontalHeaderLabels(['姓名', '年齡', '電話', '備註'])
        
        # 設置表格列寬
        self.table.setColumnWidth(0, 150)  # 姓名欄
        self.table.setColumnWidth(1, 100)  # 年齡欄
        self.table.setColumnWidth(2, 200)  # 電話欄
        self.table.setColumnWidth(3, 300)  # 備註欄
        
        # 添加 QLineEdit 到每個單元格
        for row in range(self.table.rowCount()):
            # 姓名欄位（普通文本輸入）
            name_edit = CustomLineEdit(placeholder_text="請輸入姓名")
            self.table.setCellWidget(row, 0, name_edit)
            
            # 年齡欄位（只能輸入數字）
            age_edit = CustomLineEdit(placeholder_text="請輸入年齡")
            age_edit.setValidator(QIntValidator(0, 150))  # 修正：直接使用 QIntValidator
            self.table.setCellWidget(row, 1, age_edit)
            
            # 電話欄位（可以設置輸入格式）
            phone_edit = CustomLineEdit(placeholder_text="請輸入電話號碼")
            phone_edit.setInputMask("9999-999-999")  # 設置輸入掩碼
            self.table.setCellWidget(row, 2, phone_edit)
            
            # 備註欄位（多行文本輸入）
            note_edit = CustomLineEdit(placeholder_text="請輸入備註")
            self.table.setCellWidget(row, 3, note_edit)

        # 連接編輯完成信號
        self.setup_line_edit_connections()

    def setup_line_edit_connections(self):
        """設置所有 LineEdit 的編輯完成信號連接"""
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                line_edit = self.table.cellWidget(row, col)
                if isinstance(line_edit, QLineEdit):
                    line_edit.editingFinished.connect(
                        lambda r=row, c=col: self.on_editing_finished(r, c))

    def on_editing_finished(self, row, col):
        """當編輯完成時的處理函數"""
        line_edit = self.table.cellWidget(row, col)
        if isinstance(line_edit, QLineEdit):
            value = line_edit.text()
            print(f"單元格 ({row}, {col}) 的值已更改為: {value}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())