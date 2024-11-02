import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, 
                             QVBoxLayout, QLabel, QComboBox, QLineEdit, 
                             QTableWidget, QTableWidgetItem, QGridLayout, 
                             QStackedLayout, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor

class WindowGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("窗戶圖檔生成器")
        self.setGeometry(100, 100, 1200, 800)

        # 主容器
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # 左側參數設定介面
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)

        # 第一個功能區塊：窗戶類型設定
        type_layout = QGridLayout()
        type_label = QLabel("窗戶類型")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["type 1", "type 2", "type 3"])
        type_layout.addWidget(type_label, 0, 0)
        type_layout.addWidget(self.type_combo, 0, 1)
        left_layout.addLayout(type_layout)

        # 第二個功能區塊：窗戶尺寸設定
        size_layout = QGridLayout()
        self.size_labels = [
            "窗戶寬度", "窗戶高度", "窗台高度", 
            "窗框寬度", "transom寬度", "mullion寬度"
        ]
        
        self.size_edits = []
        for i, label_text in enumerate(self.size_labels):
            label = QLabel(label_text)
            line_edit = QLineEdit()
            size_layout.addWidget(label, i, 0)
            size_layout.addWidget(line_edit, i, 1)
            self.size_edits.append(line_edit)
        
        left_layout.addLayout(size_layout)

        # 第三個功能區塊：窗戶行列數設定 - 使用堆疊佈局實現動態切換
        self.row_col_stacked_layout = QStackedLayout()
        
        # Type 1 佈局
        type1_widget = QWidget()
        type1_layout = QGridLayout()
        type1_row_label = QLabel("窗戶行數")
        type1_col_label = QLabel("窗戶列數")
        self.type1_row_edit = QLineEdit()
        self.type1_col_edit = QLineEdit()
        type1_layout.addWidget(type1_row_label, 0, 0)
        type1_layout.addWidget(self.type1_row_edit, 0, 1)
        type1_layout.addWidget(type1_col_label, 1, 0)
        type1_layout.addWidget(self.type1_col_edit, 1, 1)
        type1_widget.setLayout(type1_layout)
        
        # Type 2 佈局 - 可滾動的動態輸入框區域
        type2_widget = QWidget()
        type2_layout = QVBoxLayout()
        type2_scroll_area = QScrollArea()
        type2_scroll_widget = QWidget()
        self.type2_scroll_layout = QVBoxLayout()
        
        self.type2_row_label = QLabel("窗戶行數")
        self.type2_row_edit = QLineEdit()
        self.type2_row_edit.textChanged.connect(self.update_type2_unit_inputs)
        
        type2_layout.addWidget(self.type2_row_label)
        type2_layout.addWidget(self.type2_row_edit)
        
        type2_scroll_widget.setLayout(self.type2_scroll_layout)
        type2_scroll_area.setWidget(type2_scroll_widget)
        type2_scroll_area.setWidgetResizable(True)
        type2_layout.addWidget(type2_scroll_area)
        
        type2_widget.setLayout(type2_layout)
        
        # Type 3 佈局 - 可滾動的動態輸入框區域
        type3_widget = QWidget()
        type3_layout = QVBoxLayout()
        type3_scroll_area = QScrollArea()
        type3_scroll_widget = QWidget()
        self.type3_scroll_layout = QVBoxLayout()
        
        self.type3_col_label = QLabel("窗戶列數")
        self.type3_col_edit = QLineEdit()
        self.type3_col_edit.textChanged.connect(self.update_type3_unit_inputs)
        
        type3_layout.addWidget(self.type3_col_label)
        type3_layout.addWidget(self.type3_col_edit)
        
        type3_scroll_widget.setLayout(self.type3_scroll_layout)
        type3_scroll_area.setWidget(type3_scroll_widget)
        type3_scroll_area.setWidgetResizable(True)
        type3_layout.addWidget(type3_scroll_area)
        
        type3_widget.setLayout(type3_layout)
        
        # 將不同類型的佈局加入堆疊佈局
        self.row_col_stacked_layout.addWidget(type1_widget)
        self.row_col_stacked_layout.addWidget(type2_widget)
        self.row_col_stacked_layout.addWidget(type3_widget)
        
        # 創建一個容器來包裹堆疊佈局
        row_col_container = QWidget()
        row_col_container.setLayout(self.row_col_stacked_layout)
        left_layout.addWidget(row_col_container)

        # 第四個功能區塊：窗扇單元類型設定
        self.unit_table = QTableWidget()
        self.unit_table.setColumnCount(6)
        self.unit_table.setHorizontalHeaderLabels(
            ["單元編號", "窗扇類型", "窗扇邊框寬度", "窗扇數量", "窗扇寬度", "窗扇高度"]
        )
        left_layout.addWidget(self.unit_table)

        # 右側設計預覽介面
        preview_panel = QWidget()
        preview_layout = QVBoxLayout()
        preview_panel.setLayout(preview_layout)
        preview_panel.setStyleSheet("background-color: lightgray;")

        # 將左側和右側面板加入主佈局
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(preview_panel, 1)

        # 連接窗戶類型改變的信號
        self.type_combo.currentIndexChanged.connect(self.on_type_changed)
        
        # 連接行數/列數輸入的信號
        self.type1_row_edit.textChanged.connect(self.update_unit_table)
        self.type1_col_edit.textChanged.connect(self.update_unit_table)

    def on_type_changed(self, index):
        # 根據選擇的窗戶類型切換行列數設定佈局
        self.row_col_stacked_layout.setCurrentIndex(index)
        
        # 更新單元表格
        self.update_unit_table()

    def update_type2_unit_inputs(self, text):
        # 清除之前的輸入框
        for i in reversed(range(self.type2_scroll_layout.count())): 
            self.type2_scroll_layout.itemAt(i).widget().setParent(None)
        
        try:
            row_count = int(text)
            for i in range(row_count):
                row_layout = QHBoxLayout()
                label = QLabel(f"第 {i+1} 行單元數")
                edit = QLineEdit()
                edit.textChanged.connect(self.update_unit_table)
                row_layout.addWidget(label)
                row_layout.addWidget(edit)
                
                # 創建一個臨時widget來容納水平佈局
                row_widget = QWidget()
                row_widget.setLayout(row_layout)
                
                self.type2_scroll_layout.addWidget(row_widget)
        except ValueError:
            pass
        
        # 觸發單元表格更新
        self.update_unit_table()

    def update_type3_unit_inputs(self, text):
        # 清除之前的輸入框
        for i in reversed(range(self.type3_scroll_layout.count())): 
            self.type3_scroll_layout.itemAt(i).widget().setParent(None)
        
        try:
            col_count = int(text)
            for i in range(col_count):
                col_layout = QHBoxLayout()
                label = QLabel(f"第 {i+1} 列單元數")
                edit = QLineEdit()
                edit.textChanged.connect(self.update_unit_table)
                col_layout.addWidget(label)
                col_layout.addWidget(edit)
                
                # 創建一個臨時widget來容納水平佈局
                col_widget = QWidget()
                col_widget.setLayout(col_layout)
                
                self.type3_scroll_layout.addWidget(col_widget)
        except ValueError:
            pass
        
        # 觸發單元表格更新
        self.update_unit_table()

    def update_unit_table(self):
        # 清空當前表格
        self.unit_table.setRowCount(0)
        
        # 根據當前窗戶類型計算行數
        current_type = self.type_combo.currentText()
        
        try:
            if current_type == "type 1":
                rows = int(self.type1_row_edit.text()) * int(self.type1_col_edit.text()) + 1
                rows_count = int(self.type1_row_edit.text()) * int(self.type1_col_edit.text())
            elif current_type == "type 2":
                row_count = int(self.type2_row_edit.text())
                # 計算單元數總和
                unit_inputs = [
                    self.type2_scroll_layout.itemAt(i).widget().layout().itemAt(1).widget() 
                    for i in range(self.type2_scroll_layout.count())
                ]
                unit_count = sum(int(edit.text() or 0) for edit in unit_inputs)
                rows = row_count + 1 
                rows_count = unit_count
            else:  # type 3
                col_count = int(self.type3_col_edit.text())
                # 計算單元數總和
                unit_inputs = [
                    self.type3_scroll_layout.itemAt(i).widget().layout().itemAt(1).widget() 
                    for i in range(self.type3_scroll_layout.count())
                ]
                unit_count = sum(int(edit.text() or 0) for edit in unit_inputs)
                rows = col_count + 1
                rows_count = unit_count
            
            # 設置表格行數
            self.unit_table.setRowCount(rows_count)
            
            # 填充單元編號
            for row in range(rows_count):
                unit_number_item = QTableWidgetItem(str(row))
                self.unit_table.setItem(row, 0, unit_number_item)
        
        except (ValueError, TypeError):
            # 如果輸入無效，不做任何操作
            pass

def main():
    app = QApplication(sys.argv)
    window = WindowGeneratorApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()