from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="PetFinder EDA - Pro",
    page_icon="PAW",
    layout="wide",
    initial_sidebar_state="expanded",
)

STATE_META = {
    41324: {"state_name": "Melaka", "country": "Malaysia", "lat": 2.1896, "lon": 102.2501},
    41325: {"state_name": "Kedah", "country": "Malaysia", "lat": 6.1184, "lon": 100.3685},
    41326: {"state_name": "Selangor", "country": "Malaysia", "lat": 3.0738, "lon": 101.5183},
    41327: {"state_name": "Perlis", "country": "Malaysia", "lat": 6.4414, "lon": 100.1986},
    41330: {"state_name": "Pulau Pinang", "country": "Malaysia", "lat": 5.4141, "lon": 100.3288},
    41332: {"state_name": "Negeri Sembilan", "country": "Malaysia", "lat": 2.7297, "lon": 101.9381},
    41335: {"state_name": "Pahang", "country": "Malaysia", "lat": 3.8126, "lon": 103.3256},
    41336: {"state_name": "Johor", "country": "Malaysia", "lat": 1.4927, "lon": 103.7414},
    41342: {"state_name": "Sarawak", "country": "Malaysia", "lat": 1.5533, "lon": 110.3592},
    41345: {"state_name": "Sabah", "country": "Malaysia", "lat": 5.9804, "lon": 116.0735},
    41361: {"state_name": "Terengganu", "country": "Malaysia", "lat": 5.3302, "lon": 103.1408},
    41367: {"state_name": "Kelantan", "country": "Malaysia", "lat": 6.1254, "lon": 102.2381},
    41401: {"state_name": "Kuala Lumpur", "country": "Malaysia", "lat": 3.1390, "lon": 101.6869},
    41415: {"state_name": "Labuan", "country": "Malaysia", "lat": 5.2831, "lon": 115.2308},
}
TYPE_LABEL = {1: "Dog", 2: "Cat"}
ADOPTION_LABEL = {
    0: "0 - Muy rapido",
    1: "1 - Rapido",
    2: "2 - Medio",
    3: "3 - Lento",
    4: "4 - Muy lento",
}

THEME = {
    "blue": "#0ea5e9",
    "cyan": "#06b6d4",
    "teal": "#14b8a6",
    "orange": "#f97316",
    "pink": "#ec4899",
    "slate": "#1e293b",
}


def inject_styles() -> None:
    st.markdown(
        """
        <style>
          .hero {
            padding: 1.25rem 1.5rem;
            border-radius: 18px;
            background: linear-gradient(120deg, #082f49 0%, #0f766e 50%, #134e4a 100%);
            color: #ecfeff;
            border: 1px solid rgba(255,255,255,0.15);
            box-shadow: 0 8px 30px rgba(2,132,199,0.2);
          }
          .hero h1 { margin: 0; font-size: 2.15rem; line-height: 1.15; }
          .hero p { margin: .5rem 0 0 0; color: #d1fae5; font-size: 1rem; }
          .note {
            background: #f0f9ff;
            border-left: 5px solid #0ea5e9;
            color: #0f172a;
            padding: .75rem .9rem;
            border-radius: 10px;
            margin-top: .7rem;
          }
          .insight {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: .8rem .9rem;
            color: #0f172a;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    root = Path(__file__).resolve().parents[2]
    csv_path = root / "input" / "petfinder-adoption-prediction" / "train" / "train.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"No se encontro el archivo: {csv_path}")

    df = pd.read_csv(csv_path)
    df["TypeLabel"] = df["Type"].map(TYPE_LABEL).fillna("Unknown")
    df["StateName"] = df["State"].map({k: v["state_name"] for k, v in STATE_META.items()}).fillna("Unknown")
    df["AdoptionLabel"] = df["AdoptionSpeed"].map(ADOPTION_LABEL)
    df["PhotoAmt"] = df["PhotoAmt"].fillna(0)
    return df


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    with st.sidebar:
        st.header("Filtros")
        pet_type = st.selectbox("Tipo", ["All", "Dog", "Cat"], index=0)

        state_options = sorted(df["StateName"].unique().tolist())
        selected_states = st.multiselect("Estados", state_options, default=state_options)

        age_min, age_max = int(df["Age"].min()), int(df["Age"].max())
        age_range = st.slider("Edad (meses)", age_min, age_max, (age_min, age_max))

        fee_q = st.slider("Percentil max de Fee", 50, 100, 99)

    out = df.copy()
    if pet_type != "All":
        out = out[out["TypeLabel"] == pet_type]
    out = out[out["StateName"].isin(selected_states)]
    out = out[(out["Age"] >= age_range[0]) & (out["Age"] <= age_range[1])]

    fee_cap = out["Fee"].quantile(fee_q / 100) if len(out) else 0
    out = out[out["Fee"] <= fee_cap] if len(out) else out
    return out


def kpis(df: pd.DataFrame) -> None:
    quick = (df["AdoptionSpeed"].isin([0, 1]).mean() * 100) if len(df) else 0
    st_cols = st.columns(6)
    st_cols[0].metric("Registros", f"{len(df):,}")
    st_cols[1].metric("Columnas", f"{df.shape[1]}")
    st_cols[2].metric("Edad mediana", f"{df['Age'].median():.0f}m" if len(df) else "-")
    st_cols[3].metric("Fee medio", f"{df['Fee'].mean():.0f}" if len(df) else "-")
    st_cols[4].metric("Fotos promedio", f"{df['PhotoAmt'].mean():.1f}" if len(df) else "-")
    st_cols[5].metric("Adopcion rapida", f"{quick:.1f}%")


def fig_target(df: pd.DataFrame) -> go.Figure:
    dist = df["AdoptionLabel"].value_counts().reindex(list(ADOPTION_LABEL.values()), fill_value=0).reset_index()
    dist.columns = ["AdoptionLabel", "count"]
    dist["pct"] = (dist["count"] / dist["count"].sum() * 100).round(1)

    fig = px.bar(
        dist,
        x="AdoptionLabel",
        y="count",
        color="count",
        color_continuous_scale="Tealgrn",
        text="pct",
        title="Distribucion del target con etiquetas",
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside", cliponaxis=False)
    fig.update_layout(showlegend=False, yaxis_title="Cantidad", xaxis_title="", coloraxis_showscale=False, height=430)
    return fig


def fig_map(df: pd.DataFrame) -> go.Figure:
    geo = (
        df.groupby(["State", "StateName"], as_index=False)
        .agg(listings=("PetID", "count"), median_fee=("Fee", "median"), quick_adopt=("AdoptionSpeed", lambda s: (s.isin([0, 1]).mean() * 100)))
        .sort_values("listings", ascending=False)
    )
    geo["lat"] = geo["State"].map({k: v["lat"] for k, v in STATE_META.items()})
    geo["lon"] = geo["State"].map({k: v["lon"] for k, v in STATE_META.items()})
    geo = geo.dropna(subset=["lat", "lon"])

    fig = px.scatter_map(
        geo,
        lat="lat",
        lon="lon",
        size="listings",
        color="quick_adopt",
        hover_name="StateName",
        hover_data={"listings": True, "median_fee": True, "quick_adopt": ':.1f', "lat": False, "lon": False},
        color_continuous_scale="Turbo",
        size_max=42,
        zoom=4.3,
        center={"lat": 4.6, "lon": 102.2},
        map_style="carto-positron",
        title="Mapa profesional: volumen por estado y color por adopcion rapida",
    )

    # Etiquetas superpuestas (solo top 8 para mantener legibilidad)
    labels = geo.head(8)
    fig.add_trace(
        go.Scattermap(
            lat=labels["lat"],
            lon=labels["lon"],
            mode="text",
            text=labels["StateName"],
            textfont={"size": 12, "color": "#0f172a"},
            hoverinfo="skip",
            showlegend=False,
        )
    )

    fig.update_layout(height=560, margin={"l": 0, "r": 0, "t": 55, "b": 0})
    return fig


def fig_numeric_story(df: pd.DataFrame) -> go.Figure:
    metrics = ["Age", "Fee", "PhotoAmt", "Quantity"]
    corr = df[metrics + ["AdoptionSpeed"]].corr(numeric_only=True)["AdoptionSpeed"].drop("AdoptionSpeed").sort_values()

    fig = px.bar(
        corr.reset_index().rename(columns={"index": "feature", "AdoptionSpeed": "corr"}),
        x="corr",
        y="feature",
        orientation="h",
        text="corr",
        color="corr",
        color_continuous_scale="RdBu",
        title="Sensibilidad del target a variables numericas",
    )
    fig.update_traces(texttemplate="%{text:.3f}", textposition="outside")
    fig.update_layout(height=420, coloraxis_showscale=False, yaxis_title="", xaxis_title="Correlacion")
    return fig


def fig_corr_heatmap(df: pd.DataFrame) -> go.Figure:
    num_df = df.select_dtypes(include=["number"]).copy()
    if "AdoptionSpeed" in num_df.columns:
        corr_full = num_df.corr(numeric_only=True)
        target_rank = (
            corr_full["AdoptionSpeed"].drop("AdoptionSpeed", errors="ignore").abs().sort_values(ascending=False)
        )
        keep = list(target_rank.head(10).index)
        if "AdoptionSpeed" not in keep:
            keep.append("AdoptionSpeed")
    else:
        keep = list(num_df.var(numeric_only=True).sort_values(ascending=False).head(11).index)

    corr = num_df[keep].corr(numeric_only=True).round(2)
    labels = corr.columns.tolist()
    z = corr.values

    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            x=labels,
            y=labels,
            colorscale="RdBu",
            zmin=-1,
            zmax=1,
            text=z,
            texttemplate="%{text:.2f}",
            hovertemplate="X: %{x}<br>Y: %{y}<br>Corr: %{z:.2f}<extra></extra>",
            colorbar=dict(title="Corr"),
        )
    )
    fig.update_layout(
        title="Diagrama de correlaciones (top variables)",
        height=520,
        xaxis_title="",
        yaxis_title="",
    )
    return fig


def fig_age_stack(df: pd.DataFrame) -> go.Figure:
    bins = pd.cut(df["Age"], bins=[-1, 3, 12, 36, 120, 600], labels=["0-3", "4-12", "13-36", "37-120", "120+"])
    tb = pd.crosstab(bins, df["AdoptionLabel"], normalize="index").mul(100).reset_index().rename(columns={"Age": "AgeBin"})
    long = tb.melt(id_vars=[tb.columns[0]], var_name="AdoptionLabel", value_name="pct")
    long = long.rename(columns={tb.columns[0]: "AgeBin"})

    fig = px.bar(
        long,
        x="AgeBin",
        y="pct",
        color="AdoptionLabel",
        barmode="stack",
        text="pct",
        title="Mezcla de clases por grupo etario",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_traces(texttemplate="%{text:.0f}", textposition="inside")
    fig.update_layout(height=430, yaxis_title="% dentro del grupo")
    return fig


def fig_state_leaderboard(df: pd.DataFrame) -> go.Figure:
    top = df["StateName"].value_counts().head(10).reset_index()
    top.columns = ["StateName", "count"]

    fig = px.bar(
        top.sort_values("count"),
        x="count",
        y="StateName",
        orientation="h",
        text="count",
        color="count",
        color_continuous_scale="Blues",
        title="Top estados por publicaciones",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(height=430, coloraxis_showscale=False, yaxis_title="", xaxis_title="Publicaciones")
    return fig


def fig_catdog(df: pd.DataFrame) -> go.Figure:
    t = pd.crosstab(df["TypeLabel"], df["AdoptionLabel"], normalize="index").mul(100).reset_index()
    long = t.melt(id_vars=["TypeLabel"], var_name="AdoptionLabel", value_name="pct")
    fig = px.bar(
        long,
        x="TypeLabel",
        y="pct",
        color="AdoptionLabel",
        barmode="group",
        text="pct",
        color_discrete_sequence=px.colors.qualitative.Safe,
        title="Dog vs Cat: perfil de adopcion",
    )
    fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
    fig.update_layout(height=430, yaxis_title="%")
    return fig


def insight_block(df: pd.DataFrame) -> None:
    if df.empty:
        return
    top_state = df["StateName"].value_counts().idxmax()
    top_n = int(df["StateName"].value_counts().max())
    top_feature = (
        df.select_dtypes(include=["number"])
        .corr(numeric_only=True)["AdoptionSpeed"]
        .drop("AdoptionSpeed")
        .abs()
        .sort_values(ascending=False)
        .index[0]
    )
    quick = (df["AdoptionSpeed"].isin([0, 1]).mean() * 100)

    st.markdown("### Insights de impacto")
    st.markdown(
        f"""
        <div class="insight">
          <b>1)</b> El estado con mayor concentracion es <b>{top_state}</b> ({top_n} publicaciones).<br>
          <b>2)</b> Tasa de adopcion rapida estimada: <b>{quick:.1f}%</b>.<br>
          <b>3)</b> Senal numerica dominante para modelado: <b>{top_feature}</b>.<br>
          <b>4)</b> Recomendacion competitiva: segmentar estrategia por estado y por tipo (Dog/Cat), ajustando fee y calidad visual.
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    inject_styles()
    df = load_data()
    fdf = apply_filters(df)

    st.markdown(
        """
        <div class="hero">
          <h1>PetFinder EDA - Competition Edition</h1>
          <p>Dashboard de nivel presentacion: mapa legible, etiquetas superpuestas, historias de negocio y visuales premium.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if fdf.empty:
        st.error("No hay datos con los filtros actuales.")
        return

    kpis(fdf)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Executive Overview",
        "Geo Story",
        "Target Drivers",
        "Segments",
        "Winning Insights",
    ])

    with tab1:
        c1, c2 = st.columns([1.05, 1], gap="large")
        with c1:
            st.plotly_chart(fig_target(fdf), use_container_width=True)
        with c2:
            st.plotly_chart(fig_state_leaderboard(fdf), use_container_width=True)
        st.dataframe(fdf.head(35), width="stretch", height=300)

    with tab2:
        st.plotly_chart(fig_map(fdf), use_container_width=True)

    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(fig_numeric_story(fdf), use_container_width=True)
        with c2:
            st.plotly_chart(fig_age_stack(fdf), use_container_width=True)
        st.plotly_chart(fig_corr_heatmap(fdf), use_container_width=True)

    with tab4:
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(fig_catdog(fdf), use_container_width=True)
        with c2:
            out = []
            for col in ["Age", "Fee", "Quantity", "PhotoAmt", "VideoAmt"]:
                s = fdf[col].dropna()
                if len(s) == 0:
                    continue
                q1, q3 = s.quantile(0.25), s.quantile(0.75)
                iqr = q3 - q1
                low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
                n = int(((s < low) | (s > high)).sum())
                out.append({"Feature": col, "Outliers": n, "Pct": round(n / len(s) * 100, 2)})
            out_df = pd.DataFrame(out).sort_values("Pct", ascending=False)
            fig = px.bar(out_df, x="Feature", y="Pct", text="Pct", color="Pct", color_continuous_scale="OrRd", title="Outliers por feature")
            fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig.update_layout(height=430, coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)

    with tab5:
        insight_block(fdf)


if __name__ == "__main__":
    main()
