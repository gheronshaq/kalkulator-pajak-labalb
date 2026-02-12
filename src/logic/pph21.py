"""
logic/pph21.py - Logic untuk perhitungan PPh 21
"""

class PPh21Calculator:
    """Class untuk perhitungan PPh 21"""
    
    # ========================================
    # 1. DATA PTKP (Penghasilan Tidak Kena Pajak) - TAHUNAN
    # ========================================
    PTKP_DATA = {
        "TK/0": 54000000,
        "TK/1": 58500000,
        "TK/2": 63000000,
        "TK/3": 67500000,
        "K/0": 58500000,
        "K/1": 63000000,
        "K/2": 67500000,
        "K/3": 72000000
    }
    
    # ========================================
    # 2. MAPPING PTKP KE KATEGORI TER
    # ========================================
    PTKP_TO_CATEGORY = {
        "TK/0": "A",
        "TK/1": "A",
        "K/0": "A",
        "TK/2": "B",
        "TK/3": "B",
        "K/1": "B",
        "K/2": "B",
        "K/3": "C"
    }
    
    # ========================================
    # 3. TABEL TER BULANAN KATEGORI A
    # ========================================
    TER_KATEGORI_A = [
        (0, 5400000, 0),
        (5400000, 5650000, 0.25),
        (5650000, 5950000, 0.5),
        (5950000, 6300000, 0.75),
        (6300000, 6750000, 1),
        (6750000, 7500000, 1.25),
        (7500000, 8550000, 1.5),
        (8550000, 9650000, 1.75),
        (9650000, 10050000, 2),
        (10050000, 10350000, 2.25),
        (10350000, 10700000, 2.5),
        (10700000, 11050000, 3),
        (11050000, 11600000, 3.5),
        (11600000, 12500000, 4),
        (12500000, 13750000, 5),
        (13750000, 15100000, 6),
        (15100000, 16950000, 7),
        (16950000, 19750000, 8),
        (19750000, 24150000, 9),
        (24150000, 26450000, 10),
        (26450000, 28000000, 11),
        (28000000, 30050000, 12),
        (30050000, 32400000, 13),
        (32400000, 35400000, 14),
        (35400000, 39100000, 15),
        (39100000, 43850000, 16),
        (43850000, 47800000, 17),
        (47800000, 51400000, 18),
        (51400000, 56300000, 19),
        (56300000, 62200000, 20),
        (62200000, 68600000, 21),
        (68600000, 77500000, 22),
        (77500000, 89000000, 23),
        (89000000, 103000000, 24),
        (103000000, 125000000, 25),
        (125000000, 157000000, 26),
        (157000000, 206000000, 27),
        (206000000, 337000000, 28),
        (337000000, 454000000, 29),
        (454000000, 550000000, 30),
        (550000000, 695000000, 31),
        (695000000, 910000000, 32),
        (910000000, 1400000000, 33),
        (1400000000, float('inf'), 34)
    ]
    
    # ========================================
    # 4. TABEL TER BULANAN KATEGORI B
    # ========================================
    TER_KATEGORI_B = [
        (0, 6200000, 0),
        (6200000, 6500000, 0.25),
        (6500000, 6850000, 0.5),
        (6850000, 7300000, 0.75),
        (7300000, 9200000, 1),
        (9200000, 10750000, 1.5),
        (10750000, 11250000, 2),
        (11250000, 11600000, 2.5),
        (11600000, 12600000, 3),
        (12600000, 13600000, 4),
        (13600000, 14950000, 5),
        (14950000, 16400000, 6),
        (16400000, 18450000, 7),
        (18450000, 21850000, 8),
        (21850000, 26000000, 9),
        (26000000, 27700000, 10),
        (27700000, 29350000, 11),
        (29350000, 31450000, 12),
        (31450000, 33950000, 13),
        (33950000, 37100000, 14),
        (37100000, 41100000, 15),
        (41100000, 45800000, 16),
        (45800000, 49500000, 17),
        (49500000, 53800000, 18),
        (53800000, 58500000, 19),
        (58500000, 64000000, 20),
        (64000000, 71000000, 21),
        (71000000, 80000000, 22),
        (80000000, 93000000, 23),
        (93000000, 109000000, 24),
        (109000000, 129000000, 25),
        (129000000, 163000000, 26),
        (163000000, 211000000, 27),
        (211000000, 374000000, 28),
        (374000000, 459000000, 29),
        (459000000, 555000000, 30),
        (555000000, 704000000, 31),
        (704000000, 957000000, 32),
        (957000000, 1405000000, 33),
        (1405000000, float('inf'), 34)
    ]
    
    # ========================================
    # 5. TABEL TER BULANAN KATEGORI C
    # ========================================
    TER_KATEGORI_C = [
        (0, 6600000, 0),
        (6600000, 6950000, 0.25),
        (6950000, 7350000, 0.5),
        (7350000, 7800000, 0.75),
        (7800000, 8850000, 1),
        (8850000, 9800000, 1.25),
        (9800000, 10950000, 1.5),
        (10950000, 11200000, 1.75),
        (11200000, 12050000, 2),
        (12050000, 12950000, 3),
        (12950000, 14150000, 4),
        (14150000, 15550000, 5),
        (15550000, 17050000, 6),
        (17050000, 19500000, 7),
        (19500000, 22700000, 8),
        (22700000, 26600000, 9),
        (26600000, 28100000, 10),
        (28100000, 30100000, 11),
        (30100000, 32600000, 12),
        (32600000, 35400000, 13),
        (35400000, 38900000, 14),
        (38900000, 43000000, 15),
        (43000000, 47400000, 16),
        (47400000, 51200000, 17),
        (51200000, 55800000, 18),
        (55800000, 60400000, 19),
        (60400000, 66700000, 20),
        (66700000, 74500000, 21),
        (74500000, 83300000, 22),
        (83300000, 95600000, 23),
        (95600000, 110000000, 24),
        (110000000, 134000000, 25),
        (134000000, 169000000, 26),
        (169000000, 221000000, 27),
        (221000000, 390000000, 28),
        (390000000, 463000000, 29),
        (463000000, 561000000, 30),
        (561000000, 709000000, 31),
        (709000000, 965000000, 32),
        (965000000, 1419000000, 33),
        (1419000000, float('inf'), 34)
    ]
    
    # ========================================
    # FUNGSI HELPER
    # ========================================
    
    @staticmethod
    def get_ter_category(ptkp_status):
        """Dapatkan kategori TER berdasarkan status PTKP"""
        return PPh21Calculator.PTKP_TO_CATEGORY.get(ptkp_status, "A")
    
    @staticmethod
    def get_tarif_ter(penghasilan_bruto, kategori):
        """Dapatkan tarif TER berdasarkan penghasilan bruto dan kategori"""
        if kategori == "A":
            ter_table = PPh21Calculator.TER_KATEGORI_A
        elif kategori == "B":
            ter_table = PPh21Calculator.TER_KATEGORI_B
        else:  # C
            ter_table = PPh21Calculator.TER_KATEGORI_C
        
        for min_val, max_val, tarif in ter_table:
            if min_val < penghasilan_bruto <= max_val:
                return tarif
        
        return 0
    
    # ========================================
    # FUNGSI UTAMA: HITUNG PPh 21 BULANAN
    # ========================================
    
    @staticmethod
    def hitung_pph21_bulanan(gaji_bruto, ptkp_status, kode_objek, metode_gross="gross", 
                             ada_penghasilan_dipotong=False, penghasilan_dipotong=0):
        """
        Hitung PPh 21 Bulanan dengan metode TER
        
        URUTAN PERHITUNGAN METODE TER:
        1. Validasi input
        2. Hitung total penghasilan bruto
        3. DPP = Total Penghasilan Bruto (TIDAK dikurangi biaya jabatan untuk TER!)
        4. Tentukan kategori TER dari PTKP
        5. Cari tarif TER yang sesuai berdasarkan DPP
        6. Hitung PPh 21 = DPP × Tarif TER
        7. Hitung gaji bersih sesuai metode (Gross/Gross Up)
        
        CATATAN PENTING:
        - Metode TER TIDAK mengurangi biaya jabatan/pensiun dari DPP
        - Biaya jabatan/pensiun hanya untuk informasi, tidak mempengaruhi perhitungan
        - DPP = Penghasilan Bruto (langsung!)
        
        Args:
            gaji_bruto (float): Gaji bruto per bulan
            ptkp_status (str): Status PTKP (TK/0, TK/1, K/0, dst)
            kode_objek (str): Kode objek pajak
            metode_gross (str): "gross" atau "gross_up"
            ada_penghasilan_dipotong (bool): Apakah ada penghasilan yang sudah dipotong
            penghasilan_dipotong (float): Jumlah penghasilan yang sudah dipotong
        
        Returns:
            dict: Dictionary berisi hasil perhitungan lengkap
        """
        
        # ========================================
        # LANGKAH 1: VALIDASI INPUT
        # ========================================
        if gaji_bruto <= 0:
            raise ValueError("Gaji bruto harus lebih dari 0")
        
        if ptkp_status not in PPh21Calculator.PTKP_DATA:
            raise ValueError(f"Status PTKP tidak valid: {ptkp_status}")
        
        # ========================================
        # LANGKAH 2: HITUNG TOTAL PENGHASILAN BRUTO
        # ========================================
        # Jika ada penghasilan yang sudah dipotong, tambahkan ke gaji bruto
        if ada_penghasilan_dipotong and penghasilan_dipotong > 0:
            total_bruto = gaji_bruto + penghasilan_dipotong
        else:
            total_bruto = gaji_bruto
        
        # ========================================
        # LANGKAH 3: HITUNG BIAYA JABATAN/PENSIUN (UNTUK INFORMASI SAJA)
        # ========================================
        # PENTING: Biaya jabatan/pensiun TIDAK digunakan dalam perhitungan TER!
        # Ini hanya untuk informasi di output
        
        # 21-100-01: Pegawai Tetap
        # - Biaya Jabatan 5% dari penghasilan bruto, max Rp 500.000/bulan
        if "Pegawai" in kode_objek or "21-100-01" in kode_objek:
            biaya_pengurang = min(total_bruto * 0.05, 500000)
            jenis_pengurang = "Biaya Jabatan"
        
        # 21-100-02: Penerima Pensiun Berkala
        # - Biaya Pensiun 5% dari penghasilan bruto, max Rp 200.000/bulan
        else:
            biaya_pengurang = min(total_bruto * 0.05, 200000)
            jenis_pengurang = "Biaya Pensiun"
        
        # ========================================
        # LANGKAH 4: HITUNG DPP (DASAR PENGENAAN PAJAK)
        # ========================================
        # RUMUS TER: DPP = Penghasilan Bruto (TIDAK DIKURANGI APAPUN!)
        dpp = total_bruto
        
        # ========================================
        # LANGKAH 5: TENTUKAN KATEGORI TER DARI PTKP
        # ========================================
        kategori_ter = PPh21Calculator.get_ter_category(ptkp_status)
        
        # ========================================
        # LANGKAH 6: CARI TARIF TER YANG SESUAI
        # ========================================
        tarif_persen = PPh21Calculator.get_tarif_ter(dpp, kategori_ter)
        
        # ========================================
        # LANGKAH 7: HITUNG PPh 21 SESUAI METODE
        # ========================================
        
        if metode_gross == "gross":
            # ========================================
            # METODE GROSS: PPh 21 DITANGGUNG KARYAWAN
            # - Pajak dipotong langsung dari gaji
            # - PPh 21 = DPP × Tarif TER
            # - Gaji Bersih = Gaji Bruto - PPh 21
            # ========================================
            
            # Hitung PPh 21 bulanan
            pph21_bulanan = dpp * (tarif_persen / 100)
            
            # Gaji bersih = Bruto - PPh 21
            gaji_bersih = gaji_bruto - pph21_bulanan
            
            # Tidak ada tunjangan PPh 21
            tunjangan_pph21 = 0
            
        else:  # metode_gross == "gross_up"
            # ========================================
            # METODE GROSS UP: PPh 21 DITANGGUNG PERUSAHAAN
            # - Pajak tidak mengurangi gaji karyawan
            # - Hitung tunjangan PPh 21 dengan iterasi
            # - Tunjangan ditambahkan ke penghasilan bruto
            # - Iterasi sampai konvergen
            # ========================================
            
            # Hitung PPh 21 awal
            pph21_bulanan = dpp * (tarif_persen / 100)
            
            # Iterasi untuk mencari nilai gross up yang tepat
            # Maksimal 10 iterasi untuk konvergensi
            for iterasi in range(10):
                # DPP Gross Up = Gaji Bruto + Tunjangan PPh 21 (yang sedang dicari)
                dpp_gross_up = gaji_bruto + pph21_bulanan
                
                # Tambahkan penghasilan dipotong jika ada
                if ada_penghasilan_dipotong and penghasilan_dipotong > 0:
                    dpp_gross_up += penghasilan_dipotong
                
                # Cari tarif TER baru berdasarkan DPP Gross Up
                kategori_ter_new = PPh21Calculator.get_ter_category(ptkp_status)
                tarif_persen_new = PPh21Calculator.get_tarif_ter(dpp_gross_up, kategori_ter_new)
                
                # Hitung PPh 21 baru
                pph21_baru = dpp_gross_up * (tarif_persen_new / 100)
                
                # Jika sudah konvergen (selisih < 1 rupiah), berhenti
                if abs(pph21_baru - pph21_bulanan) < 1:
                    break
                
                # Update nilai untuk iterasi berikutnya
                pph21_bulanan = pph21_baru
                tarif_persen = tarif_persen_new
                dpp = dpp_gross_up
            
            # Tunjangan PPh 21 = PPh 21 yang dihitung
            tunjangan_pph21 = pph21_bulanan
            
            # Gaji bersih = Gaji bruto (tidak dipotong pajak)
            gaji_bersih = gaji_bruto
        
        # ========================================
        # LANGKAH 8: RETURN HASIL PERHITUNGAN
        # ========================================
        return {
            'gaji_bruto': gaji_bruto,
            'penghasilan_dipotong': penghasilan_dipotong if ada_penghasilan_dipotong else 0,
            'total_bruto': total_bruto,
            'jenis_pengurang': jenis_pengurang,
            'biaya_pengurang': biaya_pengurang,
            'dpp': dpp,
            'ptkp_status': ptkp_status,
            'ptkp_tahunan': PPh21Calculator.PTKP_DATA[ptkp_status],
            'kategori_ter': kategori_ter,
            'tarif_persen': tarif_persen,
            'pph21_bulanan': pph21_bulanan,
            'tunjangan_pph21': tunjangan_pph21,
            'gaji_bersih': gaji_bersih,
            'metode': metode_gross,
            'kode_objek': kode_objek
        }
    
    # ========================================
    # FUNGSI FORMAT OUTPUT
    # ========================================
    
    @staticmethod
    def format_hasil(hasil):
        """Format hasil perhitungan ke string yang rapi"""
        metode_text = "GROSS" if hasil['metode'] == "gross" else "GROSS UP"
        
        result = f"""
╔══════════════════════════════════════════════════╗
║      HASIL PERHITUNGAN PPh 21 BULANAN ({metode_text})    ║
╚══════════════════════════════════════════════════╝

📋 INFORMASI DASAR:
─────────────────────────────────────────────────
Kode Objek Pajak    : {hasil['kode_objek']}
Status PTKP         : {hasil['ptkp_status']}
PTKP Tahunan        : Rp {hasil['ptkp_tahunan']:,.0f}
Kategori TER        : {hasil['kategori_ter']}
Metode Perhitungan  : {metode_text}

💰 PERHITUNGAN PENGHASILAN:
─────────────────────────────────────────────────
Gaji Bruto/Bulan    : Rp {hasil['gaji_bruto']:,.0f}
"""
        
        if hasil['penghasilan_dipotong'] > 0:
            result += f"Penghasilan Dipotong: Rp {hasil['penghasilan_dipotong']:,.0f}\n"
            result += f"Total Penghasilan   : Rp {hasil['total_bruto']:,.0f}\n"
        
        result += f"""
{hasil['jenis_pengurang']} (5%) : Rp {hasil['biaya_pengurang']:,.0f}
(Catatan: Biaya ini hanya informasi, tidak mengurangi DPP dalam metode TER)

─────────────────────────────────────────────────
DPP (Dasar Pengenaan): Rp {hasil['dpp']:,.0f}

📊 PERHITUNGAN PAJAK:
─────────────────────────────────────────────────
Tarif TER           : {hasil['tarif_persen']}%
PPh 21 Bulanan      : Rp {hasil['pph21_bulanan']:,.0f}
"""
        
        if hasil['metode'] == "gross_up":
            result += f"Tunjangan PPh 21    : Rp {hasil['tunjangan_pph21']:,.0f}\n"
        
        result += f"""
─────────────────────────────────────────────────
🏠 GAJI BERSIH      : Rp {hasil['gaji_bersih']:,.0f}
─────────────────────────────────────────────────
"""
        
        if hasil['metode'] == "gross_up":
            result += "\n💡 Catatan: Metode Gross Up - PPh 21 ditanggung perusahaan\n"
            result += "   (Gaji yang diterima karyawan = Gaji Bruto)\n"
        else:
            result += "\n💡 Catatan: Metode Gross - PPh 21 dipotong dari gaji\n"
            result += "   (Gaji yang diterima = Gaji Bruto - PPh 21)\n"
        
        result += "\n⚠️  PENTING: Metode TER tidak mengurangi biaya jabatan/pensiun dari DPP!\n"
        result += "   DPP = Penghasilan Bruto (langsung)\n"
        
        return result