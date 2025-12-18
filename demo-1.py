import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Custom Color Scheme for Banking Dashboard
OPPORTUNITY_COLORS = {
    'TARGET SME LOAN': '#d32f2f',      # Red - Critical opportunity
    'TARGET PAYROLL': '#f57c00',       # Orange - Medium priority
    'MAINTAIN': '#388e3c'              # Green - Stable
}

LOYALTY_COLORS = {
    'Platinum': '#9c27b0',
    'Gold': '#ffa000',
    'Silver': '#757575'
}

# Set Layout to Wide and Force Light Mode
st.set_page_config(
    page_title="Mandiri Smart-RM Co-Pilot",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Mandiri Smart-RM Co-Pilot - Banking Intelligence Dashboard"
    }
)


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
    
    # Enhanced visual progress bar for SME penetration
    st.markdown("### SME Penetration")
    sme_penetration = 0.33
    color = '#d32f2f' if sme_penetration < 0.4 else '#f57c00' if sme_penetration < 0.7 else '#388e3c'
    
    st.markdown(f"""
    <style>
    .stProgress > div > div > div > div {{
        background-color: {color};
    }}
    </style>
    """, unsafe_allow_html=True)
    
    st.progress(sme_penetration)
    st.caption(f"Target: 100% | Current: {sme_penetration*100:.0f}%")
    
    st.metric(
        label="Tabungan (Retail)", 
        value="85%", 
        delta="-Rp 22M",
        delta_color="inverse"
    )
    
    st.markdown("---")
    
    # Problem Statement - Enhanced with Metrics and Actions
    sme_gap = df[df["SME Loan Status"] == "None"]
    sme_gap_high_value = sme_gap[sme_gap["Avg Giro Balance (M)"] >= 2000]
    sme_gap_percentage = (len(sme_gap) / len(df)) * 100
    potential_revenue = sme_gap_high_value['Potential Value (M)'].sum()
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #ff6b6b 0%, #c92a2a 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #a61e1e;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
    ">
        <h3 style="color: white; margin: 0 0 10px 0; font-size: 18px;">
            LIQUIDITY UNBALANCE
        </h3>
        <p style="color: white; margin: 0 0 15px 0; font-size: 14px; line-height: 1.6;">
            Funding Giro tinggi namun lending SME sangat rendah. 
            <strong>Diperlukan tindakan segera</strong> untuk menyeimbangkan portfolio.
        </p>
        <div style="background: rgba(255,255,255,0.2); padding: 10px; border-radius: 5px; margin-bottom: 10px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span style="color: white; font-size: 12px;">Klien Tanpa Pinjaman SME</span>
                <span style="color: white; font-weight: bold;">{len(sme_gap)} klien ({sme_gap_percentage:.0f}%)</span>
            </div>
            <div style="background: rgba(255,255,255,0.3); height: 6px; border-radius: 3px; overflow: hidden;">
                <div style="background: white; width: {sme_gap_percentage}%; height: 100%;"></div>
            </div>
        </div>
        <div style="background: rgba(255,255,255,0.2); padding: 10px; border-radius: 5px;">
            <div style="color: white; font-size: 12px; margin-bottom: 3px;">Potensi Revenue</div>
            <div style="color: white; font-size: 20px; font-weight: bold;">Rp {potential_revenue:.0f}M</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📊 View SME Opportunities", key="nav_sme", use_container_width=True):
        st.session_state['nav_override'] = "Smart Opportunities"
        st.rerun()
    
    # Relationship Health Alert - Enhanced
    loyal_clients = df[df["Tenure Years"] > 10]
    ignored_loyal = df[(df["Tenure Years"] > 10) & (df["Days Since Contact"] > 90)]
    ignored_percentage = (len(ignored_loyal) / len(loyal_clients)) * 100 if len(loyal_clients) > 0 else 0
    at_risk_value = ignored_loyal['Avg Giro Balance (M)'].sum()
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #a626d3;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
    ">
        <h3 style="color: white; margin: 0 0 10px 0; font-size: 18px;">
            RELATIONSHIP RISK
        </h3>
        <p style="color: white; margin: 0 0 15px 0; font-size: 14px; line-height: 1.6;">
            <strong>{len(ignored_loyal)} nasabah loyal</strong> (>10 tahun) belum dihubungi lebih dari 90 hari. 
            Risiko churn tinggi jika tidak segera ditangani.
        </p>
        <div style="background: rgba(255,255,255,0.2); padding: 10px; border-radius: 5px; margin-bottom: 10px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span style="color: white; font-size: 12px;">Loyal Clients Terabaikan</span>
                <span style="color: white; font-weight: bold;">{len(ignored_loyal)}/{len(loyal_clients)} ({ignored_percentage:.0f}%)</span>
            </div>
            <div style="background: rgba(255,255,255,0.3); height: 6px; border-radius: 3px; overflow: hidden;">
                <div style="background: white; width: {ignored_percentage}%; height: 100%;"></div>
            </div>
        </div>
        <div style="background: rgba(255,255,255,0.2); padding: 10px; border-radius: 5px;">
            <div style="color: white; font-size: 12px; margin-bottom: 3px;">Nilai Portfolio At-Risk</div>
            <div style="color: white; font-size: 20px; font-weight: bold;">Rp {at_risk_value:.0f}M</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("💝 View Relationship Health", key="nav_relationship", use_container_width=True):
        st.session_state['nav_override'] = "Relationship Health"
        st.rerun()
    
    st.markdown("---")
    
    # Navigation - Check for override from alert buttons
    if 'nav_override' in st.session_state and st.session_state['nav_override']:
        default_view = st.session_state['nav_override']
        st.session_state['nav_override'] = None  # Clear override
    else:
        default_view = "Smart Opportunities"
    
    view_mode = st.radio(
        "📍 Navigasi", 
        ["Smart Opportunities", "Relationship Health", "Data View", "Analytics"],
        index=["Smart Opportunities", "Relationship Health", "Data View", "Analytics"].index(default_view) if default_view in ["Smart Opportunities", "Relationship Health", "Data View", "Analytics"] else 0
    )

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
                
                # Copy button with JavaScript clipboard functionality
                import json
                script_json = json.dumps(celebration_script)
                copy_button_html = f"""
                <button onclick="copyToClipboard()" 
                        style="background: #4CAF50; color: white; border: none; padding: 8px 16px; 
                               border-radius: 5px; cursor: pointer; width: 100%; margin-bottom: 10px;">
                    📋 Salin Skrip
                </button>
                <script>
                function copyToClipboard() {{
                    navigator.clipboard.writeText({script_json}).then(function() {{
                        alert('Skrip berhasil disalin ke clipboard!');
                    }}).catch(function(err) {{
                        alert('Gagal menyalin: ' + err);
                    }});
                }}
                </script>
                """
                components.html(copy_button_html, height=50)
                
                # WhatsApp button with actual link
                import urllib.parse
                wa_message = urllib.parse.quote(celebration_script)
                wa_link = f"https://wa.me/6286276272612?text={wa_message}"
                st.markdown(f'<a href="{wa_link}" target="_blank"><button style="background: #25D366; color: white; border: none; padding: 8px 16px; border-radius: 5px; cursor: pointer; width: 100%;">✉️ Kirim WA</button></a>', unsafe_allow_html=True)
    
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
                # Copy button with JavaScript
                import json
                script_json = json.dumps(greeting_script)
                copy_button_html = f"""
                <button onclick="copyToClipboard()" 
                        style="background: #4CAF50; color: white; border: none; padding: 8px 16px; 
                               border-radius: 5px; cursor: pointer; width: 100%;">
                    📋 Salin Skrip
                </button>
                <script>
                function copyToClipboard() {{
                    navigator.clipboard.writeText({script_json}).then(function() {{
                        alert('Skrip berhasil disalin ke clipboard!');
                    }}).catch(function(err) {{
                        alert('Gagal menyalin: ' + err);
                    }});
                }}
                </script>
                """
                components.html(copy_button_html, height=50)
            with col_btn2:
                import urllib.parse
                wa_message = urllib.parse.quote(greeting_script)
                wa_link = f"https://wa.me/6286276272612?text={wa_message}"
                st.markdown(f'<a href="{wa_link}" target="_blank"><button style="background: #25D366; color: white; border: none; padding: 8px 16px; border-radius: 5px; cursor: pointer; width: 100%;">✉️ Kirim WA</button></a>', unsafe_allow_html=True)
        
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
    
    st.markdown("---")
    
    # ========== ENHANCED RINGKASAN STATISTIK (MOVED TO TOP) ==========
    st.subheader("📊 Ringkasan Statistik")
    
    # Calculate key metrics
    total_giro = filtered_df['Avg Giro Balance (M)'].sum()
    total_potential = filtered_df['Potential Value (M)'].sum()
    target_count = len(filtered_df[filtered_df["Opportunity Tag"].str.contains("TARGET")])
    no_sme = len(filtered_df[filtered_df["SME Loan Status"] == "None"])
    sme_active = len(filtered_df[filtered_df["SME Loan Status"] == "Active"])
    payroll_active = len(filtered_df[filtered_df["Payroll Status"] == "Active"])
    avg_tenure = filtered_df['Tenure Years'].mean()
    avg_giro = filtered_df['Avg Giro Balance (M)'].mean()
    
    # Top Row - Main KPIs with Enhanced Cards
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    with col_stat1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1976d2 0%, #42a5f5 100%); 
                    padding: 25px; border-radius: 12px; text-align: center; color: white;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h4 style="margin: 0; font-size: 14px; opacity: 0.9;">Total Giro</h4>
            <h1 style="margin: 10px 0; font-size: 32px; font-weight: bold;">Rp {total_giro:,.0f}M</h1>
            <p style="margin: 0; font-size: 12px; opacity: 0.8;">Avg: Rp {avg_giro:,.0f}M per klien</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 25px; border-radius: 12px; text-align: center; color: white;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h4 style="margin: 0; font-size: 14px; opacity: 0.9;">Total Potensial</h4>
            <h1 style="margin: 10px 0; font-size: 32px; font-weight: bold;">Rp {total_potential:,.0f}M</h1>
            <p style="margin: 0; font-size: 12px; opacity: 0.8;">Revenue opportunity</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat3:
        target_percentage = (target_count / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ff6b6b 0%, #c92a2a 100%); 
                    padding: 25px; border-radius: 12px; text-align: center; color: white;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h4 style="margin: 0; font-size: 14px; opacity: 0.9;">Klien Target</h4>
            <h1 style="margin: 10px 0; font-size: 32px; font-weight: bold;">{target_count}</h1>
            <p style="margin: 0; font-size: 12px; opacity: 0.8;">{target_percentage:.1f}% dari portfolio</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat4:
        sme_gap_percentage = (no_sme / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f57c00 0%, #e65100 100%); 
                    padding: 25px; border-radius: 12px; text-align: center; color: white;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h4 style="margin: 0; font-size: 14px; opacity: 0.9;">Tanpa Pinjaman SME</h4>
            <h1 style="margin: 10px 0; font-size: 32px; font-weight: bold;">{no_sme}</h1>
            <p style="margin: 0; font-size: 12px; opacity: 0.8;">{sme_gap_percentage:.1f}% - Opportunity!</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Second Row - Penetration Metrics with Progress Bars
    col_pen1, col_pen2, col_pen3, col_pen4 = st.columns(4)
    
    with col_pen1:
        sme_penetration = (sme_active / len(filtered_df)) if len(filtered_df) > 0 else 0
        st.markdown("**SME Loan Penetration**")
        st.progress(sme_penetration)
        st.caption(f"{sme_active}/{len(filtered_df)} klien ({sme_penetration*100:.1f}%)")
    
    with col_pen2:
        payroll_penetration = (payroll_active / len(filtered_df)) if len(filtered_df) > 0 else 0
        st.markdown("**Payroll Penetration**")
        st.progress(payroll_penetration)
        st.caption(f"{payroll_active}/{len(filtered_df)} klien ({payroll_penetration*100:.1f}%)")
    
    with col_pen3:
        full_package = len(filtered_df[(filtered_df["SME Loan Status"] == "Active") & (filtered_df["Payroll Status"] == "Active")])
        full_penetration = (full_package / len(filtered_df)) if len(filtered_df) > 0 else 0
        st.markdown("**Full Package (SME+Payroll)**")
        st.progress(full_penetration)
        st.caption(f"{full_package}/{len(filtered_df)} klien ({full_penetration*100:.1f}%)")
    
    with col_pen4:
        st.metric("Avg Tenure", f"{avg_tenure:.1f} tahun", "Loyalty indicator")
    
    # Third Row - Opportunity Breakdown Chart
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("**📈 Opportunity Breakdown**")
        tag_counts = filtered_df['Opportunity Tag'].value_counts()
        
        fig_breakdown = px.bar(
            x=tag_counts.values,
            y=tag_counts.index,
            orientation='h',
            color=tag_counts.index,
            color_discrete_map=OPPORTUNITY_COLORS,
            text=tag_counts.values
        )
        fig_breakdown.update_traces(texttemplate='%{text} klien', textposition='outside')
        fig_breakdown.update_layout(
            showlegend=False,
            height=200,
            margin=dict(t=10, b=10, l=10, r=80),
            xaxis_title="",
            yaxis_title=""
        )
        st.plotly_chart(fig_breakdown, use_container_width=True)
    
    with col_chart2:
        st.markdown("**💰 Value Distribution**")
        
        value_by_tag = filtered_df.groupby('Opportunity Tag')['Potential Value (M)'].sum().sort_values(ascending=True)
        
        fig_value = px.bar(
            x=value_by_tag.values,
            y=value_by_tag.index,
            orientation='h',
            color=value_by_tag.index,
            color_discrete_map=OPPORTUNITY_COLORS,
            text=value_by_tag.values
        )
        fig_value.update_traces(texttemplate='Rp %{text:,.0f}M', textposition='outside')
        fig_value.update_layout(
            showlegend=False,
            height=200,
            margin=dict(t=10, b=10, l=10, r=100),
            xaxis_title="",
            yaxis_title=""
        )
        st.plotly_chart(fig_value, use_container_width=True)
    
    st.markdown("---")
    
    # Data Table Section
    st.markdown(f"Menampilkan **{len(filtered_df)}** klien dari total **{len(df)}** klien")
    
    # Apply conditional formatting with styled dataframe
    def highlight_priority(row):
        if row['Opportunity Tag'] == 'TARGET SME LOAN':
            return ['background-color: #ffebee'] * len(row)
        elif row['Opportunity Tag'] == 'TARGET PAYROLL':
            return ['background-color: #fff3e0'] * len(row)
        elif row['Days Since Contact'] > 90:
            return ['background-color: #fce4ec'] * len(row)
        return [''] * len(row)
    
    # Create a copy for styling
    display_df = filtered_df.copy()
    
    st.dataframe(
        display_df.style.apply(highlight_priority, axis=1),
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
    
    # Legend for color coding
    col_leg1, col_leg2, col_leg3 = st.columns(3)
    with col_leg1:
        st.markdown("🔴 **Red highlight:** TARGET SME LOAN")
    with col_leg2:
        st.markdown("🟠 **Orange highlight:** TARGET PAYROLL")
    with col_leg3:
        st.markdown("🟣 **Pink highlight:** Not contacted >90 days")

elif view_mode == "Analytics":
    # Full-width analytics dashboard
    st.header("📊 Dashboard Analitik Portfolio")
    st.markdown("---")
    
    # Top KPI Row with Enhanced Styling
    st.subheader("Indikator Kinerja Utama")
    
    total_clients = len(df)
    total_giro = df['Avg Giro Balance (M)'].sum()
    total_potential = df['Potential Value (M)'].sum()
    target_sme = len(df[df["Opportunity Tag"] == "TARGET SME LOAN"])
    target_payroll = len(df[df["Opportunity Tag"] == "TARGET PAYROLL"])
    
    col_k1, col_k2, col_k3, col_k4, col_k5 = st.columns(5)
    
    with col_k1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 12px; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
                    height: 200px; padding: 20px 10px;
                    display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
            <h4 style="margin: 0 0 10px 0; font-size: 15px; font-weight: normal;">Total Klien</h4>
            <h1 style="margin: 0 0 8px 0; font-size: 56px; font-weight: bold; line-height: 1;">{total_clients}</h1>
            <p style="margin: 0; font-size: 12px; opacity: 0.9;">Portfolio aktif</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_k2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1976d2 0%, #42a5f5 100%); 
                    border-radius: 12px; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
                    height: 200px; padding: 20px 10px;
                    display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
            <h4 style="margin: 0 0 10px 0; font-size: 15px; font-weight: normal;">Total Giro</h4>
            <h1 style="margin: 0 0 8px 0; font-size: 36px; font-weight: bold; line-height: 1.1; white-space: nowrap;">Rp {total_giro:,.0f}M</h1>
            <p style="margin: 0; font-size: 11px; opacity: 0.9;">▲ +18% vs last month</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_k3:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    border-radius: 12px; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
                    height: 200px; padding: 20px 10px;
                    display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
            <h4 style="margin: 0 0 10px 0; font-size: 15px; font-weight: normal;">Total Potensial</h4>
            <h1 style="margin: 0 0 8px 0; font-size: 36px; font-weight: bold; line-height: 1.1; white-space: nowrap;">Rp {total_potential:,.0f}M</h1>
            <p style="margin: 0; font-size: 11px; opacity: 0.9;">Revenue opportunity</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_k4:
        target_sme_pct = (target_sme/total_clients*100) if total_clients > 0 else 0
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ff6b6b 0%, #c92a2a 100%); 
                    border-radius: 12px; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
                    height: 200px; padding: 20px 10px;
                    display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
            <h4 style="margin: 0 0 10px 0; font-size: 15px; font-weight: normal;">Target SME</h4>
            <h1 style="margin: 0 0 8px 0; font-size: 56px; font-weight: bold; line-height: 1;">{target_sme}</h1>
            <p style="margin: 0; font-size: 11px; opacity: 0.9;">▲ {target_sme_pct:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_k5:
        target_payroll_pct = (target_payroll/total_clients*100) if total_clients > 0 else 0
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f57c00 0%, #e65100 100%); 
                    border-radius: 12px; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
                    height: 200px; padding: 20px 10px;
                    display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
            <h4 style="margin: 0 0 10px 0; font-size: 15px; font-weight: normal;">Target Payroll</h4>
            <h1 style="margin: 0 0 8px 0; font-size: 56px; font-weight: bold; line-height: 1;">{target_payroll}</h1>
            <p style="margin: 0; font-size: 11px; opacity: 0.9;">▲ {target_payroll_pct:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Monthly Trend Analysis
    st.subheader("📈 Trend Bulanan - SME Loan Achievement")
    
    # Simulate 6-month trend
    months = pd.date_range(end=datetime.now(), periods=6, freq='M')
    trend_data = pd.DataFrame({
        'Month': months.strftime('%b %Y'),
        'SME Loans (%)': [25, 27, 29, 31, 32, 33],
        'Target (%)': [100] * 6
    })
    
    fig_trend = go.Figure()
    
    # Add actual line
    fig_trend.add_trace(go.Scatter(
        x=trend_data['Month'],
        y=trend_data['SME Loans (%)'],
        mode='lines+markers+text',
        name='Actual',
        line=dict(color='#d32f2f', width=3),
        marker=dict(size=10),
        text=trend_data['SME Loans (%)'],
        textposition='top center',
        texttemplate='%{text}%'
    ))
    
    # Add target line
    fig_trend.add_trace(go.Scatter(
        x=trend_data['Month'],
        y=trend_data['Target (%)'],
        mode='lines',
        name='Target',
        line=dict(color='#2e7d32', width=2, dash='dash')
    ))
    
    fig_trend.update_layout(
        height=280,
        yaxis_title='Achievement (%)',
        xaxis_title='',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=40, b=20, l=20, r=20)
    )
    
    st.plotly_chart(fig_trend, use_container_width=True)
    
    col_trend1, col_trend2, col_trend3 = st.columns(3)
    with col_trend1:
        st.metric("Current Month", "33%", "+1% MoM")
    with col_trend2:
        st.metric("Gap to Target", "-67%", "Action needed!", delta_color="inverse")
    with col_trend3:
        st.metric("Projected Next Month", "35%", "+2% forecast")
    
    st.markdown("---")
    
    # Portfolio Distribution
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("📈 Distribusi Peluang")
        tag_counts = df['Opportunity Tag'].value_counts()
        
        chart_data = pd.DataFrame({
            'Tag': tag_counts.index,
            'Jumlah': tag_counts.values
        }).sort_values('Jumlah', ascending=False)
        
        # Replace pie with horizontal bar chart for better comparison
        fig1 = px.bar(
            chart_data,
            y='Tag',
            x='Jumlah',
            color='Tag',
            color_discrete_map=OPPORTUNITY_COLORS,
            text='Jumlah',
            orientation='h'
        )
        fig1.update_traces(
            texttemplate='%{text} klien<br>(%{x:.1%} of total)', 
            textposition='outside'
        )
        fig1.update_layout(
            showlegend=False,
            height=350,
            margin=dict(t=10, b=0, l=0, r=80),
            xaxis_title="Jumlah Klien",
            yaxis_title=""
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        # Contact Recency Alert for Opportunity Segment
        st.markdown("**Alert: Klien Belum Dihubungi**")
        target_clients = df[df['Opportunity Tag'].str.contains('TARGET')]
        not_contacted = len(target_clients[target_clients['Days Since Contact'] > 30])
        urgent = len(target_clients[target_clients['Days Since Contact'] > 90])
        
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            st.metric(">30 hari", not_contacted, f"{not_contacted/len(target_clients)*100:.0f}%" if len(target_clients) > 0 else "0%")
        with col_a2:
            st.metric(">90 hari", urgent, "URGENT!" if urgent > 0 else "OK", delta_color="inverse")
    
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
        }).sort_values('Jumlah', ascending=False)
        
        # Create funnel chart for better hierarchy visualization
        fig2 = px.funnel(
            chart_data2,
            x='Jumlah',
            y='Rentang',
            color='Rentang',
            color_discrete_sequence=['#1976d2', '#42a5f5', '#90caf9', '#bbdefb']
        )
        fig2.update_traces(textinfo='value+percent total')
        fig2.update_layout(
            showlegend=False,
            height=350,
            margin=dict(t=10, b=0, l=0, r=0)
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        # High-Value Client Contact Status
        st.markdown("**Alert: High-Value Klien**")
        high_value = df[df['Avg Giro Balance (M)'] >= 2000]
        hv_not_contacted = len(high_value[high_value['Days Since Contact'] > 30])
        hv_urgent = len(high_value[high_value['Days Since Contact'] > 90])
        
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.metric(">30 hari", hv_not_contacted, f"{hv_not_contacted/len(high_value)*100:.0f}%" if len(high_value) > 0 else "0%")
        with col_b2:
            st.metric(">90 hari", hv_urgent, "CRITICAL!" if hv_urgent > 0 else "OK", delta_color="inverse")
    
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
    
    # Portfolio Heat Map
    st.subheader("🗺️ Portfolio Heat Map: Giro vs Aktivitas")
    
    fig_scatter = px.scatter(
        df,
        x='Days Since Contact',
        y='Avg Giro Balance (M)',
        size='Potential Value (M)',
        color='Opportunity Tag',
        color_discrete_map=OPPORTUNITY_COLORS,
        hover_data=['Client Name', 'SME Loan Status', 'Payroll Status', 'Tenure Years'],
        labels={'Days Since Contact': 'Hari Sejak Kontak Terakhir',
                'Avg Giro Balance (M)': 'Saldo Giro (Juta)'}
    )
    
    # Add quadrant lines
    fig_scatter.add_hline(y=2000, line_dash="dash", line_color="red", opacity=0.5, annotation_text="High Value Threshold")
    fig_scatter.add_vline(x=30, line_dash="dash", line_color="orange", opacity=0.5, annotation_text="Contact Threshold")
    
    fig_scatter.update_layout(
        height=450,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Quadrant explanation
    col_q1, col_q2, col_q3, col_q4 = st.columns(4)
    with col_q1:
        st.info("**🔴 Top Right:** High Value + Recent Contact = Ideal")
    with col_q2:
        st.warning("**🟡 Top Left:** High Value + Old Contact = URGENT!")
    with col_q3:
        st.success("**🟢 Bottom Right:** Low Value + Recent = Good")
    with col_q4:
        st.error("**⚫ Bottom Left:** Low Value + Old = Re-evaluate")
    
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
    
    # Client Journey Sankey
    st.subheader("🔄 Customer Journey Flow")
    
    # Calculate flows
    giro_only = len(df[(df['SME Loan Status'] == 'None') & (df['Payroll Status'] == 'None')])
    giro_sme = len(df[(df['SME Loan Status'] == 'Active') & (df['Payroll Status'] == 'None')])
    giro_payroll = len(df[(df['SME Loan Status'] == 'None') & (df['Payroll Status'] == 'Active')])
    full_package = len(df[(df['SME Loan Status'] == 'Active') & (df['Payroll Status'] == 'Active')])
    
    fig_sankey = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=["Total Clients", "Giro Only", "+ SME Loan", "+ Payroll", "Full Package"],
            color=["#1976d2", "#ff9800", "#4caf50", "#9c27b0", "#ffd700"]
        ),
        link=dict(
            source=[0, 0, 0, 0],
            target=[1, 2, 3, 4],
            value=[giro_only, giro_sme, giro_payroll, full_package],
            color=["rgba(255, 152, 0, 0.4)", "rgba(76, 175, 80, 0.4)", 
                   "rgba(156, 39, 176, 0.4)", "rgba(255, 215, 0, 0.6)"]
        )
    )])
    
    fig_sankey.update_layout(
        title_text="Product Penetration Flow",
        height=300,
        font_size=12,
        margin=dict(t=40, b=10, l=10, r=10)
    )
    
    st.plotly_chart(fig_sankey, use_container_width=True)
    
    col_sk1, col_sk2, col_sk3 = st.columns(3)
    with col_sk1:
        st.metric("Giro Only", giro_only, f"{giro_only/len(df)*100:.1f}% - Opportunity!")
    with col_sk2:
        st.metric("Single Product", giro_sme + giro_payroll, "Cross-sell potential")
    with col_sk3:
        st.metric("Full Package", full_package, f"{full_package/len(df)*100:.1f}% - Excellent!")
    
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
        
        # Create styled dataframe
        top_5_display = top_5.copy()
        top_5_display['Rank'] = [1, 2, 3, 4, 5]
        top_5_display = top_5_display[['Rank', 'Client Name', 'Opportunity Tag', 'Potential Value (M)']]
        top_5_display.columns = ['Rank', 'Nama Klien', 'Tag', 'Nilai Potensial (M)']
        
        st.dataframe(
            top_5_display,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Rank": st.column_config.NumberColumn("Rank"),
                "Nama Klien": st.column_config.TextColumn("Nama Klien"),
                "Tag": st.column_config.TextColumn("Opportunity Tag"),
                "Nilai Potensial (M)": st.column_config.NumberColumn("Nilai Potensial", format="Rp %.1f M"),
            }
        )
    
    with col_rec2:
        st.write("**Aksi Strategis Minggu Ini:**")
        
        # Create action items table
        action_items = pd.DataFrame({
            'Priority': ['🔴', '🔴', '🟡', '🟡', '🟢'],
            'Action': [
                'Hubungi semua klien PRIORITAS TINGGI',
                f'Lakukan {target_sme} pitching pinjaman SME',
                f'Jadwalkan {min(target_payroll, 5)} demo payroll',
                f'Review {len(low_activity)} akun aktivitas rendah',
                'Update status pipeline setiap hari'
            ],
            'Target': ['Semua', f'{target_sme} klien', f'{min(target_payroll, 5)} klien', f'{len(low_activity)} klien', 'Harian']
        })
        
        st.dataframe(
            action_items,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Priority": st.column_config.TextColumn(""),
                "Action": st.column_config.TextColumn("Aksi"),
                "Target": st.column_config.TextColumn("Target"),
            }
        )

else:
    # Original two-column layout for Smart Opportunities
    
    # ========== SUMMARY DASHBOARD AT TOP ==========
    st.header("🎯 Peluang Hari Ini")
    
    # Filter high-priority leads
    priority_leads = df[df["Opportunity Tag"].str.contains("TARGET")].nlargest(5, "Potential Value (M)")
    
    # Visual Summary Dashboard
    col_sum1, col_sum2, col_sum3, col_sum4 = st.columns(4)
    
    with col_sum1:
        st.metric(
            "Total Leads Prioritas",
            len(priority_leads),
            f"{len(priority_leads)/len(df)*100:.0f}% dari portfolio"
        )
    
    with col_sum2:
        total_potential = priority_leads['Potential Value (M)'].sum()
        st.metric(
            "Total Nilai Potensial",
            f"Rp {total_potential:.0f}M",
            "Revenue opportunity"
        )
    
    with col_sum3:
        target_sme_count = len(priority_leads[priority_leads['Opportunity Tag'] == 'TARGET SME LOAN'])
        st.metric(
            "SME Loan Targets",
            target_sme_count,
            f"Rp {priority_leads[priority_leads['Opportunity Tag'] == 'TARGET SME LOAN']['Potential Value (M)'].sum():.0f}M"
        )
    
    with col_sum4:
        avg_days_contact = priority_leads['Days Since Contact'].mean()
        contact_status = "Good" if avg_days_contact < 30 else "Warning" if avg_days_contact < 60 else "Critical"
        st.metric(
            "Avg Days Since Contact",
            f"{avg_days_contact:.0f} hari",
            contact_status,
            delta_color="inverse" if avg_days_contact > 30 else "normal"
        )
    
    st.markdown("---")
    
    col_middle, col_right = st.columns([4, 6])

    # ========== ZONE 2: MIDDLE COLUMN (ACTION LIST) ==========
    with col_middle:
        st.subheader(f"📋 {len(priority_leads)} Leads Aktif")
        
        # Display top leads as enhanced visual cards
        for idx, row in priority_leads.iterrows():
            with st.container():
                # Card styling with border
                if row["Opportunity Tag"] == "TARGET SME LOAN":
                    border_color = "#e74c3c"
                    bg_color = "#fee"
                    icon = "💰"
                    tag_badge = "SME LOAN"
                else:
                    border_color = "#3498db"
                    bg_color = "#eef"
                    icon = "💼"
                    tag_badge = "PAYROLL"
                
                # Determine frequency color and badge
                freq = row['Transaction Frequency']
                if freq == "Low":
                    freq_color = "#e74c3c"
                    freq_badge = "🔴"
                elif freq == "Medium":
                    freq_color = "#f39c12"
                    freq_badge = "🟡"
                else:
                    freq_color = "#27ae60"
                    freq_badge = "🟢"
                
                # Calculate priority score (0-100)
                priority_score = min(100, int((row['Potential Value (M)'] / 100) + (50 if freq == "High" else 25 if freq == "Medium" else 0)))
                
                # Card header with visual elements
                st.markdown(f"""
                <div style="
                    border-left: 6px solid {border_color};
                    background: {bg_color};
                    padding: 15px;
                    border-radius: 8px;
                    margin-bottom: 15px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <h4 style="margin: 0;">{icon} {row['Client Name']}</h4>
                        <span style="
                            background: {border_color};
                            color: white;
                            padding: 4px 12px;
                            border-radius: 12px;
                            font-size: 12px;
                            font-weight: bold;
                        ">{tag_badge}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Metrics row with visual indicators
                col_a, col_b = st.columns([3, 2])
                
                with col_a:
                    # Giro with progress bar
                    giro_val = row['Avg Giro Balance (M)']
                    giro_pct = min(100, (giro_val / 10000) * 100)
                    st.markdown(f"**Saldo Giro:** Rp {giro_val}M")
                    st.progress(giro_pct / 100)
                    
                    # Potential value with progress bar
                    potential_val = row['Potential Value (M)']
                    potential_pct = min(100, (potential_val / 3000) * 100)
                    st.markdown(f"**Nilai Potensial:** Rp {potential_val}M")
                    st.progress(potential_pct / 100)
                
                with col_b:
                    # Frequency badge
                    st.markdown(f"""
                    <div style="text-align: center; margin-bottom: 10px;">
                        <div style="font-size: 11px; color: #666;">Frekuensi Transaksi</div>
                        <div style="font-size: 24px;">{freq_badge}</div>
                        <div style="color: {freq_color}; font-weight: bold;">{freq}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Priority score gauge
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <div style="font-size: 11px; color: #666;">Priority Score</div>
                        <div style="
                            font-size: 28px;
                            font-weight: bold;
                            color: {border_color};
                        ">{priority_score}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Action button
                if st.button(f"🔍 Analisis Detail", key=f"btn_{idx}", use_container_width=True):
                    st.session_state['selected_client'] = row['Client Name']
                    st.rerun()
                
                st.markdown("<br>", unsafe_allow_html=True)
        
        # ========== OTHER CLIENTS SECTION ==========
        st.markdown("---")
        st.subheader(f"📊 Klien Lainnya ({len(df) - len(priority_leads)} klien)")
        
        # Get other clients (not in top 5 priority)
        other_clients = df[~df.index.isin(priority_leads.index)].sort_values('Avg Giro Balance (M)', ascending=False)
        
        # Display options
        display_mode = st.radio(
            "Tampilkan sebagai:",
            ["Compact Cards", "Table View"],
            horizontal=True,
            key="other_clients_view"
        )
        
        if display_mode == "Compact Cards":
            # Compact card view with analysis buttons
            for idx, row in other_clients.iterrows():
                with st.expander(f"{row['Client Name']} - Rp {row['Avg Giro Balance (M)']}M - {row['Opportunity Tag']}", expanded=False):
                    col_c1, col_c2, col_c3 = st.columns([2, 2, 1])
                    
                    with col_c1:
                        st.metric("Saldo Giro", f"Rp {row['Avg Giro Balance (M)']}M")
                        st.caption(f"📍 {row['SME Loan Status']} SME | {row['Payroll Status']} Payroll")
                    
                    with col_c2:
                        st.metric("Potensial", f"Rp {row['Potential Value (M)']}M")
                        st.caption(f"🔄 {row['Transaction Frequency']} | 📅 {row['Days Since Contact']} hari lalu")
                    
                    with col_c3:
                        # Opportunity badge
                        tag_color = OPPORTUNITY_COLORS.get(row['Opportunity Tag'], '#95a5a6')
                        st.markdown(f"""
                        <div style="
                            background: {tag_color};
                            color: white;
                            padding: 5px;
                            border-radius: 5px;
                            text-align: center;
                            font-size: 10px;
                            margin-bottom: 10px;
                        ">
                            {row['Opportunity Tag'].replace('TARGET ', '')}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button("🔍 Analisis", key=f"other_{idx}", use_container_width=True):
                            st.session_state['selected_client'] = row['Client Name']
                            st.rerun()
        
        else:
            # Table view with action column
            table_df = other_clients[['Client Name', 'Avg Giro Balance (M)', 'Potential Value (M)', 
                                      'Opportunity Tag', 'Transaction Frequency', 'Days Since Contact']].copy()
            
            # Add analyze column with buttons
            st.dataframe(
                table_df,
                use_container_width=True,
                height=400,
                column_config={
                    "Client Name": st.column_config.TextColumn("Nama Klien", width="medium"),
                    "Avg Giro Balance (M)": st.column_config.NumberColumn("Giro (M)", format="Rp %.1f M"),
                    "Potential Value (M)": st.column_config.NumberColumn("Potensial (M)", format="Rp %.1f M"),
                    "Opportunity Tag": st.column_config.TextColumn("Tag", width="medium"),
                    "Transaction Frequency": st.column_config.TextColumn("Freq", width="small"),
                    "Days Since Contact": st.column_config.NumberColumn("Hari", format="%d hari"),
                }
            )
            
            # Quick analyze selector below table
            st.markdown("**Pilih klien untuk analisis:**")
            selected_client_name = st.selectbox(
                "Klien",
                options=["-- Pilih Klien --"] + other_clients['Client Name'].tolist(),
                key="select_other_client"
            )
            
            col_btn1, col_btn2 = st.columns([1, 3])
            with col_btn1:
                if st.button("🔍 Analisis Client Terpilih", disabled=(selected_client_name == "-- Pilih Klien --")):
                    st.session_state['selected_client'] = selected_client_name
                    st.rerun()
            with col_btn2:
                if selected_client_name != "-- Pilih Klien --":
                    st.info(f"Siap menganalisis: {selected_client_name}")

    # ========== ZONE 3: RIGHT COLUMN (CO-PILOT PANEL) ==========
    with col_right:
        if st.session_state['selected_client']:
            client_name = st.session_state['selected_client']
            client_row = df[df["Client Name"] == client_name].iloc[0]
            
            st.header(f"🤖 Co-Pilot: {client_name}")
            
            # Client Profile Section - Enhanced with Color-Coded Cards
            st.subheader("📋 Profil Klien")
            
            # Timeline/Context Row
            col_ctx1, col_ctx2, col_ctx3 = st.columns(3)
            
            with col_ctx1:
                tenure = client_row['Tenure Years']
                loyalty_color = "#9b59b6" if client_row['Loyalty Status'] == "Platinum" else "#3498db" if client_row['Loyalty Status'] == "Gold" else "#95a5a6"
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, {loyalty_color} 0%, {loyalty_color}cc 100%);
                    padding: 15px;
                    border-radius: 8px;
                    text-align: center;
                    color: white;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                    <div style="font-size: 12px; opacity: 0.9;">Tenure</div>
                    <div style="font-size: 24px; font-weight: bold; margin: 5px 0;">{tenure}</div>
                    <div style="font-size: 11px;">{client_row['Loyalty Status']} Member</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_ctx2:
                days_contact = client_row['Days Since Contact']
                contact_color = "#27ae60" if days_contact < 30 else "#f39c12" if days_contact < 90 else "#e74c3c"
                contact_status = "Good" if days_contact < 30 else "Warning" if days_contact < 90 else "Critical"
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, {contact_color} 0%, {contact_color}cc 100%);
                    padding: 15px;
                    border-radius: 8px;
                    text-align: center;
                    color: white;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                    <div style="font-size: 12px; opacity: 0.9;">Last Contact</div>
                    <div style="font-size: 24px; font-weight: bold; margin: 5px 0;">{days_contact}</div>
                    <div style="font-size: 11px;">hari lalu • {contact_status}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_ctx3:
                freq = client_row['Transaction Frequency']
                freq_color = "#27ae60" if freq == "High" else "#f39c12" if freq == "Medium" else "#e74c3c"
                freq_icon = "🟢" if freq == "High" else "🟡" if freq == "Medium" else "🔴"
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, {freq_color} 0%, {freq_color}cc 100%);
                    padding: 15px;
                    border-radius: 8px;
                    text-align: center;
                    color: white;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                    <div style="font-size: 12px; opacity: 0.9;">Frekuensi</div>
                    <div style="font-size: 24px; font-weight: bold; margin: 5px 0;">{freq_icon}</div>
                    <div style="font-size: 11px;">{freq}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Financial Metrics Row with Color-Coded Cards
            col_fin1, col_fin2 = st.columns(2)
            
            with col_fin1:
                giro_val = client_row['Avg Giro Balance (M)']
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
                    padding: 15px;
                    border-radius: 8px;
                    color: white;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    margin-bottom: 10px;
                ">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="font-size: 28px;">💰</div>
                        <div style="flex: 1;">
                            <div style="font-size: 12px; opacity: 0.9;">Saldo Giro</div>
                            <div style="font-size: 22px; font-weight: bold;">Rp {giro_val}M</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                potential_val = client_row['Potential Value (M)']
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #16a085 0%, #138d75 100%);
                    padding: 15px;
                    border-radius: 8px;
                    color: white;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="font-size: 28px;">📈</div>
                        <div style="flex: 1;">
                            <div style="font-size: 12px; opacity: 0.9;">Nilai Potensial</div>
                            <div style="font-size: 22px; font-weight: bold;">Rp {potential_val}M</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_fin2:
                sme_status = client_row['SME Loan Status']
                sme_color = "#e74c3c" if sme_status == "None" else "#27ae60"
                sme_icon = "⚠️" if sme_status == "None" else "✅"
                sme_label = "Belum Ada" if sme_status == "None" else "Aktif"
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, {sme_color} 0%, {sme_color}cc 100%);
                    padding: 15px;
                    border-radius: 8px;
                    color: white;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    margin-bottom: 10px;
                ">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="font-size: 28px;">{sme_icon}</div>
                        <div style="flex: 1;">
                            <div style="font-size: 12px; opacity: 0.9;">Pinjaman SME</div>
                            <div style="font-size: 22px; font-weight: bold;">{sme_label}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                payroll_status = client_row['Payroll Status']
                payroll_color = "#f39c12" if payroll_status == "None" else "#27ae60"
                payroll_icon = "💼" if payroll_status == "None" else "✅"
                payroll_label = "Belum Ada" if payroll_status == "None" else "Aktif"
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, {payroll_color} 0%, {payroll_color}cc 100%);
                    padding: 15px;
                    border-radius: 8px;
                    color: white;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="font-size: 28px;">{payroll_icon}</div>
                        <div style="flex: 1;">
                            <div style="font-size: 12px; opacity: 0.9;">Payroll</div>
                            <div style="font-size: 22px; font-weight: bold;">{payroll_label}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
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
                # Copy button with JavaScript
                import json
                script_json = json.dumps(script_area)
                copy_button_html = f"""
                <button onclick="copyToClipboard()" 
                        style="background: #4CAF50; color: white; border: none; padding: 8px 16px; 
                               border-radius: 5px; cursor: pointer; width: 100%; height: 38px;">
                    📋 Salin Skrip
                </button>
                <script>
                function copyToClipboard() {{
                    navigator.clipboard.writeText({script_json}).then(function() {{
                        alert('Skrip berhasil disalin ke clipboard!');
                    }}).catch(function(err) {{
                        alert('Gagal menyalin: ' + err);
                    }});
                }}
                </script>
                """
                components.html(copy_button_html, height=50)
            with col_b2:
                if st.button("🔄 Generate Ulang (Formal)"):
                    st.info("Sedang generate ulang dengan tone formal...")
            with col_b3:
                import urllib.parse
                wa_message = urllib.parse.quote(script)
                wa_link = f"https://wa.me/6286276272612?text={wa_message}"
                st.markdown(f'<a href="{wa_link}" target="_blank"><button style="background: #25D366; color: white; border: none; padding: 8px 16px; border-radius: 5px; cursor: pointer; width: 100%; height: 38px;">✉️ Kirim WA</button></a>', unsafe_allow_html=True)
            
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
            # Empty state with visual tips cards
            st.info("Pilih klien dari daftar peluang untuk mengaktifkan analisis Co-Pilot")
            
            st.markdown("---")
            st.markdown("### 💡 Tips & Best Practices")
            
            # Visual tip cards
            tip_cards = [
                {
                    "icon": "🎯",
                    "title": "Prioritas",
                    "desc": "Fokus pada leads dengan tag TARGET SME LOAN",
                    "color": "#e74c3c"
                },
                {
                    "icon": "⏰",
                    "title": "Waktu Terbaik",
                    "desc": "Hubungi antara jam 10-11 pagi atau 2-3 sore",
                    "color": "#3498db"
                },
                {
                    "icon": "🤝",
                    "title": "Pendekatan",
                    "desc": "Gunakan personal touch, referensi riwayat transaksi",
                    "color": "#9b59b6"
                },
                {
                    "icon": "📞",
                    "title": "Follow-up",
                    "desc": "Jangan lebih dari 3 hari untuk merespons",
                    "color": "#27ae60"
                }
            ]
            
            for tip in tip_cards:
                st.markdown(f"""
                <div style="
                    border-left: 4px solid {tip['color']};
                    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                    padding: 15px;
                    margin-bottom: 12px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.08);
                ">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <div style="font-size: 32px;">{tip['icon']}</div>
                        <div>
                            <div style="font-weight: bold; color: {tip['color']}; margin-bottom: 4px;">{tip['title']}</div>
                            <div style="font-size: 14px; color: #555;">{tip['desc']}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)