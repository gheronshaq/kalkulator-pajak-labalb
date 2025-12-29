"""
main.py - File utama untuk menjalankan aplikasi Kalkulator Pajak
"""
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QScrollArea, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Import UI components
from ui.pph21_tab import PPh21Widget


class SidebarButton(QPushButton):
    """Custom button untuk sidebar dengan styling khusus"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(45)
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #cbd5e1;
                text-align: left;
                padding: 12px 20px;
                font-size: 14px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #334155;
                color: white;
            }
            QPushButton:pressed {
                background-color: #475569;
            }
        """)


class MainWindow(QMainWindow):
    """Main Window aplikasi Kalkulator Pajak"""
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI components"""
        self.setWindowTitle("Kalkulator Pajak Indonesia")
        self.setGeometry(100, 100, 1400, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        
        # Content area with scroll
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f3f4f6;
            }
        """)
        
        # Set initial content (PPh 21)
        self.current_widget = PPh21Widget()
        self.scroll_area.setWidget(self.current_widget)
        
        main_layout.addWidget(self.scroll_area, 1)
        
    def create_sidebar(self):
        """Create sidebar dengan menu navigasi"""
        sidebar = QFrame()
        sidebar.setFixedWidth(280)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
            }
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setSpacing(8)
        layout.setContentsMargins(15, 20, 15, 20)
        
        # Header/Logo
        header = QLabel("📊 KALKULATOR\nPAJAK")
        header.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: bold;
            padding: 15px;
        """)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #334155; max-height: 1px;")
        layout.addWidget(separator)
        
        # Menu items
        menu_items = [
            ("PPh 21", self.show_pph21),
            ("PPh 23", self.show_pph23),
            ("PPh 4 (2)", self.show_pph4_2),
            ("PPh 22", self.show_pph22),
            ("PPh Badan", self.show_pph_badan),
            ("PPN", self.show_ppn),
            ("PPnBM", self.show_ppnbm),
        ]
        
        for text, callback in menu_items:
            btn = SidebarButton(text)
            btn.clicked.connect(callback)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # Footer
        footer = QLabel("v1.0 © 2025")
        footer.setStyleSheet("color: #64748b; font-size: 11px; padding: 10px;")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer)
        
        return sidebar
    
    def show_pph21(self):
        """Tampilkan widget PPh 21"""
        self.current_widget = PPh21Widget()
        self.scroll_area.setWidget(self.current_widget)
    
    def show_pph23(self):
        """Tampilkan widget PPh 23"""
        placeholder = QLabel("PPh 23 - Coming Soon")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("font-size: 24px; color: #5b6b8c;")
        self.scroll_area.setWidget(placeholder)
    
    def show_pph4_2(self):
        """Tampilkan widget PPh 4(2)"""
        placeholder = QLabel("PPh 4 (2) - Coming Soon")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("font-size: 24px; color: #5b6b8c;")
        self.scroll_area.setWidget(placeholder)
    
    def show_pph22(self):
        """Tampilkan widget PPh 22"""
        placeholder = QLabel("PPh 22 - Coming Soon")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("font-size: 24px; color: #5b6b8c;")
        self.scroll_area.setWidget(placeholder)
    
    def show_pph_badan(self):
        """Tampilkan widget PPh Badan"""
        placeholder = QLabel("PPh Badan - Coming Soon")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("font-size: 24px; color: #5b6b8c;")
        self.scroll_area.setWidget(placeholder)
    
    def show_ppn(self):
        """Tampilkan widget PPN"""
        placeholder = QLabel("PPN - Coming Soon")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("font-size: 24px; color: #5b6b8c;")
        self.scroll_area.setWidget(placeholder)
    
    def show_ppnbm(self):
        """Tampilkan widget PPnBM"""
        placeholder = QLabel("PPnBM - Coming Soon")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("font-size: 24px; color: #5b6b8c;")
        self.scroll_area.setWidget(placeholder)


def main():
    """Main function untuk menjalankan aplikasi"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()