"""
Configuration file for Mandiri Smart-RM Co-Pilot Dashboard
Contains all constants, color schemes, and configuration settings
"""

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

# Chart color schemes
CHART_COLORS = {
    'giro_distribution': ['#1976d2', '#42a5f5', '#90caf9', '#bbdefb'],
    'primary_gradient': ['#667eea', '#764ba2'],
    'blue_gradient': ['#1976d2', '#42a5f5'],
    'pink_gradient': ['#f093fb', '#f5576c'],
    'red_gradient': ['#ff6b6b', '#c92a2a'],
    'orange_gradient': ['#f57c00', '#e65100']
}

# Streamlit Page Configuration
PAGE_CONFIG = {
    'page_title': "Mandiri Smart-RM Co-Pilot",
    'layout': "wide",
    'initial_sidebar_state': "expanded",
    'menu_items': {
        'About': "Mandiri Smart-RM Co-Pilot - Banking Intelligence Dashboard"
    }
}

# User Profile
USER_PROFILE = {
    'name': 'Budi Santoso',
    'branch': 'Tangerang BSD',
    'phone': '0812-3456-7890'
}

# Giro Balance Bins
GIRO_BINS = [0, 1000, 2000, 5000, 10000]
GIRO_LABELS = ['< 1M', '1-2M', '2-5M', '> 5M']

# Thresholds
THRESHOLDS = {
    'high_value_giro': 2000,
    'medium_value_giro': 1000,
    'contact_warning_days': 30,
    'contact_critical_days': 90,
    'loyal_client_years': 10,
    'platinum_years': 15,
    'gold_years': 5
}
