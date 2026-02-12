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


class CustomComboBox(QComboBox):
    """Custom ComboBox yang tidak berubah saat di-scroll"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def wheelEvent(self, event):
        """Override wheelEvent untuk mencegah perubahan nilai saat scroll"""
        # Jika dropdown sedang tidak terbuka, abaikan scroll
        if not self.view().isVisible():
            event.ignore()
        else:
            # Jika dropdown terbuka, izinkan scroll normal
            super().wheelEvent(event)


class PPh21BulananForm(QWidget):
    """Form untuk PPh 21 Bulanan"""
    def __init__(self):
        super().__init__()
        self.is_formatting = False  # Flag untuk mencegah infinite loop saat formatting
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
        self.radio_gross = QRadioButton("Gross (PPh dipotong dari gaji)")
        self.radio_gross_up = QRadioButton("Gross Up (PPh ditanggung perusahaan)")
        self.radio_gross.setChecked(True)
        self.radio_gross.setStyleSheet("color: #7b2f8f; font-size: 14px;")
        self.radio_gross_up.setStyleSheet("color: #7b2f8f; font-size: 14px;")
        radio_layout.addWidget(self.radio_gross)
        radio_layout.addWidget(self.radio_gross_up)
        radio_layout.addStretch()
        self.add_form_row(layout, "Skema Perhitungan", radio_widget)
        
        # Checkbox untuk penghasilan yang sudah dipotong
        self.checkbox_dipotong = QCheckBox("Ada penghasilan yang sudah dipotong PPh 21")
        self.checkbox_dipotong.setStyleSheet("color: #7b2f8f; font-size: 14px;")
        self.checkbox_dipotong.stateChanged.connect(self.toggle_penghasilan_dipotong)
        self.add_form_row(layout, "Penghasilan yang telah dipotong\nPPh Pasal 21 pada masa pajak\nyang sama", 
                         self.checkbox_dipotong)
        
        # Input penghasilan yang dipotong (hidden by default)
        self.dipotong_input = self.create_input("Masukkan jumlah penghasilan yang sudah dipotong")
        self.dipotong_input.setVisible(False)
        
        # Row untuk penghasilan dipotong dengan label
        dipotong_row = QHBoxLayout()
        self.dipotong_label = QLabel("Jumlah Penghasilan Dipotong")
        self.dipotong_label.setStyleSheet("color: #5b6b8c; font-size: 14px;")
        self.dipotong_label.setMinimumWidth(250)
        self.dipotong_label.setVisible(False)
        
        dipotong_row.addWidget(self.dipotong_label)
        dipotong_row.addWidget(self.dipotong_input, 1)
        layout.addLayout(dipotong_row)
        
        # Penghasilan Bruto - pastikan terlihat
        self.bruto_input = self.create_input("Masukkan gaji bruto bulanan")
        self.bruto_input.setMinimumHeight(45)
        self.bruto_input.textChanged.connect(self.format_currency)
        self.add_form_row(layout, "Penghasilan Bruto/Bulan", self.bruto_input)
        
        # PTKP
        self.ptkp_combo = self.create_combo([
            "Pilih Status PTKP",
            "TK/0 - Tidak Kawin, 0 Tanggungan",
            "TK/1 - Tidak Kawin, 1 Tanggungan",
            "TK/2 - Tidak Kawin, 2 Tanggungan",
            "TK/3 - Tidak Kawin, 3 Tanggungan",
            "K/0 - Kawin, 0 Tanggungan",
            "K/1 - Kawin, 1 Tanggungan",
            "K/2 - Kawin, 2 Tanggungan",
            "K/3 - Kawin, 3 Tanggungan"
        ])
        self.add_form_row(layout, "Status PTKP", self.ptkp_combo)
        
        # Info boxes
        info_layout = QHBoxLayout()
        self.dpp_frame = self.create_info_box("DPP", "Rp 0")
        self.tarif_frame = self.create_info_box("Tarif TER", "0 %")
        self.pph21_frame = self.create_info_box("PPh 21", "Rp 0")
        info_layout.addWidget(self.dpp_frame)
        info_layout.addWidget(self.tarif_frame)
        info_layout.addWidget(self.pph21_frame)
        layout.addLayout(info_layout)
        
        layout.addStretch()
        self.setLayout(layout)
        
    def toggle_penghasilan_dipotong(self, state):
        """Toggle visibility of penghasilan dipotong input"""
        is_checked = state == Qt.CheckState.Checked.value
        self.dipotong_input.setVisible(is_checked)
        self.dipotong_label.setVisible(is_checked)
        
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
        """Create styled combobox dengan fix scroll bug"""
        combo = CustomComboBox()  # Gunakan CustomComboBox
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
                color: #1f2937;
            }
            QLineEdit:focus {
                border: 2px solid #691B8D;
                background-color: white;
            }
            QLineEdit::placeholder {
                color: #9ca3af;
            }
        """)
        return input_field
        
    def format_currency(self):
        """Real-time currency formatting untuk bruto_input dengan format Rupiah Indonesia"""
        if self.is_formatting:
            return
            
        self.is_formatting = True
        
        try:
            # Ambil text dan cursor position
            text = self.bruto_input.text()
            cursor_pos = self.bruto_input.cursorPosition()
            
            # Extract hanya angka dari text
            only_digits = ''.join(filter(str.isdigit, text))
            
            # Format dengan separator ribuan (dots untuk Indonesian Rupiah)
            if only_digits:
                formatted = ""
                for i, digit in enumerate(reversed(only_digits)):
                    if i > 0 and i % 3 == 0:
                        formatted = "." + formatted
                    formatted = digit + formatted
            else:
                formatted = ""
            
            # Update text tanpa trigger recursive textChanged
            self.bruto_input.blockSignals(True)
            self.bruto_input.setText(formatted)
            
            original_pos = cursor_pos
            dots_added = 0
            
            if formatted:
                
                digits_before = 0
                for i in range(original_pos):
                    if i < len(text) and text[i].isdigit():
                        digits_before += 1
                
                # Hitung dots dalam format string sebelum position yang baru
                digits_count = 0
                for i, char in enumerate(formatted):
                    if char.isdigit():
                        digits_count += 1
                    if digits_count == digits_before:
                        cursor_pos = i + 1
                        break
                else:
                    cursor_pos = len(formatted)
            
            self.bruto_input.setCursorPosition(cursor_pos)
            self.bruto_input.blockSignals(False)
            
        finally:
            self.is_formatting = False
        
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
        value.setObjectName("value_label")
        value.setStyleSheet("color: #1f2937; font-size: 18px; font-weight: bold;")
        value.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        layout.addWidget(label)
        layout.addWidget(value)
        return box
    
    def update_info_boxes(self, dpp, tarif, pph21):
        """Update nilai di info boxes"""
        # Update DPP
        dpp_label = self.dpp_frame.findChild(QLabel, "value_label")
        if dpp_label:
            dpp_label.setText(f"Rp {dpp:,.0f}")
        
        # Update Tarif
        tarif_label = self.tarif_frame.findChild(QLabel, "value_label")
        if tarif_label:
            tarif_label.setText(f"{tarif}%")
        
        # Update PPh 21
        pph21_label = self.pph21_frame.findChild(QLabel, "value_label")
        if pph21_label:
            pph21_label.setText(f"Rp {pph21:,.0f}")


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
        
        self.jenis_combo = CustomComboBox()  # Gunakan CustomComboBox
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
        
        self.btn_hitung = QPushButton("HITUNG PPh PASAL 21")
        self.btn_hitung.setMinimumHeight(50)
        self.btn_hitung.setStyleSheet("""
            QPushButton {
                background-color: #691B8D;
                color: white;
                border-radius: 8px;
                padding: 15px 30px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4a1262;
            }
        """)
        self.btn_hitung.clicked.connect(self.hitung_pph21)
        
        btn_layout.addWidget(self.btn_hitung)
        content_layout.addLayout(btn_layout)
        
        main_layout.addWidget(content_frame)
        
        # Result box
        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setMinimumHeight(400)
        self.result_box.setStyleSheet("""
            QTextEdit {
                background-color: #f9fafb;
                border: 1px solid #d0d5dd;
                border-radius: 8px;
                padding: 15px;
                font-family: 'Courier New', monospace;
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
            kode_text = self.bulanan_form.kode_combo.currentText()
            bruto_text = self.bulanan_form.bruto_input.text()
            ptkp_text = self.bulanan_form.ptkp_combo.currentText()
            
            # Validasi
            if "Pilih" in kode_text:
                self.result_box.setText("⚠️ Silakan pilih Kode Objek Pajak!")
                return
                
            if not bruto_text:
                self.result_box.setText("⚠️ Silakan masukkan Penghasilan Bruto!")
                return
                
            if "Pilih" in ptkp_text:
                self.result_box.setText("⚠️ Silakan pilih Status PTKP!")
                return
            
            # Parse input
            bruto = float(bruto_text.replace(",", "").replace(".", "").replace("Rp", "").strip())
            ptkp_status = ptkp_text.split(" - ")[0]
            
            # Cek metode gross
            metode = "gross" if self.bulanan_form.radio_gross.isChecked() else "gross_up"
            
            # Cek penghasilan yang sudah dipotong
            ada_dipotong = self.bulanan_form.checkbox_dipotong.isChecked()
            penghasilan_dipotong = 0
            
            if ada_dipotong:
                dipotong_text = self.bulanan_form.dipotong_input.text()
                if dipotong_text:
                    penghasilan_dipotong = float(dipotong_text.replace(",", "").replace(".", "").replace("Rp", "").strip())
            
            # Hitung menggunakan logic
            hasil = PPh21Calculator.hitung_pph21_bulanan(
                gaji_bruto=bruto,
                ptkp_status=ptkp_status,
                kode_objek=kode_text,
                metode_gross=metode,
                ada_penghasilan_dipotong=ada_dipotong,
                penghasilan_dipotong=penghasilan_dipotong
            )
            
            # Update info boxes
            self.bulanan_form.update_info_boxes(
                hasil['dpp'],
                hasil['tarif_persen'],
                hasil['pph21_bulanan']
            )
            
            # Format dan tampilkan hasil
            result_text = PPh21Calculator.format_hasil(hasil)
            self.result_box.setText(result_text)
            
        except ValueError as e:
            self.result_box.setText(f"❌ Error: {str(e)}\n\nPastikan semua input berupa angka yang valid!")
        except Exception as e:
            self.result_box.setText(f"❌ Terjadi kesalahan: {str(e)}")