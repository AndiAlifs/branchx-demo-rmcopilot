import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set Layout to Wide
st.set_page_config(page_title="Mandiri Smart-RM Co-Pilot", layout="wide")

# Data Generation Function
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
        
        # NEW: Relationship Health fields
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
        if tenure_years > 15:
            loyalty_status = "Platinum"
        elif tenure_years > 5:
            loyalty_status = "Gold"
        else:
            loyalty_status = "Silver"
        
        # Last note
        last_note = last_notes_samples[i]
        
        # Calculate opportunity tag
        if giro_balance >= 2000 and sme_status == "None":
            tag = "TARGET SME LOAN"
            potential_value = giro_balance * 0.7  # 70% of balance as loan potential
        elif giro_balance >= 1000 and payroll_status == "None":
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

# Mock AI Analysis Function
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
    if giro >= 2000:
        insights.append(f"🔴 **CRITICAL ALERT:** {name} memiliki saldo Giro {giro}M namun tidak memiliki pinjaman SME. Risiko tinggi churn ke competitor yang menawarkan lending.")
    elif giro >= 1000:
        insights.append(f"⚠️ **PERINGATAN:** Saldo Giro {giro}M cukup tinggi. Opportunity untuk deepening relationship.")
    
    # SME Loan Opportunity
    if sme_status == "None" and giro >= 2000:
        insights.append(f"💡 **OPPORTUNITY:** Estimasi kebutuhan modal kerja ~Rp {giro * 0.7}M berdasarkan pola transaksi. Pitch Kredit Modal Kerja dengan tenor 12-24 bulan.")
    
    # Payroll Opportunity
    if payroll_status == "None" and giro >= 1000:
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

# Generate WhatsApp Script
def generate_script(client_name, tag, giro_balance):
    """Generate draft WhatsApp message based on opportunity type"""
    
    if tag == "TARGET SME LOAN":
        script = f"""Selamat pagi/siang Bapak/Ibu,

Saya Budi Santoso, Relationship Manager dari Bank Mandiri Cabang BSD Tangerang.

Terima kasih atas kepercayaan {client_name} selama ini menggunakan layanan Giro kami. Kami melihat aktivitas bisnis Bapak/Ibu sangat baik dengan rata-rata saldo Rp {giro_balance}M.

Sebagai bentuk apresiasi dan untuk mendukung pertumbuhan bisnis, kami ingin menawarkan fasilitas **Kredit Modal Kerja** dengan:
✅ Limit hingga Rp {giro_balance * 0.7}M
✅ Tenor fleksibel 12-24 bulan
✅ Proses approval cepat (3 hari kerja)
✅ Rate kompetitif & competitive

Apakah Bapak/Ibu berkenan untuk saya schedule meeting minggu ini untuk diskusi lebih lanjut?

Terima kasih 🙏

Salam,
Budi Santoso
RM Bank Mandiri BSD
📱 0812-3456-7890"""
    
    elif tag == "TARGET PAYROLL":
        script = f"""Selamat pagi/siang Bapak/Ibu,

Saya Budi Santoso, RM Bank Mandiri yang menangani account {client_name}.

Kami sangat appreciate partnership yang sudah terjalin dengan saldo Giro rata-rata Rp {giro_balance}M.

Saya ingin memperkenalkan solusi **Kopra Payroll** (Kompensasi Prakerja) yang bisa membantu efisiensi operasional HRD:
✅ Otomasi pembayaran gaji karyawan
✅ No cost transfer antar Mandiri
✅ Dashboard monitoring real-time
✅ Potensi penghematan biaya admin hingga 70%

Untuk perusahaan seperti {client_name}, estimasi fee hanya Rp {giro_balance * 0.05}M/bulan.

Boleh saya arrange demo singkat dengan tim HRD minggu ini?

Best regards,
Budi Santoso
RM Bank Mandiri BSD
📱 0812-3456-7890"""
    
    else:
        script = f"""Selamat pagi/siang Bapak/Ibu,

Saya Budi Santoso dari Bank Mandiri BSD.

Terima kasih atas kepercayaan {client_name} menggunakan layanan kami. Saya ingin melakukan courtesy call untuk memastikan semua layanan berjalan dengan baik.

Apakah ada kebutuhan banking lainnya yang bisa kami bantu?

Salam,
Budi Santoso
📱 0812-3456-7890"""
    
    return script

# Generate Relationship Script
def generate_relationship_script(client_row):
    """Generate greeting/milestone script for relationship building"""
    name = client_row["Client Name"]
    tenure = client_row["Tenure Years"]
    loyalty = client_row["Loyalty Status"]
    last_note = client_row["Last Note"]
    
    script = f"""Selamat pagi/siang Bapak/Ibu Pimpinan {name},

Saya Budi Santoso, Relationship Manager baru di Bank Mandiri Cabang BSD Tangerang.

Saya baru saja mempelajari portfolio cabang kami dan sangat terkesan melihat {name} telah menjadi nasabah setia Bank Mandiri selama **{tenure} tahun**! Ini adalah pencapaian luar biasa dan kami sangat menghargai kepercayaan yang telah diberikan.

Dari catatan kami: "{last_note}"

Sebagai bentuk apresiasi, saya ingin:
✅ Memperkenalkan diri sebagai PIC baru Anda
✅ Memastikan semua layanan berjalan optimal
✅ Mendengarkan feedback atau kebutuhan baru dari {name}

Apakah Bapak/Ibu berkenan untuk saya jadwalkan courtesy visit minggu ini? Saya ingin memastikan relationship kita tetap kuat dan saling menguntungkan.

Terima kasih atas loyalitas {name} selama {tenure} tahun ini. Kami berkomitmen untuk terus memberikan layanan terbaik.

Salam hormat,
Budi Santoso
RM Bank Mandiri BSD
📱 0812-3456-7890

Status Loyalitas: {loyalty} Member ⭐"""
    
    return script

# Initialize session state
if 'selected_client' not in st.session_state:
    st.session_state['selected_client'] = None
if 'pipeline_updates' not in st.session_state:
    st.session_state['pipeline_updates'] = {}
if 'selected_relationship_client' not in st.session_state:
    st.session_state['selected_relationship_client'] = None

# Load data
df = load_data()

# ========== ZONE 1: SIDEBAR ==========
with st.sidebar:
    st.title("🏦 Mandiri Smart-RM")
    st.markdown("---")
    
    # User Profile
    st.markdown("### 👤 Profil")
    st.write("**RM:** Budi Santoso")
    st.write("**Cabang:** Tangerang BSD")
    st.write(f"**Tanggal:** {datetime.now().strftime('%d %B %Y')}")
    
    st.markdown("---")
    
    # Branch KPIs
    st.markdown("### 📊 Performa Cabang")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="Giro (Funding)", 
            value="118%", 
            delta="+Rp 98M",
            delta_color="normal"
        )
    with col2:
        st.metric(
            label="SME (Lending)", 
            value="33%", 
            delta="-Rp 144M",
            delta_color="inverse"
        )
    
    st.metric(
        label="Tabungan (Retail)", 
        value="85%", 
        delta="-Rp 22M",
        delta_color="inverse"
    )
    
    st.markdown("---")
    
    # Problem Statement
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #c92a2a;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
    ">
        <h3 style="color: white; margin: 0 0 10px 0; font-size: 18px;">
            LIQUIDITY UNBALANCE
        </h3>
        <p style="color: white; margin: 0; font-size: 14px; line-height: 1.6;">
            Funding Giro tinggi namun lending SME sangat rendah. 
            <strong>Diperlukan tindakan segera</strong> untuk menyeimbangkan portfolio.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation
    view_mode = st.radio("📍 Navigasi", ["Smart Opportunities", "Relationship Health", "Data View", "Analytics"])

# ========== MAIN LAYOUT ==========

if view_mode == "Relationship Health":
    # NEW: Relationship Health Dashboard
    st.header("💝 Relationship Health Dashboard")
    st.markdown("*Memastikan nasabah loyal merasa dihargai dan dikenali*")
    st.markdown("---")
    
    # Retention KPIs
    st.subheader("📊 Retention KPIs")
    col_r1, col_r2, col_r3, col_r4 = st.columns(4)
    
    loyal_clients = df[df["Tenure Years"] > 10]
    ignored_loyal = df[(df["Tenure Years"] > 10) & (df["Days Since Contact"] > 90)]
    platinum_clients = df[df["Loyalty Status"] == "Platinum"]
    at_risk_clients = df[(df["Avg Giro Balance (M)"] > 1000) & (df["Days Since Contact"] > 120)]
    
    with col_r1:
        st.metric("Nasabah Loyal (>10 Tahun)", len(loyal_clients), f"{len(loyal_clients)/len(df)*100:.0f}%")
    with col_r2:
        st.metric("Loyal Tapi Terabaikan", len(ignored_loyal), "Action needed!", delta_color="inverse")
    with col_r3:
        st.metric("Platinum Members", len(platinum_clients), f"{len(platinum_clients)/len(df)*100:.0f}%")
    with col_r4:
        st.metric("At-Risk (High Value)", len(at_risk_clients), "Need attention", delta_color="inverse")
    
    st.markdown("---")
    
    # Milestone Celebrations
    st.subheader("🎉 Milestone Celebrations - Top 3 Oldest Customers")
    
    oldest_clients = df.nlargest(3, "Tenure Years")
    
    for idx, row in oldest_clients.iterrows():
        with st.container():
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                border-radius: 10px;
                border-left: 5px solid #5a67d8;
                margin-bottom: 15px;
                color: white;
            ">
                <h3 style="margin: 0; color: white;">{row['Client Name']}</h3>
                <p style="margin: 5px 0; font-size: 18px;"><strong>{row['Tenure Years']} TAHUN</strong> bersama Bank Mandiri | Status: {row['Loyalty Status']}</p>
                <p style="margin: 5px 0; font-size: 14px;">Giro: Rp {row['Avg Giro Balance (M)']}M | Terakhir kontak: {row['Days Since Contact']} hari lalu</p>
            </div>
            """, unsafe_allow_html=True)
            
            col_cel1, col_cel2 = st.columns([7, 3])
            
            with col_cel1:
                celebration_script = generate_relationship_script(row)
                st.text_area(
                    f"Skrip Apresiasi untuk {row['Client Name']}", 
                    value=celebration_script, 
                    height=200,
                    key=f"celebration_{idx}"
                )
            
            with col_cel2:
                st.write(f"**Catatan Terakhir:**")
                st.info(row['Last Note'])
                
                if st.button(f"📋 Salin Skrip", key=f"copy_cel_{idx}"):
                    st.success("Skrip berhasil disalin!")
                
                if st.button(f"✉️ Kirim WA", key=f"send_cel_{idx}"):
                    st.success("Membuka WhatsApp...")
    
    st.markdown("---")
    
    # Action Tabs
    tab1, tab2 = st.tabs(["🎯 Priority Recognition", "🔄 Re-engagement Needed"])
    
    with tab1:
        st.subheader("Nasabah High Tenure yang Perlu Pengakuan")
        
        high_tenure = df[df["Tenure Years"] >= 10].sort_values("Tenure Years", ascending=False)
        
        st.markdown(f"**{len(high_tenure)} nasabah** telah setia lebih dari 10 tahun")
        
        for idx, row in high_tenure.iterrows():
            with st.expander(f"📌 {row['Client Name']} - {row['Tenure Years']} tahun - {row['Loyalty Status']}"):
                col_t1, col_t2, col_t3 = st.columns([2, 2, 1])
                
                with col_t1:
                    st.write(f"**Saldo Giro:** Rp {row['Avg Giro Balance (M)']}M")
                    st.write(f"**Frekuensi Transaksi:** {row['Transaction Frequency']}")
                    st.write(f"**Terakhir Kontak:** {row['Days Since Contact']} hari lalu")
                
                with col_t2:
                    st.write(f"**Status SME:** {row['SME Loan Status']}")
                    st.write(f"**Payroll:** {row['Payroll Status']}")
                    st.write(f"**Tag Peluang:** {row['Opportunity Tag']}")
                
                with col_t3:
                    if st.button(f"🔍 Detail", key=f"detail_t1_{idx}"):
                        st.session_state['selected_relationship_client'] = row['Client Name']
                        st.rerun()
                
                st.markdown("**Context:**")
                st.info(row['Last Note'])
    
    with tab2:
        st.subheader("Nasabah Bernilai Tinggi yang Lama Tidak Dihubungi")
        
        reengagement = df[(df["Avg Giro Balance (M)"] >= 1000) & (df["Days Since Contact"] > 60)].sort_values("Days Since Contact", ascending=False)
        
        st.markdown(f"**{len(reengagement)} nasabah** dengan saldo tinggi namun lama tidak dihubungi")
        
        # Color code by urgency
        for idx, row in reengagement.iterrows():
            days = row['Days Since Contact']
            
            if days > 180:
                urgency_color = "#e74c3c"  # Red - Critical
                urgency_label = "CRITICAL"
            elif days > 90:
                urgency_color = "#f39c12"  # Orange - High
                urgency_label = "HIGH"
            else:
                urgency_color = "#3498db"  # Blue - Medium
                urgency_label = "MEDIUM"
            
            with st.expander(f"{urgency_label} {row['Client Name']} - {days} hari | {row['Tenure Years']} tahun tenure"):
                col_t1, col_t2, col_t3 = st.columns([2, 2, 1])
                
                with col_t1:
                    st.write(f"**Saldo Giro:** Rp {row['Avg Giro Balance (M)']}M")
                    st.write(f"**Status Loyalitas:** {row['Loyalty Status']}")
                    st.write(f"**Tenure:** {row['Tenure Years']} tahun")
                
                with col_t2:
                    st.write(f"**Terakhir Kontak:** {days} hari lalu")
                    st.write(f"**Frekuensi Transaksi:** {row['Transaction Frequency']}")
                    st.write(f"**Risiko:** {'Sangat Tinggi' if days > 180 else 'Tinggi' if days > 90 else 'Sedang'}")
                
                with col_t3:
                    if st.button(f"🔍 Re-engage", key=f"detail_t2_{idx}"):
                        st.session_state['selected_relationship_client'] = row['Client Name']
                        st.rerun()
                
                st.markdown("**Last Context:**")
                st.warning(row['Last Note'])
    
    # Context Log Panel
    if st.session_state['selected_relationship_client']:
        st.markdown("---")
        st.subheader(f"📝 Context Log: {st.session_state['selected_relationship_client']}")
        
        client_row = df[df["Client Name"] == st.session_state['selected_relationship_client']].iloc[0]
        
        col_ctx1, col_ctx2 = st.columns([6, 4])
        
        with col_ctx1:
            st.markdown("**Informasi Lengkap untuk RM Baru:**")
            
            st.write(f"**Nama Perusahaan:** {client_row['Client Name']}")
            st.write(f"**Status Loyalitas:** {client_row['Loyalty Status']}")
            st.write(f"**Tenure:** {client_row['Tenure Years']} tahun")
            st.write(f"**Saldo Giro:** Rp {client_row['Avg Giro Balance (M)']}M")
            st.write(f"**Terakhir Dihubungi:** {client_row['Days Since Contact']} hari yang lalu")
            st.write(f"**Frekuensi Transaksi:** {client_row['Transaction Frequency']}")
            
            st.markdown("---")
            st.markdown("**Catatan Penting (Context History):**")
            st.text_area(
                "Last Note", 
                value=client_row['Last Note'],
                height=100,
                key="context_note",
                help="Informasi penting yang harus diketahui RM baru"
            )
            
            st.markdown("---")
            st.markdown("**Suggested Greeting Script:**")
            greeting_script = generate_relationship_script(client_row)
            st.text_area(
                "Draft Pesan",
                value=greeting_script,
                height=300,
                key="greeting_script"
            )
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("📋 Salin Skrip"):
                    st.success("Skrip berhasil disalin!")
            with col_btn2:
                if st.button("✉️ Kirim via WA"):
                    st.success("Membuka WhatsApp...")
        
        with col_ctx2:
            st.markdown("**Quick Actions:**")
            
            with st.form("relationship_update"):
                contact_date = st.date_input("Tanggal Kontak", datetime.now())
                contact_type = st.selectbox(
                    "Tipe Kontak",
                    ["Phone Call", "WhatsApp", "Email", "Meeting", "Courtesy Visit"]
                )
                notes = st.text_area("Catatan Baru", placeholder="Tambahkan catatan tentang interaksi...")
                next_action = st.text_input("Follow-up Action", placeholder="Tindakan selanjutnya...")
                
                submitted = st.form_submit_button("💾 Simpan Log Kontak")
                
                if submitted:
                    st.success(f"Log kontak untuk {client_row['Client Name']} berhasil disimpan!")
                    st.info(f"Kontak via {contact_type} pada {contact_date}")
            
            st.markdown("---")
            st.markdown("**Red Flags:**")
            
            if client_row['Days Since Contact'] > 180:
                st.error("Lebih dari 6 bulan tidak dihubungi!")
            elif client_row['Days Since Contact'] > 90:
                st.warning("Lebih dari 3 bulan tidak dihubungi")
            
            if client_row['Transaction Frequency'] == "Low":
                st.warning("Frekuensi transaksi rendah")
            
            if client_row['Tenure Years'] > 15 and client_row['Days Since Contact'] > 60:
                st.error("Nasabah VIP lama tidak diperhatikan!")

elif view_mode == "Data View":
    # Full-width table view
    st.header("📋 Data Semua Klien")
    st.markdown("---")
    
    # Add filters
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        filter_tag = st.multiselect(
            "Filter berdasarkan Tag Peluang",
            options=df["Opportunity Tag"].unique(),
            default=df["Opportunity Tag"].unique()
        )
    with col_f2:
        filter_sme = st.multiselect(
            "Filter berdasarkan Status Pinjaman SME",
            options=df["SME Loan Status"].unique(),
            default=df["SME Loan Status"].unique()
        )
    with col_f3:
        min_giro = st.number_input("Saldo Giro Minimum (M)", min_value=0, value=0, step=100)
    
    # Apply filters
    filtered_df = df[
        (df["Opportunity Tag"].isin(filter_tag)) &
        (df["SME Loan Status"].isin(filter_sme)) &
        (df["Avg Giro Balance (M)"] >= min_giro)
    ]
    
    st.markdown(f"Menampilkan **{len(filtered_df)}** klien dari total **{len(df)}** klien")
    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=600,
        column_config={
            "Client Name": st.column_config.TextColumn("Nama Klien", width="medium"),
            "Avg Giro Balance (M)": st.column_config.NumberColumn("Saldo Giro (M)", format="Rp %.1f M"),
            "Potential Value (M)": st.column_config.NumberColumn("Nilai Potensial (M)", format="Rp %.1f M"),
            "Opportunity Tag": st.column_config.TextColumn("Tag", width="medium"),
            "Tenure Years": st.column_config.NumberColumn("Tenure (Tahun)", format="%d tahun"),
            "Days Since Contact": st.column_config.NumberColumn("Hari Sejak Kontak", format="%d hari"),
            "Loyalty Status": st.column_config.TextColumn("Status Loyalitas", width="small"),
        }
    )
    
    # Summary statistics
    st.markdown("---")
    st.subheader("📊 Ringkasan Statistik")
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        st.metric("Total Giro", f"Rp {filtered_df['Avg Giro Balance (M)'].sum():.1f}M")
    with col_s2:
        st.metric("Total Potensial", f"Rp {filtered_df['Potential Value (M)'].sum():.1f}M")
    with col_s3:
        target_count = len(filtered_df[filtered_df["Opportunity Tag"].str.contains("TARGET")])
        st.metric("Klien Target", target_count)
    with col_s4:
        no_sme = len(filtered_df[filtered_df["SME Loan Status"] == "None"])
        st.metric("Tanpa Pinjaman SME", no_sme)

elif view_mode == "Analytics":
    # Full-width analytics dashboard
    st.header("📊 Dashboard Analitik Portfolio")
    st.markdown("---")
    
    # Top KPI Row
    st.subheader("Indikator Kinerja Utama")
    col_k1, col_k2, col_k3, col_k4, col_k5 = st.columns(5)
    
    total_clients = len(df)
    total_giro = df['Avg Giro Balance (M)'].sum()
    total_potential = df['Potential Value (M)'].sum()
    target_sme = len(df[df["Opportunity Tag"] == "TARGET SME LOAN"])
    target_payroll = len(df[df["Opportunity Tag"] == "TARGET PAYROLL"])
    
    with col_k1:
        st.metric("Total Klien", total_clients)
    with col_k2:
        st.metric("Total Giro", f"Rp {total_giro:,.0f}M")
    with col_k3:
        st.metric("Total Potensial", f"Rp {total_potential:,.0f}M")
    with col_k4:
        st.metric("Target SME", target_sme, f"{target_sme/total_clients*100:.1f}%")
    with col_k5:
        st.metric("Target Payroll", target_payroll, f"{target_payroll/total_clients*100:.1f}%")
    
    st.markdown("---")
    
    # Portfolio Distribution
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("📈 Distribusi Peluang")
        tag_counts = df['Opportunity Tag'].value_counts()
        
        chart_data = pd.DataFrame({
            'Tag': tag_counts.index,
            'Jumlah': tag_counts.values
        })
        
        st.bar_chart(chart_data.set_index('Tag'))
        
        st.write("**Rincian:**")
        for tag, count in tag_counts.items():
            percentage = (count / total_clients) * 100
            st.write(f"• {tag}: {count} klien ({percentage:.1f}%)")
    
    with col_chart2:
        st.subheader("💰 Distribusi Saldo Giro")
        
        # Create bins for giro balance
        bins = [0, 1000, 2000, 5000, 10000]
        labels = ['< 1M', '1-2M', '2-5M', '> 5M']
        df['Giro Range'] = pd.cut(df['Avg Giro Balance (M)'], bins=bins, labels=labels, include_lowest=True)
        
        range_counts = df['Giro Range'].value_counts().sort_index()
        
        chart_data2 = pd.DataFrame({
            'Rentang': range_counts.index.astype(str),
            'Jumlah': range_counts.values
        })
        
        st.bar_chart(chart_data2.set_index('Rentang'))
        
        st.write("**Distribusi:**")
        for range_val, count in range_counts.items():
            st.write(f"• {range_val}: {count} klien")
    
    st.markdown("---")
    
    # Cross-Sell Analysis
    st.subheader("🎯 Analisis Cross-Sell")
    col_cross1, col_cross2, col_cross3 = st.columns(3)
    
    with col_cross1:
        st.write("**Penetrasi Pinjaman SME**")
        sme_active = len(df[df["SME Loan Status"] == "Active"])
        sme_none = len(df[df["SME Loan Status"] == "None"])
        
        st.metric("Pinjaman Aktif", sme_active, f"{sme_active/total_clients*100:.1f}%")
        st.metric("Tanpa Pinjaman", sme_none, f"{sme_none/total_clients*100:.1f}%")
        
        st.progress(sme_active / total_clients)
        st.caption(f"Tingkat Penetrasi: {sme_active/total_clients*100:.1f}%")
    
    with col_cross2:
        st.write("**Penetrasi Payroll**")
        payroll_active = len(df[df["Payroll Status"] == "Active"])
        payroll_none = len(df[df["Payroll Status"] == "None"])
        
        st.metric("Payroll Aktif", payroll_active, f"{payroll_active/total_clients*100:.1f}%")
        st.metric("Tanpa Payroll", payroll_none, f"{payroll_none/total_clients*100:.1f}%")
        
        st.progress(payroll_active / total_clients)
        st.caption(f"Tingkat Penetrasi: {payroll_active/total_clients*100:.1f}%")
    
    with col_cross3:
        st.write("**Aktivitas Transaksi**")
        high_freq = len(df[df["Transaction Frequency"] == "High"])
        med_freq = len(df[df["Transaction Frequency"] == "Medium"])
        low_freq = len(df[df["Transaction Frequency"] == "Low"])
        
        st.write(f"🟢 Tinggi: {high_freq} ({high_freq/total_clients*100:.1f}%)")
        st.write(f"🟡 Sedang: {med_freq} ({med_freq/total_clients*100:.1f}%)")
        st.write(f"🔴 Rendah: {low_freq} ({low_freq/total_clients*100:.1f}%)")
        
        engagement_score = (high_freq * 3 + med_freq * 2 + low_freq * 1) / (total_clients * 3)
        st.metric("Skor Engagement", f"{engagement_score*100:.1f}%")
    
    st.markdown("---")
    
    # Priority Matrix
    st.subheader("🎯 Matriks Prioritas Aksi")
    
    # Create priority segments
    high_value_no_loan = df[(df['Avg Giro Balance (M)'] >= 2000) & (df['SME Loan Status'] == 'None')]
    med_value_no_payroll = df[(df['Avg Giro Balance (M)'] >= 1000) & 
                               (df['Avg Giro Balance (M)'] < 2000) & 
                               (df['Payroll Status'] == 'None')]
    low_activity = df[df['Transaction Frequency'] == 'Low']
    
    col_matrix1, col_matrix2, col_matrix3 = st.columns(3)
    
    with col_matrix1:
        st.error("🔴 **PRIORITAS KRITIS**")
        st.metric("Giro Tinggi, Tanpa Pinjaman SME", len(high_value_no_loan))
        st.write(f"Potensial: Rp {high_value_no_loan['Potential Value (M)'].sum():,.0f}M")
        st.write("**Tindakan:** Segera tawarkan pinjaman SME")
    
    with col_matrix2:
        st.warning("🟡 **PRIORITAS SEDANG**")
        st.metric("Giro Sedang, Tanpa Payroll", len(med_value_no_payroll))
        st.write(f"Potensial: Rp {med_value_no_payroll['Potential Value (M)'].sum():,.0f}M")
        st.write("**Tindakan:** Tawarkan produk Payroll")
    
    with col_matrix3:
        st.info("🔵 **FOKUS RETENSI**")
        st.metric("Aktivitas Transaksi Rendah", len(low_activity))
        st.write("**Risiko Churn:** Tinggi")
        st.write("**Tindakan:** Review relasi & tingkatkan engagement")
    
    st.markdown("---")
    
    # Pipeline Forecast
    st.subheader("📈 Proyeksi Pipeline")
    
    if st.session_state['pipeline_updates']:
        st.write("**Status Pipeline Saat Ini:**")
        
        pipeline_df = pd.DataFrame([
            {
                'Klien': client,
                'Status': data['status'],
                'Terakhir Diperbarui': data['updated_at']
            }
            for client, data in st.session_state['pipeline_updates'].items()
        ])
        
        status_counts = pipeline_df['Status'].value_counts()
        
        col_pipe1, col_pipe2 = st.columns(2)
        
        with col_pipe1:
            st.dataframe(pipeline_df, use_container_width=True, height=300)
        
        with col_pipe2:
            st.write("**Distribusi Status:**")
            for status, count in status_counts.items():
                st.write(f"• {status}: {count}")
            
            st.markdown("---")
            
            # Calculate conversion estimate
            interested = status_counts.get('Interested', 0)
            closed_won = status_counts.get('Closed Won', 0)
            total_pipeline = len(pipeline_df)
            
            if total_pipeline > 0:
                conversion_rate = (closed_won / total_pipeline) * 100
                st.metric("Tingkat Konversi", f"{conversion_rate:.1f}%")
                
                # Estimate based on clients in pipeline
                clients_in_pipeline = list(st.session_state['pipeline_updates'].keys())
                pipeline_potential = df[df['Client Name'].isin(clients_in_pipeline)]['Potential Value (M)'].sum()
                
                st.metric("Nilai Pipeline", f"Rp {pipeline_potential:,.0f}M")
                st.metric("Estimasi Revenue", f"Rp {pipeline_potential * (conversion_rate/100):,.0f}M")
    else:
        st.info("Belum ada aktivitas pipeline yang tercatat. Mulai analisis klien untuk membangun pipeline Anda.")
    
    st.markdown("---")
    
    # Recommendations
    st.subheader("💡 Rekomendasi AI")
    
    col_rec1, col_rec2 = st.columns(2)
    
    with col_rec1:
        st.write("**5 Klien Prioritas Tertinggi (berdasarkan Nilai Potensial):**")
        top_5 = df.nlargest(5, 'Potential Value (M)')[['Client Name', 'Opportunity Tag', 'Potential Value (M)']]
        
        for idx, row in top_5.iterrows():
            st.write(f"🎯 **{row['Client Name']}**")
            st.write(f"   Tag: {row['Opportunity Tag']} | Nilai: Rp {row['Potential Value (M)']}M")
    
    with col_rec2:
        st.write("**Aksi Strategis Minggu Ini:**")
        st.write("1. ✅ Hubungi semua klien PRIORITAS TINGGI (target Pinjaman SME)")
        st.write(f"2. 📞 Lakukan {target_sme} pitching pinjaman SME")
        st.write(f"3. 💼 Jadwalkan {min(target_payroll, 5)} demo payroll")
        st.write(f"4. ⚠️ Review {len(low_activity)} akun dengan aktivitas rendah")
        st.write("5. 📊 Update status pipeline setiap hari")

else:
    # Original two-column layout for Smart Opportunities
    col_middle, col_right = st.columns([4, 6])

    # ========== ZONE 2: MIDDLE COLUMN (ACTION LIST) ==========
    with col_middle:
        st.header("🎯 Peluang Hari Ini")
        
        # Filter high-priority leads
        priority_leads = df[df["Opportunity Tag"].str.contains("TARGET")].nlargest(5, "Potential Value (M)")
        
        st.markdown(f"**{len(priority_leads)} Leads Prioritas Tinggi** | Target: Tutup 3 deals minggu ini")
        st.markdown("---")
        
        # Display top leads as cards
        for idx, row in priority_leads.iterrows():
            with st.container():
                # Card styling with border
                if row["Opportunity Tag"] == "TARGET SME LOAN":
                    border_color = "#e74c3c"  # Red
                    icon = "💰"
                else:
                    border_color = "#3498db"  # Blue
                    icon = "💼"
                
                # Determine frequency color
                freq = row['Transaction Frequency']
                if freq == "Low":
                    freq_color = "#e74c3c"  # Red
                elif freq == "Medium":
                    freq_color = "#f39c12"  # Yellow/Orange
                else:  # High
                    freq_color = "#27ae60"  # Green
                
                st.markdown(f"""
                <div style="border-left: 4px solid {border_color}; padding-left: 15px; margin-bottom: 15px;">
                    <h4>{icon} {row['Client Name']}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                col_a, col_b, col_c = st.columns([3, 2, 2])
                with col_a:
                    st.write(f"**Tag:** {row['Opportunity Tag']}")
                    st.write(f"**Giro:** Rp {row['Avg Giro Balance (M)']}M")
                with col_b:
                    st.write(f"**Potensial:** Rp {row['Potential Value (M)']}M")
                    st.markdown(f"**Frek:** <span style='color: {freq_color}; font-weight: bold;'>{freq}</span>", unsafe_allow_html=True)
                with col_c:
                    if st.button(f"🔍 Analisis", key=f"btn_{idx}"):
                        st.session_state['selected_client'] = row['Client Name']
                        st.rerun()
                
                st.markdown("---")

    # ========== ZONE 3: RIGHT COLUMN (CO-PILOT PANEL) ==========
    with col_right:
        if st.session_state['selected_client']:
            client_name = st.session_state['selected_client']
            client_row = df[df["Client Name"] == client_name].iloc[0]
            
            st.header(f"🤖 Co-Pilot: {client_name}")
            
            # Client Profile Section
            st.subheader("📋 Profil Klien")
            col_p1, col_p2, col_p3 = st.columns(3)
            with col_p1:
                st.metric("Saldo Giro", f"Rp {client_row['Avg Giro Balance (M)']}M")
            with col_p2:
                st.metric("Pinjaman SME", client_row['SME Loan Status'])
            with col_p3:
                st.metric("Payroll", client_row['Payroll Status'])
            
            col_p4, col_p5 = st.columns(2)
            with col_p4:
                st.metric("Frekuensi Transaksi", client_row['Transaction Frequency'])
            with col_p5:
                st.metric("Nilai Potensial", f"Rp {client_row['Potential Value (M)']}M")
            
            st.markdown("---")
            
            # AI Analysis Section
            st.subheader("🧠 Analisis AI")
            with st.expander("📊 Insight Lengkap", expanded=True):
                analysis = mock_ai_analysis(client_row)
                st.markdown(analysis)
            
            st.markdown("---")
            
            # Script Generation Section
            st.subheader("💬 Skrip WhatsApp yang Dihasilkan")
            script = generate_script(
                client_row['Client Name'], 
                client_row['Opportunity Tag'],
                client_row['Avg Giro Balance (M)']
            )
            
            script_area = st.text_area(
                "Draft Pesan", 
                value=script, 
                height=300,
                key="script_area"
            )
            
            col_b1, col_b2, col_b3 = st.columns(3)
            with col_b1:
                if st.button("📋 Salin ke Clipboard"):
                    st.success("Skrip berhasil disalin!")
            with col_b2:
                if st.button("🔄 Generate Ulang (Formal)"):
                    st.info("Sedang generate ulang dengan tone formal...")
            with col_b3:
                if st.button("✉️ Kirim via WA"):
                    st.success("Membuka WhatsApp...")
            
            st.markdown("---")
            
            # Pipeline Management
            st.subheader("📈 Aksi Pipeline")
            with st.form("pipeline_form"):
                status = st.selectbox(
                    "Perbarui Status",
                    ["Belum Dihubungi", "Sudah Dihubungi", "Meeting Terjadwal", "Proposal Terkirim", "Tertarik", "Berhasil Closing", "Gagal Closing"]
                )
                
                notes = st.text_area("Catatan", placeholder="Tambahkan catatan tentang interaksi ini...")
                
                next_action = st.text_input("Tindakan Selanjutnya", placeholder="contoh: Jadwalkan meeting Jumat jam 2 siang")
                
                submitted = st.form_submit_button("💾 Simpan Update")
                
                if submitted:
                    st.session_state['pipeline_updates'][client_name] = {
                        "status": status,
                        "notes": notes,
                        "next_action": next_action,
                        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    st.success(f"Pipeline berhasil diperbarui untuk {client_name}!")
            
            # Show previous updates
            if client_name in st.session_state['pipeline_updates']:
                st.markdown("---")
                st.subheader("📝 Update Sebelumnya")
                update = st.session_state['pipeline_updates'][client_name]
                st.write(f"**Status:** {update['status']}")
                st.write(f"**Terakhir Diperbarui:** {update['updated_at']}")
                if update['notes']:
                    st.write(f"**Catatan:** {update['notes']}")
                if update['next_action']:
                    st.write(f"**Tindakan Selanjutnya:** {update['next_action']}")
        
        else:
            # Empty state
            st.info("Pilih klien dari daftar peluang untuk mengaktifkan analisis Co-Pilot")
            
            st.markdown("---")
            st.markdown("### 💡 Tips Cepat")
            st.write("1. **Prioritas:** Fokus pada leads dengan tag 'TARGET SME LOAN'")
            st.write("2. **Waktu Terbaik:** Hubungi antara jam 10-11 pagi atau 2-3 sore")
            st.write("3. **Pendekatan:** Gunakan personal touch, referensi riwayat transaksi")
            st.write("4. **Follow-up:** Jangan lebih dari 3 hari untuk merespons")