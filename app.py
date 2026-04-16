

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="DataFill · Interpolation Studio",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS  — dark-teal scientific aesthetic
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root palette ── */
:root {
    --bg:        #0d1117;
    --surface:   #161b22;
    --surface2:  #1c2330;
    --border:    #30363d;
    --teal:      #2dd4bf;
    --teal-dim:  #134e4a;
    --amber:     #fbbf24;
    --rose:      #fb7185;
    --text:      #e6edf3;
    --muted:     #8b949e;
    --radius:    10px;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Header banner ── */
.hero {
    background: linear-gradient(135deg, #0f2027 0%, #1a3a4a 50%, #0d2137 100%);
    border: 1px solid var(--teal-dim);
    border-radius: var(--radius);
    padding: 2.4rem 2.8rem 2rem;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(45,212,191,.18) 0%, transparent 70%);
}
.hero-title {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: var(--teal);
    margin: 0 0 .35rem;
    letter-spacing: -0.5px;
}
.hero-sub {
    color: var(--muted);
    font-size: .95rem;
    font-weight: 300;
    margin: 0;
}
.hero-tag {
    display: inline-block;
    background: var(--teal-dim);
    color: var(--teal);
    font-family: 'Space Mono', monospace;
    font-size: .72rem;
    padding: .25rem .65rem;
    border-radius: 20px;
    margin-top: .8rem;
    border: 1px solid var(--teal);
}

/* ── Stat cards ── */
.stat-row { display: flex; gap: 1rem; margin: 1.2rem 0; flex-wrap: wrap; }
.stat-card {
    flex: 1; min-width: 140px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 1.3rem;
    text-align: center;
}
.stat-card.teal  { border-color: var(--teal);  }
.stat-card.amber { border-color: var(--amber); }
.stat-card.rose  { border-color: var(--rose);  }
.stat-val  { font-family: 'Space Mono', monospace; font-size: 1.9rem; font-weight: 700; }
.teal  .stat-val { color: var(--teal);  }
.amber .stat-val { color: var(--amber); }
.rose  .stat-val { color: var(--rose);  }
.stat-lbl  { color: var(--muted); font-size: .78rem; margin-top: .2rem; }

/* ── Section labels ── */
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: .72rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--teal);
    margin: 1.6rem 0 .6rem;
    padding-bottom: .4rem;
    border-bottom: 1px solid var(--teal-dim);
}

/* ── Pill badge ── */
.badge {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: .7rem;
    padding: .2rem .55rem;
    border-radius: 12px;
    margin: .15rem .1rem;
}
.badge-nan    { background: rgba(251,113,133,.15); color: var(--rose);  border:1px solid rgba(251,113,133,.4); }
.badge-filled { background: rgba(45,212,191,.12);  color: var(--teal);  border:1px solid rgba(45,212,191,.4); }
.badge-method { background: rgba(251,191,36,.12);  color: var(--amber); border:1px solid rgba(251,191,36,.4); }

/* ── Streamlit widget overrides ── */
.stSelectbox > div > div,
.stFileUploader > div {
    background-color: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
}
.stButton > button {
    background: var(--teal) !important;
    color: #000 !important;
    font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: var(--radius) !important;
    padding: .55rem 1.4rem !important;
    transition: opacity .2s;
}
.stButton > button:hover { opacity: .85 !important; }
.stDownloadButton > button {
    background: var(--surface2) !important;
    color: var(--teal) !important;
    border: 1px solid var(--teal) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: .8rem !important;
    border-radius: var(--radius) !important;
}

/* ── Dataframe styling ── */
.stDataFrame { border-radius: var(--radius); overflow: hidden; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Info/warning boxes ── */
.info-box {
    background: rgba(45,212,191,.07);
    border-left: 3px solid var(--teal);
    border-radius: 0 var(--radius) var(--radius) 0;
    padding: .8rem 1rem;
    margin: .8rem 0;
    font-size: .88rem;
}
.warn-box {
    background: rgba(251,191,36,.07);
    border-left: 3px solid var(--amber);
    border-radius: 0 var(--radius) var(--radius) 0;
    padding: .8rem 1rem;
    margin: .8rem 0;
    font-size: .88rem;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def detect_missing(df: pd.DataFrame) -> dict:
    """Return per-column missing value counts."""
    return {col: int(df[col].isna().sum()) for col in df.columns if df[col].isna().any()}


def get_numeric_cols(df: pd.DataFrame) -> list:
    return df.select_dtypes(include=[np.number]).columns.tolist()


def apply_interpolation(series: pd.Series, method: str, order: int = 2) -> pd.Series:
    """
    Apply interpolation to a pandas Series.
    method: 'linear' | 'polynomial'
    """
    if method == "Linear":
        return series.interpolate(method="linear", limit_direction="both")
    elif method == "Polynomial (order=2)":
        return series.interpolate(method="polynomial", order=order, limit_direction="both")
    return series


def style_dataframe(df: pd.DataFrame, filled_mask: pd.DataFrame = None):
    """
    Apply cell-level styling:
    - NaN cells → rose tint
    - filled cells (mask) → teal tint
    """
    def colorize(val, col, row_idx):
        if filled_mask is not None and col in filled_mask.columns:
            if filled_mask.at[row_idx, col]:
                return "background-color: rgba(45,212,191,.18); color: #2dd4bf; font-weight:600;"
        if pd.isna(val):
            return "background-color: rgba(251,113,133,.18); color: #fb7185;"
        return ""

    styled = df.style
    for col in df.columns:
        styled = styled.applymap(
            lambda v, c=col, rows=df.index: colorize(v, c, rows[df.index.get_loc(rows[0])]),
            subset=[col]
        )
    # Simpler approach: use Styler.apply on the whole frame
    def highlight(data):
        styles = pd.DataFrame("", index=data.index, columns=data.columns)
        for col in data.columns:
            for idx in data.index:
                val = data.at[idx, col]
                if filled_mask is not None and col in filled_mask.columns and filled_mask.at[idx, col]:
                    styles.at[idx, col] = "background-color: rgba(45,212,191,.20); color: #2dd4bf; font-weight:600;"
                elif pd.isna(val):
                    styles.at[idx, col] = "background-color: rgba(251,113,133,.20); color: #fb7185;"
        return styles

    return df.style.apply(highlight, axis=None).format(
        lambda x: "NaN" if (isinstance(x, float) and np.isnan(x)) else x
    )


def build_comparison_chart(original: pd.Series, interpolated: pd.Series, col_name: str, method: str):
    """Build a side-by-side Plotly comparison figure."""
    x = list(range(len(original)))
    nan_mask = original.isna()

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("⚠ Before Interpolation", "✅ After Interpolation"),
        horizontal_spacing=0.08,
    )

    # ── Before ──
    fig.add_trace(go.Scatter(
        x=x, y=original,
        mode="lines+markers",
        name="Original",
        line=dict(color="#fb7185", width=2, dash="dot"),
        marker=dict(size=6, color="#fb7185"),
        connectgaps=False,
    ), row=1, col=1)

    # Mark NaN positions
    nan_x = [i for i, m in enumerate(nan_mask) if m]
    fig.add_trace(go.Scatter(
        x=nan_x,
        y=[interpolated.iloc[i] for i in nan_x],
        mode="markers",
        name="Missing",
        marker=dict(size=10, color="#fb7185", symbol="x", line=dict(width=2, color="#fb7185")),
        showlegend=True,
    ), row=1, col=1)

    # ── After ──
    fig.add_trace(go.Scatter(
        x=x, y=interpolated,
        mode="lines+markers",
        name="Interpolated",
        line=dict(color="#2dd4bf", width=2.5),
        marker=dict(size=6, color="#2dd4bf"),
    ), row=1, col=2)

    # Highlight filled points
    fig.add_trace(go.Scatter(
        x=nan_x,
        y=[interpolated.iloc[i] for i in nan_x],
        mode="markers",
        name="Filled",
        marker=dict(size=11, color="#fbbf24", symbol="diamond",
                    line=dict(width=1.5, color="#fbbf24")),
    ), row=1, col=2)

    # Shared layout
    fig.update_layout(
        height=420,
        paper_bgcolor="#0d1117",
        plot_bgcolor="#161b22",
        font=dict(family="DM Sans", color="#8b949e", size=12),
        title=dict(
            text=f"<b>{col_name}</b>  ·  {method} Interpolation",
            font=dict(family="Space Mono", color="#2dd4bf", size=14),
            x=0.5,
        ),
        legend=dict(
            bgcolor="#1c2330",
            bordercolor="#30363d",
            borderwidth=1,
            font=dict(size=11),
        ),
        margin=dict(t=70, b=40, l=50, r=30),
    )
    for row in [1]:
        for col in [1, 2]:
            fig.update_xaxes(
                gridcolor="#21262d", zeroline=False,
                title_text="Index", title_font=dict(size=11),
                row=row, col=col,
            )
            fig.update_yaxes(
                gridcolor="#21262d", zeroline=False,
                title_text=col_name, title_font=dict(size=11),
                row=row, col=col,
            )
    for ann in fig.layout.annotations:
        ann.font.update(family="Space Mono", color="#8b949e", size=12)

    return fig


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="font-family:'Space Mono',monospace; color:#2dd4bf;
                font-size:1.1rem; font-weight:700; margin-bottom:.3rem;">
        ⚙ Controls
    </div>
    <div style="color:#8b949e; font-size:.82rem; margin-bottom:1.2rem;">
        Configure interpolation settings
    </div>
    """, unsafe_allow_html=True)

    interp_method = st.selectbox(
        "Interpolation Method",
        ["Linear", "Polynomial (order=2)"],
        help="Linear: straight-line fill · Polynomial: smooth curved fit (order 2)",
    )

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("""
    <div class='section-label'>ℹ About</div>
    <div style='color:#8b949e; font-size:.8rem; line-height:1.6;'>
    Interpolation estimates missing data points based on surrounding known values.<br><br>
    <b style='color:#e6edf3;'>Linear</b> — connects two known points with a straight line.<br><br>
    <b style='color:#e6edf3;'>Polynomial (n=2)</b> — fits a smooth parabolic curve through surrounding points.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.caption("Numerical Methods · College Project")


# ─────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <p class="hero-title">📈 DataFill</p>
    <p class="hero-sub">Interpolation Studio for Missing Values</p>
    <span class="hero-tag">NUMERICAL METHODS PROJECT</span>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FILE UPLOAD
# ─────────────────────────────────────────────
st.markdown('<div class="section-label">01 · Upload Dataset</div>', unsafe_allow_html=True)
uploaded = st.file_uploader(
    "Drop a CSV file here — missing values should be blank or NaN",
    type=["csv"],
    label_visibility="visible",
)

# ── Sample CSV download ──
sample_data = """Time,Temperature,Pressure,Humidity,Wind_Speed
1,22.1,1013.2,65.0,12.3
2,,1012.8,66.2,
3,23.4,,67.5,11.8
4,24.0,1011.5,,13.1
5,24.8,1010.9,70.0,
6,,1010.2,71.3,14.5
7,25.9,1009.8,,15.2
8,26.1,,73.0,15.8
9,,1009.0,74.1,
10,27.0,1008.5,75.0,17.0
11,27.3,1008.0,,17.5
12,,1007.5,76.8,18.0
13,28.1,1007.0,77.5,
14,28.5,,78.0,19.2
15,29.0,1006.0,79.0,20.0
"""
st.download_button(
    "⬇ Download Sample CSV",
    data=sample_data,
    file_name="sample_weather_data.csv",
    mime="text/csv",
)

# ─────────────────────────────────────────────
# MAIN LOGIC
# ─────────────────────────────────────────────
if uploaded:
    # ── Load data ──
    df_original = pd.read_csv(uploaded)
    numeric_cols = get_numeric_cols(df_original)
    missing_info = detect_missing(df_original)
    total_missing = sum(missing_info.values())
    total_cells   = df_original.shape[0] * df_original.shape[1]

    # ── Stats row ──
    st.markdown('<div class="section-label">02 · Dataset Overview</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card teal">
            <div class="stat-val">{df_original.shape[0]}</div>
            <div class="stat-lbl">Rows</div>
        </div>
        <div class="stat-card teal">
            <div class="stat-val">{df_original.shape[1]}</div>
            <div class="stat-lbl">Columns</div>
        </div>
        <div class="stat-card rose">
            <div class="stat-val">{total_missing}</div>
            <div class="stat-lbl">Missing Values</div>
        </div>
        <div class="stat-card amber">
            <div class="stat-val">{round(total_missing/total_cells*100,1)}%</div>
            <div class="stat-lbl">Missing Rate</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Missing per column badges
    if missing_info:
        badges = " ".join(
            f'<span class="badge badge-nan">⚠ {col}: {cnt} NaN</span>'
            for col, cnt in missing_info.items()
        )
        st.markdown(f"<div style='margin:.4rem 0 1rem;'>{badges}</div>", unsafe_allow_html=True)
    else:
        st.markdown(
            "<div class='info-box'>✅ No missing values found in this dataset.</div>",
            unsafe_allow_html=True,
        )

    # ── Before table ──
    st.markdown('<div class="section-label">03 · Raw Data (Before)</div>', unsafe_allow_html=True)
    st.markdown("<div class='warn-box'>🔴 Cells highlighted in <b style='color:#fb7185;'>rose</b> are missing (NaN).</div>",
                unsafe_allow_html=True)

    def highlight_nan(data):
        styles = pd.DataFrame("", index=data.index, columns=data.columns)
        for col in data.columns:
            for idx in data.index:
                if pd.isna(data.at[idx, col]):
                    styles.at[idx, col] = "background-color:rgba(251,113,133,.22);color:#fb7185;font-weight:600;"
        return styles

    st.dataframe(
        df_original.style.apply(highlight_nan, axis=None),
        use_container_width=True,
        height=260,
    )

    # ─────────────────────────────────────────────
    # COLUMN SELECTION + INTERPOLATION
    # ─────────────────────────────────────────────
    if not numeric_cols:
        st.markdown("<div class='warn-box'>⚠ No numeric columns found — interpolation requires numeric data.</div>",
                    unsafe_allow_html=True)
        st.stop()

    st.markdown('<div class="section-label">04 · Interpolate</div>', unsafe_allow_html=True)

    cols_with_nan = [c for c in numeric_cols if c in missing_info]
    if not cols_with_nan:
        st.markdown("<div class='info-box'>All numeric columns are complete — nothing to interpolate.</div>",
                    unsafe_allow_html=True)
        st.stop()

    col_choice = st.selectbox(
        "Select column to interpolate",
        ["— All numeric columns —"] + cols_with_nan,
    )

    run_btn = st.button("▶ Run Interpolation", use_container_width=False)

    if run_btn:
        df_filled = df_original.copy()
        fill_log  = {}  # col → filled indices

        targets = cols_with_nan if col_choice.startswith("—") else [col_choice]

        for col in targets:
            before = df_filled[col].copy()
            df_filled[col] = apply_interpolation(df_filled[col], interp_method)
            filled_indices = before.index[before.isna() & df_filled[col].notna()].tolist()
            if filled_indices:
                fill_log[col] = filled_indices

        total_filled = sum(len(v) for v in fill_log.values())
        remaining    = total_missing - total_filled

        # ── After-stats ──
        st.markdown(f"""
        <div class="stat-row">
            <div class="stat-card teal">
                <div class="stat-val">{total_filled}</div>
                <div class="stat-lbl">Values Filled</div>
            </div>
            <div class="stat-card rose">
                <div class="stat-val">{remaining}</div>
                <div class="stat-lbl">Still Missing</div>
            </div>
            <div class="stat-card amber">
                <div class="stat-val">{round(total_filled/max(total_missing,1)*100)}%</div>
                <div class="stat-lbl">Fill Rate</div>
            </div>
        </div>
        <div style='margin:.3rem 0 .8rem;'>
            <span class='badge badge-method'>Method · {interp_method}</span>
            {"".join(f'<span class="badge badge-filled">✓ {c}: {len(v)} filled</span>' for c, v in fill_log.items())}
        </div>
        """, unsafe_allow_html=True)

        # ── After table ──
        st.markdown('<div class="section-label">05 · Interpolated Data (After)</div>',
                    unsafe_allow_html=True)
        st.markdown(
            "<div class='info-box'>🟢 Cells highlighted in <b style='color:#2dd4bf;'>teal</b> were filled by interpolation.</div>",
            unsafe_allow_html=True,
        )

        # Build filled-positions mask
        filled_mask = pd.DataFrame(False, index=df_filled.index, columns=df_filled.columns)
        for col, indices in fill_log.items():
            for idx in indices:
                filled_mask.at[idx, col] = True

        def highlight_filled(data):
            styles = pd.DataFrame("", index=data.index, columns=data.columns)
            for col in data.columns:
                for idx in data.index:
                    if filled_mask.at[idx, col]:
                        styles.at[idx, col] = ("background-color:rgba(45,212,191,.22);"
                                               "color:#2dd4bf; font-weight:600;")
            return styles

        st.dataframe(
            df_filled.style.apply(highlight_filled, axis=None),
            use_container_width=True,
            height=260,
        )

        # ── Visualisation ──
        st.markdown('<div class="section-label">06 · Visual Comparison</div>',
                    unsafe_allow_html=True)

        for col in targets:
            if col in fill_log:   # only plot columns we actually touched
                fig = build_comparison_chart(
                    df_original[col],
                    df_filled[col],
                    col,
                    interp_method,
                )
                st.plotly_chart(fig, use_container_width=True)

        # ── Download ──
        st.markdown('<div class="section-label">07 · Export</div>', unsafe_allow_html=True)
        csv_bytes = df_filled.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇ Download Interpolated CSV",
            data=csv_bytes,
            file_name="interpolated_data.csv",
            mime="text/csv",
        )

else:
    # ── Landing placeholder ──
    st.markdown("""
    <div style="
        text-align:center;
        padding: 4rem 2rem;
        background: var(--surface);
        border: 1px dashed var(--border);
        border-radius: var(--radius);
        color: var(--muted);
    ">
        <div style="font-size:3.5rem; margin-bottom:1rem;">📂</div>
        <div style="font-family:'Space Mono',monospace; font-size:1rem; color:#e6edf3; margin-bottom:.5rem;">
            Upload a CSV to get started
        </div>
        <div style="font-size:.88rem; max-width:420px; margin:0 auto; line-height:1.7;">
            The app will detect missing values, let you choose an interpolation strategy,
            and show you a before/after visual comparison.
            <br><br>
            No data yet? Download the <b style="color:#2dd4bf;">Sample CSV</b> above ↑
        </div>
    </div>
    """, unsafe_allow_html=True)
