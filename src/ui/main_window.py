from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QWidget, 
                             QVBoxLayout, QLabel)
from src.ui.pph21_tab import PPh21Tab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kalkulator Pajak Indonesia")
        self.setGeometry(100, 100, 1000, 700)
        self.setup_ui()
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Tab PPh 21 sudah lengkap
        tabs.addTab(PPh21Tab(), "PPh 21")
        
        # Tab lainnya masih sederhana
        tabs.addTab(self.create_simple_tab("PPh 23"), "PPh 23")
        tabs.addTab(self.create_simple_tab("PPh Pasal 4(2)"), "PPh 4(2)")
        tabs.addTab(self.create_simple_tab("PPh 22"), "PPh 22")
        tabs.addTab(self.create_simple_tab("PPh Badan"), "PPh Badan")
        tabs.addTab(self.create_simple_tab("PPN"), "PPN")
        tabs.addTab(self.create_simple_tab("PPNBM"), "PPNBM")
    
    def create_simple_tab(self, text):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Halaman {text} - Akan dikembangkan"))
        widget.setLayout(layout)
        return widget