import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings("ignore")

# ── Configuración de página ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Simpsons Dashboard",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Conexión a BD ─────────────────────────────────────────────────────────────
@st.cache_resource
def get_engine():
    # Streamlit Cloud: usa st.secrets; local: usa config.database
    try:
        from sqlalchemy import create_engine as _ce
        db_url = st.secrets.get("DATABASE_URL", None)
        if db_url:
            return _ce(db_url, pool_pre_ping=True)
    except Exception:
        pass
    from config.database import engine
    return engine

engine = get_engine()

# ── Carga de datos con caché ──────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_characters():
    return pd.read_sql("SELECT * FROM dim_characters", engine)

@st.cache_data(ttl=300)
def load_episodes():
    return pd.read_sql("SELECT * FROM dim_episodes", engine)

@st.cache_data(ttl=300)
def load_ratings():
    return pd.read_sql("SELECT * FROM fact_ratings", engine)

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/The_Simpsons_Logo.svg/320px-The_Simpsons_Logo.svg.png",
    use_container_width=True,
)
st.sidebar.title("Navegación")
seccion = st.sidebar.radio(
    "Ir a",
    ["📊 Estadísticas", "👥 Personajes", "📺 Episodios", "🤖 Regresión Lineal", "📥 Datos"],
)

# ── Carga global ──────────────────────────────────────────────────────────────
try:
    df_chars = load_characters()
    df_eps   = load_episodes()
    df_rat   = load_ratings()
    data_ok  = True
except Exception as e:
    st.error(f"❌ No se pudo conectar a la base de datos: {e}")
    st.info("Asegúrate de que DATABASE_URL está configurado en `.env` o en los Secrets de Streamlit Cloud.")
    data_ok = False
    st.stop()

# ═════════════════════════════════════════════════════════════════════════════
# SECCIÓN 1 — ESTADÍSTICAS GENERALES
# ═════════════════════════════════════════════════════════════════════════════
if seccion == "📊 Estadísticas":
    st.title("📊 Estadísticas Generales")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total personajes", len(df_chars))
    col2.metric("Total episodios", len(df_eps))
    col3.metric("Temporadas", int(df_eps["season"].max()) if "season" in df_eps.columns else "—")
    col4.metric("Rating promedio IMDB", f"{df_rat['imdb_rating'].mean():.2f}" if not df_rat.empty else "—")

    st.divider()

    # Rating promedio por temporada
    if not df_rat.empty and "season" in df_rat.columns:
        avg_rating = df_rat.groupby("season")["imdb_rating"].mean().reset_index()
        fig = px.line(
            avg_rating, x="season", y="imdb_rating",
            title="Rating IMDB promedio por temporada",
            labels={"season": "Temporada", "imdb_rating": "Rating IMDB"},
            markers=True, color_discrete_sequence=["#FED90F"],
        )
        fig.update_layout(plot_bgcolor="#1a1a2e", paper_bgcolor="#1a1a2e",
                          font_color="white")
        st.plotly_chart(fig, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        # Viewers por temporada
        if "viewers_millions" in df_rat.columns:
            avg_viewers = df_rat.groupby("season")["viewers_millions"].mean().reset_index()
            fig2 = px.bar(
                avg_viewers, x="season", y="viewers_millions",
                title="Audiencia promedio (millones) por temporada",
                labels={"season": "Temporada", "viewers_millions": "Viewers (M)"},
                color="viewers_millions", color_continuous_scale="YlOrRd",
            )
            st.plotly_chart(fig2, use_container_width=True)

    with col_b:
        # Distribución de ratings
        fig3 = px.histogram(
            df_rat, x="imdb_rating", nbins=20,
            title="Distribución de ratings IMDB",
            labels={"imdb_rating": "Rating IMDB"},
            color_discrete_sequence=["#FED90F"],
        )
        st.plotly_chart(fig3, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# SECCIÓN 2 — PERSONAJES
# ═════════════════════════════════════════════════════════════════════════════
elif seccion == "👥 Personajes":
    st.title("👥 Personajes")

    col1, col2 = st.columns(2)
    with col1:
        gender_filter = st.multiselect(
            "Filtrar por género",
            options=df_chars["gender"].dropna().unique().tolist(),
        )
    with col2:
        status_opts = df_chars["status"].dropna().unique().tolist() if "status" in df_chars.columns else []
        status_filter = st.multiselect("Filtrar por estado", options=status_opts)

    filtered = df_chars.copy()
    if gender_filter:
        filtered = filtered[filtered["gender"].isin(gender_filter)]
    if status_filter:
        filtered = filtered[filtered["status"].isin(status_filter)]

    st.dataframe(filtered, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        fig = px.bar(
            filtered["gender"].value_counts().reset_index(),
            x="gender", y="count",
            title="Personajes por género",
            color="gender", color_discrete_sequence=px.colors.qualitative.Set2,
        )
        st.plotly_chart(fig, use_container_width=True)
    with col4:
        top_occ = filtered["occupation"].value_counts().head(10).reset_index()
        fig2 = px.bar(
            top_occ, x="count", y="occupation", orientation="h",
            title="Top 10 ocupaciones",
            color_discrete_sequence=["#FED90F"],
        )
        st.plotly_chart(fig2, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# SECCIÓN 3 — EPISODIOS
# ═════════════════════════════════════════════════════════════════════════════
elif seccion == "📺 Episodios":
    st.title("📺 Episodios")

    season_opts = sorted(df_eps["season"].dropna().unique().tolist()) if "season" in df_eps.columns else []
    season_filter = st.multiselect("Filtrar por temporada", options=season_opts)

    filtered_eps = df_eps.copy()
    if season_filter:
        filtered_eps = filtered_eps[filtered_eps["season"].isin(season_filter)]

    st.dataframe(filtered_eps, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        if "season" in filtered_eps.columns:
            eps_count = filtered_eps["season"].value_counts().sort_index().reset_index()
            fig = px.bar(
                eps_count, x="season", y="count",
                title="Episodios por temporada",
                labels={"season": "Temporada", "count": "Episodios"},
                color_discrete_sequence=["#FED90F"],
            )
            st.plotly_chart(fig, use_container_width=True)
    with col2:
        if not df_rat.empty and "season" in df_rat.columns:
            merged = filtered_eps.merge(df_rat[["episode_id","imdb_rating","viewers_millions"]], on="episode_id", how="left")
            if "imdb_rating" in merged.columns:
                fig2 = px.scatter(
                    merged, x="season", y="imdb_rating",
                    title="Rating IMDB por episodio",
                    labels={"season": "Temporada", "imdb_rating": "Rating IMDB"},
                    hover_data=["name"] if "name" in merged.columns else None,
                    color="imdb_rating", color_continuous_scale="RdYlGn",
                )
                st.plotly_chart(fig2, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# SECCIÓN 4 — REGRESIÓN LINEAL
# ═════════════════════════════════════════════════════════════════════════════
elif seccion == "🤖 Regresión Lineal":
    st.title("🤖 Modelo de Regresión Lineal")
    st.markdown(
        "**Variable objetivo:** `imdb_rating`  \n"
        "**Predictores:** `viewers_millions`, `season`, `duration_min`, `number_in_season`"
    )

    if df_rat.empty:
        st.warning("No hay datos en fact_ratings. Ejecuta el pipeline primero.")
        st.stop()

    FEATURES = [c for c in ["viewers_millions", "season", "duration_min", "number_in_season"] if c in df_rat.columns]
    TARGET = "imdb_rating"

    df_model = df_rat[FEATURES + [TARGET]].dropna()

    if len(df_model) < 10:
        st.warning("Datos insuficientes para entrenar el modelo.")
        st.stop()

    X = df_model[FEATURES]
    y = df_model[TARGET]

    # ── Parámetros del modelo ─────────────────────────────────────────────
    st.sidebar.subheader("Parámetros del modelo")
    test_size = st.sidebar.slider("Tamaño del conjunto de prueba", 0.1, 0.4, 0.2, 0.05)
    random_state = st.sidebar.number_input("Random state", value=42, step=1)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=int(random_state)
    )
    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc  = scaler.transform(X_test)

    # ── Entrenar modelos ──────────────────────────────────────────────────
    # Simple: mejor predictor por correlación
    best_pred = X.corrwith(y).abs().idxmax()
    reg_simple = LinearRegression()
    reg_simple.fit(X_train[[best_pred]], y_train)
    y_pred_simple = reg_simple.predict(X_test[[best_pred]])

    # Múltiple
    reg_mult = LinearRegression()
    reg_mult.fit(X_train_sc, y_train)
    y_pred_mult = reg_mult.predict(X_test_sc)

    # ── Métricas ──────────────────────────────────────────────────────────
    def metricas(y_true, y_pred, nombre):
        return {
            "Modelo": nombre,
            "R²": round(r2_score(y_true, y_pred), 4),
            "RMSE": round(np.sqrt(mean_squared_error(y_true, y_pred)), 4),
            "MAE": round(mean_absolute_error(y_true, y_pred), 4),
        }

    tabla = pd.DataFrame([
        metricas(y_test, y_pred_simple, f"Simple ({best_pred})"),
        metricas(y_test, y_pred_mult,   "Múltiple"),
    ])

    st.subheader("📋 Tabla comparativa de métricas")
    st.dataframe(tabla, use_container_width=True, hide_index=True)

    col1, col2, col3 = st.columns(3)
    for col, met in zip([col1, col2, col3], ["R²", "RMSE", "MAE"]):
        fig = go.Figure(go.Bar(
            x=tabla["Modelo"], y=tabla[met],
            marker_color=["#2196F3", "#4CAF50"],
            text=tabla[met], textposition="outside",
        ))
        fig.update_layout(title=met, yaxis_title=met, showlegend=False,
                          height=300, margin=dict(t=40, b=20))
        col.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ── Gráficas de ajuste ────────────────────────────────────────────────
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader(f"Regresión Simple: imdb_rating ~ {best_pred}")
        fig_s = px.scatter(
            x=X_test[best_pred], y=y_test,
            labels={"x": best_pred, "y": "imdb_rating"},
            opacity=0.5, color_discrete_sequence=["#2196F3"],
        )
        x_line = np.linspace(X_test[best_pred].min(), X_test[best_pred].max(), 100)
        m = reg_simple.coef_[0]; b = reg_simple.intercept_
        fig_s.add_scatter(x=x_line, y=m * x_line + b, mode="lines",
                          line=dict(color="red", width=2), name="Regresión")
        st.plotly_chart(fig_s, use_container_width=True)

    with col_b:
        st.subheader("Real vs Predicho — Modelo Múltiple")
        fig_m = px.scatter(
            x=y_test, y=y_pred_mult,
            labels={"x": "imdb_rating real", "y": "imdb_rating predicho"},
            opacity=0.5, color_discrete_sequence=["#4CAF50"],
        )
        lim = [min(y_test.min(), y_pred_mult.min()), max(y_test.max(), y_pred_mult.max())]
        fig_m.add_scatter(x=lim, y=lim, mode="lines",
                          line=dict(color="red", dash="dash"), name="Línea perfecta")
        st.plotly_chart(fig_m, use_container_width=True)

    # ── Coeficientes ──────────────────────────────────────────────────────
    st.subheader("Coeficientes del modelo múltiple")
    coef_df = pd.DataFrame({
        "Variable": FEATURES,
        "Coeficiente": reg_mult.coef_,
    }).sort_values("Coeficiente")

    fig_coef = px.bar(
        coef_df, x="Coeficiente", y="Variable", orientation="h",
        color="Coeficiente", color_continuous_scale="RdYlGn",
        title="Importancia de variables (coeficientes estandarizados)",
    )
    fig_coef.add_vline(x=0, line_dash="dash", line_color="white")
    st.plotly_chart(fig_coef, use_container_width=True)

    # ── Predictor interactivo ─────────────────────────────────────────────
    st.divider()
    st.subheader("🔮 Predictor interactivo")
    st.markdown("Ingresa valores para predecir el rating IMDB de un episodio:")

    pred_cols = st.columns(len(FEATURES))
    input_vals = {}
    defaults = {
        "viewers_millions": float(df_rat["viewers_millions"].mean()),
        "season": int(df_rat["season"].median()),
        "duration_min": 22,
        "number_in_season": 10,
    }
    for col, feat in zip(pred_cols, FEATURES):
        if feat == "duration_min":
            input_vals[feat] = col.selectbox("duration_min", [22, 44], index=0)
        elif feat == "season":
            input_vals[feat] = col.slider(feat, 1, 35, defaults.get(feat, 1))
        elif feat == "number_in_season":
            input_vals[feat] = col.slider(feat, 1, 25, defaults.get(feat, 10))
        else:
            input_vals[feat] = col.number_input(feat, value=float(defaults.get(feat, 0.0)), step=0.5)

    X_input = pd.DataFrame([input_vals])[FEATURES]
    X_input_sc = scaler.transform(X_input)
    pred_rating = reg_mult.predict(X_input_sc)[0]
    pred_rating = float(np.clip(pred_rating, 1.0, 10.0))

    st.metric("Rating IMDB predicho", f"{pred_rating:.2f} / 10")

# ═════════════════════════════════════════════════════════════════════════════
# SECCIÓN 5 — DATOS Y EXPORTAR
# ═════════════════════════════════════════════════════════════════════════════
elif seccion == "📥 Datos":
    st.title("📥 Datos y Exportar")

    tab1, tab2, tab3 = st.tabs(["Personajes", "Episodios", "Ratings"])

    with tab1:
        st.dataframe(df_chars, use_container_width=True)
        st.download_button(
            "⬇️ Descargar personajes CSV",
            df_chars.to_csv(index=False).encode("utf-8"),
            "characters.csv", "text/csv",
        )
    with tab2:
        st.dataframe(df_eps, use_container_width=True)
        st.download_button(
            "⬇️ Descargar episodios CSV",
            df_eps.to_csv(index=False).encode("utf-8"),
            "episodes.csv", "text/csv",
        )
    with tab3:
        st.dataframe(df_rat, use_container_width=True)
        st.download_button(
            "⬇️ Descargar ratings CSV",
            df_rat.to_csv(index=False).encode("utf-8"),
            "ratings.csv", "text/csv",
        )
