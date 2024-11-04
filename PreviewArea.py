import sys
from PyQt6.QtWidgets import (QWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QPen
from PreviewArea import *
from PyQt6 import QtWidgets

class PreviewArea(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 600)
        self.setStyleSheet("background-color: white;")
        self.window_data = None  # 存儲窗戶數據
    
    def update_preview(self, size_values, window_type):
        """更新預覽數據"""
        self.window_data = {
            'size_values': size_values,
            'window_type': window_type,
            #'layout_data': layout_data
        }
        self.update()  # 触发重繪
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        if not self.window_data:
            # 如果沒有數據，繪製提示信息
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "點擊預覽按鈕查看窗戶設計")
            return
            
        # 獲取視窗大小
        width = self.width()
        height = self.height()
        
        # 計算繪圖區域（保留邊距）
        margin = 50
        draw_width = width - 2 * margin
        draw_height = height - 2 * margin
        draw_width_center = int(draw_width/2)
        draw_height_center = int(draw_height/2)
        
        # 根據窗戶類型繪製不同的預覽
        if self.window_data['window_type'] == "type 1":
            self._draw_type1_window(painter, margin, draw_width_center, draw_height_center)
        elif self.window_data['window_type'] == "type 2":
            self._draw_type2_window(painter, margin, draw_width_center, draw_height_center)
        elif self.window_data['window_type'] == "type 3":
            self._draw_type3_window(painter, margin, draw_width_center, draw_height_center)
    
    def _draw_type1_window(self, painter, margin, draw_width_center, draw_height_center):
        """繪製type 1類型的窗戶"""
        window_width = int(self.window_data["size_values"]['窗戶寬度'])
        window_height = int(self.window_data["size_values"]['窗戶高度'])
        origin_x = int(draw_width_center - window_width/2)
        origin_y = int(draw_height_center - window_height/2)

        painter.setPen(QPen(QColor('#ff0000'),2))  # 設定畫筆顏色和寬度
        painter.drawRect(origin_x, origin_y, window_width, window_height)  # 繪製正方形

        painter.end()  
        # 獲取行列數
        #rows = self.window_data['layout_data'].get('rows', 1)
        #cols = self.window_data['layout_data'].get('cols', 1)
        
        # 計算單個窗格大小
        #cell_width = draw_width / cols
        #cell_height = draw_height / rows
        
        # 繪製網格
        # painter.setPen(QPen(QColor(0, 0, 0), 2))
        # for i in range(rows + 1):
        #     y = margin + i * cell_height
        #     painter.drawLine(margin, y, margin + draw_width, y)
            
        # for j in range(cols + 1):
        #     x = margin + j * cell_width
        #     painter.drawLine(x, margin, x, margin + draw_height)
    
    def _draw_type2_window(self, painter, margin, draw_width, draw_height):
        """繪製type 2類型的窗戶"""
        # 實現type 2的繪製邏輯
        pass
    
    def _draw_type3_window(self, painter, margin, draw_width, draw_height):
        """繪製type 3類型的窗戶"""
        # 實現type 3的繪製邏輯
        pass