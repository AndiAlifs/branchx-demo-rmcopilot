"""
Relationship Health View Component
Displays customer relationship metrics and engagement tracking
"""

import streamlit as st
from datetime import datetime
from utils import generate_relationship_script
from config import THRESHOLDS


def render_relationship_health(df):
    """Render the Relationship Health view"""
    
    st.header("💝 Relationship Health Dashboard")
    st.markdown("*Memastikan nasabah loyal merasa dihargai dan dikenali*")
    st.markdown("---")
    
    # Retention KPIs
    st.subheader("📊 Retention KPIs")
    col_r1, col_r2, col_r3, col_r4 = st.columns(4)
    
    loyal_clients = df[df["Tenure Years"] > THRESHOLDS['loyal_client_years']]
    ignored_loyal = df[(df["Tenure Years"] > THRESHOLDS['loyal_client_years']) & 
                       (df["Days Since Contact"] > THRESHOLDS['contact_critical_days'])]
    platinum_clients = df[df["Loyalty Status"] == "Platinum"]
    at_risk_clients = df[(df["Avg Giro Balance (M)"] > THRESHOLDS['medium_value_giro']) & 
                          (df["Days Since Contact"] > 120)]
    
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
        _render_priority_recognition(df)
    
    with tab2:
        _render_reengagement_needed(df)
    
    # Context Log Panel
    if st.session_state.get('selected_relationship_client'):
        _render_context_log(df)


def _render_priority_recognition(df):
    """Render priority recognition tab"""
    st.subheader("Nasabah High Tenure yang Perlu Pengakuan")
    
    high_tenure = df[df["Tenure Years"] >= THRESHOLDS['loyal_client_years']].sort_values("Tenure Years", ascending=False)
    
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


def _render_reengagement_needed(df):
    """Render re-engagement needed tab"""
    st.subheader("Nasabah Bernilai Tinggi yang Lama Tidak Dihubungi")
    
    reengagement = df[(df["Avg Giro Balance (M)"] >= THRESHOLDS['medium_value_giro']) & 
                      (df["Days Since Contact"] > 60)].sort_values("Days Since Contact", ascending=False)
    
    st.markdown(f"**{len(reengagement)} nasabah** dengan saldo tinggi namun lama tidak dihubungi")
    
    for idx, row in reengagement.iterrows():
        days = row['Days Since Contact']
        
        if days > 180:
            urgency_label = "🔴 CRITICAL"
        elif days > 90:
            urgency_label = "🟠 HIGH"
        else:
            urgency_label = "🟡 MEDIUM"
        
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


def _render_context_log(df):
    """Render context log panel"""
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
