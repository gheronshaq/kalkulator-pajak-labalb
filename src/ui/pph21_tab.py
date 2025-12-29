"""
ui/pph21_tab.py - UI Widget untuk PPh 21
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFrame, QComboBox, QLineEdit, QRadioButton,
                             QCheckBox, QStackedWidget, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Import logic
from logic.pph21 import PPh21Calculator


class PPh21BulananForm(QWidget):
    """Form untuk PPh 21 Bulanan"""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Kode Objek Pajak
        self.kode_combo = self.create_combo([
            "Pilih Kode Objek Pajak",
            "21-100-01 Pegawai Tetap",
            "21-100-02 Penerima Pensiun Berkala"
        ])
        self.add_form_row(layout, "Kode Objek Pajak", self.kode_combo)
        
        # Skema Perhitungan
        radio_widget = QWidget()
        radio_layout = QHBoxLayout(radio_widget)
        self.radio_gross = QRadioButton("Gross")
        self.radio_gross_up = QRadioButton("Gross Up")
        self.radio_gross.setChecked(True)
        self.radio_gross.setStyleSheet("color: #7b2f8f; font-size: 14px;")
        self.radio_gross_up.setStyleSheet("color: #7b2f8f; font-size: 14px;")
        radio_layout.addWidget(self.radio_gross)
        radio_layout.addWidget(self.radio_gross_up)
        radio_layout.addStretch()
        self.add_form_row(layout, "Skema Perhitungan", radio_widget)
        
        # Checkbox
        self.checkbox_dipotong = QCheckBox("Tidak Ada")
        self.checkbox_dipotong.setStyleSheet("color: #7b2f8f; font-size: 14px;")
        self.add_form_row(layout, "Penghasilan yang telah dipotong\nPPh Pasal 21 pada masa pajak\nyang sama", 
                         self.checkbox_dipotong)
        
        # Penghasilan Bruto
        self.bruto_input = self.create_input("0")
        self.add_form_row(layout, "Penghasilan Bruto", self.bruto_input)
        
        # PTKP
        self.ptkp_combo = self.create_combo([
            "Pilih PTKP",
            "TK/0 - 54000000",
            "TK/1 - 58500000",
            "TK/2 - 63000000",
            "TK/3 - 67500000",
            "K/0 - 58500000",
            "K/1 - 63000000",
            "K/2 - 67500000",
            "K/3 - 72000000"
        ])
        self.add_form_row(layout, "PTKP", self.ptkp_combo)
        
        # Info boxes
        info_layout = QHBoxLayout()
        self.dpp_label = self.create_info_box("DPP", "0")
        self.tarif_label = self.create_info_box("Tarif", "0 %")
        self.pph21_label = self.create_info_box("PPh 21", "0")
        info_layout.addWidget(self.dpp_label)
        info_layout.addWidget(self.tarif_label)
        info_layout.addWidget(self.pph21_label)
        layout.addLayout(info_layout)
        
        layout.addStretch()
        self.setLayout(layout)
        
    def add_form_row(self, parent_layout, label_text, widget):
        """Tambahkan row form dengan label dan widget"""
        row_layout = QHBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("color: #5b6b8c; font-size: 14px;")
        label.setMinimumWidth(250)
        row_layout.addWidget(label)
        row_layout.addWidget(widget, 1)
        parent_layout.addLayout(row_layout)
        
    def create_combo(self, items):
        """Create styled combobox"""
        combo = QComboBox()
        combo.addItems(items)
        combo.setMinimumHeight(45)
        combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #d0d5dd;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                background-color: white;
                color: #1f2937;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #6b7280;
                width: 0px;
                height: 0px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #d0d5dd;
                border-radius: 8px;
                background-color: white;
                selection-background-color: #f3f4f6;
                selection-color: #1f2937;
                outline: none;
                padding: 5px;
            }
            QComboBox QAbstractItemView::item {
                padding: 10px;
                border: none;
                color: #1f2937;
                min-height: 35px;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #f3f4f6;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #e5e7eb;
                color: #1f2937;
            }
        """)
        return combo
        
    def create_input(self, placeholder):
        """Create styled input field"""
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setMinimumHeight(45)
        input_field.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d0d5dd;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                background-color: white;
            }
        """)
        return input_field
        
    def create_info_box(self, label_text, value_text):
        """Create info box untuk menampilkan hasil"""
        box = QFrame()
        box.setStyleSheet("""
            QFrame {
                background-color: #f3f4f6;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        layout = QVBoxLayout(box)
        
        label = QLabel(label_text)
        label.setStyleSheet("color: #6b7280; font-size: 12px;")
        
        value = QLabel(value_text)
        value.setStyleSheet("color: #1f2937; font-size: 18px; font-weight: bold;")
        value.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        layout.addWidget(label)
        layout.addWidget(value)
        return box


class PPh21Widget(QWidget):
    """Main Widget untuk PPh 21"""
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        
        # Header
        header = QLabel("PPh 21")
        header.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        header.setStyleSheet("color: #5b6b8c;")
        main_layout.addWidget(header)
        
        # Content Frame
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        content_layout = QVBoxLayout(content_frame)
        
        # Jenis Pemotongan
        jenis_layout = QHBoxLayout()
        jenis_label = QLabel("Jenis Pemotongan")
        jenis_label.setStyleSheet("color: #5b6b8c; font-size: 14px;")
        jenis_label.setMinimumWidth(250)
        
        self.jenis_combo = QComboBox()
        self.jenis_combo.addItems([
            "PPh 21 Bulanan",
            "PPh 21 Final",
            "PPh 21 Tidak Final",
            "PPh 21 Tahunan"
        ])
        self.jenis_combo.setMinimumHeight(45)
        self.jenis_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #d0d5dd;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                background-color: white;
                color: #1f2937;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #6b7280;
                width: 0px;
                height: 0px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #d0d5dd;
                border-radius: 8px;
                background-color: white;
                selection-background-color: #f3f4f6;
                selection-color: #1f2937;
                outline: none;
                padding: 5px;
            }
            QComboBox QAbstractItemView::item {
                padding: 10px;
                border: none;
                color: #1f2937;
                min-height: 35px;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #f3f4f6;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #e5e7eb;
                color: #1f2937;
            }
        """)
        self.jenis_combo.currentIndexChanged.connect(self.on_jenis_changed)
        
        jenis_layout.addWidget(jenis_label)
        jenis_layout.addWidget(self.jenis_combo, 1)
        content_layout.addLayout(jenis_layout)
        
        # Stacked widget for different forms
        self.stacked_widget = QStackedWidget()
        
        # Add different forms
        self.bulanan_form = PPh21BulananForm()
        self.final_form = QLabel("Form PPh 21 Final - Coming Soon")
        self.final_form.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.final_form.setStyleSheet("color: #9ca3af; font-size: 16px; padding: 50px;")
        
        self.tidak_final_form = QLabel("Form PPh 21 Tidak Final - Coming Soon")
        self.tidak_final_form.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tidak_final_form.setStyleSheet("color: #9ca3af; font-size: 16px; padding: 50px;")
        
        self.tahunan_form = QLabel("Form PPh 21 Tahunan - Coming Soon")
        self.tahunan_form.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tahunan_form.setStyleSheet("color: #9ca3af; font-size: 16px; padding: 50px;")
        
        self.stacked_widget.addWidget(self.bulanan_form)
        self.stacked_widget.addWidget(self.final_form)
        self.stacked_widget.addWidget(self.tidak_final_form)
        self.stacked_widget.addWidget(self.tahunan_form)
        
        content_layout.addWidget(self.stacked_widget)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.btn_hitung = QPushButton("PENGHITUNGAN PPh PASAL 21")
        self.btn_hitung.setMinimumHeight(50)
        self.btn_hitung.setStyleSheet("""
            QPushButton {
                background-color: #2d3748;
                color: white;
                border-radius: 8px;
                padding: 15px 30px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1a202c;
            }
        """)
        self.btn_hitung.clicked.connect(self.hitung_pph21)
        
        self.btn_panduan = QPushButton("📥 Panduan")
        self.btn_panduan.setMinimumHeight(50)
        self.btn_panduan.setStyleSheet("""
            QPushButton {
                background-color: #fbbf24;
                color: #1a202c;
                border-radius: 8px;
                padding: 15px 30px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f59e0b;
            }
        """)
        
        btn_layout.addWidget(self.btn_hitung)
        btn_layout.addWidget(self.btn_panduan)
        content_layout.addLayout(btn_layout)
        
        main_layout.addWidget(content_frame)
        
        # Result box
        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setMinimumHeight(200)
        self.result_box.setStyleSheet("""
            QTextEdit {
                background-color: #f9fafb;
                border: 1px solid #d0d5dd;
                border-radius: 8px;
                padding: 15px;
                font-family: monospace;
                font-size: 13px;
            }
        """)
        main_layout.addWidget(self.result_box)
        
        main_layout.addStretch()
        self.setLayout(main_layout)
        
    def on_jenis_changed(self, index):
        """Handler ketika jenis pemotongan berubah"""
        self.stacked_widget.setCurrentIndex(index)
        
    def hitung_pph21(self):
        """Handler untuk button hitung"""
        current_index = self.jenis_combo.currentIndex()
        
        if current_index == 0:  # Bulanan
            self.hitung_bulanan()
        else:
            self.result_box.setText(f"Perhitungan untuk {self.jenis_combo.currentText()}\n\nComing Soon...")
            
    def hitung_bulanan(self):
        """Hitung PPh 21 Bulanan"""
        try:
            # Ambil data dari form
            bruto_text = self.bulanan_form.bruto_input.text()
            ptkp_text = self.bulanan_form.ptkp_combo.currentText()
            
            # Validasi
            if not bruto_text or "Pilih" in ptkp_text:
                self.result_box.setText("⚠️ Lengkapi semua data terlebih dahulu!")
                return
            
            # Parse input
            bruto = float(bruto_text.replace(",", "").replace(".", ""))
            ptkp_status = ptkp_text.split(" - ")[0]
            
            # Hitung menggunakan logic
            hasil = PPh21Calculator.hitung_pph21_bulanan(bruto, ptkp_status)
            
            # Format dan tampilkan hasil
            result_text = PPh21Calculator.format_hasil(hasil)
            self.result_box.setText(result_text)
            
        except ValueError as e:
            self.result_box.setText(f"❌ Error: {str(e)}")
        except Exception as e:
            self.result_box.setText(f"❌ Terjadi kesalahan: {str(e)}")