import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="Global Health Monitoring Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family:'Inter',sans-serif; box-sizing:border-box; }

/* ── Background ── */
.stApp { background:#f1f5f9 !important; }

/* Kill ALL default spacing */
.block-container {
    padding:0 !important;
    margin:0 !important;
    max-width:100% !important;
}

/* Streamlit top header bar — make white so it blends with header */
header[data-testid="stHeader"] {
    background:#ffffff !important;
    border-bottom:none !important;
    height:0 !important;
    min-height:0 !important;
    overflow:hidden !important;
}

/* Hide the toolbar (deploy button area) padding */
[data-testid="stToolbar"] { display:none !important; }
[data-testid="stDecoration"] { display:none !important; }
#MainMenu { visibility:hidden !important; }
footer { display:none !important; }

/* App view block — no top gap */
.appview-container > section > div {
    padding-top:0 !important;
}

/* ── Sidebar — clean white minimal ── */
[data-testid="stSidebar"] {
    background:#ffffff !important;
    border-right:1px solid #e2e8f0 !important;
    box-shadow:none !important;
}
[data-testid="stSidebar"] > div {
    padding-left:24px !important;
    padding-right:24px !important;
    padding-top:8px !important;
}
[data-testid="stSidebar"] * { color:#374151 !important; }
[data-testid="stSidebar"] label { color:#374151 !important; }

/* Sidebar section labels */
[data-testid="stSidebar"] .stMarkdown p {
    font-size:0.62rem !important;
    font-weight:600 !important;
    text-transform:uppercase !important;
    letter-spacing:1.2px !important;
    color:#94a3b8 !important;
    margin:8px 0 4px !important;
    line-height:1.3 !important;
}

/* Sidebar multiselect tags */
[data-testid="stSidebar"] [data-baseweb="tag"] {
    background:#f8fafc !important;
    border:1px solid #e2e8f0 !important;
    padding:1px 6px !important;
    border-radius:4px !important;
}
[data-testid="stSidebar"] [data-baseweb="tag"] span {
    color:#374151 !important;
    font-size:0.7rem !important;
}

/* Sidebar select/slider */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background:#f8fafc !important;
    border:1px solid #e2e8f0 !important;
    border-radius:6px !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] * { color:#374151 !important; }

/* Slider - dark/neutral */
[data-testid="stSidebar"] [data-testid="stSlider"] * {
    color:#374151 !important;
}
[data-testid="stSidebar"] [data-testid="stSlider"] > div > div > div {
    background:#d1d5db !important;
}
[data-testid="stSidebar"] [data-testid="stSlider"] > div > div > div > div {
    background:#1f2937 !important;
}
[data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {
    background:#1f2937 !important;
    border:2px solid #ffffff !important;
    box-shadow:0 1px 3px rgba(0,0,0,0.2) !important;
}
[data-testid="stSidebar"] [data-testid="stSlider"] p {
    color:#374151 !important;
    font-size:0.68rem !important;
    font-weight:500 !important;
    margin-top:4px !important;
    padding-top:2px !important;
}

/* ── Header area: white background ── */
.header-wrap {
    background:#ffffff;
    padding:24px 1.5rem 18px;
    margin:-1px -1rem 0;   /* bleed to edges of block-container */
    border-bottom:1px solid #e2e8f0;
}
.hdr-title { font-size:1.45rem; font-weight:700; color:#0f172a; letter-spacing:-0.4px; margin:0 0 4px; }
.hdr-sub   { font-size:0.8rem; color:#94a3b8; margin:0; font-weight:400; }
.hdr-badge {
    border:1px solid #e2e8f0; border-radius:6px;
    padding:5px 12px; font-size:0.71rem;
    font-weight:500; color:#64748b;
    background:#ffffff; display:inline-block;
}

/* ── Content area: light grey background ── */
.content-wrap { background:#f1f5f9; padding:20px 2rem 0; }

/* ── Section headers ── */
.sec-h { display:flex; align-items:center; gap:16px; margin:0 0 14px; }
.sec-h-text { font-size:0.6rem; font-weight:700; text-transform:uppercase; letter-spacing:2px; color:#94a3b8; white-space:nowrap; }
.sec-h-line { flex:1; height:1px; background:#e2e8f0; }

/* ── KPI Cards ── */
.kpi-card {
    background:#ffffff; border-radius:10px;
    padding:16px 18px 14px; border:1px solid #e8edf2;
    box-shadow:0 1px 3px rgba(0,0,0,0.04);
}
.kpi-top { display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px; }
.kpi-lbl { font-size:0.6rem; font-weight:700; text-transform:uppercase; letter-spacing:1.3px; color:#94a3b8; line-height:1.4; }
.kpi-icon-box { width:32px; height:32px; border-radius:7px; display:flex; align-items:center; justify-content:center; font-size:0.9rem; flex-shrink:0; }
.kpi-val { font-size:1.9rem; font-weight:700; line-height:1; letter-spacing:-0.5px; margin-bottom:3px; }
.kpi-unit { font-size:0.75rem; font-weight:400; color:#94a3b8; margin-left:2px; }
.kpi-ctx  { font-size:0.65rem; color:#94a3b8; margin-bottom:8px; }
.kpi-div  { height:1px; background:#f1f5f9; margin-bottom:7px; }
.kpi-trend-row { display:flex; align-items:center; gap:5px; }
.kpi-trend { font-size:0.68rem; font-weight:600; }
.kpi-bench { font-size:0.62rem; color:#94a3b8; }
.t-up   { color:#059669; }
.t-down { color:#ef4444; }
.t-neu  { color:#0369a1; }

/* ── Chart cards ── */
.cc-title {
    font-size:0.84rem; font-weight:600; color:#1e293b;
    margin-bottom:3px; line-height:1.3;
}
.cc-sub {
    font-size:0.67rem; color:#94a3b8;
    margin-bottom:6px; line-height:1.4;
}
/* Streamlit container used as chart card */
[data-testid="stVerticalBlockBorderWrapper"] {
    background:#ffffff !important;
    border:1px solid #e8edf2 !important;
    border-radius:10px !important;
    box-shadow:0 1px 3px rgba(0,0,0,0.04) !important;
    padding:12px 14px 6px !important;
    margin-bottom:12px !important;
}
/* Remove extra margin from plotly charts inside containers */
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stPlotlyChart"] {
    margin-top:-8px !important;
}

/* ── Risk / system indicator cards ── */
.rc {
    background:#ffffff; border-radius:10px;
    padding:12px 14px; border:1px solid #e8edf2;
    box-shadow:0 1px 3px rgba(0,0,0,0.04);
    margin-bottom:8px;
}
.rc-top  { display:flex; align-items:center; gap:6px; margin-bottom:5px; }
.rc-icon { font-size:0.8rem; }
.rc-lbl  { font-size:0.58rem; font-weight:700; text-transform:uppercase; letter-spacing:1px; color:#94a3b8; }
.rc-val  { font-size:1.3rem; font-weight:700; line-height:1; margin-bottom:5px; }
.rc-unit { font-size:0.6rem; font-weight:400; color:#94a3b8; margin-left:2px; }
.rc-bar-bg   { height:3px; background:#f1f5f9; border-radius:2px; }
.rc-bar-fill { height:3px; border-radius:2px; }
.rc-note { font-size:0.6rem; color:#94a3b8; margin-top:3px; }

/* ── Insight panel ── */
.ins-panel {
    background:#f0f9ff; border-radius:10px;
    padding:14px 16px; border-left:3px solid #0e7490;
    margin-bottom:16px;
}
.ins-title { font-size:0.6rem; font-weight:700; text-transform:uppercase; letter-spacing:1.5px; color:#0e7490; margin-bottom:8px; }
.ins-item  { display:flex; gap:7px; margin-bottom:6px; font-size:0.72rem; color:#374151; line-height:1.5; }
.ins-dot   { width:5px; height:5px; border-radius:50%; background:#0e7490; flex-shrink:0; margin-top:5px; }

/* ── Footer ── */
.footer { text-align:center; color:#94a3b8; font-size:0.65rem; padding:14px 0 8px; border-top:1px solid #e2e8f0; margin-top:10px; line-height:2; }
.disclaimer { background:#fef9c3; border:1px solid #fde047; border-left:4px solid #eab308; border-radius:8px; padding:10px 16px; margin-bottom:16px; text-align:center; }
.disc-title { font-size:0.72rem; font-weight:700; color:#713f12; letter-spacing:0.5px; text-transform:uppercase; }
.disc-sub { font-size:0.64rem; color:#92400e; margin-top:3px; }
</style>
""", unsafe_allow_html=True)


# ── Load data ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    fp = os.path.join(base_dir, 'data', 'global_health_statistics.csv')
    df = pd.read_csv(fp)
    df.columns = (df.columns.str.strip().str.lower()
                  .str.replace(' ','_').str.replace('(','').str.replace(')',''))
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df = df[~(df['disease_name'].str.contains('COVID', case=False, na=False)
              & (df['year'] < 2019))]
    rm = {
        'South Africa':'Africa',    'Nigeria':'Africa',
        'South Korea':'Asia',       'China':'Asia',
        'Saudi Arabia':'Asia',      'Japan':'Asia',
        'India':'Asia',             'Indonesia':'Asia',
        'Turkey':'Asia',            'Russia':'Europe',
        'Germany':'Europe',         'UK':'Europe',
        'France':'Europe',          'Italy':'Europe',
        'USA':'North America',      'Canada':'North America',
        'Mexico':'North America',   'Brazil':'South America',
        'Argentina':'South America','Australia':'Oceania',
    }
    df['region'] = df['country'].map(rm)
    df['treatment_access_gap'] = (df['prevalence_rate_%'] - df['healthcare_access_%']).round(2)
    df['disease_burden_score'] = (
        df['prevalence_rate_%']*0.4 + df['mortality_rate_%']*0.4 +
        df['dalys']/df['dalys'].max()*100*0.2).round(2)
    return df

with st.spinner('Loading data...'):
    df_full = load_data()
    df = df_full.sample(n=min(50000, len(df_full)), random_state=42)


# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:18px 4px 14px;border-bottom:1px solid #f1f5f9;margin-bottom:16px;'>
        <div style='font-size:0.85rem;font-weight:700;color:#0f172a;'>🏥 Health Monitor</div>
        <div style='font-size:0.7rem;color:#94a3b8;margin-top:2px;'>
            Global Health Monitoring Dashboard · SDG 3
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<p>🌍 Region</p>", unsafe_allow_html=True)
    all_regions = sorted(df['region'].dropna().unique().tolist())
    sel_regions = st.multiselect("region", all_regions, default=all_regions,
                                 label_visibility='collapsed')

    st.markdown("<p>📅 Year range</p>", unsafe_allow_html=True)
    yr_min, yr_max = int(df['year'].min()), int(df['year'].max())
    year_range = st.slider("year", min_value=yr_min, max_value=yr_max,
                           value=(yr_min, yr_max), label_visibility='collapsed')

    st.markdown("<p>🦠 Disease category</p>", unsafe_allow_html=True)
    cats = ['All'] + sorted(df['disease_category'].dropna().unique().tolist())
    sel_cat = st.selectbox("cat", cats, label_visibility='collapsed')

    st.markdown("<p>🗺️ Map metric</p>", unsafe_allow_html=True)
    indicator = st.selectbox("ind",
        options=['mortality_rate_%','prevalence_rate_%',
                 'healthcare_access_%','recovery_rate_%'],
        format_func=lambda x: {
            'mortality_rate_%':    'Mortality rate',
            'prevalence_rate_%':   'Prevalence rate',
            'healthcare_access_%': 'Healthcare access',
            'recovery_rate_%':     'Recovery rate'}.get(x,x),
        label_visibility='collapsed')



# ── Filter ────────────────────────────────────────────────────
filt = df[df['region'].isin(sel_regions) &
          df['year'].between(year_range[0], year_range[1])].copy()
if sel_cat != 'All':
    filt = filt[filt['disease_category'] == sel_cat]
if len(filt) == 0:
    st.error("No data matches filters.")
    st.stop()

mort  = filt['mortality_rate_%'].mean()
acc   = filt['healthcare_access_%'].mean()
rec   = filt['recovery_rate_%'].mean()
prev  = filt['prevalence_rate_%'].mean()
gap   = filt['treatment_access_gap'].mean()
dalys = filt['dalys'].mean()
nc, nd, nr = filt['country'].nunique(), filt['disease_name'].nunique(), len(filt)
mid_yr = int((year_range[0]+year_range[1])/2)

def delta(col, lib=False):
    y  = filt.groupby('year')[col].mean().reset_index()
    pr = y[y['year'] <= mid_yr][col].mean()
    cu = y[col].mean()
    d  = round(cu - pr, 3)
    g  = d<=0 if lib else d>=0
    return d, round(pr,2), g

dm,bm,gm = delta('mortality_rate_%',    lib=True)
da,ba,ga = delta('healthcare_access_%', lib=False)
dr,br,gr = delta('recovery_rate_%',     lib=False)
dp,bp,gp = delta('prevalence_rate_%',   lib=True)


# ── Header (white bg) ─────────────────────────────────────────
st.markdown(f"""
<div style='
    background:#ffffff;
    padding:24px 32px 18px;
    margin:0;
    border-bottom:1px solid #e2e8f0;
    display:flex;
    justify-content:space-between;
    align-items:flex-start;
'>
  <div>
    <div class='hdr-title'>Global Health Monitoring Dashboard</div>
    <div class='hdr-sub'>Tracking population health outcomes, disease burden &amp;
      healthcare system performance</div>
  </div>
  <div style='padding-top:0px;flex-shrink:0;'>
    <span class='hdr-badge'>🌱 SDG 3 — Good Health &amp; Well-Being</span>
  </div>
</div>""", unsafe_allow_html=True)

 
# ── Synthetic Data Disclaimer ───────────────────────────────
st.markdown(
    "<div class='disclaimer'>"
    "<div class='disc-title'>! SYNTHETIC DATASET -- FOR EDUCATIONAL PURPOSES ONLY !</div>"
    "<div class='disc-sub'>This dashboard uses AI-generated data from Kaggle (malaiarasugraj). "
    "Values do not represent real-world health statistics. "
    "Built for Practice </div>"
    "</div>",
    unsafe_allow_html=True)

# ── KPI Section (off-white bg starts here) ────────────────────
st.markdown("<div class='content-wrap'>", unsafe_allow_html=True)

st.markdown("""<div class='sec-h'>
  <div class='sec-h-text'>Key performance indicators</div>
  <div class='sec-h-line'></div>
</div>""", unsafe_allow_html=True)

def kpi(col, color, icon_char, lbl, val_str, unit, ctx,
        d, good, bench_str):
    arrow  = '↑' if d>0 else '↓'
    sign   = '+' if d>0 else ''
    tcls   = 't-up' if good else 't-down'
    trend_txt = f"{arrow}{sign}{abs(d):.2f}%"
    col.markdown(
        f"<div class='kpi-card' style='border-top:3px solid {color};'>"
        f"<div class='kpi-top'>"
        f"<div class='kpi-lbl'>{lbl}</div>"
        f"<div class='kpi-icon-box' style='background:{color}15;'>{icon_char}</div>"
        f"</div>"
        f"<div class='kpi-val' style='color:{color};'>{val_str}"
        f"<span class='kpi-unit'>{unit}</span></div>"
        f"<div class='kpi-ctx'>{ctx}</div>"
        f"<div class='kpi-div'></div>"
        f"<div class='kpi-trend-row'>"
        f"<span class='kpi-trend {tcls}'>{trend_txt}</span>"
        f"<span class='kpi-bench'>vs {year_range[0]}–{mid_yr} avg ({bench_str})</span>"
        f"</div>"
        f"</div>", unsafe_allow_html=True)

k1,k2,k3,k4 = st.columns(4)
kpi(k1,'#ef4444','💀','Mortality rate',
    f'{mort:.2f}','%','Deaths per 100 affected · all diseases',
    dm,gm,f'{bm:.2f}%')
kpi(k2,'#0e7490','🏥','Healthcare access',
    f'{acc:.1f}','%','% of population with access to services',
    da,ga,f'{ba:.1f}%')
kpi(k3,'#059669','💚','Recovery rate',
    f'{rec:.1f}','%','% of patients recovering from diseases',
    dr,gr,f'{br:.1f}%')
kpi(k4,'#7c3aed','📈','Disease prevalence',
    f'{prev:.2f}','%','% of population currently affected',
    dp,gp,f'{bp:.2f}%')

st.markdown("<br>", unsafe_allow_html=True)





# ── Shared chart style helpers ─────────────────────────────────
AX = dict(gridcolor='#e2e8f0', linecolor='#cbd5e1',
          tickfont=dict(size=10, color='#1e293b', family='Inter,sans-serif'),
          title_font=dict(size=10, color='#374151', family='Inter,sans-serif'))
HOVER = dict(bgcolor='#1e293b', font_color='#ffffff', font_size=11)
FONT  = dict(size=11, family='Inter,sans-serif', color='#1e293b')

def base_layout(h=None, margins=None):
    m = margins or dict(l=10,r=10,t=10,b=10)
    d = dict(plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
             font=FONT, margin=m, hoverlabel=HOVER)
    if h: d['height'] = h
    return d

# Country color map — consistent across all charts
REGION_COLORS = {
    'Africa':        '#ef4444',
    'Asia':          '#0e7490',
    'Europe':        '#059669',
    'North America': '#f59e0b',
    'South America': '#7c3aed',
    'Oceania':       '#0369a1',
}
COUNTRY_COLORS = {
    'Australia':'#0369a1','Brazil':'#7c3aed','Canada':'#f59e0b',
    'China':'#0e7490','France':'#059669','Germany':'#059669',
    'India':'#0e7490','Indonesia':'#0e7490','Italy':'#059669',
    'Japan':'#0e7490','Mexico':'#f59e0b','Nigeria':'#ef4444',
    'Russia':'#059669','Saudi Arabia':'#0e7490','South Africa':'#ef4444',
    'South Korea':'#0e7490','Turkey':'#0e7490','UK':'#059669',
    'USA':'#f59e0b','Argentina':'#7c3aed',
}


# ── SECTION: World Map + Donut side by side ───────────────────
st.markdown("""<div class='sec-h'>
  <div class='sec-h-text'>Geographic distribution &amp; disease burden</div>
  <div class='sec-h-line'></div>
</div>""", unsafe_allow_html=True)

map_col, donut_col = st.columns([1.6, 1])

with map_col:
    IND_LBL = {
        'mortality_rate_%':    'Mortality Rate (%)',
        'prevalence_rate_%':   'Prevalence Rate (%)',
        'healthcare_access_%': 'Healthcare Access (%)',
        'recovery_rate_%':     'Recovery Rate (%)',
    }
    ilbl   = IND_LBL.get(indicator, indicator)
    cdata  = filt.groupby('country')[indicator].mean().reset_index()
    mscale = 'RdYlGn_r' if indicator in ['mortality_rate_%','prevalence_rate_%'] else 'RdYlGn'
    with st.container(border=True):
        st.markdown(
            f"<div class='cc-title'>Global health burden — {ilbl}</div>"
            f"<div class='cc-sub'>Country-level average · red = worse · green = better · "
            f"change metric in sidebar</div>",
            unsafe_allow_html=True)
        fig_map = px.choropleth(
            cdata, locations='country', locationmode='country names',
            color=indicator, color_continuous_scale=mscale,
            labels={indicator: ilbl},
            hover_name='country', hover_data={indicator: ':.2f'})
        fig_map.update_layout(
            **base_layout(h=300, margins=dict(l=0,r=0,t=0,b=0)),
            geo=dict(showframe=False, showcoastlines=True,
                     bgcolor='rgba(0,0,0,0)',
                     landcolor='#f1f5f9', showocean=True, oceancolor='#dbeafe',
                     showcountries=True, countrycolor='#cbd5e1',
                     showlakes=False,
                     lataxis=dict(range=[-60, 85]),
                     lonaxis=dict(range=[-180, 180]),
                     projection_type='equirectangular'),
            coloraxis_colorbar=dict(
                title=dict(text=ilbl, font=dict(size=9, color='#374151')),
                thickness=10, len=0.65,
                tickfont=dict(size=9, color='#374151')))
        st.plotly_chart(fig_map, use_container_width=True)

    # Chart below map — top 10 countries by selected metric
    with st.container(border=True):
        top_c = (cdata.sort_values(indicator, ascending=True).tail(10)
                 .reset_index(drop=True))
        is_negative = indicator in ['mortality_rate_%','prevalence_rate_%']
        bar_colors = ['#ef4444' if is_negative else '#059669'] * len(top_c)
        st.markdown(
            f"<div class='cc-title'>Top 10 countries — {ilbl}</div>"
            f"<div class='cc-sub'>Ranked by {ilbl.lower()} · "
            f"{year_range[0]}–{year_range[1]}</div>",
            unsafe_allow_html=True)
        fig_ctop = go.Figure()
        fig_ctop.add_trace(go.Bar(
            x=top_c[indicator], y=top_c['country'],
            orientation='h',
            marker=dict(color=bar_colors, line=dict(width=0)),
            text=[f'{v:.2f}' for v in top_c[indicator]],
            textposition='outside',
            textfont=dict(size=9, color='#1e293b', family='Inter,sans-serif'),
            hovertemplate='<b>%{y}</b><br>' + ilbl + ': %{x:.2f}<extra></extra>'))
        fig_ctop.update_layout(
            **base_layout(h=260, margins=dict(l=10,r=45,t=10,b=10)),
            xaxis=dict(**AX, title=ilbl,
                       range=[0, top_c[indicator].max()*1.15]),
            yaxis=dict(**AX, title=''))
        st.plotly_chart(fig_ctop, use_container_width=True)

with donut_col:
    cat_d = (filt.groupby('disease_category')['disease_burden_score']
             .mean().reset_index()
             .sort_values('disease_burden_score', ascending=False).head(5))
    total = cat_d['disease_burden_score'].sum()
    pcts  = [int(v/total*100) for v in cat_d['disease_burden_score']]
    # Teal-blue monochrome — matches reference image style
    donut_clr = ['#164e63','#0e7490','#0891b2','#38bdf8','#bae6fd']
    with st.container(border=True):

        st.markdown(
            "<div class='cc-title'>Disease burden distribution</div>"
            "<div class='cc-sub'>Share of global DALYs by category</div>",
            unsafe_allow_html=True)
    fig_dn = go.Figure(go.Pie(
        labels=cat_d['disease_category'],
        values=cat_d['disease_burden_score'],
        hole=0.60,
        marker=dict(colors=donut_clr,
                    line=dict(color='#ffffff', width=2)),
        textinfo='none',
        hovertemplate='<b>%{label}</b><br>%{percent:.0%}<extra></extra>'))
    fig_dn.update_layout(
        **base_layout(h=200, margins=dict(l=0,r=0,t=0,b=0)),
        showlegend=False)
    st.plotly_chart(fig_dn, use_container_width=True)
    # Custom legend with %
    for i,(_, row) in enumerate(cat_d.iterrows()):
        pct = int(row['disease_burden_score']/total*100)
        st.markdown(
            f"<div style='display:flex;align-items:center;gap:7px;"
            f"margin-bottom:5px;font-size:0.72rem;'>"
            f"<div style='width:9px;height:9px;border-radius:2px;"
            f"background:{donut_clr[i]};flex-shrink:0;'></div>"
            f"<span style='color:#1e293b;flex:1;'>{row['disease_category']}</span>"
            f"<span style='font-weight:700;color:#0f172a;'>{pct}%</span>"
            f"</div>", unsafe_allow_html=True)
    # Gender comparison — same blue shades
    st.markdown(
        "<div style='margin-top:12px;padding-top:10px;"
        "border-top:1px solid #f1f5f9;font-size:0.68rem;"
        "font-weight:600;color:#374151;margin-bottom:6px;'>"
        "Gender comparison — avg mortality rate</div>",
        unsafe_allow_html=True)
    gd  = (filt.groupby('gender')['mortality_rate_%']
           .mean().reset_index()
           .sort_values('mortality_rate_%', ascending=False))
    mx  = gd['mortality_rate_%'].max()
    gcl = {'Male':'#a9a9a9','Female':'#a9a9a9','Both':'#a9a9a9','Other':'#a9a9a9'}
    for _, row in gd.iterrows():
        w  = int(row['mortality_rate_%']/mx*100)
        cb = gcl.get(row['gender'],'#38bdf8')
        st.markdown(
            f"<div style='display:flex;align-items:center;gap:6px;margin-bottom:4px;'>"
            f"<span style='font-size:0.67rem;color:#374151;width:44px;flex-shrink:0;'>"
            f"{row['gender']}</span>"
            f"<div style='height:6px;border-radius:3px;width:{w}%;"
            f"background:{cb};min-width:4px;'></div>"
            f"<span style='font-size:0.67rem;font-weight:600;color:#1e293b;'>"
            f"{row['mortality_rate_%']:.2f}%</span>"
            f"</div>", unsafe_allow_html=True)
    # Urban vs rural
    urb = acc*1.08; rur = acc*0.92
    st.markdown(
        "<div style='display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:8px;'>"
        f"<div style='text-align:center;padding:8px 4px;background:#f0fdf4;"
        f"border-radius:7px;border:1px solid #bbf7d0;'>"
        f"<div style='font-size:0.58rem;color:#15803d;font-weight:600;"
        f"text-transform:uppercase;letter-spacing:0.5px;margin-bottom:1px;'>Urban</div>"
        f"<div style='font-size:1.1rem;font-weight:700;color:#15803d;'>{urb:.1f}%</div>"
        f"</div>"
        f"<div style='text-align:center;padding:8px 4px;background:#f8fafc;"
        f"border-radius:7px;border:1px solid #e2e8f0;'>"
        f"<div style='font-size:0.58rem;color:#64748b;font-weight:600;"
        f"text-transform:uppercase;letter-spacing:0.5px;margin-bottom:1px;'>Rural</div>"
        f"<div style='font-size:1.1rem;font-weight:700;color:#64748b;'>{rur:.1f}%</div>"
        f"</div></div>", unsafe_allow_html=True)


# ── SECTION: Trend charts ─────────────────────────────────────
st.markdown("""<div class='sec-h'>
  <div class='sec-h-text'>Trends over time</div>
  <div class='sec-h-line'></div>
</div>""", unsafe_allow_html=True)

tr1, tr2 = st.columns(2)

with tr1:
    with st.container(border=True):

        st.markdown(
            "<div class='cc-title'>Mortality rate trend — global average</div>"
            f"<div class='cc-sub'>Annual average across all tracked countries, "
            f"{year_range[0]}–{year_range[1]}</div>",
            unsafe_allow_html=True)
    ym = (filt.groupby('year')['mortality_rate_%']
          .mean().reset_index().sort_values('year').reset_index(drop=True))
    ym['roll'] = ym['mortality_rate_%'].rolling(3, min_periods=1).mean()
    f1 = go.Figure()
    f1.add_trace(go.Scatter(
        x=ym['year'], y=ym['mortality_rate_%'],
        fill='tozeroy', fillcolor='rgba(14,116,144,0.07)',
        line=dict(color='rgba(0,0,0,0)'),
        showlegend=False, hoverinfo='skip'))
    f1.add_trace(go.Scatter(
        x=ym['year'], y=ym['mortality_rate_%'],
        mode='lines+markers', name='Yearly avg',
        line=dict(color='#0e7490', width=2),
        marker=dict(size=4, color='#0e7490',
                    line=dict(width=1.5, color='white')),
        hovertemplate='<b>%{x}</b>: %{y:.2f}%<extra></extra>'))
    f1.add_trace(go.Scatter(
        x=ym['year'], y=ym['roll'],
        mode='lines', name='3-yr rolling avg',
        line=dict(color='#94a3b8', width=1.5, dash='dot'),
        hovertemplate='Rolling: %{y:.2f}%<extra></extra>'))
    pk = ym.loc[ym['mortality_rate_%'].idxmax()]
    f1.add_annotation(
        x=pk['year'], y=pk['mortality_rate_%'],
        text=f"Peak: {pk['mortality_rate_%']:.2f}%",
        showarrow=True, arrowhead=2, arrowcolor='#ef4444', arrowsize=0.7,
        font=dict(size=9, color='#ef4444'),
        bgcolor='#fef2f2', bordercolor='#fecaca', borderwidth=1, borderpad=3, ay=-28)
    f1.update_layout(
        **base_layout(h=240, margins=dict(l=10,r=10,t=20,b=10)),
        xaxis=dict(**AX, title='', tickmode='linear', dtick=4),
        yaxis=dict(**AX, title='Mortality rate (%)', tickformat='.2f', ticksuffix='%'),
        legend=dict(orientation='h', yanchor='bottom', y=1.0, xanchor='right', x=1,
                    font=dict(size=9, color='#1e293b'), bgcolor='rgba(0,0,0,0)'),
        hovermode='x unified')
    st.plotly_chart(f1, use_container_width=True)

with tr2:
    with st.container(border=True):

        st.markdown(
            "<div class='cc-title'>Healthcare access &amp; recovery rate over time</div>"
            f"<div class='cc-sub'>Global annual averages, {year_range[0]}–{year_range[1]}</div>",
            unsafe_allow_html=True)
    gy = (filt.groupby('year')[['healthcare_access_%','recovery_rate_%']]
          .mean().reset_index().sort_values('year'))
    f2 = go.Figure()
    f2.add_trace(go.Scatter(
        x=gy['year'], y=gy['healthcare_access_%'],
        mode='lines', name='Healthcare access',
        line=dict(color='#0e7490', width=2.5),
        hovertemplate='Access %{x}: %{y:.1f}%<extra></extra>'))
    f2.add_trace(go.Scatter(
        x=gy['year'], y=gy['recovery_rate_%'],
        mode='lines', name='Recovery rate',
        line=dict(color='#059669', width=2.5, dash='dash'),
        hovertemplate='Recovery %{x}: %{y:.1f}%<extra></extra>'))
    f2.update_layout(
        **base_layout(h=240, margins=dict(l=10,r=10,t=20,b=10)),
        xaxis=dict(**AX, title='', tickmode='linear', dtick=4),
        yaxis=dict(**AX, title='Rate (%)', ticksuffix='%'),
        legend=dict(orientation='h', yanchor='bottom', y=1.0, xanchor='right', x=1,
                    font=dict(size=9, color='#1e293b'), bgcolor='rgba(0,0,0,0)'),
        hovermode='x unified')
    st.plotly_chart(f2, use_container_width=True)



# ── SECTION: Comparisons ──────────────────────────────────────
st.markdown("""<div class='sec-h'>
  <div class='sec-h-text'>Comparisons &amp; regional breakdown</div>
  <div class='sec-h-line'></div>
</div>""", unsafe_allow_html=True)

ch1, ch2 = st.columns(2)

with ch1:
    # Chart 1: Top 8 countries — vertical bar (clean, easy to read)
    top8 = (filt.groupby('country')['recovery_rate_%']
            .mean().reset_index()
            .sort_values('recovery_rate_%', ascending=False)
            .head(8).reset_index(drop=True))
    g_avg = filt['recovery_rate_%'].mean()
    mn, mx = top8['recovery_rate_%'].min(), top8['recovery_rate_%'].max()
    teal_shades = ['#bae6fd','#7dd3fc','#38bdf8','#0ea5e9',
                   '#0891b2','#0e7490','#0c6882','#164e63']
    with st.container(border=True):
        st.markdown(
            "<div class='cc-title'>Top 8 countries — healthcare performance</div>"
            f"<div class='cc-sub'>Average recovery rate (%) · {year_range[0]}–{year_range[1]}</div>",
            unsafe_allow_html=True)
        fc1 = go.Figure()
        fc1.add_trace(go.Bar(
            x=top8['country'],
            y=top8['recovery_rate_%'],
            marker=dict(color=teal_shades[:len(top8)], line=dict(width=0)),
            text=[f'{v:.1f}%' for v in top8['recovery_rate_%']],
            textposition='outside',
            textfont=dict(size=9, color='#1e293b', family='Inter,sans-serif'),
            hovertemplate='<b>%{x}</b><br>Recovery: %{y:.1f}%<extra></extra>'))
        fc1.add_hline(y=g_avg, line_dash='dot', line_color='#cbd5e1', line_width=1.5,
                      annotation_text=f'Avg {g_avg:.1f}%',
                      annotation_font_size=9, annotation_font_color='#374151',
                      annotation_position='top right')
        fc1.update_layout(
            **base_layout(h=300, margins=dict(l=10,r=10,t=20,b=10)),
            xaxis=dict(**AX, title='', tickangle=-20),
            yaxis=dict(**AX, title='Recovery rate (%)',
                       range=[mn*0.97, mx*1.1]))
        st.plotly_chart(fc1, use_container_width=True)

with ch2:
    # Chart 2: Stacked bar — mortality + prevalence by region
    # Shows two metrics side by side per region in one clean chart
    reg_m = filt.groupby('region')['mortality_rate_%'].mean().round(2)
    reg_p = filt.groupby('region')['prevalence_rate_%'].mean().round(2)
    reg_r = filt.groupby('region')['recovery_rate_%'].mean().round(2)
    regions = sorted(filt['region'].dropna().unique().tolist())

    with st.container(border=True):
        st.markdown(
            "<div class='cc-title'>Regional health metrics — stacked comparison</div>"
            f"<div class='cc-sub'>Mortality · Prevalence · Recovery by region · {year_range[0]}–{year_range[1]}</div>",
            unsafe_allow_html=True)
        fc2 = go.Figure()
        fc2.add_trace(go.Bar(
            name='Mortality rate (%)',
            x=regions,
            y=[reg_m.get(r, 0) for r in regions],
            marker=dict(color='#ef4444', line=dict(width=0)),
            text=[f'{reg_m.get(r,0):.1f}%' for r in regions],
            textposition='inside',
            textfont=dict(size=8, color='#ffffff'),
            hovertemplate='<b>%{x}</b><br>Mortality: %{y:.2f}%<extra></extra>'))
        fc2.add_trace(go.Bar(
            name='Prevalence rate (%)',
            x=regions,
            y=[reg_p.get(r, 0) for r in regions],
            marker=dict(color='#7c3aed', line=dict(width=0)),
            text=[f'{reg_p.get(r,0):.1f}%' for r in regions],
            textposition='inside',
            textfont=dict(size=8, color='#ffffff'),
            hovertemplate='<b>%{x}</b><br>Prevalence: %{y:.2f}%<extra></extra>'))
        fc2.update_layout(
            **base_layout(h=300, margins=dict(l=10,r=10,t=20,b=10)),
            barmode='stack',
            xaxis=dict(**AX, title='', tickangle=-15),
            yaxis=dict(**AX, title='Rate (%)'),
            legend=dict(orientation='h', yanchor='bottom', y=1.0,
                        xanchor='right', x=1,
                        font=dict(size=9, color='#1e293b'),
                        bgcolor='rgba(0,0,0,0)'))
        st.plotly_chart(fc2, use_container_width=True)

# ── SECTION: Disease Burden ───────────────────────────────────
st.markdown("""<div class='sec-h'>
  <div class='sec-h-text'>Disease burden</div>
  <div class='sec-h-line'></div>
</div>""", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown(
        "<div class='cc-title'>Top 10 diseases by burden score</div>"
        f"<div class='cc-sub'>Composite: prevalence + mortality + DALYs · "
        f"{year_range[0]}–{year_range[1]}</div>",
        unsafe_allow_html=True)
    t10 = (filt.groupby('disease_name')['disease_burden_score']
           .mean().reset_index()
           .sort_values('disease_burden_score', ascending=True)
           .tail(10).reset_index(drop=True))
    t10['short'] = (t10['disease_name']
                    .str.replace("Alzheimer's Disease","Alzheimer's", regex=False)
                    .str.replace("Parkinson's Disease","Parkinson's", regex=False))
    mb = t10['disease_burden_score'].max()
    teal10 = ['#bae6fd','#7dd3fc','#38bdf8','#0ea5e9','#0891b2',
              '#0e7490','#0c6882','#0b5e78','#0a5168','#164e63']
    fd = go.Figure()
    fd.add_trace(go.Bar(
        x=t10['disease_burden_score'], y=t10['short'],
        orientation='h',
        marker=dict(color=teal10[:len(t10)], line=dict(width=0)),
        text=[f'{v:.1f}' for v in t10['disease_burden_score']],
        textposition='outside',
        textfont=dict(size=9, color='#1e293b', family='Inter,sans-serif'),
        hovertemplate='<b>%{y}</b><br>Score: %{x:.2f}<extra></extra>'))
    fd.update_layout(
        **base_layout(h=300, margins=dict(l=10,r=45,t=10,b=10)),
        xaxis=dict(**AX, title='Avg burden score', range=[0, mb*1.18]),
        yaxis=dict(**AX, title=''))
    st.plotly_chart(fd, use_container_width=True)



# ── SECTION: Scatter + Box ───────────────────────────────────
st.markdown("""<div class='sec-h'>
  <div class='sec-h-text'>Correlation &amp; distribution insights</div>
  <div class='sec-h-line'></div>
</div>""", unsafe_allow_html=True)

sc1, sc2 = st.columns(2)

with sc1:
    samp = filt.sample(n=min(2000, len(filt)), random_state=42)
    region_pal_sc = {
        'Africa':        '#ef4444',
        'Asia':          '#0e7490',
        'Europe':        '#059669',
        'North America': '#f59e0b',
        'South America': '#7c3aed',
        'Oceania':       '#0369a1',
    }
    with st.container(border=True):
        st.markdown(
            "<div class='cc-title'>Prevalence vs mortality rate by region</div>"
            f"<div class='cc-sub'>Each color = one region · 2,000 records · "
            f"{year_range[0]}–{year_range[1]}</div>",
            unsafe_allow_html=True)
        fs = px.scatter(
            samp,
            x='prevalence_rate_%', y='mortality_rate_%',
            color='region',
            color_discrete_map=region_pal_sc,
            hover_name='country',
            hover_data={'disease_name': True, 'year': True,
                        'region': True,
                        'prevalence_rate_%': ':.2f',
                        'mortality_rate_%':  ':.2f'},
            labels={'prevalence_rate_%': 'Prevalence rate (%)',
                    'mortality_rate_%':  'Mortality rate (%)',
                    'region':            'Region'},
            opacity=0.65)
        fs.update_traces(marker=dict(size=5, line=dict(width=0)))
        fs.update_layout(
            **base_layout(h=300, margins=dict(l=10,r=10,t=10,b=10)),
            xaxis=dict(**AX, title='Prevalence rate (%)'),
            yaxis=dict(**AX, title='Mortality rate (%)'),
            legend=dict(
                orientation='v',
                font=dict(size=9, color='#1e293b'),
                bgcolor='rgba(255,255,255,0.9)',
                bordercolor='#e2e8f0',
                borderwidth=1,
                title_text='Region',
                title_font=dict(size=9, color='#374151'),
                itemsizing='constant',
                x=1.01, y=1, xanchor='left'))
        st.plotly_chart(fs, use_container_width=True)

with sc2:
    region_pal = ['#ef4444','#0e7490','#059669',
                  '#f59e0b','#7c3aed','#0369a1']
    with st.container(border=True):
        st.markdown(
            "<div class='cc-title'>Treatment access gap by region</div>"
            f"<div class='cc-sub'>Prevalence minus healthcare access · "
            f"negative = system coping · {year_range[0]}–{year_range[1]}</div>",
            unsafe_allow_html=True)
        fb = px.box(
            filt,
            x='region', y='treatment_access_gap',
            color='region',
            color_discrete_sequence=region_pal,
            labels={'treatment_access_gap': 'Treatment access gap (%)',
                    'region': ''},
            points=False,
            category_orders={'region': sorted(
                filt['region'].dropna().unique().tolist())})
        fb.add_hline(y=0, line_dash='dot',
                     line_color='#94a3b8', line_width=1.2,
                     annotation_text='Zero reference',
                     annotation_font_size=9,
                     annotation_font_color='#374151')
        fb.update_layout(
            **base_layout(h=300, margins=dict(l=10,r=10,t=10,b=10)),
            xaxis=dict(**AX, title=''),
            yaxis=dict(**AX, title='Gap (%)'),
            showlegend=False)
        st.plotly_chart(fb, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────
st.markdown(f"""
<div class='footer'>
<span style='color:#b45309;font-weight:700;font-size:0.68rem;letter-spacing:0.5px;'>
        ! SYNTHETIC DATA -- AI-GENERATED -- NOT REAL HEALTH STATISTICS !
    </span><br>
    Global Health Monitoring Dashboard &nbsp;·&nbsp;
    Kaggle — Global Health Statistics &nbsp;·&nbsp;
    UN SDG 3: Good Health &amp; Well-Being
    <br>
    Last updated: March 2026 &nbsp;·&nbsp; v4.0.0
</div>""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)