import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Notebook Market Intelligence",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg: #0d0d0d;
    --surface: #161616;
    --border: #2a2a2a;
    --accent: #00e5a0;
    --accent2: #ff6b35;
    --text: #f0f0f0;
    --muted: #666;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border);
}

h1, h2, h3 { font-family: 'Space Mono', monospace !important; }

.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    padding: 1.2rem 1.5rem;
    border-radius: 4px;
}
.metric-value {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: var(--accent);
}
.metric-label {
    font-size: 0.75rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.25rem;
}
.section-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    color: var(--muted);
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
}
[data-testid="stDataFrame"] { border: 1px solid var(--border) !important; }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    conn = sqlite3.connect('data/mercadolivre.db')
    df = pd.read_sql('SELECT * FROM notebook', conn)
    conn.close()
    df['_datetime'] = pd.to_datetime(df['_datetime'])
    return df

df = load_data()

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.markdown("## Filters")

sellers = sorted(df['seller'].dropna().unique())
selected_sellers = st.sidebar.multiselect("Seller", sellers, default=sellers)

price_min, price_max = int(df['new_price'].min()), int(df['new_price'].max())
price_range = st.sidebar.slider("Price range (R$)", price_min, price_max, (price_min, price_max))

min_rating = st.sidebar.slider("Minimum avg review", 0.0, 5.0, 0.0, 0.1)

# ── Apply filters ─────────────────────────────────────────────────────────────
filtered = df[
    (df['seller'].isin(selected_sellers)) &
    (df['new_price'].between(*price_range)) &
    (df['avg_review'] >= min_rating)
]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# Notebook Market Intelligence")
st.markdown(f"<p style='color:#666;font-size:0.85rem'>Source: {df['_source'].iloc[0]} · Last updated: {df['_datetime'].max().strftime('%Y-%m-%d %H:%M')}</p>", unsafe_allow_html=True)
st.markdown("---")

# ── KPI cards ─────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{len(filtered)}</div>
        <div class="metric-label">Products listed</div>
    </div>""", unsafe_allow_html=True)

with c2:
    avg_discount = filtered['_discount_pct'].mean()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{avg_discount:.1f}%</div>
        <div class="metric-label">Avg discount</div>
    </div>""", unsafe_allow_html=True)

with c3:
    avg_price = filtered['new_price'].mean()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">R$ {avg_price:,.0f}</div>
        <div class="metric-label">Avg current price</div>
    </div>""", unsafe_allow_html=True)

with c4:
    avg_rating = filtered['avg_review'].mean()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{avg_rating:.2f}</div>
        <div class="metric-label">Avg rating</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts row 1 ──────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown('<p class="section-title">Listings by seller</p>', unsafe_allow_html=True)
    seller_counts = filtered['seller'].value_counts().reset_index()
    seller_counts.columns = ['seller', 'count']
    fig = px.bar(
        seller_counts,
        x='count', y='seller',
        orientation='h',
        color='count',
        color_continuous_scale=[[0, '#1a1a1a'], [1, '#00e5a0']],
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='#f0f0f0', showlegend=False,
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=10, b=0),
        yaxis=dict(gridcolor='#2a2a2a'),
        xaxis=dict(gridcolor='#2a2a2a'),
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('<p class="section-title">Price distribution</p>', unsafe_allow_html=True)
    fig2 = px.histogram(
        filtered, x='new_price', nbins=30,
        color_discrete_sequence=['#00e5a0'],
    )
    fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='#f0f0f0', showlegend=False,
        margin=dict(l=0, r=0, t=10, b=0),
        yaxis=dict(gridcolor='#2a2a2a'),
        xaxis=dict(gridcolor='#2a2a2a', title='Price (R$)'),
        bargap=0.05,
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── Charts row 2 ──────────────────────────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.markdown('<p class="section-title">Discount % vs current price</p>', unsafe_allow_html=True)
    fig3 = px.scatter(
        filtered, x='new_price', y='_discount_pct',
        color='avg_review',
        color_continuous_scale=[[0, '#ff6b35'], [0.5, '#ffcc00'], [1, '#00e5a0']],
        hover_data=['name', 'seller'],
        labels={'new_price': 'Current Price (R$)', '_discount_pct': 'Discount (%)'},
    )
    fig3.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='#f0f0f0',
        margin=dict(l=0, r=0, t=10, b=0),
        yaxis=dict(gridcolor='#2a2a2a'),
        xaxis=dict(gridcolor='#2a2a2a'),
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.markdown('<p class="section-title">Avg rating by seller</p>', unsafe_allow_html=True)
    rating_by_seller = filtered.groupby('seller')['avg_review'].mean().sort_values(ascending=False).reset_index()
    fig4 = px.bar(
        rating_by_seller, x='seller', y='avg_review',
        color='avg_review',
        color_continuous_scale=[[0, '#ff6b35'], [0.5, '#ffcc00'], [1, '#00e5a0']],
        labels={'avg_review': 'Avg Rating', 'seller': 'Seller'},
    )
    fig4.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='#f0f0f0', showlegend=False,
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=10, b=0),
        yaxis=dict(gridcolor='#2a2a2a', range=[0, 5.5]),
        xaxis=dict(gridcolor='#2a2a2a'),
    )
    st.plotly_chart(fig4, use_container_width=True)

# ── Best deals table ──────────────────────────────────────────────────────────
st.markdown('<p class="section-title">Best deals — highest discount with top ratings</p>', unsafe_allow_html=True)
best_deals = (
    filtered[filtered['avg_review'] >= 4.5]
    .sort_values('_discount_pct', ascending=False)
    .head(10)[['name', 'seller', 'old_price', 'new_price', '_discount_pct', 'avg_review']]
    .rename(columns={
        'name': 'Product',
        'seller': 'Seller',
        'old_price': 'Old Price (R$)',
        'new_price': 'New Price (R$)',
        '_discount_pct': 'Discount (%)',
        'avg_review': 'Rating',
    })
)
st.dataframe(best_deals, use_container_width=True, hide_index=True)
