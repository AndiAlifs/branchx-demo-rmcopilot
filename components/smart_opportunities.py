"""
Smart Opportunities View Component
Displays priority leads and opportunity analysis
"""

import streamlit as st
from utils import mock_ai_analysis, generate_script


def render_smart_opportunities(df):
    """Render the Smart Opportunities view"""
    
    # Filter high-priority leads
    priority_leads = df[df["Opportunity Tag"].str.contains("TARGET")].nlargest(5, "Potential Value (M)")
    
    # Summary Dashboard at Top
    st.header("🎯 Peluang Hari Ini")
    
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

    # Action List
    with col_middle:
        st.subheader(f"📋 {len(priority_leads)} Leads Aktif")
        
        for idx, row in priority_leads.iterrows():
            with st.container():
                if row["Opportunity Tag"] == "TARGET SME LOAN":
                    border_color = "#e74c3c"
                    bg_color = "#fee"
                    icon = "💰"
                    tag_badge = "SME LOAN"
                else:
                    border_color = "#3498db"
                    bg_color = "#eff"
                    icon = "💼"
                    tag_badge = "PAYROLL"
                
                st.markdown(f"""
                <div style="
                    border-left: 5px solid {border_color};
                    background-color: {bg_color};
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 5px;
                ">
                    <h4 style="margin: 0; color: #333;">{icon} {row['Client Name']}</h4>
                    <p style="margin: 5px 0;"><strong>Giro:</strong> Rp {row['Avg Giro Balance (M)']}M | <strong>Potensial:</strong> Rp {row['Potential Value (M)']}M</p>
                    <span style="
                        background-color: {border_color};
                        color: white;
                        padding: 3px 10px;
                        border-radius: 3px;
                        font-size: 12px;
                        font-weight: bold;
                    ">{tag_badge}</span>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"🔍 Analisis {row['Client Name']}", key=f"analyze_{idx}"):
                    st.session_state['selected_client'] = row['Client Name']
                    st.rerun()

    # Analysis Panel
    with col_right:
        if st.session_state.get('selected_client'):
            st.subheader(f"🤖 AI Analysis: {st.session_state['selected_client']}")
            
            client_row = df[df["Client Name"] == st.session_state['selected_client']].iloc[0]
            
            # AI Insights
            with st.expander("📊 Smart Insights", expanded=True):
                insights = mock_ai_analysis(client_row)
                st.markdown(insights)
            
            # Action Script
            with st.expander("📝 Draft WhatsApp Script", expanded=True):
                script = generate_script(
                    client_row['Client Name'],
                    client_row['Opportunity Tag'],
                    client_row['Avg Giro Balance (M)']
                )
                st.text_area("Script", value=script, height=400, key="wa_script")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("📋 Copy Script"):
                        st.success("Script copied to clipboard!")
                with col_btn2:
                    if st.button("✉️ Send via WhatsApp"):
                        st.success("Opening WhatsApp...")
            
            # Pipeline Tracker
            with st.expander("📈 Pipeline Status"):
                status = st.selectbox(
                    "Update Status",
                    ["Not Contacted", "Contacted", "Interested", "Proposal Sent", "Negotiation", "Closed Won", "Closed Lost"],
                    key=f"status_{st.session_state['selected_client']}"
                )
                
                notes = st.text_area("Notes", placeholder="Add notes about this interaction...")
                
                if st.button("💾 Save Update"):
                    if 'pipeline_updates' not in st.session_state:
                        st.session_state['pipeline_updates'] = {}
                    
                    st.session_state['pipeline_updates'][st.session_state['selected_client']] = {
                        'status': status,
                        'notes': notes,
                        'updated_at': st.timestamp()
                    }
                    st.success(f"Pipeline updated for {st.session_state['selected_client']}")
        else:
            st.info("👈 Pilih klien dari daftar untuk melihat analisis lengkap dan generate action script")
