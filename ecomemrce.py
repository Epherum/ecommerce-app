import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Ecommerce Cost Calculator - Qatar Business",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        color: #1f77b4;
    }
    .platform-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #007bff;
        margin-bottom: 1rem;
    }
    .cost-highlight {
        font-size: 1.5rem;
        font-weight: bold;
        color: #28a745;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-header">🛒 Ecommerce Platform Cost Calculator</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">For Qatar-based International Businesses</p>', unsafe_allow_html=True)

# Sidebar controls
st.sidebar.header("📊 Business Parameters")

# Business size selection
business_size = st.sidebar.selectbox(
    "Business Size",
    ["Startup (0-100 products)", "Small Business (100-1,000 products)", "Medium Business (1,000-10,000 products)", "Enterprise (10,000+ products)"]
)

# Monthly revenue slider
monthly_revenue = st.sidebar.slider(
    "Expected Monthly Revenue (USD)",
    min_value=0,
    max_value=500000,
    value=10000,
    step=1000,
    format="$%d"
)

# Number of products
num_products = st.sidebar.slider(
    "Number of Products",
    min_value=1,
    max_value=50000,
    value=500,
    step=50
)

# Monthly traffic
monthly_traffic = st.sidebar.slider(
    "Monthly Website Traffic",
    min_value=100,
    max_value=1000000,
    value=10000,
    step=1000
)

# Market focus
market_focus = st.sidebar.multiselect(
    "Target Markets",
    ["Qatar/GCC", "Middle East", "Europe", "North America", "Asia", "Global"],
    default=["Qatar/GCC", "Global"]
)

# Business type
business_type = st.sidebar.selectbox(
    "Business Type",
    ["B2C Retail", "B2B Wholesale", "Digital Products", "Subscription", "Marketplace"]
)

# Platform comparison data
def get_platform_data():
    return {
        'Shopify': {
            'plans': {
                'Basic': {'monthly': 39, 'transaction_fee': 0.029, 'products': 'Unlimited'},
                'Shopify': {'monthly': 105, 'transaction_fee': 0.025, 'products': 'Unlimited'},
                'Advanced': {'monthly': 399, 'transaction_fee': 0.022, 'products': 'Unlimited'},
                'Plus': {'monthly': 2500, 'transaction_fee': 0.015, 'products': 'Unlimited'}
            },
            'additional_costs': {
                'theme': 300,  # One-time premium theme
                'apps_basic': 150,  # Monthly for essential apps
                'apps_advanced': 500,  # Monthly for advanced apps
                'third_party_gateway': 0.02,  # Additional fee for Qatar (no Shopify Payments)
                'international_fee': 0.015,  # Currency conversion
                'ssl': 0  # Included
            },
            'pros': ['Easy setup', 'Great app ecosystem', 'International features', 'Reliable hosting'],
            'cons': ['No Shopify Payments in Qatar', 'Transaction fees', 'Limited customization', '2024 price increases']
        },
        'WooCommerce': {
            'plans': {
                'Starter': {'monthly': 25, 'transaction_fee': 0, 'products': 'Unlimited'},
                'Growth': {'monthly': 100, 'transaction_fee': 0, 'products': 'Unlimited'},
                'Scale': {'monthly': 300, 'transaction_fee': 0, 'products': 'Unlimited'},
                'Enterprise': {'monthly': 1500, 'transaction_fee': 0, 'products': 'Unlimited'}
            },
            'additional_costs': {
                'hosting': 50,  # Monthly hosting cost
                'plugins': 100,  # Monthly for essential plugins
                'security': 25,  # Monthly security plugins
                'ssl': 10,  # Monthly SSL certificate
                'maintenance': 200,  # Monthly maintenance/updates
                'payment_gateway': 0.025  # Dibsy for Qatar
            },
            'pros': ['Full customization', 'No transaction fees', 'Open source', 'Qatar payment gateways'],
            'cons': ['Requires technical expertise', 'Hosting costs', 'Security responsibility', 'Maintenance overhead']
        },
        'Custom Next.js': {
            'plans': {
                'Startup': {'monthly': 150, 'transaction_fee': 0, 'products': 'Unlimited'},
                'Small': {'monthly': 500, 'transaction_fee': 0, 'products': 'Unlimited'},
                'Medium': {'monthly': 2000, 'transaction_fee': 0, 'products': 'Unlimited'},
                'Enterprise': {'monthly': 5000, 'transaction_fee': 0, 'products': 'Unlimited'}
            },
            'additional_costs': {
                'development': 10000,  # One-time development cost
                'database': 100,  # Monthly database cost
                'cdn': 50,  # Monthly CDN cost
                'monitoring': 100,  # Monthly monitoring tools
                'email_service': 20,  # Monthly email service
                'stripe_fee': 0.029,  # Stripe processing fee
                'international_fee': 0.015  # International card fee
            },
            'pros': ['Ultimate flexibility', 'Best performance', 'Full control', 'Scalable architecture'],
            'cons': ['High development cost', 'Technical expertise required', 'Infrastructure management', 'Longer time to market']
        },
        'BigCommerce': {
            'plans': {
                'Standard': {'monthly': 29, 'transaction_fee': 0, 'products': 'Unlimited'},
                'Plus': {'monthly': 79, 'transaction_fee': 0, 'products': 'Unlimited'},
                'Pro': {'monthly': 299, 'transaction_fee': 0, 'products': 'Unlimited'},
                'Enterprise': {'monthly': 1000, 'transaction_fee': 0, 'products': 'Unlimited'}
            },
            'additional_costs': {
                'payment_processing': 0.0259,  # Base processing fee
                'international_fee': 0.015,  # International transactions
                'apps': 100,  # Monthly apps cost
                'theme': 200,  # One-time theme cost
                'ssl': 0  # Included
            },
            'pros': ['No transaction fees', 'Built-in features', 'Auto-scaling', 'Good API'],
            'cons': ['Limited themes', 'Revenue-based plan upgrades', 'Fewer apps than Shopify', 'Complex pricing tiers']
        },
        'Wix': {
            'plans': {
                'Core': {'monthly': 29, 'transaction_fee': 0.029, 'products': 'Unlimited'},
                'Business': {'monthly': 36, 'transaction_fee': 0.029, 'products': 'Unlimited'},
                'Business Elite': {'monthly': 159, 'transaction_fee': 0.029, 'products': 'Unlimited'}
            },
            'additional_costs': {
                'payment_processing': 0.029,  # Wix Payments
                'international_fee': 0.025,  # International transactions
                'apps': 50,  # Monthly apps cost
                'ssl': 0  # Included
            },
            'pros': ['Easy drag-and-drop', 'Included hosting', 'Good templates', 'All-in-one solution'],
            'cons': ['Limited scalability', 'Fewer ecommerce features', 'Limited customization', 'Vendor lock-in']
        },
        'Squarespace': {
            'plans': {
                'Basic': {'monthly': 16, 'transaction_fee': 0.03, 'products': 'Unlimited'},
                'Commerce': {'monthly': 29, 'transaction_fee': 0.03, 'products': 'Unlimited'},
                'Advanced': {'monthly': 99, 'transaction_fee': 0, 'products': 'Unlimited'}
            },
            'additional_costs': {
                'payment_processing': 0.029,  # Stripe processing
                'international_fee': 0.015,  # International transactions
                'ssl': 0,  # Included
                'apps': 30  # Limited app ecosystem
            },
            'pros': ['Beautiful templates', 'Included hosting', 'Good for content', 'Simple pricing'],
            'cons': ['Limited apps', 'Basic ecommerce features', 'Not for high volume', 'Limited integrations']
        }
    }

# Calculate costs based on parameters
def calculate_platform_costs(platform_name, platform_data, monthly_revenue, business_size):
    plans = platform_data['plans']
    additional = platform_data['additional_costs']
    
    # Determine appropriate plan based on business size and revenue
    if business_size.startswith("Startup"):
        plan_name = list(plans.keys())[0]  # First plan
    elif business_size.startswith("Small"):
        plan_name = list(plans.keys())[min(1, len(plans)-1)]  # Second plan or last
    elif business_size.startswith("Medium"):
        plan_name = list(plans.keys())[min(2, len(plans)-1)]  # Third plan or last
    else:  # Enterprise
        plan_name = list(plans.keys())[-1]  # Last plan
    
    plan = plans[plan_name]
    
    # Calculate monthly costs
    monthly_platform = plan['monthly']
    
    # Transaction fees
    transaction_volume = monthly_revenue
    base_transaction_fee = plan['transaction_fee']
    
    # Additional fees specific to Qatar
    if platform_name == 'Shopify':
        # No Shopify Payments in Qatar, must use third-party
        total_transaction_rate = base_transaction_fee + additional.get('third_party_gateway', 0) + additional.get('international_fee', 0)
        monthly_apps = additional['apps_basic'] if business_size.startswith("Startup") else additional['apps_advanced']
        monthly_additional = monthly_apps
        one_time = additional['theme']
    elif platform_name == 'WooCommerce':
        total_transaction_rate = additional['payment_gateway']  # Dibsy for Qatar
        monthly_additional = additional['hosting'] + additional['plugins'] + additional['security'] + additional['ssl'] + additional['maintenance']
        one_time = 0
    elif platform_name == 'Custom Next.js':
        total_transaction_rate = additional['stripe_fee'] + additional['international_fee']
        monthly_additional = additional['database'] + additional['cdn'] + additional['monitoring'] + additional['email_service']
        one_time = additional['development']
    else:
        total_transaction_rate = base_transaction_fee + additional.get('international_fee', 0)
        monthly_additional = additional.get('apps', 0)
        one_time = additional.get('theme', 0)
    
    monthly_transaction_fees = transaction_volume * total_transaction_rate
    
    total_monthly = monthly_platform + monthly_additional + monthly_transaction_fees
    annual_cost = total_monthly * 12 + one_time
    
    return {
        'plan_name': plan_name,
        'monthly_platform': monthly_platform,
        'monthly_additional': monthly_additional,
        'monthly_transaction_fees': monthly_transaction_fees,
        'total_monthly': total_monthly,
        'annual_cost': annual_cost,
        'one_time_costs': one_time,
        'transaction_rate': total_transaction_rate
    }

# Main dashboard
platforms_data = get_platform_data()

# Calculate costs for all platforms
platform_costs = {}
for platform_name, platform_data in platforms_data.items():
    platform_costs[platform_name] = calculate_platform_costs(
        platform_name, platform_data, monthly_revenue, business_size
    )

# Display key metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Business Size", business_size.split(" ")[0])

with col2:
    st.metric("Monthly Revenue", f"${monthly_revenue:,}")

with col3:
    st.metric("Products", f"{num_products:,}")

with col4:
    st.metric("Monthly Traffic", f"{monthly_traffic:,}")

st.markdown("---")

# Platform comparison section
st.header("💰 Platform Cost Comparison")

# Create comparison table
comparison_data = []
for platform_name, costs in platform_costs.items():
    comparison_data.append({
        'Platform': platform_name,
        'Plan': costs['plan_name'],
        'Monthly Platform Fee': f"${costs['monthly_platform']:.0f}",
        'Monthly Additional': f"${costs['monthly_additional']:.0f}",
        'Transaction Fees': f"${costs['monthly_transaction_fees']:.0f}",
        'Total Monthly': f"${costs['total_monthly']:.0f}",
        'Annual Cost': f"${costs['annual_cost']:.0f}",
        'Transaction Rate': f"{costs['transaction_rate']:.1%}"
    })

df_comparison = pd.DataFrame(comparison_data)
st.dataframe(df_comparison, use_container_width=True)

# Cost breakdown charts
col1, col2 = st.columns(2)

with col1:
    # Monthly cost breakdown
    monthly_costs = [costs['total_monthly'] for costs in platform_costs.values()]
    platform_names = list(platform_costs.keys())
    
    fig_monthly = px.bar(
        x=platform_names,
        y=monthly_costs,
        title="Monthly Total Costs by Platform",
        labels={'x': 'Platform', 'y': 'Monthly Cost (USD)'},
        color=monthly_costs,
        color_continuous_scale='viridis'
    )
    fig_monthly.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_monthly, use_container_width=True)

with col2:
    # Annual cost breakdown
    annual_costs = [costs['annual_cost'] for costs in platform_costs.values()]
    
    fig_annual = px.bar(
        x=platform_names,
        y=annual_costs,
        title="Annual Total Costs by Platform",
        labels={'x': 'Platform', 'y': 'Annual Cost (USD)'},
        color=annual_costs,
        color_continuous_scale='plasma'
    )
    fig_annual.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_annual, use_container_width=True)

# Detailed cost breakdown
st.header("📊 Detailed Cost Breakdown")

# Create stacked bar chart
platforms = list(platform_costs.keys())
platform_fees = [costs['monthly_platform'] for costs in platform_costs.values()]
additional_fees = [costs['monthly_additional'] for costs in platform_costs.values()]
transaction_fees = [costs['monthly_transaction_fees'] for costs in platform_costs.values()]

fig_breakdown = go.Figure(data=[
    go.Bar(name='Platform Fees', x=platforms, y=platform_fees),
    go.Bar(name='Additional Services', x=platforms, y=additional_fees),
    go.Bar(name='Transaction Fees', x=platforms, y=transaction_fees)
])

fig_breakdown.update_layout(
    barmode='stack',
    title='Monthly Cost Breakdown by Component',
    xaxis_title='Platform',
    yaxis_title='Cost (USD)',
    height=500
)

st.plotly_chart(fig_breakdown, use_container_width=True)

# Platform details
st.header("🔍 Platform Details & Recommendations")

# Create tabs for each platform
tabs = st.tabs(list(platforms_data.keys()))

for i, (platform_name, platform_data) in enumerate(platforms_data.items()):
    with tabs[i]:
        costs = platform_costs[platform_name]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f'<div class="platform-card">', unsafe_allow_html=True)
            st.markdown(f"**{platform_name}** - {costs['plan_name']} Plan")
            st.markdown(f'<div class="cost-highlight">${costs["total_monthly"]:.0f}/month</div>', unsafe_allow_html=True)
            st.markdown(f"Annual Cost: **${costs['annual_cost']:,.0f}**")
            st.markdown(f"Transaction Rate: **{costs['transaction_rate']:.1%}**")
            if costs['one_time_costs'] > 0:
                st.markdown(f"One-time Costs: **${costs['one_time_costs']:,.0f}**")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Pros and cons
            col_pro, col_con = st.columns(2)
            with col_pro:
                st.markdown("**✅ Pros:**")
                for pro in platform_data['pros']:
                    st.markdown(f"• {pro}")
            
            with col_con:
                st.markdown("**❌ Cons:**")
                for con in platform_data['cons']:
                    st.markdown(f"• {con}")
        
        with col2:
            # Cost components pie chart
            labels = ['Platform Fee', 'Additional Services', 'Transaction Fees']
            values = [costs['monthly_platform'], costs['monthly_additional'], costs['monthly_transaction_fees']]
            
            fig_pie = px.pie(
                values=values,
                names=labels,
                title=f"{platform_name} Cost Breakdown"
            )
            fig_pie.update_layout(height=300)
            st.plotly_chart(fig_pie, use_container_width=True)

# Qatar-specific considerations
st.header("🇶🇦 Qatar-Specific Considerations")

st.markdown("""
<div class="warning-box">
<h4>⚠️ Important Notes for Qatar-based Businesses:</h4>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Payment Gateways in Qatar:**
    - Shopify Payments not available
    - Recommended: Dibsy, PayTabs, Telr, 2Checkout
    - Qatar Central Bank licensing required
    - Additional 0.6-2% fees for third-party gateways
    
    **Tax Considerations:**
    - Potential 0% corporate tax for GCC-owned companies
    - No VAT currently (5% under consideration)
    - Compliance costs: $10,000-50,000 annually
    """)

with col2:
    st.markdown("""
    **Market Insights:**
    - 40% credit/debit card usage
    - Growing digital wallet adoption
    - Significant cash-on-delivery preference
    - Currency stability (QAR-USD peg: 1 USD = 3.64 QAR)
    
    **Regulatory Requirements:**
    - Qatar Central Bank licensed payment providers
    - Local data residency considerations
    - Arabic language support recommended
    """)

# ROI Calculator
st.header("📈 ROI & Break-even Analysis")

st.markdown("Compare platforms based on your revenue projections:")

# Revenue projection inputs
col1, col2, col3 = st.columns(3)

with col1:
    growth_rate = st.slider("Monthly Growth Rate (%)", 0, 50, 10)

with col2:
    projection_months = st.slider("Projection Period (months)", 3, 36, 12)

with col3:
    conversion_rate = st.slider("Conversion Rate (%)", 0.5, 10.0, 2.5)

# Calculate ROI projections
months = list(range(1, projection_months + 1))
revenues = [monthly_revenue * (1 + growth_rate/100)**i for i in months]

# Create projection chart
fig_projection = go.Figure()

for platform_name, costs in platform_costs.items():
    monthly_cost = costs['total_monthly']
    cumulative_costs = [monthly_cost * i + costs['one_time_costs'] for i in months]
    cumulative_revenues = [sum(revenues[:i+1]) for i in range(len(revenues))]
    profits = [rev - cost for rev, cost in zip(cumulative_revenues, cumulative_costs)]
    
    fig_projection.add_trace(go.Scatter(
        x=months,
        y=profits,
        mode='lines+markers',
        name=platform_name,
        line=dict(width=3)
    ))

fig_projection.update_layout(
    title='Cumulative Profit Projection by Platform',
    xaxis_title='Months',
    yaxis_title='Cumulative Profit (USD)',
    height=500,
    hovermode='x unified'
)

# Add break-even line
fig_projection.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Break-even")

st.plotly_chart(fig_projection, use_container_width=True)

# Recommendations
st.header("🎯 Recommendations")

# Sort platforms by total monthly cost
sorted_platforms = sorted(platform_costs.items(), key=lambda x: x[1]['total_monthly'])
cheapest = sorted_platforms[0]
most_expensive = sorted_platforms[-1]

col1, col2 = st.columns(2)

with col1:
    st.success(f"""
    **💡 Most Cost-Effective: {cheapest[0]}**
    
    Monthly Cost: ${cheapest[1]['total_monthly']:.0f}
    Annual Cost: ${cheapest[1]['annual_cost']:,.0f}
    
    Best for: Budget-conscious businesses, startups
    """)

with col2:
    if business_size.startswith("Enterprise"):
        enterprise_rec = "Custom Next.js" if "Custom Next.js" in platform_costs else "Shopify"
        st.info(f"""
        **🚀 Enterprise Recommendation: {enterprise_rec}**
        
        Best for: High-volume, custom requirements
        Scalability: Unlimited
        Control: Maximum flexibility
        """)
    else:
        st.info(f"""
        **⚖️ Balanced Option: Shopify**
        
        Best for: Growing businesses
        Features: Comprehensive app ecosystem
        Support: Excellent documentation
        """)

# Final recommendations based on business type
st.markdown("### 📋 Tailored Recommendations:")

if business_size.startswith("Startup"):
    st.markdown("""
    - **Start with Squarespace or Wix** for minimal costs and quick setup
    - **Upgrade to Shopify** when revenue exceeds $5,000/month
    - Focus on local payment gateways from day one
    """)
elif business_size.startswith("Small"):
    st.markdown("""
    - **Shopify Basic** for ease of use and growth potential
    - **WooCommerce** if you have technical expertise
    - Implement multi-gateway strategy for Qatar market
    """)
elif business_size.startswith("Medium"):
    st.markdown("""
    - **BigCommerce Pro** to eliminate transaction fees
    - **Shopify Advanced** for comprehensive features
    - Consider **Custom Next.js** for unique requirements
    """)
else:  # Enterprise
    st.markdown("""
    - **Custom Next.js solution** for maximum control
    - **Adobe Commerce** for complex B2B requirements
    - **Shopify Plus** for rapid deployment with enterprise features
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>💼 Created for Qatar-based international ecommerce businesses</p>
    <p>📊 Based on 2024-2025 pricing data | 🔄 Last updated: September 2025</p>
    <p>⚠️ Costs are estimates. Actual costs may vary based on specific requirements and negotiations.</p>
</div>
""", unsafe_allow_html=True)
