"""
Utility functions for the dashboard
Contains AI analysis, script generation, and helper functions
"""

from config import USER_PROFILE, THRESHOLDS


def mock_ai_analysis(client_row):
    """Generate AI-driven insights based on client data"""
    name = client_row["Client Name"]
    giro = client_row["Avg Giro Balance (M)"]
    sme_status = client_row["SME Loan Status"]
    payroll_status = client_row["Payroll Status"]
    txn_freq = client_row["Transaction Frequency"]
    tag = client_row["Opportunity Tag"]
    
    insights = []
    
    # Liquidity Analysis
    if giro >= THRESHOLDS['high_value_giro']:
        insights.append(f"🔴 **CRITICAL ALERT:** {name} memiliki saldo Giro {giro}M namun tidak memiliki pinjaman SME. Risiko tinggi churn ke competitor yang menawarkan lending.")
    elif giro >= THRESHOLDS['medium_value_giro']:
        insights.append(f"⚠️ **PERINGATAN:** Saldo Giro {giro}M cukup tinggi. Opportunity untuk deepening relationship.")
    
    # SME Loan Opportunity
    if sme_status == "None" and giro >= THRESHOLDS['high_value_giro']:
        insights.append(f"💡 **OPPORTUNITY:** Estimasi kebutuhan modal kerja ~Rp {giro * 0.7}M berdasarkan pola transaksi. Pitch Kredit Modal Kerja dengan tenor 12-24 bulan.")
    
    # Payroll Opportunity
    if payroll_status == "None" and giro >= THRESHOLDS['medium_value_giro']:
        insights.append(f"💼 **CROSS-SELL:** Tidak ada Payroll aktif. Potensi revenue Rp {giro * 0.05}M/bulan dari fee Kopra Payroll.")
    
    # Transaction Pattern
    if txn_freq == "High":
        insights.append(f"📊 **BEHAVIOR INSIGHT:** Frekuensi transaksi tinggi menunjukkan aktivitas bisnis yang sehat. Client engagement score: 9/10.")
    elif txn_freq == "Low":
        insights.append(f"⚠️ **CHURN RISK:** Frekuensi transaksi rendah. Perlu investigasi apakah client sudah diversifikasi ke bank lain.")
    
    # Relationship Strategy
    if tag == "TARGET SME LOAN":
        insights.append(f"🎯 **ACTION PLAN:** Segera schedule meeting untuk presentasi Working Capital Loan. Siapkan proposal dengan rate kompetitif.")
    elif tag == "TARGET PAYROLL":
        insights.append(f"🎯 **ACTION PLAN:** Hubungi HRD untuk pitch Kopra Payroll. Emphasize kemudahan integrasi & cost efficiency.")
    
    return "\n\n".join(insights) if insights else "Client dalam kondisi stabil. Monitoring rutin tetap diperlukan."


def generate_script(client_name, tag, giro_balance):
    """Generate draft WhatsApp message based on opportunity type"""
    
    user_name = USER_PROFILE['name']
    user_branch = USER_PROFILE['branch']
    user_phone = USER_PROFILE['phone']
    
    if tag == "TARGET SME LOAN":
        script = f"""Selamat pagi/siang Bapak/Ibu,

Saya {user_name}, Relationship Manager dari Bank Mandiri Cabang {user_branch}.

Terima kasih atas kepercayaan {client_name} selama ini menggunakan layanan Giro kami. Kami melihat aktivitas bisnis Bapak/Ibu sangat baik dengan rata-rata saldo Rp {giro_balance}M.

Sebagai bentuk apresiasi dan untuk mendukung pertumbuhan bisnis, kami ingin menawarkan fasilitas **Kredit Modal Kerja** dengan:
✅ Limit hingga Rp {giro_balance * 0.7}M
✅ Tenor fleksibel 12-24 bulan
✅ Proses approval cepat (3 hari kerja)
✅ Rate kompetitif & competitive

Apakah Bapak/Ibu berkenan untuk saya schedule meeting minggu ini untuk diskusi lebih lanjut?

Terima kasih 🙏

Salam,
{user_name}
RM Bank Mandiri {user_branch}
📱 {user_phone}"""
    
    elif tag == "TARGET PAYROLL":
        script = f"""Selamat pagi/siang Bapak/Ibu,

Saya {user_name}, RM Bank Mandiri yang menangani account {client_name}.

Kami sangat appreciate partnership yang sudah terjalin dengan saldo Giro rata-rata Rp {giro_balance}M.

Saya ingin memperkenalkan solusi **Kopra Payroll** (Kompensasi Prakerja) yang bisa membantu efisiensi operasional HRD:
✅ Otomasi pembayaran gaji karyawan
✅ No cost transfer antar Mandiri
✅ Dashboard monitoring real-time
✅ Potensi penghematan biaya admin hingga 70%

Untuk perusahaan seperti {client_name}, estimasi fee hanya Rp {giro_balance * 0.05}M/bulan.

Boleh saya arrange demo singkat dengan tim HRD minggu ini?

Best regards,
{user_name}
RM Bank Mandiri {user_branch}
📱 {user_phone}"""
    
    else:
        script = f"""Selamat pagi/siang Bapak/Ibu,

Saya {user_name} dari Bank Mandiri {user_branch}.

Terima kasih atas kepercayaan {client_name} menggunakan layanan kami. Saya ingin melakukan courtesy call untuk memastikan semua layanan berjalan dengan baik.

Apakah ada kebutuhan banking lainnya yang bisa kami bantu?

Salam,
{user_name}
📱 {user_phone}"""
    
    return script


def generate_relationship_script(client_row):
    """Generate greeting/milestone script for relationship building"""
    name = client_row["Client Name"]
    tenure = client_row["Tenure Years"]
    loyalty = client_row["Loyalty Status"]
    last_note = client_row["Last Note"]
    
    user_name = USER_PROFILE['name']
    user_branch = USER_PROFILE['branch']
    user_phone = USER_PROFILE['phone']
    
    script = f"""Selamat pagi/siang Bapak/Ibu Pimpinan {name},

Saya {user_name}, Relationship Manager baru di Bank Mandiri Cabang {user_branch}.

Saya baru saja mempelajari portfolio cabang kami dan sangat terkesan melihat {name} telah menjadi nasabah setia Bank Mandiri selama **{tenure} tahun**! Ini adalah pencapaian luar biasa dan kami sangat menghargai kepercayaan yang telah diberikan.

Dari catatan kami: "{last_note}"

Sebagai bentuk apresiasi, saya ingin:
✅ Memperkenalkan diri sebagai PIC baru Anda
✅ Memastikan semua layanan berjalan optimal
✅ Mendengarkan feedback atau kebutuhan baru dari {name}

Apakah Bapak/Ibu berkenan untuk saya jadwalkan courtesy visit minggu ini? Saya ingin memastikan relationship kita tetap kuat dan saling menguntungkan.

Terima kasih atas loyalitas {name} selama {tenure} tahun ini. Kami berkomitmen untuk terus memberikan layanan terbaik.

Salam hormat,
{user_name}
RM Bank Mandiri {user_branch}
📱 {user_phone}

Status Loyalitas: {loyalty} Member ⭐"""
    
    return script
