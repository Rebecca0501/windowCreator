import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, 
                             QVBoxLayout, QLabel, QComboBox, QLineEdit, 
                             QTableWidget, QTableWidgetItem, QGridLayout, 
                             QStackedLayout, QScrollArea, QPushButton, QSizePolicy, )
from PreviewArea import *

class CustomLineEdit(QLineEdit):
    def __init__(self, placeholder_text="", validator=None):
        super().__init__()
        self.setPlaceholderText(placeholder_text)
        if validator:
            self.setValidator(validator)

class WindowGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("窗戶圖檔生成器")
        self.setGeometry(0, 0, 1200, 800)

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
        self.preview_layout = QVBoxLayout()
        
        # 預覽區域 - 移除paintEvent的覆蓋
        self.preview_area = PreviewArea()
        self.preview_area.setStyleSheet("background-color: lightgray;")
        self.preview_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.preview_layout.addWidget(self.preview_area)
        
        # 預覽按鈕
        preview_button = QPushButton("預覽")
        preview_button.setFixedSize(100, 30)  # 設置按鈕大小
        preview_button.clicked.connect(self.on_preview_clicked)  # 連接點擊事件
        
        # CAD下載按鈕
        downloadCAD_button = QPushButton("CAD下載")
        downloadCAD_button.setFixedSize(100, 30)  # 設置按鈕大小
        downloadCAD_button.clicked.connect(self.on_downloadCAD_clicked)  # 連接點擊事件

        # CAD下載按鈕
        downloadExcel_button = QPushButton("Excel下載")
        downloadExcel_button.setFixedSize(100, 30)  # 設置按鈕大小
        downloadExcel_button.clicked.connect(self.on_downloadExcel_clicked)  # 連接點擊事件
        
        # 創建一個水平佈局來放置按鈕，實現按鈕置中
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # 在按鈕左側添加彈性空間
        button_layout.addWidget(preview_button)
        button_layout.addWidget(downloadCAD_button)
        button_layout.addWidget(downloadExcel_button)
        button_layout.addStretch()  # 在按鈕右側添加彈性空間
        
        # 將按鈕佈局添加到預覽面板佈局中
        self.preview_layout.addLayout(button_layout)
        preview_panel.setLayout(self.preview_layout)

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
                unit_in_rows = [int(self.type1_col_edit.text())] * int(self.type1_row_edit.text())

                unit_count = sum(unit_in_rows)
                table_rows_count = unit_count
            elif current_type == "type 2":
                # 計算單元數總和
                unit_inputs = [
                    self.type2_scroll_layout.itemAt(i).widget().layout().itemAt(1).widget() 
                    for i in range(self.type2_scroll_layout.count())
                ]

                unit_in_rows = []
                for input_widget in unit_inputs:
                    text = input_widget.text()  # 取得文字內容
                    try:
                        value = int(text)       # 轉換成整數
                        unit_in_rows.append(value)
                    except ValueError:
                        # 處理無效輸入
                        print(f"無效的整數輸入: {text}")

                unit_count = sum(unit_in_rows)
                table_rows_count = unit_count
                
            else:  # type 3
                # 計算單元數總和
                unit_inputs = [
                    self.type3_scroll_layout.itemAt(i).widget().layout().itemAt(1).widget() 
                    for i in range(self.type3_scroll_layout.count())
                ]
                unit_in_rows = []
                for input_widget in unit_inputs:
                    text = input_widget.text()  # 取得文字內容
                    try:
                        value = int(text)       # 轉換成整數
                        unit_in_rows.append(value)
                    except ValueError:
                        # 處理無效輸入
                        print(f"無效的整數輸入: {text}")

                unit_count = sum(unit_in_rows)
                table_rows_count = unit_count
            
            # 設置表格行數
            self.unit_table.setRowCount(table_rows_count)
            
            # 填充單元編號
            if current_type == "type 1":
                unit_number_item = []
                # 使用ASCII碼，從'A'開始
                for index, num in enumerate(unit_in_rows):
                    # 獲取對應的字母，65是'A'的ASCII碼
                    letter = chr(65 + index)
                    # 為每個數字生成對應數量的序列
                    for i in range(1, num + 1):
                        unit_number_item.append(f"{letter}{i}")
                for index, item in enumerate(unit_number_item):
                    self.unit_table.setItem(index, 0, QTableWidgetItem(str(item)))
            elif current_type == "type 2":
                unit_number_item = []
                # 使用ASCII碼，從'A'開始
                for index, num in enumerate(unit_in_rows):
                    # 獲取對應的字母，65是'A'的ASCII碼
                    letter = chr(65 + index)
                    # 為每個數字生成對應數量的序列
                    for i in range(1, num + 1):
                        unit_number_item.append(f"{letter}{i}")
                for index, item in enumerate(unit_number_item):
                    self.unit_table.setItem(index, 0, QTableWidgetItem(str(item)))
            else:  # type 3
                unit_number_item = []
                for index, item in enumerate(unit_in_rows):
                    for i in range(item):
                        letter = chr(65 + i)
                        unit_number_item.append(f"{letter}{index+1}")
                for index, item in enumerate(unit_number_item):
                    self.unit_table.setItem(index, 0, QTableWidgetItem(str(item)))

            
            sash_options = ['固定窗', '橫拉窗', '推窗']
            for row in range(table_rows_count):
                sash_unit_number = self.unit_table.item(row, 0)
                sash_unit_number.setFlags(sash_unit_number.flags() & ~Qt.ItemFlag.ItemIsEditable)
                
                # 在第二列添加窗扇選擇的 ComboBox
                combo = QComboBox()
                combo.addItems(sash_options)
                self.unit_table.setCellWidget(row, 1, combo)

                # 在第三列添加窗扇邊框寬度的輸入欄位
                sash_frame_edit = CustomLineEdit(placeholder_text="請輸入邊框寬度")
                self.unit_table.setCellWidget(row, 2, sash_frame_edit)

                # 在第四列添加窗扇數量的輸入欄位
                sash_num_edit = CustomLineEdit(placeholder_text="請輸入窗扇數量")
                self.unit_table.setCellWidget(row, 3, sash_num_edit)

                # 在第五列添加窗扇寬度的輸入欄位
                sash_width_edit = CustomLineEdit(placeholder_text="請輸入窗扇寬度")
                self.unit_table.setCellWidget(row, 4, sash_width_edit)

                # 在第六列添加窗扇寬度的輸入欄位
                sash_height_edit = CustomLineEdit(placeholder_text="請輸入窗扇高度")
                self.unit_table.setCellWidget(row, 5, sash_height_edit)

            
            
                
            
        except (ValueError, TypeError):
            # 如果輸入無效，不做任何操作
            pass

    def get_size_values(self):
        size_values = {}
        for label, edit in zip(self.size_labels, self.size_edits):
            value = edit.text()  # 獲取輸入框的文字
            # 轉換為浮點數（如果輸入是數字的話）
            try:
                value = float(value)
            except ValueError:
                print(f"{label} 的輸入必須是數字")
                continue
            size_values[label] = value
        return size_values

    def show_preview(self):
        self.preview_layout.update()

    def on_preview_clicked(self):
        """預覽按鈕點擊事件處理"""
        # 這裡可以添加預覽功能的實現
        print("預覽按鈕被點擊")
        
        self.preview_area.update_preview(self.get_size_values(),self.type_combo.currentText())
        self.show_preview()

    def on_downloadCAD_clicked(self):
        """下載CAD檔按鈕點擊事件處理"""
        print("下載CAD檔被點擊")

    def on_downloadExcel_clicked(self):
        """下載Excel檔按鈕點擊事件處理"""
        print("下載Excel檔被點擊")
        