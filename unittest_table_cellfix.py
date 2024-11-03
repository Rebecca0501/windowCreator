from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTableWidget 只讀單元格示例")
        self.resize(600, 400)

        # 創建表格
        self.table = QTableWidget(self)
        self.table.setRowCount(5)
        self.table.setColumnCount(4)
        self.setCentralWidget(self.table)

        # 填充表格數據
        headers = ["編號", "姓名", "年齡", "分數"]
        self.table.setHorizontalHeaderLabels(headers)

        # 示例數據
        data = [
            ["001", "張三", "25", "85"],
            ["002", "李四", "28", "92"],
            ["003", "王五", "22", "78"],
            ["004", "趙六", "30", "88"],
            ["005", "孫七", "27", "95"]
        ]

        # 填充數據並設置部分單元格為只讀
        for row in range(5):
            for col in range(4):
                item = QTableWidgetItem(data[row][col])
                self.table.setItem(row, col, item)
                
                # 將"編號"列設置為只讀
                if col == 0:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                
                # 將分數大於90的單元格設置為只讀
                if col == 3 and int(data[row][col]) > 90:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()