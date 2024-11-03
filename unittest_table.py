from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidget, 
                           QTableWidgetItem, QComboBox)
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTableWidget with ComboBox Example")
        self.resize(600, 400)

        # 創建表格
        self.table = QTableWidget(self)
        self.setCentralWidget(self.table)
        
        # 設置表格的行數和列數
        self.table.setRowCount(4)
        self.table.setColumnCount(3)
        
        # 設置表頭
        self.table.setHorizontalHeaderLabels(['姓名', '性別', '職業'])
        
        # 添加一些示例數據
        self.table.setItem(0, 0, QTableWidgetItem('張三'))
        self.table.setItem(1, 0, QTableWidgetItem('李四'))
        self.table.setItem(2, 0, QTableWidgetItem('王五'))
        self.table.setItem(3, 0, QTableWidgetItem('趙六'))
        
        # 在第二列添加性別選擇的 ComboBox
        gender_options = ['男', '女', '其他']
        for row in range(4):
            combo = QComboBox()
            combo.addItems(gender_options)
            self.table.setCellWidget(row, 1, combo)
        
        # 在第三列添加職業選擇的 ComboBox
        profession_options = ['工程師', '教師', '醫生', '學生', '其他']
        for row in range(4):
            combo = QComboBox()
            combo.addItems(profession_options)
            self.table.setCellWidget(row, 2, combo)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())