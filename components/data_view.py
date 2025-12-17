"""
Data View Component
Displays full client data table with filtering and statistics
"""

import streamlit as st
import plotly.express as px
from config import OPPORTUNITY_COLORS


def render_data_view(df):
    """Render the Data View"""
    
    st.header("📋 Data Semua Klien")
    st.markdown("---")
    
    # Filters
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
    
    # Enhanced Ringkasan Statistik (at top)
    _render_statistics_summary(filtered_df, len(df))
    
    st.markdown("---")
    
    # Data Table
    st.markdown(f"Menampilkan **{len(filtered_df)}** klien dari total **{len(df)}** klien")
    
    # Apply conditional formatting
    def highlight_priority(row):
        if row['Opportunity Tag'] == 'TARGET SME LOAN':
            return ['background-color: #ffebee'] * len(row)
        elif row['Opportunity Tag'] == 'TARGET PAYROLL':
            return ['background-color: #fff3e0'] * len(row)
        elif row['Days Since Contact'] > 90:
            return ['background-color: #fce4ec'] * len(row)
        return [''] * len(row)
    
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
    
    # Legend
    col_leg1, col_leg2, col_leg3 = st.columns(3)
    with col_leg1:
        st.markdown("🔴 **Red highlight:** TARGET SME LOAN")
    with col_leg2:
        st.markdown("🟠 **Orange highlight:** TARGET PAYROLL")
    with col_leg3:
        st.markdown("🟣 **Pink highlight:** Not contacted >90 days")


def _render_statistics_summary(filtered_df, total_clients):
    """Render enhanced statistics summary"""
    
    st.subheader("📊 Ringkasan Statistik")
    
    # Calculate metrics
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
    
    # Second Row - Penetration Metrics
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
        full_package = len(filtered_df[(filtered_df["SME Loan Status"] == "Active") & 
                                       (filtered_df["Payroll Status"] == "Active")])
        full_penetration = (full_package / len(filtered_df)) if len(filtered_df) > 0 else 0
        st.markdown("**Full Package (SME+Payroll)**")
        st.progress(full_penetration)
        st.caption(f"{full_package}/{len(filtered_df)} klien ({full_penetration*100:.1f}%)")
    
    with col_pen4:
        st.metric("Avg Tenure", f"{avg_tenure:.1f} tahun", "Loyalty indicator")
    
    # Third Row - Charts
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
