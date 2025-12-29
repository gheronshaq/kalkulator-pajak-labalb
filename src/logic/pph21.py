
class PPh21Calculator:
    """Class untuk perhitungan PPh 21"""
    
    # Data PTKP (Penghasilan Tidak Kena Pajak)
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
    
    @staticmethod
    def hitung_pph21_bulanan(gaji_bruto, ptkp_status):
        """
        Hitung PPh 21 Bulanan
        
        Args:
            gaji_bruto (float): Gaji bruto per bulan
            ptkp_status (str): Status PTKP (contoh: "TK/0", "K/1")
        
        Returns:
            dict: Dictionary berisi hasil perhitungan
        """
        # Validasi input
        if gaji_bruto <= 0:
            raise ValueError("Gaji bruto harus lebih dari 0")
        
        if ptkp_status not in PPh21Calculator.PTKP_DATA:
            raise ValueError(f"Status PTKP tidak valid: {ptkp_status}")
        
        # Hitung gaji tahunan
        gaji_tahunan = gaji_bruto * 12
        
        # Biaya jabatan (5% dari gaji tahunan, max 6 juta/tahun)
        biaya_jabatan = min(gaji_tahunan * 0.05, 6000000)
        
        # Penghasilan neto tahunan
        penghasilan_neto = gaji_tahunan - biaya_jabatan
        
        # PTKP
        ptkp = PPh21Calculator.PTKP_DATA[ptkp_status]
        
        # Penghasilan Kena Pajak (PKP)
        pkp = max(0, penghasilan_neto - ptkp)
        
        # Hitung PPh 21 dengan tarif progresif
        pph_tahunan = PPh21Calculator.hitung_pph_progresif(pkp)
        
        # PPh 21 bulanan
        pph_bulanan = pph_tahunan / 12
        
        # Gaji bersih
        gaji_bersih = gaji_bruto - pph_bulanan
        
        # Return hasil perhitungan
        return {
            'gaji_bruto': gaji_bruto,
            'gaji_tahunan': gaji_tahunan,
            'biaya_jabatan': biaya_jabatan,
            'penghasilan_neto': penghasilan_neto,
            'ptkp': ptkp,
            'ptkp_status': ptkp_status,
            'pkp': pkp,
            'pph_tahunan': pph_tahunan,
            'pph_bulanan': pph_bulanan,
            'gaji_bersih': gaji_bersih
        }
    
    @staticmethod
    def hitung_pph_progresif(pkp):
        """
        Hitung PPh dengan tarif progresif
        
        Tarif:
        - 0 - 60 juta: 5%
        - 60 juta - 250 juta: 15%
        - 250 juta - 500 juta: 25%
        - > 500 juta: 30%
        
        Args:
            pkp (float): Penghasilan Kena Pajak
        
        Returns:
            float: Jumlah PPh
        """
        if pkp <= 0:
            return 0
        elif pkp <= 60000000:
            return pkp * 0.05
        elif pkp <= 250000000:
            return (60000000 * 0.05) + ((pkp - 60000000) * 0.15)
        elif pkp <= 500000000:
            return (60000000 * 0.05) + (190000000 * 0.15) + ((pkp - 250000000) * 0.25)
        else:
            return (60000000 * 0.05) + (190000000 * 0.15) + (250000000 * 0.25) + ((pkp - 500000000) * 0.30)
    
    @staticmethod
    def format_hasil(hasil):
        """
        Format hasil perhitungan ke string yang rapi
        
        Args:
            hasil (dict): Dictionary hasil perhitungan
        
        Returns:
            str: String hasil yang sudah diformat
        """
        return f"""
╔══════════════════════════════════════════════════╗
║         HASIL PERHITUNGAN PPh 21 BULANAN         ║
╚══════════════════════════════════════════════════╝

📊 RINCIAN PERHITUNGAN:
─────────────────────────────────────────────────

- Gaji Bruto/Bulan      : Rp {hasil['gaji_bruto']:,.0f}
- Gaji Bruto/Tahun      : Rp {hasil['gaji_tahunan']:,.0f}
- Biaya Jabatan (5%)    : Rp {hasil['biaya_jabatan']:,.0f}
- Penghasilan Neto      : Rp {hasil['penghasilan_neto']:,.0f}
- PTKP ({hasil['ptkp_status']})           : Rp {hasil['ptkp']:,.0f}
- Penghasilan Kena Pajak: Rp {hasil['pkp']:,.0f}

─────────────────────────────────────────────────
💰 PPh 21 TAHUNAN       : Rp {hasil['pph_tahunan']:,.0f}
💵 PPh 21 BULANAN       : Rp {hasil['pph_bulanan']:,.0f}
🏠 GAJI BERSIH/BULAN    : Rp {hasil['gaji_bersih']:,.0f}
─────────────────────────────────────────────────
        """