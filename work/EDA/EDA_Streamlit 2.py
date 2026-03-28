from pathlib import Path
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="SRV_POZOS | EDA Dark",
    page_icon=":compass:",
    layout="wide",
    initial_sidebar_state="expanded",
)


BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent.parent
INPUT_DIRS = [
    REPO_ROOT / "input",
    BASE_DIR / "input",
]
PARQUET_DIR = BASE_DIR / "data" / "output_parquet"
BG = "#020617"
PANEL = "#0F172A"
CARD = "#111827"
TEXT = "#E5EEF7"
MUTED = "#94A3B8"
PRIMARY = "#67E8F9"
ACCENT = "#F59E0B"
SUCCESS = "#34D399"
PALETTE = [
    "#67E8F9",
    "#F59E0B",
    "#34D399",
    "#A78BFA",
    "#F472B6",
    "#F87171",
    "#FCD34D",
    "#60A5FA",
    "#4ADE80",
    "#FB7185",
]


st.markdown(
    f"""
    <style>
    .stApp {{
        background:
            radial-gradient(circle at top left, rgba(103,232,249,0.14), transparent 24%),
            radial-gradient(circle at top right, rgba(245,158,11,0.10), transparent 20%),
            linear-gradient(180deg, {BG} 0%, #07101f 100%);
        color: {TEXT};
    }}
    .block-container {{
        padding-top: 1.2rem;
        padding-bottom: 1.5rem;
    }}
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0B1220 0%, {PANEL} 100%);
        border-right: 1px solid rgba(148,163,184,0.12);
    }}
    [data-testid="stSidebar"] * {{
        color: {TEXT};
    }}
    .hero {{
        background: linear-gradient(135deg, rgba(15,23,42,0.98), rgba(17,24,39,0.96));
        border: 1px solid rgba(103,232,249,0.16);
        border-radius: 24px;
        padding: 1.5rem 1.7rem;
        box-shadow: 0 22px 50px rgba(0,0,0,0.35);
        margin-bottom: 1rem;
    }}
    .hero h1 {{
        margin: 0;
        color: #F8FAFC;
        font-size: 2.2rem;
        letter-spacing: -0.03em;
    }}
    .hero p {{
        margin: 0.5rem 0 0 0;
        color: #CBD5E1;
        max-width: 960px;
    }}
    .small-note {{
        color: {MUTED};
        font-size: 0.92rem;
    }}
    .insight {{
        background: rgba(15,23,42,0.92);
        border: 1px solid rgba(148,163,184,0.14);
        border-left: 5px solid {ACCENT};
        border-radius: 16px;
        padding: 1rem;
        box-shadow: 0 14px 30px rgba(0,0,0,0.22);
        min-height: 130px;
    }}
    .insight h4 {{
        margin: 0 0 0.35rem 0;
        color: #F8FAFC;
        font-size: 1rem;
    }}
    .insight p {{
        margin: 0;
        color: #CBD5E1;
        line-height: 1.45;
    }}
    .stMetric {{
        background: rgba(17,24,39,0.92);
        border: 1px solid rgba(148,163,184,0.14);
        border-radius: 18px;
        padding: 0.75rem 0.9rem;
        box-shadow: 0 12px 25px rgba(0,0,0,0.22);
    }}
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.45rem;
    }}
    .stTabs [data-baseweb="tab"] {{
        background: rgba(15,23,42,0.82);
        border-radius: 999px;
        color: #CBD5E1;
        padding: 0.42rem 0.95rem;
    }}
    .stTabs [aria-selected="true"] {{
        background: rgba(103,232,249,0.13);
        border: 1px solid rgba(103,232,249,0.22);
        color: #F8FAFC;
    }}
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    .stMultiSelect div[data-baseweb="select"] > div {{
        background: rgba(15,23,42,0.9);
        border-color: rgba(148,163,184,0.22);
    }}
    .stSlider [data-baseweb="slider"] {{
        padding-top: 0.4rem;
    }}
    .loading-overlay {{
        position: fixed;
        inset: 0;
        background: rgba(2, 6, 23, 0.55);
        z-index: 999999;
        display: flex;
        align-items: center;
        justify-content: center;
        pointer-events: all;
        backdrop-filter: blur(3px);
    }}
    .loading-card {{
        min-width: 320px;
        max-width: 460px;
        background: rgba(3, 7, 18, 0.92);
        border: 1px solid rgba(103,232,249,0.18);
        border-radius: 18px;
        padding: 1.2rem 1.35rem;
        box-shadow: 0 30px 80px rgba(0,0,0,0.45);
        text-align: center;
    }}
    .loading-spinner {{
        width: 42px;
        height: 42px;
        border-radius: 999px;
        margin: 0 auto 0.9rem auto;
        border: 4px solid rgba(148,163,184,0.20);
        border-top-color: {PRIMARY};
        animation: spin 0.9s linear infinite;
    }}
    .loading-title {{
        color: #F8FAFC;
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 0.35rem;
    }}
    .loading-step {{
        color: #CBD5E1;
        line-height: 1.45;
        font-size: 0.95rem;
    }}
    @keyframes spin {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


def apply_dark_layout(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT),
        title_font=dict(color="#F8FAFC", size=20),
        legend=dict(bgcolor="rgba(15,23,42,0.70)", bordercolor="rgba(148,163,184,0.15)", borderwidth=1),
        margin=dict(l=10, r=10, t=60, b=20),
    )
    fig.update_xaxes(gridcolor="rgba(148,163,184,0.14)", zerolinecolor="rgba(148,163,184,0.14)")
    fig.update_yaxes(gridcolor="rgba(148,163,184,0.14)", zerolinecolor="rgba(148,163,184,0.14)")
    return fig


def fmt_file_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    if size_bytes < 1024**2:
        return f"{size_bytes / 1024:.1f} KB"
    return f"{size_bytes / (1024**2):.2f} MB"


def show_loading(placeholder, message: str) -> None:
    if not st.session_state.get("loader_enabled", False):
        return
    placeholder.markdown(
        f"""
        <div class="loading-overlay">
            <div class="loading-card">
                <div class="loading-spinner"></div>
                <div class="loading-title">Cargando EDA</div>
                <div class="loading-step">{message}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def trigger_loader() -> None:
    st.session_state["loader_enabled"] = True


def reset_state_for_new_file() -> None:
    keys_to_remove = []
    prefixes = [
        "filter_",
        "range_",
        "exec_",
        "numeric_",
        "time_",
        "rel_",
        "stats_",
        "apply_",
        "applied_",
    ]
    exact_keys = {
        "coord_check",
        "size_map_select",
        "active_section",
        "loader_enabled",
    }

    for key in list(st.session_state.keys()):
        if key in exact_keys or any(key.startswith(prefix) for prefix in prefixes):
            keys_to_remove.append(key)

    for key in keys_to_remove:
        st.session_state.pop(key, None)


def get_parquet_catalog(parquet_dir: Path) -> pd.DataFrame:
    parquet_files = sorted(parquet_dir.glob("*.parquet"))
    return pd.DataFrame(
        [
            {
                "Archivo": file.name,
                "Tamano": fmt_file_size(file.stat().st_size),
                "Modificado": pd.to_datetime(file.stat().st_mtime, unit="s").strftime("%d/%m/%Y %H:%M"),
            }
            for file in parquet_files
        ]
    )


def get_available_parquets(parquet_dir: Path) -> list:
    """Obtiene lista de archivos parquet disponibles"""
    parquet_files = sorted(list(parquet_dir.glob("*.parquet")))
    return [f.name for f in parquet_files]


@st.cache_data(show_spinner=False)
def load_data(parquet_dir: Path, selected_files: tuple = None) -> pd.DataFrame:
    """Carga los archivos .parquet seleccionados del directorio y los concatena"""
    all_parquet_files = list(parquet_dir.glob("*.parquet"))
    if not all_parquet_files:
        st.error(f"No se encontraron archivos .parquet en {parquet_dir}")
        st.stop()
    
    if selected_files is None or len(selected_files) == 0:
        files_to_load = all_parquet_files
    else:
        files_to_load = [f for f in all_parquet_files if f.name in selected_files]
    
    if not files_to_load:
        st.error("No se seleccionaron archivos para cargar")
        st.stop()
    
    dfs = []
    for file in files_to_load:
        df_temp = pd.read_parquet(file)
        dfs.append(df_temp)
    
    df = pd.concat(dfs, ignore_index=True)
    df = df.drop_duplicates(subset=['TAG'] if 'TAG' in df.columns else None, keep='first')

    # Conversión de tipos de datos - solo si existen las columnas
    date_cols = [col for col in ["FECHAINICIAL", "FECHADEPUESTAENMARCHA", "FECHADECAMPANIA"] if col in df.columns]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    if "FECHADECAMPANIA" in df.columns:
        df["ANIO_CAMPANIA"] = pd.to_numeric(df["FECHADECAMPANIA"], errors="coerce").fillna(0).astype(int)
    else:
        df["ANIO_CAMPANIA"] = 0

    if "FECHAINICIAL" in df.columns:
        df["FECHAINICIAL"] = df["FECHAINICIAL"].mask(df["FECHAINICIAL"] == pd.Timestamp("1900-01-01"))
        df["ANIO_FECHA_INICIAL"] = df["FECHAINICIAL"].dt.year
    
    # Limpieza de valores faltantes - solo para columnas que existan
    for col in ["PLANTADEINYECCIONDEAGUA", "PROYECTODESECUNDARIA"]:
        if col in df.columns:
            df[col] = df[col].fillna("Sin dato")

    # Features de geolocalización - solo si existen ambas columnas
    if "LATITUD" in df.columns and "LONGITUD" in df.columns:
        df["TIENE_COORDENADAS"] = df["LATITUD"].notna() & df["LONGITUD"].notna()
    else:
        df["TIENE_COORDENADAS"] = False

    # Features temporales
    if "FECHADEPUESTAENMARCHA" in df.columns:
        df["ANIO_PUESTA_MARCHA"] = df["FECHADEPUESTAENMARCHA"].dt.year
    else:
        df["ANIO_PUESTA_MARCHA"] = pd.NA

    # Features categóricas
    if "PLANTADEINYECCIONDEAGUA" in df.columns:
        df["ESTADO_PLANTA"] = df["PLANTADEINYECCIONDEAGUA"].ne("Sin dato").map({True: "Con planta", False: "Sin planta"})
    
    if "PROYECTODESECUNDARIA" in df.columns:
        df["ESTADO_PROYECTO"] = df["PROYECTODESECUNDARIA"].ne("Sin dato").map(
            {True: "Con proyecto", False: "Sin proyecto"}
        )
        df["MAPA_PROYECTO"] = df["PROYECTODESECUNDARIA"].replace({"Sin dato": "Yacimiento", "": "Yacimiento"})
    
    # Rango de profundidad - solo si existe
    if "PROFUNDIDADTOTAL" in df.columns:
        df["RANGO_PROFUNDIDAD"] = pd.cut(
            df["PROFUNDIDADTOTAL"],
            bins=[-1, 1500, 2000, 2500, 3000, 6000],
            labels=["<=1500", "1501-2000", "2001-2500", "2501-3000", ">3000"],
        )
    
    return df


def fmt_int(value: float | int) -> str:
    if pd.isna(value):
        return "-"
    return f"{int(round(value)):,}".replace(",", ".")


def fmt_num(value: float, decimals: int = 1) -> str:
    if pd.isna(value):
        return "-"
    return f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def pct(value: float) -> str:
    if pd.isna(value):
        return "-"
    return f"{value:.1f}%".replace(".", ",")


def add_download(df: pd.DataFrame, target=None) -> None:
    csv = df.to_csv(index=False, sep=";", encoding="utf-8-sig").encode("utf-8-sig")
    button_target = target if target is not None else st
    button_target.download_button(
        "Descargar dataset filtrado",
        data=csv,
        file_name="SRV_POZOS_filtrado.csv",
        mime="text/csv",
        use_container_width=True,
    )


def build_file_selector(available_files: list, parquet_catalog: pd.DataFrame, loading_placeholder=None) -> list:
    st.sidebar.markdown("## Panel de control")
    st.sidebar.caption("Selecciona los parquet a incluir y luego ajusta los filtros del EDA.")
    
    # Selector de archivos parquet
    st.sidebar.markdown("### Archivos parquet")
    st.sidebar.info(f"Total disponibles: {len(available_files)}")
    if st.sidebar.button("Actualizar lista de archivos", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    selected_files = st.sidebar.multiselect(
        "Selecciona archivos para analizar",
        options=available_files,
        default=available_files,
        key="file_selector",
        help="Elige qué archivos parquet deseas incluir en el análisis"
    )
    
    if not selected_files:
        st.sidebar.warning("⚠️ Debes seleccionar al menos un archivo")
        st.stop()
    
    if len(selected_files) < len(available_files):
        st.sidebar.caption(f"📊 Mostrando {len(selected_files)} de {len(available_files)} archivos")
    
    if not parquet_catalog.empty:
        st.sidebar.dataframe(parquet_catalog, use_container_width=True, hide_index=True, height=220)

    st.sidebar.markdown("---")
    return selected_files


def build_file_selector(available_files: list, parquet_catalog: pd.DataFrame) -> list:
    st.sidebar.markdown("## Panel de control")
    st.sidebar.caption("Selecciona un parquet y luego ajusta los filtros del EDA.")

    st.sidebar.markdown("### Archivos parquet")
    st.sidebar.info(f"Total disponibles: {len(available_files)}")
    if st.sidebar.button("Actualizar lista de archivos", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    default_file = max(available_files, key=lambda file_name: (PARQUET_DIR / file_name).stat().st_mtime)
    selected_file = st.sidebar.selectbox(
        "Selecciona un archivo para analizar",
        options=available_files,
        index=available_files.index(default_file),
        key="single_file_selector",
        help="Elige un solo archivo parquet para el analisis",
    )
    previous_file = st.session_state.get("applied_selected_file")
    if previous_file != selected_file:
        if previous_file is not None:
            reset_state_for_new_file()
        st.session_state["file_changed_this_run"] = True
        trigger_loader()
        if loading_placeholder is not None:
            show_loading(loading_placeholder, f"Cargando {selected_file}...")
        st.session_state["applied_selected_file"] = selected_file
        st.rerun()
    st.sidebar.caption(f"Mostrando 1 de {len(available_files)} archivos")

    if not parquet_catalog.empty:
        st.sidebar.dataframe(parquet_catalog, use_container_width=True, hide_index=True, height=220)

    st.sidebar.markdown("---")
    return [selected_file]


def build_sidebar(df: pd.DataFrame, selected_file: str) -> tuple[pd.DataFrame, str]:
    st.sidebar.markdown("### Filtros del EDA")
    st.sidebar.caption("Filtra el universo y ajusta el tamano visual del mapa.")

    filtered = df.copy()
    
    # Filtros dinámicos basados en columnas disponibles
    if "PROYECTODESECUNDARIA" in df.columns:
        proyectos = st.sidebar.multiselect(
            "Proyecto de secundaria",
            options=sorted(df["PROYECTODESECUNDARIA"].unique()),
            key="proyecto_filter"
        )
        if proyectos:
            filtered = filtered[filtered["PROYECTODESECUNDARIA"].isin(proyectos)]
    
    if "PLANTADEINYECCIONDEAGUA" in df.columns:
        plantas = st.sidebar.multiselect(
            "Planta de inyeccion de agua",
            options=sorted(df["PLANTADEINYECCIONDEAGUA"].unique()),
            key="planta_filter"
        )
        if plantas:
            filtered = filtered[filtered["PLANTADEINYECCIONDEAGUA"].isin(plantas)]

    # Slider de profundidad - solo si existe la columna
    if "PROFUNDIDADTOTAL" in df.columns:
        profundidad = df["PROFUNDIDADTOTAL"].dropna()
        if not profundidad.empty:
            prof_min = int(profundidad.min())
            prof_max = int(profundidad.max())
            if prof_min == prof_max:
                st.sidebar.caption(f"Profundidad total fija: {prof_min}")
                filtered = filtered[filtered["PROFUNDIDADTOTAL"].fillna(prof_min) == prof_min]
            else:
                rango_prof = st.sidebar.slider(
                    "Profundidad total",
                    min_value=prof_min,
                    max_value=prof_max,
                    value=(prof_min, prof_max),
                    key="prof_slider"
                )
                filtered = filtered[filtered["PROFUNDIDADTOTAL"].fillna(prof_min).between(rango_prof[0], rango_prof[1])]

    # Slider de año de campaña - solo si existe
    if "ANIO_CAMPANIA" in df.columns:
        anio_camp = df["ANIO_CAMPANIA"].dropna().astype(int)
        if not anio_camp.empty:
            camp_min = int(anio_camp.min())
            camp_max = int(anio_camp.max())
            if camp_min == camp_max:
                st.sidebar.caption(f"Ano de campana fijo: {camp_min}")
                filtered = filtered[filtered["ANIO_CAMPANIA"].fillna(camp_min).astype(int) == camp_min]
            else:
                rango_camp = st.sidebar.slider(
                    "Ano de campana",
                    min_value=camp_min,
                    max_value=camp_max,
                    value=(camp_min, camp_max),
                    key="camp_slider"
                )
                filtered = filtered[filtered["ANIO_CAMPANIA"].fillna(camp_min).astype(float).between(rango_camp[0], rango_camp[1])]

    # Checkbox para incluir/excluir sin fecha de puesta en marcha - solo si existe
    if "ANIO_PUESTA_MARCHA" in df.columns:
        con_sin_fecha = st.sidebar.checkbox("Incluir sin fecha de puesta en marcha", value=True, key="fecha_check")
        if not con_sin_fecha:
            filtered = filtered[filtered["ANIO_PUESTA_MARCHA"].notna()]
    
    # Checkbox para solo pozos con coordenadas - solo si existen ambas columnas
    if "LATITUD" in df.columns and "LONGITUD" in df.columns:
        solo_coord = st.sidebar.checkbox("Solo pozos con coordenadas", value=False, key="coord_check")
        if solo_coord:
            filtered = filtered[filtered["TIENE_COORDENADAS"]]

    # Selector de tamaño del mapa - solo si existen coordenadas
    size_map = "Constante"
    if "LATITUD" in df.columns and "LONGITUD" in df.columns:
        size_options = ["Constante"]
        if "PROFUNDIDADTOTAL" in df.columns:
            size_options.append("PROFUNDIDADTOTAL")
        if "ANIO_CAMPANIA" in df.columns:
            size_options.append("ANIO_CAMPANIA")
        
        if len(size_options) > 1:
            size_map = st.sidebar.selectbox(
                "Tamano del punto en el mapa",
                options=size_options,
                key="size_map_select"
            )

    st.sidebar.markdown("---")
    add_download(filtered)
    return filtered, size_map


def render_header(df: pd.DataFrame, selected_files: list, total_files: int) -> None:
    files_str = ", ".join(selected_files) if selected_files else "Ninguno"
    st.markdown(
        f"""
        <div class="hero">
            <h1>EDA profesional de SRV_POZOS</h1>
            <p>
                Exploracion ejecutiva e interactiva del padron de pozos de GSJ con foco en cobertura,
                calidad de datos, distribucion espacial, profundidad y comportamiento temporal.
            </p>
            <p class="small-note">Archivos seleccionados: {len(selected_files)} de {total_files} | Registros cargados: {fmt_int(len(df))}</p>
            <p class="small-note">{files_str}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpis(df: pd.DataFrame) -> None:
    total = len(df)
    kpis = {}
    
    # KPIs que dependen de columnas existentes
    if "LATITUD" in df.columns and "LONGITUD" in df.columns:
        kpis["Cobertura geografica"] = pct(100 * df["TIENE_COORDENADAS"].mean() if total else 0)
    
    if "PROFUNDIDADTOTAL" in df.columns:
        prof_data = df["PROFUNDIDADTOTAL"].dropna()
        if not prof_data.empty:
            kpis["Profundidad media"] = fmt_num(prof_data.mean())
            kpis["P75 profundidad"] = fmt_num(prof_data.quantile(0.75))
            kpis["Profundidad maxima"] = fmt_num(prof_data.max())
    
    if "PLANTADEINYECCIONDEAGUA" in df.columns:
        kpis["Con planta"] = pct(100 * df["PLANTADEINYECCIONDEAGUA"].ne("Sin dato").mean() if total else 0)
    
    if "ANIO_CAMPANIA" in df.columns:
        kpis["Anos de campana"] = fmt_int(df["ANIO_CAMPANIA"].nunique())
    
    if "PROYECTODESECUNDARIA" in df.columns:
        kpis["Con proyecto"] = pct(100 * df["PROYECTODESECUNDARIA"].ne("Sin dato").mean() if total else 0)
    
    if "ANIO_PUESTA_MARCHA" in df.columns:
        fecha_max = df["ANIO_PUESTA_MARCHA"].max()
        if pd.notna(fecha_max):
            kpis["Ano puesta en marcha reciente"] = fmt_int(fecha_max)

    # Mostrar siempre el KPI de pozos analizados primero
    cols = st.columns(max(2, len(kpis) + 1))
    cols[0].metric("Pozos analizados", fmt_int(total))
    
    for idx, (label, value) in enumerate(kpis.items(), start=1):
        if idx < len(cols):
            cols[idx].metric(label, value)


def render_insights(df: pd.DataFrame) -> None:
    missing_prof = 100 * df["PROFUNDIDADTOTAL"].isna().mean() if len(df) else 0
    
    insights = []
    
    # Insight 1: Concentración operativa (si existe PROYECTODESECUNDARIA)
    if "PROYECTODESECUNDARIA" in df.columns or "MAPA_PROYECTO" in df.columns:
        col_name = "MAPA_PROYECTO" if "MAPA_PROYECTO" in df.columns else "PROYECTODESECUNDARIA"
        top_proj = df[col_name].value_counts()
        if not top_proj.empty:
            insights.append((
                "Concentracion operativa",
                f"La categoria dominante es <b>{top_proj.index[0]}</b> con <b>{fmt_int(top_proj.iloc[0])}</b> registros."
            ))
    
    # Insight 2: Infraestructura (si existe PLANTADEINYECCIONDEAGUA)
    if "PLANTADEINYECCIONDEAGUA" in df.columns:
        top_plant = df["PLANTADEINYECCIONDEAGUA"].value_counts()
        if not top_plant.empty:
            insights.append((
                "Infraestructura asociada",
                f"La planta con mayor vinculacion es <b>{top_plant.index[0]}</b> con <b>{fmt_int(top_plant.iloc[0])}</b> registros."
            ))
    
    # Insight 3: Calidad y actualidad
    quality_text = f"La profundidad total tiene <b>{pct(missing_prof)}</b> de faltantes."
    if "FECHADEPUESTAENMARCHA" in df.columns:
        latest = df["FECHADEPUESTAENMARCHA"].max()
        latest_text = latest.strftime("%d/%m/%Y") if pd.notna(latest) else "sin dato"
        quality_text += f" La ultima puesta en marcha registrada es <b>{latest_text}</b>."
    insights.append(("Calidad y actualidad", quality_text))
    
    # Mostrar insights en columnas
    if insights:
        cols = st.columns(len(insights))
        for idx, (title, text) in enumerate(insights):
            with cols[idx]:
                st.markdown(
                    f"""
                    <div class="insight">
                        <h4>{title}</h4>
                        <p>{text}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


@st.cache_data(show_spinner=False)
def quality_table(df: pd.DataFrame) -> pd.DataFrame:
    summary = pd.DataFrame(
        {
            "Columna": df.columns,
            "Tipo": [str(dtype) for dtype in df.dtypes],
            "No nulos": df.notna().sum().values,
            "Faltantes": df.isna().sum().values,
        }
    )
    summary["Cobertura %"] = (summary["No nulos"] / len(df) * 100).round(1) if len(df) else 0
    return summary.sort_values(["Faltantes", "Columna"], ascending=[False, True])


def fig_missing(df: pd.DataFrame) -> go.Figure:
    miss = quality_table(df).head(12).sort_values("Faltantes")
    fig = px.bar(
        miss,
        x="Faltantes",
        y="Columna",
        orientation="h",
        text="Cobertura %",
        color="Cobertura %",
        color_continuous_scale=[[0, "#EF4444"], [0.5, "#F59E0B"], [1, SUCCESS]],
        title="Columnas con mayor nivel de faltantes",
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_layout(xaxis_title="Cantidad de faltantes", yaxis_title="", height=430, coloraxis_showscale=False)
    return apply_dark_layout(fig)


def fig_depth_distribution(df: pd.DataFrame) -> go.Figure:
    fig = px.histogram(
        df,
        x="PROFUNDIDADTOTAL",
        nbins=45,
        marginal="box",
        opacity=0.9,
        color_discrete_sequence=[PRIMARY],
        title="Distribucion de profundidad total",
    )
    fig.update_layout(xaxis_title="Profundidad total", yaxis_title="Cantidad de pozos", bargap=0.03, height=430)
    return apply_dark_layout(fig)


def fig_top_categories(df: pd.DataFrame, column: str, title: str) -> go.Figure:
    top = df[column].value_counts().head(12).sort_values()
    top_df = top.rename_axis("categoria").reset_index(name="cantidad")
    fig = px.bar(
        top_df,
        x="cantidad",
        y="categoria",
        orientation="h",
        text="cantidad",
        color="cantidad",
        color_continuous_scale=["#1E293B", ACCENT],
        title=title,
    )
    fig.update_layout(xaxis_title="Cantidad de pozos", yaxis_title="", height=430, coloraxis_showscale=False)
    return apply_dark_layout(fig)


def fig_depth_by_project(df: pd.DataFrame) -> go.Figure:
    top_projects = df["MAPA_PROYECTO"].value_counts().head(10).index
    subset = df[df["MAPA_PROYECTO"].isin(top_projects)].copy()
    median_order = subset.groupby("MAPA_PROYECTO")["PROFUNDIDADTOTAL"].median().sort_values(ascending=False).index
    fig = px.box(
        subset,
        x="MAPA_PROYECTO",
        y="PROFUNDIDADTOTAL",
        color="MAPA_PROYECTO",
        category_orders={"MAPA_PROYECTO": list(median_order)},
        color_discrete_sequence=PALETTE,
        points="outliers",
        title="Profundidad por proyecto dominante",
    )
    fig.update_traces(
        quartilemethod="exclusive",
        marker=dict(size=6, opacity=0.85, line=dict(width=0)),
        line=dict(width=2),
    )
    fig.update_layout(
        showlegend=False,
        xaxis_title="Proyecto de secundaria",
        yaxis_title="Profundidad total",
        height=470,
    )
    return apply_dark_layout(fig)


def fig_campaign_vs_startup(df: pd.DataFrame) -> go.Figure:
    camp = df["ANIO_CAMPANIA"].dropna().astype(int).value_counts().sort_index().reset_index()
    camp.columns = ["Ano", "Cantidad"]

    puesta = df["ANIO_PUESTA_MARCHA"].dropna().astype(int).value_counts().sort_index().reset_index()
    puesta.columns = ["Ano", "Cantidad"]

    fig = go.Figure()
    if not camp.empty:
        fig.add_trace(
            go.Scatter(
                x=camp["Ano"],
                y=camp["Cantidad"],
                mode="lines+markers",
                name="Campana",
                line=dict(color=PRIMARY, width=3),
            )
        )
    if not puesta.empty:
        fig.add_trace(
            go.Bar(
                x=puesta["Ano"],
                y=puesta["Cantidad"],
                name="Puesta en marcha",
                marker_color=ACCENT,
                opacity=0.72,
            )
        )
    fig.update_layout(title="Lectura temporal: campana vs. puesta en marcha", xaxis_title="Ano", yaxis_title="Cantidad de pozos", height=460, barmode="overlay")
    return apply_dark_layout(fig)


def fig_depth_heatmap(df: pd.DataFrame) -> go.Figure:
    pivot = (
        df.dropna(subset=["ANIO_CAMPANIA", "RANGO_PROFUNDIDAD"])
        .groupby(["RANGO_PROFUNDIDAD", "ANIO_CAMPANIA"], observed=False)
        .size()
        .reset_index(name="cantidad")
        .pivot(index="RANGO_PROFUNDIDAD", columns="ANIO_CAMPANIA", values="cantidad")
        .fillna(0)
    )
    fig = px.imshow(
        pivot,
        aspect="auto",
        color_continuous_scale="YlOrBr",
        title="Intensidad por ano de campana y rango de profundidad",
    )
    fig.update_layout(height=390, xaxis_title="Ano de campana", yaxis_title="Rango de profundidad")
    return apply_dark_layout(fig)


def fig_map(df: pd.DataFrame, size_map: str) -> go.Figure:
    map_df = df[df["TIENE_COORDENADAS"]].copy()
    if map_df.empty:
        return go.Figure()

    if size_map == "Constante":
        map_df["SIZE_VALUE"] = 10
    else:
        base = map_df[size_map].fillna(map_df[size_map].median())
        if float(base.max()) == float(base.min()):
            map_df["SIZE_VALUE"] = 10
        else:
            map_df["SIZE_VALUE"] = 8 + ((base - base.min()) / (base.max() - base.min()) * 20)

    hover_data = {
        "TAG": True,
        "PROFUNDIDADTOTAL": ":.1f",
        "PLANTADEINYECCIONDEAGUA": True,
        "MAPA_PROYECTO": True,
        "ANIO_CAMPANIA": True,
        "ANIO_PUESTA_MARCHA": True,
        "LATITUD": ":.4f",
        "LONGITUD": ":.4f",
        "SIZE_VALUE": False,
    }

    fig = px.scatter_map(
        map_df,
        lat="LATITUD",
        lon="LONGITUD",
        color="MAPA_PROYECTO",
        size="SIZE_VALUE",
        size_max=26,
        hover_name="NOMBRE",
        hover_data=hover_data,
        zoom=6.3,
        height=720,
        color_discrete_sequence=PALETTE,
        title="Distribucion espacial de pozos por proyecto de secundaria",
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=60, b=0),
        legend_title_text="Proyecto de secundaria",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def get_relation_columns(df: pd.DataFrame) -> list[str]:
    preferred = [
        "MAPA_PROYECTO",
        "PROYECTODESECUNDARIA",
        "PLANTADEINYECCIONDEAGUA",
        "ESTADO_PLANTA",
        "ESTADO_PROYECTO",
        "RANGO_PROFUNDIDAD",
        "ANIO_CAMPANIA",
    ]
    candidates = []
    for column in df.columns:
        unique_count = df[column].dropna().nunique()
        if 2 <= unique_count <= 20 and (df[column].dtype == "object" or str(df[column].dtype) == "category"):
            candidates.append(column)

    ordered = [column for column in preferred if column in candidates]
    ordered.extend(column for column in candidates if column not in ordered)
    return ordered


def fig_relationship_map(df: pd.DataFrame) -> go.Figure | None:
    relation_columns = get_relation_columns(df)
    if len(relation_columns) < 2:
        return None

    source_col, target_col = relation_columns[:2]
    relation_df = (
        df[[source_col, target_col]]
        .dropna()
        .astype(str)
        .groupby([source_col, target_col], as_index=False)
        .size()
        .sort_values("size", ascending=False)
        .head(20)
    )
    if relation_df.empty:
        return None

    source_labels = [f"{source_col}: {value}" for value in relation_df[source_col].unique()]
    target_labels = [f"{target_col}: {value}" for value in relation_df[target_col].unique()]
    labels = source_labels + [label for label in target_labels if label not in source_labels]
    label_index = {label: idx for idx, label in enumerate(labels)}

    fig = go.Figure(
        go.Sankey(
            node=dict(
                pad=18,
                thickness=18,
                line=dict(color="rgba(148,163,184,0.25)", width=1),
                label=labels,
                color=[PRIMARY] * len(source_labels) + [ACCENT] * (len(labels) - len(source_labels)),
            ),
            link=dict(
                source=[label_index[f"{source_col}: {value}"] for value in relation_df[source_col]],
                target=[label_index[f"{target_col}: {value}"] for value in relation_df[target_col]],
                value=relation_df["size"],
                color="rgba(103,232,249,0.28)",
            ),
        )
    )
    fig.update_layout(
        title=f"Mapa automatico de relaciones: {source_col} -> {target_col}",
        height=520,
        font=dict(color=TEXT),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def render_executive_tab(df: pd.DataFrame) -> None:
    c1, c2 = st.columns([1.05, 0.95])
    with c1:
        st.plotly_chart(fig_missing(df), use_container_width=True)
    with c2:
        if "PROFUNDIDADTOTAL" in df.columns:
            st.plotly_chart(fig_depth_distribution(df), use_container_width=True)
        else:
            st.info("No hay columna PROFUNDIDADTOTAL disponible")

    # Mostrar gráficos de categorías si existen las columnas
    if "PROYECTODESECUNDARIA" in df.columns or "MAPA_PROYECTO" in df.columns:
        c3, c4 = st.columns(2)
        with c3:
            col_name = "MAPA_PROYECTO" if "MAPA_PROYECTO" in df.columns else "PROYECTODESECUNDARIA"
            st.plotly_chart(fig_top_categories(df, col_name, "Top proyectos"), use_container_width=True)
        with c4:
            if "PLANTADEINYECCIONDEAGUA" in df.columns:
                st.plotly_chart(fig_top_categories(df, "PLANTADEINYECCIONDEAGUA", "Top plantas"), use_container_width=True)


def render_numeric_tab(df: pd.DataFrame) -> None:
    cols_for_desc = [col for col in ["PROFUNDIDADTOTAL", "LONGITUD", "LATITUD", "ANIO_CAMPANIA", "ANIO_PUESTA_MARCHA"] 
                     if col in df.columns]
    
    if not cols_for_desc:
        st.info("No hay columnas numéricas disponibles para análisis")
        return
    
    # Gráfico de profundidad por proyecto (si existen ambas columnas)
    c1, c2 = st.columns([1.15, 0.85])
    with c1:
        if "PROFUNDIDADTOTAL" in df.columns and ("MAPA_PROYECTO" in df.columns or "PROYECTODESECUNDARIA" in df.columns):
            st.plotly_chart(fig_depth_by_project(df), use_container_width=True)
    
    with c2:
        if cols_for_desc:
            desc = df[cols_for_desc].describe().T.round(2)
            st.dataframe(desc, use_container_width=True, height=470)

    # Matriz de correlación si hay al menos 2 columnas numéricas
    numeric = df[cols_for_desc].dropna(how="all")
    if not numeric.empty and len(cols_for_desc) >= 2:
        corr = numeric.corr(numeric_only=True)
        if not corr.empty:
            fig = px.imshow(
                corr,
                text_auto=".2f",
                aspect="auto",
                color_continuous_scale="RdBu_r",
                title="Matriz de correlacion",
            )
            fig.update_layout(height=420)
            st.plotly_chart(apply_dark_layout(fig), use_container_width=True)


def render_temporal_tab(df: pd.DataFrame) -> None:
    # Solo mostrar si existen las columnas temporales
    if "ANIO_CAMPANIA" not in df.columns and "ANIO_PUESTA_MARCHA" not in df.columns:
        st.info("No hay columnas temporales disponibles")
        return
    
    c1, c2 = st.columns([1.2, 0.8])
    with c1:
        if "ANIO_CAMPANIA" in df.columns or "ANIO_PUESTA_MARCHA" in df.columns:
            st.plotly_chart(fig_campaign_vs_startup(df), use_container_width=True)
    with c2:
        if "ANIO_CAMPANIA" in df.columns and "RANGO_PROFUNDIDAD" in df.columns:
            st.plotly_chart(fig_depth_heatmap(df), use_container_width=True)

    if "ANIO_PUESTA_MARCHA" in df.columns:
        puesta = df["ANIO_PUESTA_MARCHA"].dropna().astype(int).value_counts().sort_index().reset_index()
        if not puesta.empty:
            puesta.columns = ["Ano", "Cantidad"]
            puesta["Acumulado"] = puesta["Cantidad"].cumsum()
            fig = px.area(
                puesta,
                x="Ano",
                y="Acumulado",
                title="Evolucion acumulada de pozos con puesta en marcha",
                color_discrete_sequence=[PRIMARY],
            )
            fig.update_layout(height=360)
            st.plotly_chart(apply_dark_layout(fig), use_container_width=True)


def render_relations_tab(df: pd.DataFrame) -> None:
    relation_fig = fig_relationship_map(df)
    if relation_fig is None:
        st.info("No hay suficientes columnas categoricas compatibles para construir un mapa automatico de relaciones.")
        return

    st.plotly_chart(relation_fig, use_container_width=True)

    relation_columns = get_relation_columns(df)
    st.caption(
        "El grafico detecta automaticamente relaciones entre las dos columnas categoricas mas utiles del dataset filtrado: "
        f"{relation_columns[0]} y {relation_columns[1]}."
    )


def render_map_tab(df: pd.DataFrame, size_map: str) -> None:
    # Solo mostrar si existen coordenadas
    if "LATITUD" not in df.columns or "LONGITUD" not in df.columns:
        st.info("Este dataset no tiene coordenadas (LATITUD/LONGITUD)")
        return
    
    map_df = df[df["TIENE_COORDENADAS"]]
    if map_df.empty:
        st.warning("No hay coordenadas disponibles bajo la combinacion actual de filtros.")
        return

    st.caption("La leyenda del mapa sigue siempre el proyecto de secundaria. Los registros sin proyecto aparecen como Yacimiento.")
    st.plotly_chart(fig_map(df, size_map), use_container_width=True)

    summary = pd.DataFrame(
        {
            "Metrica": [
                "Pozos mapeados",
                "Latitud minima",
                "Latitud maxima",
                "Longitud minima",
                "Longitud maxima",
            ],
            "Valor": [
                fmt_int(len(map_df)),
                fmt_num(map_df["LATITUD"].min(), 4),
                fmt_num(map_df["LATITUD"].max(), 4),
                fmt_num(map_df["LONGITUD"].min(), 4),
                fmt_num(map_df["LONGITUD"].max(), 4),
            ],
        }
    )
    st.dataframe(summary, use_container_width=True, hide_index=True)


def render_data_tab(df: pd.DataFrame) -> None:
    c1, c2 = st.columns([0.9, 1.1])
    with c1:
        st.dataframe(quality_table(df), use_container_width=True, height=420, hide_index=True)
    with c2:
        st.dataframe(df, use_container_width=True, height=420)


def _normalized(column: str) -> str:
    return column.strip().upper().replace(" ", "_")


def is_categorical_candidate(column: str, series: pd.Series) -> bool:
    non_null = series.dropna()
    if non_null.empty:
        return False

    if str(series.dtype) not in {"object", "category", "bool"}:
        return False

    nunique = non_null.nunique()
    if nunique < 2:
        return False

    unique_ratio = nunique / max(len(non_null), 1)
    avg_len = non_null.astype(str).str.len().mean()
    normalized = _normalized(column)
    dimension_tokens = ["TIPO", "ESTADO", "CLASE", "AREA", "ZONA", "CAUSA", "MOTIVO", "NIVEL", "CAT", "GRUPO"]

    if any(token in normalized for token in dimension_tokens):
        return True

    if nunique <= 200 and avg_len <= 80:
        return True

    return unique_ratio <= 0.35 and avg_len <= 80


@st.cache_data(show_spinner=False)
def infer_schema(df: pd.DataFrame) -> dict:
    df = df.copy()
    datetime_cols = list(df.select_dtypes(include=["datetime64[ns]", "datetimetz"]).columns)
    numeric_cols = list(df.select_dtypes(include=["number"]).columns)
    categorical_cols = []

    for column in df.columns:
        series = df[column]
        normalized = _normalized(column)

        if column not in datetime_cols and (
            "FECHA" in normalized or "DATE" in normalized or normalized.endswith("_AT")
        ):
            parsed = pd.to_datetime(series, errors="coerce")
            if parsed.notna().mean() >= 0.6:
                df[column] = parsed
                datetime_cols.append(column)
                continue

        if column not in numeric_cols and series.dtype == "object":
            numeric_candidate = pd.to_numeric(series, errors="coerce")
            if numeric_candidate.notna().mean() >= 0.8:
                df[column] = numeric_candidate
                numeric_cols.append(column)
                continue

        if column not in datetime_cols and column not in numeric_cols and is_categorical_candidate(column, series):
            categorical_cols.append(column)

    lat_candidates = [
        column for column in numeric_cols if any(token in _normalized(column) for token in ["LAT", "LATITUD"])
    ]
    lon_candidates = [
        column for column in numeric_cols if any(token in _normalized(column) for token in ["LON", "LONG", "LONGITUD"])
    ]
    id_candidates = [
        column
        for column in df.columns
        if any(token in _normalized(column) for token in ["TAG", "ID", "IDENT", "COD", "CODIGO"])
    ]

    return {
        "datetime_cols": list(dict.fromkeys(datetime_cols)),
        "numeric_cols": list(dict.fromkeys(numeric_cols)),
        "categorical_cols": list(dict.fromkeys(categorical_cols)),
        "lat_col": lat_candidates[0] if lat_candidates else None,
        "lon_col": lon_candidates[0] if lon_candidates else None,
        "id_col": id_candidates[0] if id_candidates else None,
        "primary_numeric": numeric_cols[0] if numeric_cols else None,
        "primary_datetime": datetime_cols[0] if datetime_cols else None,
        "primary_category": categorical_cols[0] if categorical_cols else None,
    }


@st.cache_data(show_spinner=False)
def load_data_from_path(file_path: str) -> pd.DataFrame:
    path = Path(file_path)
    if path.suffix.lower() == ".parquet":
        df = pd.read_parquet(path)
    elif path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    else:
        st.error(f"Formato no soportado: {path.suffix}")
        st.stop()

    df = df.copy()
    df["SOURCE_FILE"] = path.name
    df = df.drop_duplicates()
    schema = infer_schema(df)

    for column in schema["datetime_cols"]:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors="coerce")

    for column in schema["numeric_cols"]:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    if schema["lat_col"] and schema["lon_col"]:
        df["TIENE_COORDENADAS"] = df[schema["lat_col"]].notna() & df[schema["lon_col"]].notna()
    else:
        df["TIENE_COORDENADAS"] = False

    return df


@st.cache_data(show_spinner=False)
def load_uploaded_csv(file_bytes: bytes, file_name: str) -> pd.DataFrame:
    df = pd.read_csv(pd.io.common.BytesIO(file_bytes))
    df = df.copy()
    df["SOURCE_FILE"] = file_name
    df = df.drop_duplicates()
    schema = infer_schema(df)

    for column in schema["datetime_cols"]:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors="coerce")

    for column in schema["numeric_cols"]:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    if schema["lat_col"] and schema["lon_col"]:
        df["TIENE_COORDENADAS"] = df[schema["lat_col"]].notna() & df[schema["lon_col"]].notna()
    else:
        df["TIENE_COORDENADAS"] = False

    return df


@st.cache_data(show_spinner=False)
def load_reference_table_from_path(file_path: str) -> pd.DataFrame:
    path = Path(file_path)
    if path.suffix.lower() == ".parquet":
        return pd.read_parquet(path)
    return pd.read_csv(path)


@st.cache_data(show_spinner=False)
def load_reference_table_from_upload(file_bytes: bytes, file_name: str) -> pd.DataFrame:
    if file_name.lower().endswith(".parquet"):
        return pd.read_parquet(pd.io.common.BytesIO(file_bytes))
    return pd.read_csv(pd.io.common.BytesIO(file_bytes))


@st.cache_data(show_spinner=False)
def load_geojson_from_path(file_path: str) -> dict:
    return json.loads(Path(file_path).read_text(encoding="utf-8"))


@st.cache_data(show_spinner=False)
def load_geojson_from_upload(file_bytes: bytes) -> dict:
    return json.loads(file_bytes.decode("utf-8"))


def get_available_local_files() -> list[dict]:
    files = []
    seen_paths = set()

    for input_dir in INPUT_DIRS:
        if not input_dir.exists():
            continue
        for file in sorted(input_dir.rglob("*")):
            resolved = file.resolve()
            if not file.is_file() or file.suffix.lower() not in {".csv", ".parquet"} or resolved in seen_paths:
                continue
            seen_paths.add(resolved)
            try:
                label = str(file.relative_to(REPO_ROOT))
            except ValueError:
                label = str(file.relative_to(BASE_DIR))
            files.append(
                {
                    "label": label,
                    "name": file.name,
                    "path": file,
                    "origin": "input",
                    "type": file.suffix.lower().replace(".", "").upper(),
                }
            )

    if PARQUET_DIR.exists():
        for file in sorted(PARQUET_DIR.rglob("*")):
            resolved = file.resolve()
            if file.is_file() and file.suffix.lower() in {".csv", ".parquet"} and resolved not in seen_paths:
                seen_paths.add(resolved)
                try:
                    label = str(file.relative_to(REPO_ROOT))
                except ValueError:
                    label = str(file.relative_to(BASE_DIR))
                files.append(
                    {
                        "label": label,
                        "name": file.name,
                        "path": file,
                        "origin": "output_parquet",
                        "type": file.suffix.lower().replace(".", "").upper(),
                    }
                )

    return files


def get_available_geojson_files() -> list[dict]:
    files = []
    seen_paths = set()

    for input_dir in INPUT_DIRS:
        if not input_dir.exists():
            continue
        for file in sorted(input_dir.rglob("*")):
            resolved = file.resolve()
            if not file.is_file() or file.suffix.lower() not in {".json", ".geojson"} or resolved in seen_paths:
                continue
            seen_paths.add(resolved)
            try:
                label = str(file.relative_to(REPO_ROOT))
            except ValueError:
                label = str(file.relative_to(BASE_DIR))
            files.append({"label": label, "path": file})

    return files


def get_local_catalog(local_files: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Archivo": item["label"],
                "Origen": item["origin"],
                "Tipo": item["type"],
                "Tamano": fmt_file_size(item["path"].stat().st_size),
                "Modificado": pd.to_datetime(item["path"].stat().st_mtime, unit="s").strftime("%d/%m/%Y %H:%M"),
            }
            for item in local_files
        ]
    )


def build_file_selector(local_files: list[dict], local_catalog: pd.DataFrame, loading_placeholder=None) -> dict:
    st.sidebar.markdown("## Panel de control")
    st.sidebar.caption("Elige un archivo de `input/` de la raiz del repo o de `work/EDA/input/`, tambien dentro de subcarpetas, o sube un CSV.")
    st.sidebar.markdown("### Fuente de datos")
    st.sidebar.info(f"Archivos locales disponibles: {len(local_files)}")

    if st.sidebar.button("Actualizar lista de archivos", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    source_mode = st.sidebar.radio(
        "Origen",
        options=["Archivo local", "Subir CSV"],
        key="data_source_mode",
    )
    previous_source = st.session_state.get("applied_data_source")
    selected_item = None

    if source_mode == "Archivo local":
        if not local_files:
            st.sidebar.warning("No hay archivos locales en `input/`, `work/EDA/input/` ni en `data/output_parquet/`, incluyendo subcarpetas.")
            uploaded_file = None
        else:
            default_item = max(local_files, key=lambda item: item["path"].stat().st_mtime)
            options = [item["label"] for item in local_files]
            selected_label = st.sidebar.selectbox(
                "Selecciona un archivo para analizar",
                options=options,
                index=options.index(default_item["label"]),
                key="single_file_selector",
                help="Puedes elegir archivos CSV o parquet",
            )
            selected_item = next(item for item in local_files if item["label"] == selected_label)
            previous_file = st.session_state.get("applied_selected_file")
            if previous_source != source_mode or previous_file != selected_label:
                if previous_file is not None or previous_source is not None:
                    reset_state_for_new_file()
                st.session_state["file_changed_this_run"] = True
                trigger_loader()
                if loading_placeholder is not None:
                    show_loading(loading_placeholder, f"Cargando {selected_label}...")
                st.session_state["applied_selected_file"] = selected_label
                st.session_state["applied_data_source"] = source_mode
                st.rerun()
            st.sidebar.caption(f"Mostrando 1 de {len(local_files)} archivos locales")
            uploaded_file = None
    else:
        uploaded_file = st.sidebar.file_uploader(
            "Sube un archivo CSV",
            type=["csv"],
            key="csv_uploader",
            help="Carga un CSV desde tu equipo para analizarlo en la app",
        )
        uploaded_name = uploaded_file.name if uploaded_file is not None else None
        previous_file = st.session_state.get("applied_selected_file")
        if previous_source != source_mode or previous_file != uploaded_name:
            if previous_file is not None or previous_source is not None:
                reset_state_for_new_file()
            st.session_state["file_changed_this_run"] = True
            st.session_state["applied_selected_file"] = uploaded_name
            st.session_state["applied_data_source"] = source_mode

    if not local_catalog.empty:
        st.sidebar.dataframe(local_catalog, use_container_width=True, hide_index=True, height=220)

    st.sidebar.markdown("---")
    return {
        "source_mode": source_mode,
        "uploaded_file": uploaded_file,
        "selected_item": selected_item if source_mode == "Archivo local" and local_files else None,
    }


def build_sidebar(df: pd.DataFrame, selected_file: str) -> tuple[pd.DataFrame, str]:
    schema = infer_schema(df)
    export_slot = st.sidebar.empty()

    st.sidebar.markdown("### Filtros del EDA")
    st.sidebar.caption("Ajusta los controles y aplica los cambios cuando quieras recalcular.")

    applied_filters_key = f"applied_sidebar_filters::{selected_file}"
    if applied_filters_key not in st.session_state or st.session_state.get("file_changed_this_run", False):
        initial_filters = {}
        for column in schema["categorical_cols"][:4]:
            options = sorted(df[column].dropna().astype(str).unique().tolist())
            if options:
                initial_filters[f"filter_{column}"] = ()
        for column in schema["numeric_cols"][:3]:
            numeric_series = pd.to_numeric(df[column], errors="coerce").dropna()
            if not numeric_series.empty:
                initial_filters[f"range_{column}"] = (float(numeric_series.min()), float(numeric_series.max()))
        initial_filters["coord_check"] = False
        initial_filters["size_map_select"] = "Constante"
        st.session_state[applied_filters_key] = initial_filters.copy()

    applied_filters = st.session_state[applied_filters_key]

    for column in schema["categorical_cols"][:4]:
        widget_key = f"filter_{column}"
        if widget_key not in st.session_state:
            st.session_state[widget_key] = list(applied_filters.get(widget_key, ()))

    for column in schema["numeric_cols"][:3]:
        widget_key = f"range_{column}"
        numeric_series = pd.to_numeric(df[column], errors="coerce").dropna()
        if numeric_series.empty:
            continue
        current_bounds = (float(numeric_series.min()), float(numeric_series.max()))
        if widget_key not in st.session_state:
            st.session_state[widget_key] = applied_filters.get(widget_key, current_bounds)

    if "coord_check" not in st.session_state:
        st.session_state["coord_check"] = applied_filters.get("coord_check", False)
    if "size_map_select" not in st.session_state:
        st.session_state["size_map_select"] = applied_filters.get("size_map_select", "Constante")

    with st.sidebar.form(key=f"sidebar_filters_form::{selected_file}"):
        for column in schema["categorical_cols"][:4]:
            options = sorted(df[column].dropna().astype(str).unique().tolist())
            if not options:
                continue
            st.multiselect(f"{column}", options=options, key=f"filter_{column}")

        for column in schema["numeric_cols"][:3]:
            numeric_series = pd.to_numeric(df[column], errors="coerce")
            series = numeric_series.dropna()
            if series.empty:
                continue
            col_min = float(series.min())
            col_max = float(series.max())
            if col_min == col_max:
                st.caption(f"{column} fijo: {fmt_num(col_min, 2)}")
                continue
            st.slider(
                column,
                min_value=float(col_min),
                max_value=float(col_max),
                value=st.session_state.get(f"range_{column}", (float(col_min), float(col_max))),
                key=f"range_{column}",
            )

        size_map_options = ["Constante"] + schema["numeric_cols"][:5]
        if schema["lat_col"] and schema["lon_col"]:
            st.checkbox("Solo registros con coordenadas", key="coord_check")
            st.selectbox(
                "Tamano del punto en el mapa",
                options=size_map_options,
                key="size_map_select",
            )
        submitted = st.form_submit_button("Aplicar filtros", use_container_width=True, on_click=trigger_loader)

    if submitted:
        current_filters = {}
        for column in schema["categorical_cols"][:4]:
            current_filters[f"filter_{column}"] = tuple(st.session_state.get(f"filter_{column}", []))
        for column in schema["numeric_cols"][:3]:
            numeric_series = pd.to_numeric(df[column], errors="coerce").dropna()
            if not numeric_series.empty:
                current_filters[f"range_{column}"] = tuple(st.session_state.get(f"range_{column}", (float(numeric_series.min()), float(numeric_series.max()))))
        current_filters["coord_check"] = bool(st.session_state.get("coord_check", False))
        current_filters["size_map_select"] = st.session_state.get("size_map_select", "Constante")
        st.session_state[applied_filters_key] = current_filters.copy()
        st.rerun()
    filtered = df.copy()
    for column in schema["categorical_cols"][:4]:
        selected = applied_filters.get(f"filter_{column}", ())
        if selected:
            filtered = filtered[filtered[column].astype(str).isin(selected)]

    for column in schema["numeric_cols"][:3]:
        numeric_series = pd.to_numeric(filtered[column], errors="coerce")
        series = numeric_series.dropna()
        if series.empty:
            continue
        col_min = float(series.min())
        selected_range = applied_filters.get(f"range_{column}", None)
        if selected_range is None:
            continue
        filtered = filtered[numeric_series.fillna(col_min).between(selected_range[0], selected_range[1])]

    size_map = applied_filters.get("size_map_select", "Constante")
    if applied_filters.get("coord_check", False):
        filtered = filtered[filtered["TIENE_COORDENADAS"]]

    export_slot.markdown("### Exportar")
    add_download(filtered, target=export_slot)
    st.sidebar.markdown("---")
    return filtered, size_map


def render_header(df: pd.DataFrame, schema: dict, selected_files: list, total_files: int) -> None:
    st.markdown(
        f"""
        <div class="hero">
            <h1>EDA generico de datasets</h1>
            <p>
                Exploracion interactiva adaptable al esquema del archivo seleccionado. El tablero detecta
                automaticamente variables numericas, categoricas, temporales y geograficas cuando existan.
            </p>
            <p class="small-note">Archivo activo: {selected_files[0] if selected_files else "Ninguno"} | Archivos locales detectados: {total_files} | Registros: {fmt_int(len(df))}</p>
            <p class="small-note">Columnas: {fmt_int(len(df.columns))} | Numericas: {fmt_int(len(schema["numeric_cols"]))} | Categoricas: {fmt_int(len(schema["categorical_cols"]))} | Fechas: {fmt_int(len(schema["datetime_cols"]))}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpis(df: pd.DataFrame, schema: dict) -> None:
    total = len(df)
    missing_ratio = df.isna().mean().mean() * 100 if total and len(df.columns) else 0
    applied_exec = st.session_state.get("applied_executive_settings", {})
    selected_numeric = applied_exec.get("numeric", schema["primary_numeric"])
    cols = st.columns(5)
    cols[0].metric("Registros", fmt_int(total))
    cols[1].metric("Columnas", fmt_int(len(df.columns)))
    cols[2].metric("Cobertura media", pct(100 - missing_ratio))
    cols[3].metric("Numericas", fmt_int(len(schema["numeric_cols"])))
    cols[4].metric("Categoricas", fmt_int(len(schema["categorical_cols"])))

    if selected_numeric in df.columns:
        numeric_series = df[selected_numeric].dropna()
        if not numeric_series.empty:
            extra = st.columns(3)
            extra[0].metric(f"Media {selected_numeric}", fmt_num(numeric_series.mean()))
            extra[1].metric(f"P75 {selected_numeric}", fmt_num(numeric_series.quantile(0.75)))
            extra[2].metric(f"Max {selected_numeric}", fmt_num(numeric_series.max()))


def render_insights(df: pd.DataFrame, schema: dict, quality_df: pd.DataFrame) -> None:
    insights = []

    if schema["primary_category"]:
        top_values = df[schema["primary_category"]].astype(str).value_counts()
        if not top_values.empty:
            insights.append(
                (
                    "Categoria dominante",
                    f"La categoria mas frecuente en <b>{schema['primary_category']}</b> es <b>{top_values.index[0]}</b> con <b>{fmt_int(top_values.iloc[0])}</b> registros.",
                )
            )

    if not quality_df.empty:
        top_missing = quality_df.iloc[0]
        insights.append(
            (
                "Calidad de datos",
                f"La columna con mas faltantes es <b>{top_missing['Columna']}</b> con cobertura de <b>{pct(top_missing['Cobertura %'])}</b>.",
            )
        )

    if schema["primary_datetime"]:
        latest = df[schema["primary_datetime"]].dropna().max()
        earliest = df[schema["primary_datetime"]].dropna().min()
        if pd.notna(latest) and pd.notna(earliest):
            insights.append(
                (
                    "Ventana temporal",
                    f"El rango detectado en <b>{schema['primary_datetime']}</b> va de <b>{earliest.strftime('%d/%m/%Y')}</b> a <b>{latest.strftime('%d/%m/%Y')}</b>.",
                )
            )

    if not insights:
        st.info("No hay suficiente informacion para construir insights automaticos.")
        return

    cols = st.columns(len(insights))
    for idx, (title, text) in enumerate(insights):
        with cols[idx]:
            st.markdown(
                f"""
                <div class="insight">
                    <h4>{title}</h4>
                    <p>{text}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def fig_distribution(df: pd.DataFrame, column: str) -> go.Figure:
    fig = px.histogram(
        df,
        x=column,
        nbins=40,
        marginal="box",
        opacity=0.9,
        color_discrete_sequence=[PRIMARY],
        title=f"Distribucion de {column}",
    )
    fig.update_layout(xaxis_title=column, yaxis_title="Cantidad", bargap=0.03, height=430)
    return apply_dark_layout(fig)


def fig_box_by_category(df: pd.DataFrame, numeric_col: str, category_col: str) -> go.Figure:
    top_categories = df[category_col].astype(str).value_counts().head(10).index
    subset = df[df[category_col].astype(str).isin(top_categories)].copy()
    fig = px.box(
        subset,
        x=category_col,
        y=numeric_col,
        color=category_col,
        color_discrete_sequence=PALETTE,
        points="outliers",
        title=f"{numeric_col} por {category_col}",
    )
    fig.update_layout(showlegend=False, xaxis_title=category_col, yaxis_title=numeric_col, height=470)
    return apply_dark_layout(fig)


def fig_time_series(df: pd.DataFrame, datetime_col: str) -> go.Figure:
    datetime_series = coerce_datetime_series(df[datetime_col])
    timeline = (
        datetime_series
        .dropna()
        .dt.to_period("M")
        .astype(str)
        .value_counts()
        .sort_index()
        .reset_index()
    )
    timeline.columns = ["Periodo", "Cantidad"]
    fig = px.line(timeline, x="Periodo", y="Cantidad", markers=True, title=f"Evolucion temporal de {datetime_col}")
    fig.update_layout(height=430, xaxis_title="Periodo", yaxis_title="Cantidad")
    return apply_dark_layout(fig)


def fig_time_series_metric(
    df: pd.DataFrame,
    datetime_col: str,
    freq: str,
    metric_mode: str,
    value_col: str | None = None,
    agg_func: str = "sum",
) -> go.Figure:
    base = df[[datetime_col] + ([value_col] if value_col else [])].dropna(subset=[datetime_col]).copy()
    base[datetime_col] = coerce_datetime_series(base[datetime_col])
    base = base.dropna(subset=[datetime_col])
    if base.empty:
        return go.Figure()

    period = base[datetime_col].dt.to_period(freq).dt.to_timestamp()
    if metric_mode == "Cantidad de registros" or not value_col:
        grouped = period.value_counts().sort_index().reset_index()
        grouped.columns = ["Periodo", "Valor"]
        y_title = "Cantidad"
    else:
        grouped = (
            base.assign(Periodo=period)
            .groupby("Periodo", as_index=False)[value_col]
            .agg(agg_func)
            .rename(columns={value_col: "Valor"})
        )
        y_title = f"{agg_func} de {value_col}"

    fig = px.line(grouped, x="Periodo", y="Valor", markers=True, title=f"Analisis temporal de {datetime_col}")
    fig.update_layout(height=430, xaxis_title="Periodo", yaxis_title=y_title)
    fig.update_xaxes(rangeslider_visible=True)
    return apply_dark_layout(fig)


@st.cache_data(show_spinner=False)
def temporal_breakdown_table(
    df: pd.DataFrame,
    datetime_col: str,
    freq: str,
    category_col: str,
    metric_mode: str,
    value_col: str | None = None,
    agg_func: str = "sum",
    selected_values: tuple[str, ...] = (),
) -> pd.DataFrame:
    required_cols = [datetime_col, category_col]
    if metric_mode != "Cantidad de registros" and value_col:
        required_cols.append(value_col)

    base = df[required_cols].copy()
    base[datetime_col] = coerce_datetime_series(base[datetime_col])
    base = base.dropna(subset=[datetime_col])
    if base.empty:
        return pd.DataFrame()

    base[category_col] = base[category_col].fillna("Sin dato").astype(str)
    if selected_values:
        base = base[base[category_col].isin(selected_values)]
    if base.empty:
        return pd.DataFrame()

    base["Periodo"] = base[datetime_col].dt.to_period(freq).astype(str)

    if metric_mode == "Cantidad de registros" or not value_col:
        grouped = base.groupby(["Periodo", category_col]).size().reset_index(name="Valor")
    else:
        base[value_col] = pd.to_numeric(base[value_col], errors="coerce")
        base = base.dropna(subset=[value_col])
        if base.empty:
            return pd.DataFrame()
        grouped = (
            base.groupby(["Periodo", category_col], as_index=False)[value_col]
            .agg(agg_func)
            .rename(columns={value_col: "Valor"})
        )

    pivot = grouped.pivot(index="Periodo", columns=category_col, values="Valor").fillna(0)
    if pivot.empty:
        return pd.DataFrame()

    pivot["Total"] = pivot.sum(axis=1)
    pivot = pivot.sort_index().reset_index()
    return pivot


def looks_like_key_column(column: str, series: pd.Series) -> bool:
    normalized = _normalized(column)
    key_tokens = ["ID", "TAG", "CODE", "COD", "IDENT", "UUID", "KEY", "CLAVE"]
    unique_ratio = series.nunique(dropna=True) / max(len(series.dropna()), 1)
    return any(token in normalized for token in key_tokens) or unique_ratio >= 0.85


@st.cache_data(show_spinner=False)
def load_parquet_profiles(parquet_dir: Path) -> dict:
    profiles = {}
    for file in sorted(parquet_dir.glob("*.parquet")):
        frame = pd.read_parquet(file)
        schema = infer_schema(frame.copy())
        comparable_columns = []
        value_sets = {}
        key_like_columns = []

        for column in frame.columns:
            unique_count = frame[column].dropna().nunique()
            if 1 < unique_count <= 300:
                comparable_columns.append(column)
                value_sets[column] = set(frame[column].dropna().astype(str).unique().tolist())
            if looks_like_key_column(column, frame[column]):
                key_like_columns.append(column)

        profiles[file.name] = {
            "columns": list(frame.columns),
            "row_count": len(frame),
            "schema": schema,
            "comparable_columns": comparable_columns,
            "value_sets": value_sets,
            "key_like_columns": key_like_columns,
        }
    return profiles


@st.cache_data(show_spinner=False)
def parquet_relationships_table(parquet_profiles: dict, parquet_a: str, parquet_b: str) -> pd.DataFrame:
    profile_a = parquet_profiles[parquet_a]
    profile_b = parquet_profiles[parquet_b]
    shared_columns = sorted(set(profile_a["columns"]).intersection(profile_b["columns"]))
    rows = []

    for column in shared_columns:
        set_a = profile_a["value_sets"].get(column, set())
        set_b = profile_b["value_sets"].get(column, set())
        if set_a and set_b:
            intersection_size = len(set_a.intersection(set_b))
            union_size = len(set_a.union(set_b))
            overlap_pct = (intersection_size / union_size * 100) if union_size else 0
        else:
            intersection_size = 0
            overlap_pct = 0

        rows.append(
            {
                "Columna": column,
                "Posible ID": "Si" if column in profile_a["key_like_columns"] or column in profile_b["key_like_columns"] else "No",
                "Coincidencias": intersection_size,
                "Overlap %": round(overlap_pct, 1),
                "Valores unicos A": len(set_a),
                "Valores unicos B": len(set_b),
            }
        )

    relation_df = pd.DataFrame(rows)
    if relation_df.empty:
        return relation_df
    return relation_df.sort_values(["Coincidencias", "Overlap %", "Columna"], ascending=[False, False, True])


def fig_parquet_relationships(relation_df: pd.DataFrame, parquet_a: str, parquet_b: str) -> go.Figure:
    top_rel = relation_df.head(12).sort_values("Coincidencias")
    fig = px.bar(
        top_rel,
        x="Coincidencias",
        y="Columna",
        orientation="h",
        color="Overlap %",
        text="Overlap %",
        color_continuous_scale=["#1E293B", PRIMARY],
        title=f"Relaciones detectadas entre {parquet_a} y {parquet_b}",
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_layout(height=460, xaxis_title="Valores compartidos", yaxis_title="", coloraxis_showscale=False)
    return apply_dark_layout(fig)


@st.cache_data(show_spinner=False)
def summarize_by_category(df: pd.DataFrame, category_col: str, numeric_cols: tuple[str, ...]) -> pd.DataFrame:
    base = df.copy()
    base[category_col] = base[category_col].fillna("Sin dato").astype(str)
    agg_map = {col: ["sum", "mean"] for col in numeric_cols}
    summary = base.groupby(category_col).agg(agg_map)
    summary.columns = [f"{col} | {'suma' if stat == 'sum' else 'media'}" for col, stat in summary.columns]
    summary = summary.reset_index()

    counts = base.groupby(category_col).size().reset_index(name="Cantidad")
    summary = counts.merge(summary, on=category_col, how="left")
    return summary.sort_values("Cantidad", ascending=False)


def fig_category_distribution(df: pd.DataFrame, category_col: str) -> go.Figure:
    top_df = (
        df[category_col]
        .fillna("Sin dato")
        .astype(str)
        .value_counts()
        .head(15)
        .sort_values()
        .rename_axis("Categoria")
        .reset_index(name="Cantidad")
    )
    fig = px.bar(
        top_df,
        x="Cantidad",
        y="Categoria",
        orientation="h",
        text="Cantidad",
        color="Cantidad",
        color_continuous_scale=["#1E293B", PRIMARY],
        title=f"Distribucion de {category_col}",
    )
    fig.update_layout(height=460, xaxis_title="Cantidad", yaxis_title="", coloraxis_showscale=False)
    return apply_dark_layout(fig)


def fig_numeric_by_category(df: pd.DataFrame, category_col: str, numeric_col: str, agg_func: str) -> go.Figure:
    grouped = (
        df[[category_col, numeric_col]]
        .dropna(subset=[category_col])
        .assign(**{category_col: lambda x: x[category_col].astype(str)})
        .groupby(category_col, as_index=False)[numeric_col]
        .agg(agg_func)
        .sort_values(numeric_col, ascending=False)
        .head(15)
        .sort_values(numeric_col)
    )
    fig = px.bar(
        grouped,
        x=numeric_col,
        y=category_col,
        orientation="h",
        text=numeric_col,
        color=numeric_col,
        color_continuous_scale=["#1E293B", ACCENT],
        title=f"{agg_func} de {numeric_col} por {category_col}",
    )
    fig.update_layout(height=460, xaxis_title=f"{agg_func} de {numeric_col}", yaxis_title="", coloraxis_showscale=False)
    return apply_dark_layout(fig)


def aggregate_numeric(series: pd.Series, agg_func: str) -> float:
    if series.empty:
        return 0.0
    if agg_func == "sum":
        return float(series.sum())
    if agg_func == "mean":
        return float(series.mean())
    if agg_func == "median":
        return float(series.median())
    if agg_func == "max":
        return float(series.max())
    if agg_func == "min":
        return float(series.min())
    return float(series.sum())


def coerce_datetime_series(series: pd.Series) -> pd.Series:
    if pd.api.types.is_datetime64_any_dtype(series):
        return pd.to_datetime(series, errors="coerce")

    parsed = pd.to_datetime(series, errors="coerce")
    if parsed.notna().mean() >= 0.6:
        return parsed

    numeric_candidate = pd.to_numeric(series, errors="coerce")
    if numeric_candidate.notna().mean() >= 0.6:
        parsed_numeric = pd.to_datetime(numeric_candidate.astype("Int64").astype(str), format="%Y%m%d", errors="coerce")
        if parsed_numeric.notna().mean() >= 0.6:
            return parsed_numeric

    return pd.to_datetime(series, errors="coerce")


def fig_map_coordinates(
    df: pd.DataFrame,
    lat_col: str,
    lon_col: str,
    size_col: str,
    color_col: str,
    hover_name: str | None,
) -> go.Figure:
    map_df = df.copy()
    map_df[lat_col] = pd.to_numeric(map_df[lat_col], errors="coerce")
    map_df[lon_col] = pd.to_numeric(map_df[lon_col], errors="coerce")
    map_df = map_df.dropna(subset=[lat_col, lon_col])
    if map_df.empty:
        return go.Figure()

    if size_col == "Constante" or size_col not in map_df.columns:
        map_df["SIZE_VALUE"] = 10
    else:
        base = pd.to_numeric(map_df[size_col], errors="coerce")
        fill_value = float(base.dropna().median()) if base.notna().any() else 0.0
        base = base.fillna(fill_value)
        map_df["SIZE_VALUE"] = 10 if float(base.max()) == float(base.min()) else 8 + ((base - base.min()) / (base.max() - base.min()) * 20)

    hover_columns = [column for column in [hover_name, color_col, lat_col, lon_col, size_col] if column and column in map_df.columns]
    hover_data = {column: True for column in hover_columns if column != hover_name}
    hover_data["SIZE_VALUE"] = False

    color_arg = color_col if color_col != "Sin color" and color_col in map_df.columns else None
    fig = px.scatter_map(
        map_df,
        lat=lat_col,
        lon=lon_col,
        color=color_arg,
        size="SIZE_VALUE",
        size_max=26,
        hover_name=hover_name if hover_name and hover_name in map_df.columns else None,
        hover_data=hover_data,
        zoom=3.5,
        height=720,
        color_discrete_sequence=PALETTE,
        title=f"Distribucion espacial ({lat_col}, {lon_col})",
    )
    fig.update_layout(margin=dict(l=0, r=0, t=60, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig


def fig_map_locations(
    df: pd.DataFrame,
    location_col: str,
    location_mode: str,
    color_col: str,
    hover_name: str | None,
) -> go.Figure:
    base = df.copy()
    base[location_col] = base[location_col].fillna("").astype(str).str.strip()
    base = base[base[location_col] != ""]
    if base.empty:
        return go.Figure()

    if color_col != "Conteo" and color_col in base.columns:
        values = pd.to_numeric(base[color_col], errors="coerce")
        base = base.assign(_map_value=values).dropna(subset=["_map_value"])
        if base.empty:
            return go.Figure()
        grouped = base.groupby(location_col, as_index=False)["_map_value"].mean()
        grouped = grouped.rename(columns={"_map_value": "Valor"})
        title = f"Mapa por ubicacion usando {location_col} y media de {color_col}"
    else:
        grouped = base.groupby(location_col, as_index=False).size().rename(columns={"size": "Valor"})
        title = f"Mapa por ubicacion usando {location_col}"

    fig = px.choropleth(
        grouped,
        locations=location_col,
        color="Valor",
        locationmode=location_mode,
        color_continuous_scale="Turbo",
        hover_name=location_col,
        height=720,
        title=title,
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=60, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        geo=dict(bgcolor="rgba(0,0,0,0)", showframe=False, showcoastlines=True, coastlinecolor="rgba(148,163,184,0.3)"),
    )
    return fig


def fig_map_geojson(
    df: pd.DataFrame,
    location_col: str,
    value_col: str,
    geojson_data: dict,
    feature_property: str,
    hover_name: str | None,
) -> go.Figure:
    base = df.copy()
    base[location_col] = base[location_col].fillna("").astype(str).str.strip()
    base = base[base[location_col] != ""]
    if base.empty:
        return go.Figure()

    if value_col != "Conteo" and value_col in base.columns:
        metric_series = pd.to_numeric(base[value_col], errors="coerce")
        base = base.assign(MAP_VALUE=metric_series).dropna(subset=["MAP_VALUE"])
        grouped = base.groupby(location_col, as_index=False)["MAP_VALUE"].mean().rename(columns={"MAP_VALUE": "Valor"})
    else:
        grouped = base.groupby(location_col, as_index=False).size().rename(columns={"size": "Valor"})

    features = geojson_data.get("features", [])
    if not features:
        return go.Figure()

    geometry_types = {feature.get("geometry", {}).get("type") for feature in features if feature.get("geometry")}
    point_only = geometry_types and geometry_types.issubset({"Point", "MultiPoint"})

    if point_only:
        rows = []
        for feature in features:
            properties = feature.get("properties", {})
            geometry = feature.get("geometry", {})
            coords = geometry.get("coordinates", [])
            if geometry.get("type") != "Point" or len(coords) < 2:
                continue
            rows.append(
                {
                    "GeoKey": str(properties.get(feature_property, "")).strip(),
                    "lon": coords[0],
                    "lat": coords[1],
                }
            )
        geo_df = pd.DataFrame(rows)
        if geo_df.empty:
            return go.Figure()
        merged = grouped.merge(geo_df, left_on=location_col, right_on="GeoKey", how="inner")
        if merged.empty:
            return go.Figure()
        merged["SIZE_VALUE"] = 10 if merged["Valor"].nunique() <= 1 else 8 + ((merged["Valor"] - merged["Valor"].min()) / (merged["Valor"].max() - merged["Valor"].min()) * 20)
        fig = px.scatter_geo(
            merged,
            lat="lat",
            lon="lon",
            size="SIZE_VALUE",
            color="Valor",
            hover_name=location_col if hover_name is None or hover_name not in merged.columns else hover_name,
            hover_data={location_col: True, "Valor": True, "SIZE_VALUE": False},
            color_continuous_scale="Turbo",
            projection="natural earth",
            height=720,
            title=f"Mapa con GeoJSON usando {location_col}",
        )
        fig.update_geos(bgcolor="rgba(0,0,0,0)", showcoastlines=True, coastlinecolor="rgba(148,163,184,0.3)")
        fig.update_layout(margin=dict(l=0, r=0, t=60, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        return fig

    fig = px.choropleth(
        grouped,
        geojson=geojson_data,
        locations=location_col,
        featureidkey=f"properties.{feature_property}",
        color="Valor",
        color_continuous_scale="Turbo",
        hover_name=location_col,
        height=720,
        title=f"Mapa con GeoJSON usando {location_col}",
    )
    fig.update_geos(fitbounds="locations", visible=False, bgcolor="rgba(0,0,0,0)")
    fig.update_layout(margin=dict(l=0, r=0, t=60, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig


def location_mode_diagnostics(series: pd.Series, location_mode: str) -> dict:
    values = series.dropna().astype(str).str.strip()
    values = values[values != ""]
    sample = values.drop_duplicates().head(8).tolist()
    if values.empty:
        return {"valid": False, "message": "La columna no tiene ubicaciones utilizables.", "sample": sample}

    alpha_ratio = values.str.contains(r"[A-Za-z]", regex=True).mean()
    digit_ratio = values.str.fullmatch(r"\d+").mean()

    if location_mode == "USA-states":
        valid_ratio = values.str.fullmatch(r"[A-Za-z]{2}").mean()
        valid = valid_ratio >= 0.7
        message = "Se esperan abreviaturas de 2 letras como CA, TX o NY."
    elif location_mode == "ISO-3":
        valid_ratio = values.str.fullmatch(r"[A-Za-z]{3}").mean()
        valid = valid_ratio >= 0.7
        message = "Se esperan codigos ISO-3 de 3 letras como ARG, USA o BRA."
    else:
        valid = alpha_ratio >= 0.5 and digit_ratio < 0.5
        valid_ratio = alpha_ratio
        message = "Se esperan nombres de paises como Argentina, Brazil o United States."

    if digit_ratio >= 0.7:
        message = (
            "La columna parece contener codigos numericos o IDs internos. "
            "Plotly no los puede ubicar automaticamente como paises o estados."
        )
        valid = False

    return {
        "valid": bool(valid),
        "valid_ratio": float(valid_ratio),
        "digit_ratio": float(digit_ratio),
        "message": message,
        "sample": sample,
    }


def get_relation_columns(df: pd.DataFrame) -> list[str]:
    schema = infer_schema(df)
    relation_columns = schema["categorical_cols"][:]
    for column in schema["numeric_cols"][:2]:
        binned_col = f"{column}__BIN"
        if df[column].dropna().nunique() >= 4:
            df[binned_col] = pd.qcut(df[column], q=min(4, df[column].dropna().nunique()), duplicates="drop").astype(str)
            relation_columns.append(binned_col)
    return relation_columns[:6]


def fig_relationship_map(df: pd.DataFrame) -> go.Figure | None:
    relation_columns = get_relation_columns(df.copy())
    if len(relation_columns) < 2:
        return None

    source_col, target_col = relation_columns[:2]
    relation_df = (
        df.copy()
        .assign(**({target_col: pd.qcut(df[target_col.replace("__BIN", "")], q=min(4, df[target_col.replace("__BIN", "")].dropna().nunique()), duplicates="drop").astype(str)} if target_col.endswith("__BIN") else {}))
        .assign(**({source_col: pd.qcut(df[source_col.replace("__BIN", "")], q=min(4, df[source_col.replace("__BIN", "")].dropna().nunique()), duplicates="drop").astype(str)} if source_col.endswith("__BIN") else {}))
        [[source_col, target_col]]
        .dropna()
        .astype(str)
        .groupby([source_col, target_col], as_index=False)
        .size()
        .sort_values("size", ascending=False)
        .head(20)
    )
    if relation_df.empty:
        return None

    source_labels = [f"{source_col}: {value}" for value in relation_df[source_col].unique()]
    target_labels = [f"{target_col}: {value}" for value in relation_df[target_col].unique()]
    labels = source_labels + [label for label in target_labels if label not in source_labels]
    label_index = {label: idx for idx, label in enumerate(labels)}

    fig = go.Figure(
        go.Sankey(
            node=dict(
                pad=18,
                thickness=18,
                line=dict(color="rgba(148,163,184,0.25)", width=1),
                label=labels,
                color=[PRIMARY] * len(source_labels) + [ACCENT] * (len(labels) - len(source_labels)),
            ),
            link=dict(
                source=[label_index[f"{source_col}: {value}"] for value in relation_df[source_col]],
                target=[label_index[f"{target_col}: {value}"] for value in relation_df[target_col]],
                value=relation_df["size"],
                color="rgba(103,232,249,0.28)",
            ),
        )
    )
    fig.update_layout(title=f"Mapa automatico de relaciones: {source_col} -> {target_col}", height=520, font=dict(color=TEXT), paper_bgcolor="rgba(0,0,0,0)")
    return fig


def render_executive_tab(df: pd.DataFrame) -> None:
    schema = infer_schema(df)
    draft_numeric_key = "exec_numeric_draft"
    draft_category_key = "exec_category_draft"
    default_numeric = schema["primary_numeric"]
    default_category = schema["primary_category"]
    applied_key = "applied_executive_settings"

    if applied_key not in st.session_state:
        st.session_state[applied_key] = {"numeric": default_numeric, "category": default_category}
    if st.session_state[applied_key].get("numeric") not in schema["numeric_cols"]:
        st.session_state[applied_key]["numeric"] = default_numeric
    if st.session_state[applied_key].get("category") not in schema["categorical_cols"]:
        st.session_state[applied_key]["category"] = default_category
    if draft_numeric_key not in st.session_state:
        st.session_state[draft_numeric_key] = st.session_state[applied_key]["numeric"]
    if draft_category_key not in st.session_state:
        st.session_state[draft_category_key] = st.session_state[applied_key]["category"]
    if st.session_state[draft_numeric_key] not in schema["numeric_cols"]:
        st.session_state[draft_numeric_key] = default_numeric
    if schema["categorical_cols"] and st.session_state[draft_category_key] not in schema["categorical_cols"]:
        st.session_state[draft_category_key] = default_category

    with st.form(key="executive_settings_form"):
        csel1, csel2, csel3 = st.columns([1, 1, 0.6])
        if schema["numeric_cols"]:
            csel1.selectbox("Variable numerica del resumen", options=schema["numeric_cols"], key=draft_numeric_key)
        if schema["categorical_cols"]:
            csel2.selectbox("Variable categorica del resumen", options=schema["categorical_cols"], key=draft_category_key)
        csel3.markdown("<div style='height:1.7rem'></div>", unsafe_allow_html=True)
        submitted = csel3.form_submit_button("Aplicar", use_container_width=True, on_click=trigger_loader)
    if submitted:
        st.session_state[applied_key] = {
            "numeric": st.session_state.get(draft_numeric_key),
            "category": st.session_state.get(draft_category_key),
        }
        st.rerun()

    selected_numeric = st.session_state[applied_key]["numeric"]
    selected_category = st.session_state[applied_key]["category"]

    c1, c2 = st.columns([1.05, 0.95])
    with c1:
        st.plotly_chart(fig_missing(df), use_container_width=True, key="exec_missing")
    with c2:
        if selected_numeric:
            st.plotly_chart(
                fig_distribution(df, selected_numeric),
                use_container_width=True,
                key=f"exec_distribution_{selected_numeric}",
            )
        else:
            st.info("No hay columnas numericas disponibles para distribucion.")

    if selected_category:
        st.plotly_chart(
            fig_top_categories(df, selected_category, f"Top categorias de {selected_category}"),
            use_container_width=True,
            key=f"exec_topcat_{selected_category}",
        )


def render_numeric_tab(df: pd.DataFrame) -> None:
    schema = infer_schema(df)
    numeric_cols = schema["numeric_cols"][:8]
    if not numeric_cols:
        st.info("No hay columnas numericas disponibles para analisis.")
        return

    category_options = ["Ninguna"] + schema["categorical_cols"][:8]
    applied_key = "applied_numeric_settings"
    if applied_key not in st.session_state:
        st.session_state[applied_key] = {"numeric": numeric_cols[0], "category": "Ninguna"}
    if st.session_state[applied_key].get("numeric") not in numeric_cols:
        st.session_state[applied_key]["numeric"] = numeric_cols[0]
    if st.session_state[applied_key].get("category") not in category_options:
        st.session_state[applied_key]["category"] = "Ninguna"
    if "numeric_primary_draft" not in st.session_state:
        st.session_state["numeric_primary_draft"] = st.session_state[applied_key]["numeric"]
    if "numeric_category_draft" not in st.session_state:
        st.session_state["numeric_category_draft"] = st.session_state[applied_key]["category"]
    if st.session_state["numeric_primary_draft"] not in numeric_cols:
        st.session_state["numeric_primary_draft"] = numeric_cols[0]
    if st.session_state["numeric_category_draft"] not in category_options:
        st.session_state["numeric_category_draft"] = "Ninguna"

    with st.form(key="numeric_settings_form"):
        f1, f2, f3 = st.columns([1, 1, 0.6])
        f1.selectbox("Variable numerica", options=numeric_cols, key="numeric_primary_draft")
        f2.selectbox("Variable de apertura", options=category_options, key="numeric_category_draft")
        f3.markdown("<div style='height:1.7rem'></div>", unsafe_allow_html=True)
        submitted = f3.form_submit_button("Aplicar", use_container_width=True, on_click=trigger_loader)
    if submitted:
        st.session_state[applied_key] = {
            "numeric": st.session_state["numeric_primary_draft"],
            "category": st.session_state["numeric_category_draft"],
        }
        st.rerun()

    selected_numeric = st.session_state[applied_key]["numeric"]
    selected_category = st.session_state[applied_key]["category"]

    c1, c2 = st.columns([1.15, 0.85])
    with c1:
        if selected_category != "Ninguna":
            st.plotly_chart(
                fig_box_by_category(df, selected_numeric, selected_category),
                use_container_width=True,
                key=f"num_box_{selected_numeric}_{selected_category}",
            )
        else:
            st.plotly_chart(
                fig_distribution(df, selected_numeric),
                use_container_width=True,
                key=f"num_distribution_{selected_numeric}",
            )
    with c2:
        st.dataframe(df[numeric_cols].describe().T.round(2), use_container_width=True, height=470)

    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr(numeric_only=True)
        if not corr.empty:
            fig = px.imshow(corr, text_auto=".2f", aspect="auto", color_continuous_scale="RdBu_r", title="Matriz de correlacion")
            fig.update_layout(height=420)
            st.plotly_chart(apply_dark_layout(fig), use_container_width=True, key="num_corr")


def render_temporal_tab(df: pd.DataFrame) -> None:
    schema = infer_schema(df)
    if not schema["datetime_cols"]:
        st.info("No hay columnas temporales detectadas.")
        return

    numeric_options = schema["numeric_cols"][:]
    applied_key = "applied_temporal_settings"
    default_temporal = {
        "datetime": schema["datetime_cols"][0],
        "freq": "M",
        "metric_mode": "Cantidad de registros",
        "value_col": numeric_options[0] if numeric_options else None,
        "agg_func": "sum",
        "extra_col": "Sin filtro",
        "extra_values": (),
    }
    if applied_key not in st.session_state:
        st.session_state[applied_key] = default_temporal.copy()
    if st.session_state[applied_key].get("datetime") not in schema["datetime_cols"]:
        st.session_state[applied_key]["datetime"] = default_temporal["datetime"]
    if st.session_state[applied_key].get("value_col") not in numeric_options:
        st.session_state[applied_key]["value_col"] = default_temporal["value_col"]
    extra_filter_options = ["Sin filtro"] + schema["categorical_cols"][:8]
    if st.session_state[applied_key].get("extra_col") not in extra_filter_options:
        st.session_state[applied_key]["extra_col"] = "Sin filtro"
    for key, value in default_temporal.items():
        draft_key = f"time_{key}_draft"
        if draft_key not in st.session_state:
            st.session_state[draft_key] = st.session_state[applied_key][key]
    if st.session_state["time_datetime_draft"] not in schema["datetime_cols"]:
        st.session_state["time_datetime_draft"] = default_temporal["datetime"]
    if numeric_options and st.session_state.get("time_value_col_draft") not in numeric_options:
        st.session_state["time_value_col_draft"] = default_temporal["value_col"]
    if st.session_state.get("time_extra_col_draft") not in extra_filter_options:
        st.session_state["time_extra_col_draft"] = st.session_state[applied_key]["extra_col"]
    with st.form(key="temporal_settings_form"):
        c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 0.6])
        c1.selectbox("Fecha", options=schema["datetime_cols"], key="time_datetime_draft")
        c2.selectbox("Agrupacion", options=["D", "W", "M", "Q", "Y"], key="time_freq_draft")
        c3.selectbox("Metrica", options=["Cantidad de registros", "Agregado numerico"], key="time_metric_mode_draft")

        draft_metric_mode = st.session_state["time_metric_mode_draft"]
        if draft_metric_mode == "Agregado numerico":
            if not numeric_options:
                st.info("No hay columnas numericas disponibles para agregacion temporal.")
                return
            c4.selectbox("Campo numerico", options=numeric_options, key="time_value_col_draft")
            c5.selectbox("Funcion de agregacion", options=["sum", "mean", "median", "max", "min"], key="time_agg_func_draft")
        else:
            c4.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
            c4.caption("La metrica sera el conteo de registros.")

        filter_cols = st.columns([1, 1.2, 0.7])
        filter_cols[0].selectbox("Filtro categórico", options=extra_filter_options, key="time_extra_col_draft")
        if st.session_state["time_extra_col_draft"] != "Sin filtro":
            extra_values = sorted(df[st.session_state["time_extra_col_draft"]].dropna().astype(str).unique().tolist())
            current_extra_values = st.session_state.get("time_extra_values_draft", [])
            valid_extra_values = [value for value in current_extra_values if value in extra_values]
            if valid_extra_values != current_extra_values:
                st.session_state["time_extra_values_draft"] = valid_extra_values
            filter_cols[1].multiselect(
                f"Valores de {st.session_state['time_extra_col_draft']}",
                options=extra_values,
                key="time_extra_values_draft",
            )
        else:
            st.session_state["time_extra_values_draft"] = []

        submitted = filter_cols[2].form_submit_button("Aplicar", use_container_width=True, on_click=trigger_loader)
    if submitted:
        st.session_state[applied_key] = {
            "datetime": st.session_state["time_datetime_draft"],
            "freq": st.session_state["time_freq_draft"],
            "metric_mode": st.session_state["time_metric_mode_draft"],
            "value_col": st.session_state.get("time_value_col_draft"),
            "agg_func": st.session_state.get("time_agg_func_draft", "sum"),
            "extra_col": st.session_state.get("time_extra_col_draft", "Sin filtro"),
            "extra_values": tuple(st.session_state.get("time_extra_values_draft", [])),
        }
        st.rerun()

    applied_settings = st.session_state[applied_key]
    datetime_col = applied_settings["datetime"]
    freq = applied_settings["freq"]
    metric_mode = applied_settings["metric_mode"]
    value_col = applied_settings["value_col"]
    agg_func = applied_settings["agg_func"]
    temporal_df = df.copy()
    if applied_settings.get("extra_col") != "Sin filtro" and applied_settings.get("extra_values"):
        temporal_df = temporal_df[temporal_df[applied_settings["extra_col"]].astype(str).isin(applied_settings["extra_values"])]

    st.plotly_chart(
        fig_time_series_metric(temporal_df, datetime_col, freq, metric_mode, value_col, agg_func),
        use_container_width=True,
        key=f"time_metric_{datetime_col}_{freq}_{metric_mode}_{value_col}_{agg_func}_{applied_settings.get('extra_col')}_{'_'.join(applied_settings.get('extra_values', ())[:3])}",
    )
    st.caption("Puedes moverte y hacer zoom horizontal usando la barra inferior del eje X.")

    if applied_settings.get("extra_col") != "Sin filtro":
        breakdown_df = temporal_breakdown_table(
            temporal_df,
            datetime_col=datetime_col,
            freq=freq,
            category_col=applied_settings["extra_col"],
            metric_mode=metric_mode,
            value_col=value_col,
            agg_func=agg_func,
            selected_values=tuple(applied_settings.get("extra_values", ())),
        )
        if not breakdown_df.empty:
            metric_label = "Cantidad" if metric_mode == "Cantidad de registros" else f"{agg_func} de {value_col}"
            st.markdown(f"### Desglose por {applied_settings['extra_col']}")
            st.caption(f"Tabla por periodo ({freq}) con {metric_label} para las categorias seleccionadas.")
            st.dataframe(breakdown_df, use_container_width=True, hide_index=True, height=320)


def render_relations_tab(df: pd.DataFrame, parquet_dir: Path, selected_files: list) -> None:
    parquet_profiles = load_parquet_profiles(parquet_dir)
    parquet_names = list(parquet_profiles.keys())
    if len(parquet_names) < 2:
        st.info("Se necesitan al menos dos parquet para detectar relaciones entre archivos.")
        return

    default_a = selected_files[0] if selected_files and selected_files[0] in parquet_names else parquet_names[0]
    default_b = next((name for name in parquet_names if name != default_a), parquet_names[0])

    applied_key = "applied_relations_settings"
    default_rel = {"parquet_a": default_a, "parquet_b": default_b}
    if applied_key not in st.session_state:
        st.session_state[applied_key] = default_rel.copy()
    if st.session_state[applied_key].get("parquet_a") not in parquet_names:
        st.session_state[applied_key]["parquet_a"] = default_a
    if st.session_state[applied_key].get("parquet_b") not in parquet_names or st.session_state[applied_key].get("parquet_b") == st.session_state[applied_key].get("parquet_a"):
        st.session_state[applied_key]["parquet_b"] = default_b
    if "rel_parquet_a_draft" not in st.session_state:
        st.session_state["rel_parquet_a_draft"] = st.session_state[applied_key]["parquet_a"]
    if "rel_parquet_b_draft" not in st.session_state:
        st.session_state["rel_parquet_b_draft"] = st.session_state[applied_key]["parquet_b"]

    with st.form(key="relations_settings_form"):
        c1, c2, c3 = st.columns([1, 1, 0.6])
        c1.selectbox("Parquet A", options=parquet_names, key="rel_parquet_a_draft")
        parquet_b_options = [name for name in parquet_names if name != st.session_state["rel_parquet_a_draft"]]
        if st.session_state["rel_parquet_b_draft"] not in parquet_b_options:
            st.session_state["rel_parquet_b_draft"] = parquet_b_options[0]
        c2.selectbox("Parquet B", options=parquet_b_options, key="rel_parquet_b_draft")
        c3.markdown("<div style='height:1.7rem'></div>", unsafe_allow_html=True)
        submitted = c3.form_submit_button("Aplicar", use_container_width=True, on_click=trigger_loader)
    if submitted:
        st.session_state[applied_key] = {
            "parquet_a": st.session_state["rel_parquet_a_draft"],
            "parquet_b": st.session_state["rel_parquet_b_draft"],
        }
        st.rerun()

    parquet_a = st.session_state[applied_key]["parquet_a"]
    parquet_b = st.session_state[applied_key]["parquet_b"]

    relation_df = parquet_relationships_table(parquet_profiles, parquet_a, parquet_b)
    if relation_df.empty:
        st.info("No se detectaron columnas comparables entre los parquet seleccionados.")
        return

    possible_keys = relation_df[relation_df["Posible ID"] == "Si"].copy()
    if not possible_keys.empty:
        st.markdown("### Posibles claves o IDs")
        st.dataframe(possible_keys, use_container_width=True, height=220, hide_index=True)

    st.plotly_chart(
        fig_parquet_relationships(relation_df, parquet_a, parquet_b),
        use_container_width=True,
        key=f"relations_between_{parquet_a}_{parquet_b}",
    )
    st.dataframe(relation_df, use_container_width=True, height=380, hide_index=True)
    st.caption(
        "La comparacion se hace entre parquet, midiendo columnas compartidas y solapamiento de valores unicos. "
        "Eso ayuda a detectar si dos archivos parecen complementarse, duplicarse o cruzarse por alguna clave."
    )


def render_statistics_tab(df: pd.DataFrame) -> None:
    schema = infer_schema(df)
    if not schema["categorical_cols"]:
        st.info("No hay columnas categoricas disponibles para el analisis estadistico.")
        return
    if not schema["numeric_cols"]:
        st.info("No hay columnas numericas disponibles para el analisis estadistico.")
        return

    applied_key = "applied_statistics_settings"
    default_stats = {
        "category": schema["categorical_cols"][0],
        "numeric": schema["numeric_cols"][0],
        "agg": "sum",
        "datetime": "Sin filtro",
        "date_range": None,
        "extra_col": "Sin filtro",
        "extra_values": (),
    }
    if applied_key not in st.session_state:
        st.session_state[applied_key] = default_stats.copy()
    if st.session_state[applied_key].get("category") not in schema["categorical_cols"]:
        st.session_state[applied_key]["category"] = default_stats["category"]
    if st.session_state[applied_key].get("numeric") not in schema["numeric_cols"]:
        st.session_state[applied_key]["numeric"] = default_stats["numeric"]
    draft_defaults = {
        "stats_category_draft": st.session_state[applied_key]["category"],
        "stats_numeric_draft": st.session_state[applied_key]["numeric"],
        "stats_agg_draft": st.session_state[applied_key]["agg"],
        "stats_datetime_draft": st.session_state[applied_key]["datetime"],
        "stats_extra_col_draft": st.session_state[applied_key]["extra_col"],
        "stats_extra_values_draft": list(st.session_state[applied_key]["extra_values"]),
    }
    for key, value in draft_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    if st.session_state["stats_category_draft"] not in schema["categorical_cols"]:
        st.session_state["stats_category_draft"] = default_stats["category"]
    if st.session_state["stats_numeric_draft"] not in schema["numeric_cols"]:
        st.session_state["stats_numeric_draft"] = default_stats["numeric"]

    with st.form(key="statistics_settings_form"):
        c1, c2, c3 = st.columns(3)
        c1.selectbox("Variable categorica", options=schema["categorical_cols"], key="stats_category_draft")
        c2.selectbox("Campo numerico", options=schema["numeric_cols"], key="stats_numeric_draft")
        c3.selectbox("Agregacion", options=["sum", "mean", "median", "max", "min"], key="stats_agg_draft")

        filter_cols = st.columns(4)
        if schema["datetime_cols"]:
            filter_cols[0].selectbox("Filtro temporal", options=["Sin filtro"] + schema["datetime_cols"], key="stats_datetime_draft")
        draft_datetime = st.session_state.get("stats_datetime_draft", "Sin filtro")
        if draft_datetime != "Sin filtro":
            date_series = coerce_datetime_series(df[draft_datetime]).dropna()
            if not date_series.empty:
                min_date = date_series.min().date()
                max_date = date_series.max().date()
                current_range = st.session_state.get("stats_datetime_range_draft")
                if current_range is None:
                    st.session_state["stats_datetime_range_draft"] = (min_date, max_date)
                filter_cols[1].date_input("Rango de fechas", min_value=min_date, max_value=max_date, key="stats_datetime_range_draft")

        extra_filter_options = ["Sin filtro"] + [col for col in schema["categorical_cols"] if col != st.session_state["stats_category_draft"]]
        if st.session_state.get("stats_extra_col_draft") not in extra_filter_options:
            st.session_state["stats_extra_col_draft"] = "Sin filtro"
        filter_cols[2].selectbox("Filtro adicional", options=extra_filter_options, key="stats_extra_col_draft")
        if st.session_state["stats_extra_col_draft"] != "Sin filtro":
            extra_values = sorted(df[st.session_state["stats_extra_col_draft"]].dropna().astype(str).unique().tolist())
            current_extra_values = st.session_state.get("stats_extra_values_draft", [])
            valid_extra_values = [value for value in current_extra_values if value in extra_values]
            if valid_extra_values != current_extra_values:
                st.session_state["stats_extra_values_draft"] = valid_extra_values
            filter_cols[3].multiselect(
                f"Valores de {st.session_state['stats_extra_col_draft']}",
                options=extra_values,
                key="stats_extra_values_draft",
            )
        else:
            st.session_state["stats_extra_values_draft"] = []

        submitted = st.form_submit_button("Aplicar", use_container_width=True, on_click=trigger_loader)

    if submitted:
        st.session_state[applied_key] = {
            "category": st.session_state["stats_category_draft"],
            "numeric": st.session_state["stats_numeric_draft"],
            "agg": st.session_state["stats_agg_draft"],
            "datetime": st.session_state.get("stats_datetime_draft", "Sin filtro"),
            "date_range": st.session_state.get("stats_datetime_range_draft"),
            "extra_col": st.session_state["stats_extra_col_draft"],
            "extra_values": tuple(st.session_state.get("stats_extra_values_draft", [])),
        }
        st.rerun()

    applied_settings = st.session_state[applied_key]
    category_col = applied_settings["category"]
    numeric_col = applied_settings["numeric"]
    agg_func = applied_settings["agg"]
    stats_df = df.copy()
    if applied_settings["datetime"] != "Sin filtro" and applied_settings["date_range"]:
        start_date, end_date = applied_settings["date_range"]
        datetime_filter_series = coerce_datetime_series(stats_df[applied_settings["datetime"]])
        stats_df = stats_df[datetime_filter_series.dt.date.between(start_date, end_date)]
    if applied_settings["extra_col"] != "Sin filtro" and applied_settings["extra_values"]:
        stats_df = stats_df[stats_df[applied_settings["extra_col"]].astype(str).isin(applied_settings["extra_values"])]

    numeric_series = pd.to_numeric(stats_df[numeric_col], errors="coerce").dropna()
    metric_cols = st.columns(7)
    metric_cols[0].metric("Registros filtrados", fmt_int(len(stats_df)))
    metric_cols[1].metric("Categorias visibles", fmt_int(stats_df[category_col].dropna().nunique()))
    metric_cols[2].metric(f"Suma {numeric_col}", fmt_num(numeric_series.sum()) if not numeric_series.empty else "-")
    metric_cols[3].metric(f"Media {numeric_col}", fmt_num(numeric_series.mean()) if not numeric_series.empty else "-")
    metric_cols[4].metric(f"Mediana {numeric_col}", fmt_num(numeric_series.median()) if not numeric_series.empty else "-")
    metric_cols[5].metric(f"Min {numeric_col}", fmt_num(numeric_series.min()) if not numeric_series.empty else "-")
    metric_cols[6].metric(f"Max {numeric_col}", fmt_num(numeric_series.max()) if not numeric_series.empty else "-")

    left, right = st.columns(2)
    with left:
        st.plotly_chart(
            fig_category_distribution(stats_df, category_col),
            use_container_width=True,
            key=f"stats_dist_{category_col}",
        )
    with right:
        st.plotly_chart(
            fig_numeric_by_category(stats_df, category_col, numeric_col, agg_func),
            use_container_width=True,
            key=f"stats_num_{category_col}_{numeric_col}_{agg_func}",
        )

    numeric_summary_cols = tuple(schema["numeric_cols"][: min(6, len(schema["numeric_cols"]))])
    st.caption("Resumen por categoria con cantidad de registros y agregados de los campos numericos disponibles.")
    st.dataframe(
        summarize_by_category(stats_df, category_col, numeric_summary_cols),
        use_container_width=True,
        height=420,
        hide_index=True,
    )


def render_map_tab(df: pd.DataFrame, size_map: str, local_files: list[dict] | None = None) -> None:
    schema = infer_schema(df)
    all_cols = list(df.columns)
    numeric_options = ["Constante"] + schema["numeric_cols"]
    categorical_options = ["Sin color"] + schema["categorical_cols"]
    location_modes = ["country names", "ISO-3", "USA-states"]
    local_files = local_files or []
    geojson_files = get_available_geojson_files()

    lat_default = schema["lat_col"] if schema["lat_col"] in all_cols else None
    lon_default = schema["lon_col"] if schema["lon_col"] in all_cols else None
    location_default = next(
        (
            col for col in all_cols
            if any(token in _normalized(col) for token in ["STATE", "PAIS", "COUNTRY", "REGION", "PROV"])
        ),
        all_cols[0] if all_cols else None,
    )

    applied_key = "applied_map_settings"
    default_settings = {
        "mode": "Lat/Lon" if lat_default and lon_default else "Ubicaciones",
        "lat_col": lat_default,
        "lon_col": lon_default,
        "size_col": size_map if size_map in numeric_options else "Constante",
        "color_col": schema["primary_category"] if schema["primary_category"] in schema["categorical_cols"] else "Sin color",
        "hover_name": schema["id_col"] if schema["id_col"] in all_cols else (all_cols[0] if all_cols else None),
        "location_col": location_default,
        "location_mode": "USA-states" if location_default and "STATE" in _normalized(location_default) else "country names",
        "location_value_col": "Conteo",
    }
    if applied_key not in st.session_state:
        st.session_state[applied_key] = default_settings.copy()

    dictionary_files = [item for item in local_files if item["type"] in {"CSV", "PARQUET"}]

    with st.form("map_settings_form"):
        c1, c2, c3, c4 = st.columns(4)
        mode = c1.selectbox("Tipo de mapa", options=["Lat/Lon", "Ubicaciones"], index=["Lat/Lon", "Ubicaciones"].index(st.session_state[applied_key].get("mode", default_settings["mode"])))
        hover_options = ["Sin etiqueta"] + all_cols

        if mode == "Lat/Lon":
            lat_idx = all_cols.index(st.session_state[applied_key].get("lat_col")) if st.session_state[applied_key].get("lat_col") in all_cols else 0
            lon_idx = all_cols.index(st.session_state[applied_key].get("lon_col")) if st.session_state[applied_key].get("lon_col") in all_cols else 0
            size_idx = numeric_options.index(st.session_state[applied_key].get("size_col", "Constante")) if st.session_state[applied_key].get("size_col", "Constante") in numeric_options else 0
            color_idx = categorical_options.index(st.session_state[applied_key].get("color_col", "Sin color")) if st.session_state[applied_key].get("color_col", "Sin color") in categorical_options else 0

            lat_col = c2.selectbox("Latitud", options=all_cols, index=lat_idx)
            lon_col = c3.selectbox("Longitud", options=all_cols, index=lon_idx)
            size_col = c4.selectbox("Tamano", options=numeric_options, index=size_idx)
            map_color_col = st.selectbox("Color", options=categorical_options, index=color_idx)
            hover_idx = hover_options.index(st.session_state[applied_key].get("hover_name")) if st.session_state[applied_key].get("hover_name") in hover_options else 0
            hover_name = st.selectbox("Etiqueta hover", options=hover_options, index=hover_idx)
            submitted = st.form_submit_button("Aplicar", use_container_width=True, on_click=trigger_loader)
            if submitted:
                st.session_state[applied_key] = {
                    "mode": mode,
                    "lat_col": lat_col,
                    "lon_col": lon_col,
                    "size_col": size_col,
                    "color_col": map_color_col,
                    "hover_name": None if hover_name == "Sin etiqueta" else hover_name,
                    "location_col": st.session_state[applied_key].get("location_col"),
                    "location_mode": st.session_state[applied_key].get("location_mode", "country names"),
                    "location_value_col": st.session_state[applied_key].get("location_value_col", "Conteo"),
                }
                st.rerun()
        else:
            location_idx = all_cols.index(st.session_state[applied_key].get("location_col")) if st.session_state[applied_key].get("location_col") in all_cols else 0
            mode_idx = location_modes.index(st.session_state[applied_key].get("location_mode", "country names")) if st.session_state[applied_key].get("location_mode", "country names") in location_modes else 0
            value_options = ["Conteo"] + schema["numeric_cols"]
            value_idx = value_options.index(st.session_state[applied_key].get("location_value_col", "Conteo")) if st.session_state[applied_key].get("location_value_col", "Conteo") in value_options else 0
            hover_idx = hover_options.index(st.session_state[applied_key].get("hover_name")) if st.session_state[applied_key].get("hover_name") in hover_options else 0

            location_col = c2.selectbox("Ubicacion", options=all_cols, index=location_idx)
            location_mode = c3.selectbox("Modo de ubicacion", options=location_modes, index=mode_idx)
            location_value_col = c4.selectbox("Valor", options=value_options, index=value_idx)
            hover_name = st.selectbox("Etiqueta hover", options=hover_options, index=hover_idx)
            submitted = st.form_submit_button("Aplicar", use_container_width=True, on_click=trigger_loader)
            if submitted:
                st.session_state[applied_key] = {
                    "mode": mode,
                    "lat_col": st.session_state[applied_key].get("lat_col"),
                    "lon_col": st.session_state[applied_key].get("lon_col"),
                    "size_col": st.session_state[applied_key].get("size_col", "Constante"),
                    "color_col": st.session_state[applied_key].get("color_col", "Sin color"),
                    "hover_name": None if hover_name == "Sin etiqueta" else hover_name,
                    "location_col": location_col,
                    "location_mode": location_mode,
                    "location_value_col": location_value_col,
                }
                st.rerun()

    settings = st.session_state[applied_key]

    map_dictionary_df = None
    dictionary_expander = st.expander("Diccionario de ubicaciones opcional", expanded=False)
    with dictionary_expander:
        use_dictionary = st.checkbox("Usar diccionario para traducir codigos", key="map_use_dictionary")
        if use_dictionary:
            dict_source = st.radio("Fuente del diccionario", options=["Archivo local", "Subir archivo"], key="map_dictionary_source", horizontal=True)
            if dict_source == "Archivo local":
                if dictionary_files:
                    dict_labels = [item["label"] for item in dictionary_files]
                    default_dict_label = next(
                        (label for label in dict_labels if "state" in label.lower() or "label" in label.lower()),
                        dict_labels[0],
                    )
                    selected_dict_label = st.selectbox("Archivo de diccionario", options=dict_labels, index=dict_labels.index(default_dict_label), key="map_dictionary_local_file")
                    selected_dict_item = next(item for item in dictionary_files if item["label"] == selected_dict_label)
                    map_dictionary_df = load_reference_table_from_path(str(selected_dict_item["path"]))
                else:
                    st.info("No hay archivos locales disponibles para usar como diccionario.")
            else:
                uploaded_dict = st.file_uploader("Sube el diccionario CSV o parquet", type=["csv", "parquet"], key="map_dictionary_upload")
                if uploaded_dict is not None:
                    map_dictionary_df = load_reference_table_from_upload(uploaded_dict.getvalue(), uploaded_dict.name)

            if map_dictionary_df is not None and not map_dictionary_df.empty:
                dict_columns = list(map_dictionary_df.columns)
                default_key_col = next((col for col in dict_columns if any(token in _normalized(col) for token in ["ID", "COD", "CODE", "KEY"])), dict_columns[0])
                default_value_col = next((col for col in dict_columns if col != default_key_col and any(token in _normalized(col) for token in ["NAME", "DESC", "STATE", "PAIS", "COUNTRY", "REGION"])), dict_columns[min(1, len(dict_columns) - 1)])
                dict_key_col = st.selectbox("Columna clave del diccionario", options=dict_columns, index=dict_columns.index(default_key_col), key="map_dictionary_key_col")
                dict_value_col = st.selectbox("Columna descriptiva del diccionario", options=dict_columns, index=dict_columns.index(default_value_col), key="map_dictionary_value_col")
                st.caption(f"Ejemplo de traduccion: `{dict_key_col}` -> `{dict_value_col}`")
            elif use_dictionary:
                st.caption("Selecciona o sube un diccionario para poder traducir codigos a nombres.")

    selected_geojson = None
    selected_geojson_property = None
    geojson_expander = st.expander("GeoJSON opcional", expanded=False)
    with geojson_expander:
        use_geojson = st.checkbox("Usar GeoJSON para dibujar ubicaciones", key="map_use_geojson")
        if use_geojson:
            geojson_source = st.radio("Fuente del GeoJSON", options=["Archivo local", "Subir archivo"], key="map_geojson_source", horizontal=True)
            if geojson_source == "Archivo local":
                if geojson_files:
                    geojson_labels = [item["label"] for item in geojson_files]
                    default_geojson = next((label for label in geojson_labels if "malaysia" in label.lower() or "state" in label.lower()), geojson_labels[0])
                    selected_geojson_label = st.selectbox("Archivo GeoJSON", options=geojson_labels, index=geojson_labels.index(default_geojson), key="map_geojson_local_file")
                    selected_geojson_item = next(item for item in geojson_files if item["label"] == selected_geojson_label)
                    selected_geojson = load_geojson_from_path(str(selected_geojson_item["path"]))
                else:
                    st.info("No hay archivos `.json` o `.geojson` disponibles en las carpetas de entrada.")
            else:
                uploaded_geojson = st.file_uploader("Sube un archivo GeoJSON", type=["json", "geojson"], key="map_geojson_upload")
                if uploaded_geojson is not None:
                    selected_geojson = load_geojson_from_upload(uploaded_geojson.getvalue())

            if selected_geojson and selected_geojson.get("features"):
                first_properties = selected_geojson["features"][0].get("properties", {})
                property_options = list(first_properties.keys()) if first_properties else []
                if property_options:
                    default_property = next((prop for prop in property_options if any(token in _normalized(prop) for token in ["NAME", "STATE", "REGION", "ID", "CODE"])), property_options[0])
                    selected_geojson_property = st.selectbox("Propiedad del feature para hacer match", options=property_options, index=property_options.index(default_property), key="map_geojson_property")
                    st.caption(f"Se comparara la columna de ubicacion elegida contra `properties.{selected_geojson_property}`.")
                else:
                    st.warning("El GeoJSON no tiene propiedades utilizables en sus features.")

    if settings["mode"] == "Lat/Lon":
        lat_col = settings.get("lat_col")
        lon_col = settings.get("lon_col")
        if not lat_col or not lon_col:
            st.info("Selecciona las columnas de latitud y longitud para construir el mapa.")
            return

        map_df = df.copy()
        map_df[lat_col] = pd.to_numeric(map_df[lat_col], errors="coerce")
        map_df[lon_col] = pd.to_numeric(map_df[lon_col], errors="coerce")
        map_df = map_df.dropna(subset=[lat_col, lon_col])
        if map_df.empty:
            st.warning("No hay coordenadas validas para las columnas elegidas.")
            return

        st.caption(f"Mapa construido con latitud `{lat_col}` y longitud `{lon_col}`.")
        st.plotly_chart(
            fig_map_coordinates(df, lat_col, lon_col, settings.get("size_col", "Constante"), settings.get("color_col", "Sin color"), settings.get("hover_name")),
            use_container_width=True,
            key=f"map_coords_{lat_col}_{lon_col}_{settings.get('size_col')}_{settings.get('color_col')}",
        )

        summary = pd.DataFrame(
            {
                "Metrica": ["Registros mapeados", f"Min {lat_col}", f"Max {lat_col}", f"Min {lon_col}", f"Max {lon_col}"],
                "Valor": [
                    fmt_int(len(map_df)),
                    fmt_num(map_df[lat_col].min(), 4),
                    fmt_num(map_df[lat_col].max(), 4),
                    fmt_num(map_df[lon_col].min(), 4),
                    fmt_num(map_df[lon_col].max(), 4),
                ],
            }
        )
        st.dataframe(summary, use_container_width=True, hide_index=True)
    else:
        location_col = settings.get("location_col")
        if not location_col:
            st.info("Selecciona la columna geografica para construir el mapa.")
            return

        location_df = df.copy()
        location_df[location_col] = location_df[location_col].fillna("").astype(str).str.strip()
        location_df = location_df[location_df[location_col] != ""]
        if location_df.empty:
            st.warning("No hay ubicaciones validas en la columna elegida.")
            return

        location_display_col = location_col
        if st.session_state.get("map_use_dictionary") and map_dictionary_df is not None and not map_dictionary_df.empty:
            dict_key_col = st.session_state.get("map_dictionary_key_col")
            dict_value_col = st.session_state.get("map_dictionary_value_col")
            if dict_key_col in map_dictionary_df.columns and dict_value_col in map_dictionary_df.columns:
                dictionary_map = (
                    map_dictionary_df[[dict_key_col, dict_value_col]]
                    .dropna()
                    .assign(
                        __dict_key=lambda frame: frame[dict_key_col].astype(str).str.strip(),
                        __dict_value=lambda frame: frame[dict_value_col].astype(str).str.strip(),
                    )
                    .drop_duplicates(subset="__dict_key")
                    .set_index("__dict_key")["__dict_value"]
                    .to_dict()
                )
                location_df["MAP_LOCATION_LABEL"] = location_df[location_col].astype(str).str.strip().map(dictionary_map)
                match_ratio = location_df["MAP_LOCATION_LABEL"].notna().mean()
                st.caption(f"Diccionario aplicado sobre `{location_col}`. Cobertura: {pct(match_ratio * 100)}.")
                location_df["MAP_LOCATION_LABEL"] = location_df["MAP_LOCATION_LABEL"].fillna(location_df[location_col].astype(str).str.strip())
                location_display_col = "MAP_LOCATION_LABEL"

        if st.session_state.get("map_use_geojson") and selected_geojson and selected_geojson_property:
            st.caption(
                f"Mapa construido con la columna `{location_display_col}` y el GeoJSON usando `properties.{selected_geojson_property}`."
            )
            st.plotly_chart(
                fig_map_geojson(
                    location_df,
                    location_display_col,
                    settings.get("location_value_col", "Conteo"),
                    selected_geojson,
                    selected_geojson_property,
                    settings.get("hover_name"),
                ),
                use_container_width=True,
                key=f"map_geojson_{location_display_col}_{selected_geojson_property}_{settings.get('location_value_col')}",
            )
        else:
            diagnostics = location_mode_diagnostics(location_df[location_display_col], settings.get("location_mode", "country names"))
            if not diagnostics["valid"]:
                sample_text = ", ".join(diagnostics["sample"]) if diagnostics["sample"] else "sin ejemplos"
                st.warning(f"{diagnostics['message']} Ejemplos detectados: {sample_text}.")
                st.caption(
                    "Prueba otro modo de ubicacion solo si los valores realmente son nombres de paises, codigos ISO-3 o abreviaturas de estados de USA. "
                    "Si son IDs numericos del dataset, ese campo no se puede mapear directamente sin una tabla de equivalencias."
                )

            st.caption(
                f"Mapa construido con la columna `{location_display_col}` usando el modo `{settings.get('location_mode', 'country names')}`."
            )
            st.plotly_chart(
                fig_map_locations(
                    location_df,
                    location_display_col,
                    settings.get("location_mode", "country names"),
                    settings.get("location_value_col", "Conteo"),
                    settings.get("hover_name"),
                ),
                use_container_width=True,
                key=f"map_locations_{location_display_col}_{settings.get('location_mode')}_{settings.get('location_value_col')}",
            )

        summary = location_df.groupby(location_display_col, as_index=False).size().rename(columns={"size": "Registros"}).sort_values("Registros", ascending=False).head(20)
        st.dataframe(summary, use_container_width=True, hide_index=True)


def main() -> None:
    loading_placeholder = st.empty()
    show_loading(loading_placeholder, "Verificando carpetas y preparando el entorno...")

    show_loading(loading_placeholder, "Buscando archivos locales disponibles...")
    local_files = get_available_local_files()
    local_catalog = get_local_catalog(local_files)

    show_loading(loading_placeholder, "Armando selector de archivos y panel lateral...")
    selection = build_file_selector(local_files, local_catalog, loading_placeholder=loading_placeholder)

    if selection["source_mode"] == "Archivo local":
        selected_item = selection["selected_item"]
        if selected_item is None:
            loading_placeholder.empty()
            st.info("Agrega archivos `.csv` o `.parquet` a `work/EDA/input` o usa la opcion `Subir CSV`.")
            st.stop()
        selected_files = [selected_item["label"]]
        show_loading(loading_placeholder, f"Leyendo {selected_files[0]} y detectando el esquema...")
        df = load_data_from_path(str(selected_item["path"]))
        active_file_label = selected_files[0]
    else:
        uploaded_file = selection["uploaded_file"]
        if uploaded_file is None:
            loading_placeholder.empty()
            st.info("Sube un archivo CSV para comenzar el analisis.")
            st.stop()
        show_loading(loading_placeholder, f"Leyendo {uploaded_file.name} y detectando el esquema...")
        df = load_uploaded_csv(uploaded_file.getvalue(), uploaded_file.name)
        active_file_label = f"upload/{uploaded_file.name}"
        selected_files = [active_file_label]

    show_loading(loading_placeholder, "Aplicando filtros dinamicos y preparando exportacion...")
    filtered, size_map = build_sidebar(df, active_file_label)
    filtered_schema = infer_schema(filtered)
    filtered_quality = quality_table(filtered)
    show_loading(loading_placeholder, "Calculando resumen ejecutivo, metricas e insights...")
    render_header(filtered, filtered_schema, selected_files, len(local_files))
    render_kpis(filtered, filtered_schema)
    st.markdown("<div style='height:0.35rem'></div>", unsafe_allow_html=True)
    render_insights(filtered, filtered_schema, filtered_quality)
    st.markdown("<div style='height:0.65rem'></div>", unsafe_allow_html=True)

    show_loading(loading_placeholder, "Construyendo pestañas, graficos interactivos y tablas...")
    sections = ["Resumen ejecutivo", "Analisis numerico", "Analisis temporal", "Estadistica", "Relaciones", "Mapa", "Datos"]
    active_section = st.radio(
        "Seccion",
        options=sections,
        index=0,
        horizontal=True,
        key="active_section",
        label_visibility="collapsed",
        on_change=trigger_loader,
    )

    show_loading(loading_placeholder, f"Construyendo la seccion {active_section}...")

    if active_section == "Resumen ejecutivo":
        render_executive_tab(filtered)
    elif active_section == "Analisis numerico":
        render_numeric_tab(filtered)
    elif active_section == "Analisis temporal":
        render_temporal_tab(filtered)
    elif active_section == "Estadistica":
        render_statistics_tab(filtered)
    elif active_section == "Relaciones":
        render_relations_tab(filtered, PARQUET_DIR, selected_files)
    elif active_section == "Mapa":
        render_map_tab(filtered, size_map, local_files=local_files)
    elif active_section == "Datos":
        render_data_tab(filtered)

    loading_placeholder.empty()
    st.session_state["loader_enabled"] = False
    st.session_state["file_changed_this_run"] = False


if __name__ == "__main__":
    main()
