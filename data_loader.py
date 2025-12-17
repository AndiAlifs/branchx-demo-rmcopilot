"""
Data loading and generation module
Handles all data generation and loading operations
"""

import pandas as pd
import numpy as np
from config import THRESHOLDS


def load_data():
    """Generate dummy corporate client data reflecting liquidity mismatch scenario"""
    np.random.seed(42)
    
    client_names = [
        "PT. Maju Mundur", "PT. Karya Sejahtera", "PT. Sukses Bersama",
        "PT. Indo Makmur", "PT. Sentosa Jaya", "PT. Buana Perkasa",
        "PT. Mega Indah", "PT. Surya Gemilang", "PT. Citra Abadi",
        "PT. Duta Mandiri", "PT. Graha Prima", "PT. Harapan Kita",
        "PT. Jaya Raya", "PT. Kartika Sari", "PT. Lestari Makmur",
        "PT. Mitra Usaha", "PT. Nusantara Sejahtera", "PT. Pelita Harapan",
        "PT. Rezeki Berlimpah", "PT. Trijaya Abadi"
    ]
    
    last_notes_samples = [
        "Anak pemilik baru lulus kuliah dari ITB jurusan Teknik Industri",
        "Komplain kliring bulan lalu sudah selesai, klien puas dengan penanganan",
        "Merayakan ulang tahun perusahaan ke-20 bulan depan",
        "Sedang ekspansi ke Surabaya, butuh info cabang di sana",
        "Direktur baru dilantik 3 bulan lalu, masih adaptasi",
        "Pernah komplain tentang service charge, sudah direview",
        "Loyal sejak era Pak Harto, generasi ke-2 sekarang yang handle",
        "Istri owner adalah guru besar UI, sering keluar negeri",
        "Baru saja merger dengan PT lain, struktur organisasi berubah",
        "Klien sangat peduli CSR, aktif di Rotary Club",
        "Pernah ada issue fraud internal tahun lalu, sudah clear",
        "Owner hobi golf, member di Pondok Indah Golf",
        "Perusahaan keluarga, sangat menjaga privasi",
        "Sedang proses suksesi ke anak, butuh pendampingan",
        "Pernah pindah ke bank lain, kembali 2 tahun lalu",
        "Supplier utama untuk perusahaan BUMN",
        "Cash flow sangat teratur, jarang ada masalah",
        "Owner adalah alumni Mandiri program beasiswa",
        "Bisnis turun-temurun sejak kakek, sudah 3 generasi",
        "Baru selesai renovasi kantor besar-besaran"
    ]
    
    data = []
    for i, name in enumerate(client_names):
        # Generate data with intentional mismatch (high giro, low loans)
        giro_balance = np.random.choice([500, 800, 1200, 1500, 2500, 3500, 5000, 8000, 10000], 
                                       p=[0.15, 0.15, 0.15, 0.15, 0.15, 0.10, 0.08, 0.04, 0.03])
        
        # Most clients don't have SME loans (reflecting the gap)
        sme_status = np.random.choice(["None", "Active"], p=[0.75, 0.25])
        
        # Mix of payroll statuses
        payroll_status = np.random.choice(["None", "Active"], p=[0.60, 0.40])
        
        # Transaction frequency
        txn_freq = np.random.choice(["Low", "Medium", "High"], p=[0.2, 0.5, 0.3])
        
        # Relationship Health fields
        tenure_years = np.random.choice(
            [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 18, 20, 22, 25],
            p=[0.05, 0.05, 0.08, 0.08, 0.10, 0.10, 0.10, 0.10, 0.10, 0.08, 0.06, 0.04, 0.03, 0.02, 0.01]
        )
        
        # Days since contact - weighted towards recent but some neglected
        days_since_contact = np.random.choice(
            [3, 7, 14, 21, 30, 45, 60, 90, 120, 180, 240, 365],
            p=[0.15, 0.15, 0.15, 0.12, 0.10, 0.08, 0.07, 0.06, 0.05, 0.04, 0.02, 0.01]
        )
        
        # Loyalty Status based on tenure
        if tenure_years > THRESHOLDS['platinum_years']:
            loyalty_status = "Platinum"
        elif tenure_years > THRESHOLDS['gold_years']:
            loyalty_status = "Gold"
        else:
            loyalty_status = "Silver"
        
        # Last note
        last_note = last_notes_samples[i]
        
        # Calculate opportunity tag
        if giro_balance >= THRESHOLDS['high_value_giro'] and sme_status == "None":
            tag = "TARGET SME LOAN"
            potential_value = giro_balance * 0.7  # 70% of balance as loan potential
        elif giro_balance >= THRESHOLDS['medium_value_giro'] and payroll_status == "None":
            tag = "TARGET PAYROLL"
            potential_value = giro_balance * 0.05  # 5% monthly fee potential
        else:
            tag = "MAINTAIN"
            potential_value = giro_balance * 0.02
        
        data.append({
            "Client Name": name,
            "Avg Giro Balance (M)": giro_balance,
            "Transaction Frequency": txn_freq,
            "SME Loan Status": sme_status,
            "Payroll Status": payroll_status,
            "Opportunity Tag": tag,
            "Potential Value (M)": round(potential_value, 1),
            "Tenure Years": tenure_years,
            "Days Since Contact": days_since_contact,
            "Loyalty Status": loyalty_status,
            "Last Note": last_note
        })
    
    return pd.DataFrame(data)
