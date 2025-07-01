"""
Dashboard Ambiental em Streamlit – Narrativa e Interatividade Completa
---------------------------------------------------------------------
Autor: (seu nome aqui)
Descrição: Aplicação Streamlit para:
    • Séries temporais contínuas + marcadores binários
    • Histogramas, boxplots, análises bivariadas
    • Mapa de calor de correlações de Spearman
    • **Correlação cruzada temporal interativa** (novidade desta versão)
Execute:
    streamlit run dashboard_ambiental.py
Requisitos:
    streamlit, pandas, numpy, matplotlib, seaborn, scipy
"""

# ---------------------- Imports ---------------------- #
import itertools as itera
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr
import streamlit as st

import streamlit.components.v1 as components
st.write("✅ App iniciou")


plt.rcParams.update({
    'figure.facecolor': 'none',
    'axes.facecolor': 'none'
})

st.markdown("""
    <style>
        body {
            background-color: #f7f7f7;
        }
        .stApp {
            background-color: #f7f7f7;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------- Configuração da Página ---------------------- #
st.set_page_config(
    page_title="Dashboard Ambiental",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🌎 O Desafio dos Recursos Hídricos e Produtividade na Amazônia - Dashboard 💧  ")


st.markdown("""
###  Contexto
A gestão dos recursos hídricos na Amazônia vem se tornando crítica: estiagens prolongadas e enchentes severas
desorganizam os ciclos naturais, reduzindo a disponibilidade e a qualidade da água — e, por consequência,impactando:

- 💧 **Qualidade e disponibilidade de água** para consumo, irrigação e uso doméstico.  
- 🌽 **Produtividade agrícola** de comunidades ribeirinhas/agricultores familiares.  
- 🏥 **Saúde pública**, via aumento de doenças transmitidas por água contaminada.  

### 🎯 Objetivos 
Este estudo integra **duas bases de dados** com foco em  quantificar e explicar essas inter-relações climáticas-socioeconômicas, gerando indicadores, visualizações e estatísticas que orientem decisões locais de infraestrutura hídrica, planejamento agrícola e saúde pública.

""")
st.divider()

# ---------------------- Carregamento dos Dados ---------------------- #

# @st.cache_data(show_spinner=True)
def load_data(file) -> pd.DataFrame:
    """Carrega dados CSV e garante a coluna 'data' como datetime."""
    return pd.read_csv(file, parse_dates=["data"])
#
# st.sidebar.header("📂 Origem dos Dados")
# uploaded_file = st.sidebar.file_uploader("Carregue seu arquivo CSV", type=["csv"])
#
# if uploaded_file is not None:
#     df = load_data(uploaded_file)
#     st.sidebar.success("Dados carregados com sucesso! ✅")
# else:
#     # Caminho padrão para o arquivo fixo
#     default_path = Path(__file__).parent.parent / "/home/akel/PycharmProjects/I2A2/data/processed/base_merge_interp.csv"
#     if default_path.exists():
#         df = load_data(default_path)
#         st.sidebar.info("Usando base padrão: `base_merge_interp.csv`")
#     else:
#         st.sidebar.error("Arquivo padrão não encontrado em `data/processed/`")
#         df = None
#
default_path = Path(__file__).parent.parent / "data/processed/base_merge_interp.csv"
df = load_data(default_path)

# ---------------------- Utilidades ---------------------- #

def binary_columns(dataframe: pd.DataFrame):
    bins = []
    for col in dataframe.select_dtypes(include=["int64", "float64"]).columns:
        vals = dataframe[col].dropna().unique()
        if set(vals).issubset({0, 1}):
            bins.append(col)
    return bins

def numeric_continuous_columns(dataframe: pd.DataFrame):
    nums = dataframe.select_dtypes(include=["float64", "int64"]).columns.tolist()
    return [c for c in nums if c not in binary_columns(dataframe)]

def xcorr(a: pd.Series, b: pd.Series, max_lag: int = 30):
    """Retorna tupla (lags, r(lag)) usando correlação de Pearson."""
    lags = np.arange(-max_lag, max_lag + 1)
    rs = [a.corr(b.shift(l)) for l in lags]
    return lags, rs

# ---------------------- Conteúdo Principal ---------------------- #

if df is not None:
    # Organiza por data
    df = df.sort_values("data").reset_index(drop=True)

    # Identifica tipos de colunas
    bin_cols = binary_columns(df)
    num_cols = numeric_continuous_columns(df)

    # ========== Séries Temporais ==========
    st.subheader("📊 Séries Temporais – Contínuas & Marcadores")
    with st.expander("Como interpretar", expanded=False):
        st.markdown(
            """Selecione variáveis contínuas para ver suas trajetórias ao longo do tempo.
            Variáveis **binárias** são plotadas como marcadores ^ indicando
            ocorrências (valor = 1). Isso facilita relacionar eventos discretos a
            padrões contínuos.
            """
        )
    cols_ts_num = st.multiselect(
        "Variáveis contínuas:", options=num_cols, default=num_cols[:3]
    )
    cols_ts_bin = st.multiselect(
        "Marcadores binários:", options=bin_cols, default=bin_cols
    )
    if cols_ts_num or cols_ts_bin:
        fig_ts, ax_ts = plt.subplots(figsize=(12, 4))
        for col in cols_ts_num:
            ax_ts.plot(df["data"], df[col], label=col)
        # Marcadores binários
        y_min, y_max = ax_ts.get_ylim()
        span = y_max - y_min
        marker_y = y_max + 0.04 * span
        for col in cols_ts_bin:
            ones = df[df[col] == 1]["data"]
            ax_ts.scatter(ones, [marker_y] * len(ones), marker="^", s=80, label=f"{col}=1")
        ax_ts.set_ylim(y_min, marker_y + 0.05 * span)
        ax_ts.grid(True, linestyle=":", alpha=0.5)
        ax_ts.legend(ncol=5, loc=1,bbox_to_anchor=(1.0, -0.15), fontsize=8)
        st.pyplot(fig_ts, use_container_width=True)

    st.divider()

    # ========== Análise Univariada – Histogramas Interativos ==========
    st.markdown(
        """### 📈 Análise Univariada – Histogramas Interativos
Esta seção permite observar a **distribuição histórica** de até três variáveis.
Linhas vermelha (**média**) e verde (**mediana**) ajudam na interpretação.
        """
    )

    colunas_hist = [
        "chuvas_reais_mm",
        "temperatura_media_C",
        "indice_umidade_solo",
        "volume_producao_tons",
        "incidencia_doencas",
        "indicador_seguranca_alimentar",
    ]
    titulos_hist = [
        "Chuvas Reais (mm)",
        "Temperatura Média (°C)",
        "Índice Umidade Solo (%)",
        "Volume Produção (ton)",
        "Incidência Doenças",
        "Segurança Alimentar",
    ]
    bins_var = [20, 20, 15, 20, 6, 20]

    selecao_vars = st.multiselect(
        "Selecione até 3 variáveis:",
        options=list(zip(colunas_hist, titulos_hist)),
        format_func=lambda x: x[1],
        default=list(zip(colunas_hist, titulos_hist))[:3],
        max_selections=3,
    )
    if selecao_vars:
        fig_hist, axes = plt.subplots(1, len(selecao_vars), figsize=(6 * len(selecao_vars), 4))
        if len(selecao_vars) == 1:
            axes = [axes]
        sns.set(style="whitegrid")
        for i, (col, title) in enumerate(selecao_vars):
            ax = axes[i]
            bins = bins_var[colunas_hist.index(col)]
            sns.histplot(df[col].dropna(), color="dodgerblue", bins=bins, alpha=0.7, ax=ax)
            ax.axvline(df[col].mean(), color="red", ls="--", lw=1.5, label=f"Média: {df[col].mean():.2f}")
            ax.axvline(df[col].median(), color="green", ls="-", lw=1.5, label=f"Mediana: {df[col].median():.2f}")
            ax.set_title(title)
            ax.set_xlim(df[col].quantile(0.05), df[col].quantile(0.95))
            ax.legend(fontsize=8)
        plt.tight_layout(pad=2.0)
        st.pyplot(fig_hist, use_container_width=True)

    st.divider()

    # ========== Boxplots ==========
    st.subheader("📦 Boxplots Comparativos")
    with st.expander("O que você verá aqui?", expanded=False):
        st.markdown(
            """Explicação box-plot e critérios
            """
        )
    vars_box = st.multiselect("Variáveis (até 3):", options=num_cols, default=num_cols[:3], max_selections=3)
    if vars_box:
        fig_box, axes_box = plt.subplots(1, len(vars_box), figsize=(4 * len(vars_box), 4))
        if len(vars_box) == 1:
            axes_box = [axes_box]
        for ax, col in zip(axes_box, vars_box):
            # Tornar fundo da figura e do eixo transparentes
            fig_box.patch.set_alpha(0.0)  # fundo da figura
            ax.set_facecolor("none")  # fundo do eixo

            sns.boxplot(y=df[col], ax=ax)
            ax.set_title(col)
        st.pyplot(fig_box, use_container_width=True)

    st.divider()

    # ========== Análise Bivariada ==========
    sns.set_theme(style="whitegrid", rc={"axes.facecolor": "none", "figure.facecolor": "none"})

    st.subheader("🔗 Análise Bivariada – Dois Pares Paralelos")
    with st.expander("O que você verá aqui?", expanded=False):
        st.markdown(
            """Explicação bi-variada
            """
        )
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        x1 = st.selectbox("X1", options=num_cols + bin_cols, key="x1",
                          index=(num_cols + bin_cols).index("chuvas_reais_mm"))
    with col2:
        y1 = st.selectbox("Y1", options=num_cols + bin_cols, key="y1",
                          index=(num_cols + bin_cols).index("temperatura_media_C"))
    with col3:
        x2 = st.selectbox("X2", options=num_cols + bin_cols, key="x2",
                          index=(num_cols + bin_cols).index("chuvas_reais_mm"))
    with col4:
        y2 = st.selectbox("Y2", options=num_cols + bin_cols, key="y2",
                          index=(num_cols + bin_cols).index("chuvas_previstas_mm"))
    fig_bi, axes_bi = plt.subplots(1, 2, figsize=(12, 4))
    pairs_to_plot = [(x1, y1, axes_bi[0]), (x2, y2, axes_bi[1])]
    for xi, yi, ax in pairs_to_plot:
        ax.set_facecolor("none")
        if xi != yi:
            sns.regplot(data=df, x=xi, y=yi, ax=ax, scatter_kws={"alpha": 0.6})
            r_val = df[[xi, yi]].corr(method="spearman").iloc[0, 1]
            ax.set_title(f"{xi} vs {yi} (ρ = {r_val:.2f})")
        else:
            ax.set_visible(False)
    st.pyplot(fig_bi, use_container_width=True)

    st.divider()

    # ========== Mapa de Calor Spearman ==========
    st.subheader("🌡️ Mapa de Calor de Correlações de Spearman")
    with st.expander("O que você verá aqui?", expanded=False):
        st.markdown(
            """Explicação mapa de calor
            """
        )
    df_interp = df.set_index("data").interpolate(method="time")

    def corr_spearman_pvals(data):
        cols = data.columns
        rho = pd.DataFrame(np.eye(len(cols)), index=cols, columns=cols, dtype=float)
        p = pd.DataFrame(np.zeros_like(rho), index=cols, columns=cols, dtype=float)
        for i in range(len(cols)):
            for j in range(i + 1, len(cols)):
                mask = data[[cols[i], cols[j]]].dropna()
                if mask.empty:
                    continue
                rho_ij, p_ij = spearmanr(mask[cols[i]], mask[cols[j]])
                rho.iloc[i, j] = rho.iloc[j, i] = rho_ij
                p.iloc[i, j] = p.iloc[j, i] = p_ij
        return rho, p

    R, P = corr_spearman_pvals(df_interp[num_cols + bin_cols])
    R.mask(abs(R) < 0.2, inplace=True)
    R.mask(P >= 0.05, inplace=True)
    R.mask(R.abs() >= 0.99, inplace=True)

    fig_heat, ax_heat = plt.subplots(figsize=(10, 8))
    sns.heatmap(R, cmap="coolwarm", annot=True, fmt=".2f", vmin=-1, vmax=1, ax=ax_heat)
    ax_heat.set_title("Correlação de Spearman |ρ| > 0.2 & p < 0.05")
    st.pyplot(fig_heat, use_container_width=True)


    st.divider()

    # ========== Correlação Cruzada Temporal ==========
    st.subheader("🔄 Correlação Cruzada Temporal (r(lag))")
    with st.expander("O que você verá aqui?", expanded=False):
        st.markdown(
            """Esta seção investiga se **mudanças em uma variável precedem ou seguem mudanças em outra**.
            O gráfico mostra **r(lag)** para deslocamentos de –\(k\) … +\(k\) dias.
            Picos altos indicam forte relacionamento com defasagem específica.
            """
        )

    # Parâmetros interativos
    var_x_cc = st.selectbox("Série X", options=num_cols, index=0)
    var_y_cc = st.selectbox("Série Y", options=[c for c in num_cols if c != var_x_cc], index=1)
    max_lag = st.slider("Deslocamento máximo (dias)", 5, 60, 30)
    thr_r = st.slider("|r| mínimo para destac", 0.0, 1.0, 0.20, 0.05)

    if var_x_cc and var_y_cc and var_x_cc != var_y_cc:
        lags_cc, rs_cc = xcorr(df_interp[var_x_cc], df_interp[var_y_cc], max_lag)
        best_idx = int(np.nanargmax(np.abs(rs_cc)))
        best_lag = lags_cc[best_idx]
        best_r = rs_cc[best_idx]

        fig_cc, ax_cc = plt.subplots(figsize=(10, 4))
        ax_cc.stem(lags_cc, rs_cc, basefmt=" ")
        ax_cc.axhline(thr_r, ls="--", color="gray", alpha=0.7)
        ax_cc.axhline(-thr_r, ls="--", color="gray", alpha=0.7)
        ax_cc.axvline(best_lag, color="red", ls=":" , alpha=0.6)
        ax_cc.set_xlabel("Defasagem (dias)")
        ax_cc.set_ylabel("r(lag)")
        ax_cc.set_title(f"{var_x_cc} ↔ {var_y_cc}   •   rₘₐₓ = {best_r:.2f} @ lag = {best_lag} d")
        ax_cc.grid(alpha=0.3)
        st.pyplot(fig_cc, use_container_width=True)

    # ---- Top N pares automaticamente ----
#     st.subheader("🔥 Pares com Maior |r(lag)| (auto)")
#     top_n = st.slider("Mostrar top N pares", 1, 5, 3)
#     # gera todas as combinações numéricas
#     resultados = []
#     for var_x, var_y in itera.combinations(num_cols, 2):
#         lags, rs = xcorr(df_interp[var_x], df_interp[var_y], max_lag)
#         rs = np.array(rs)
#         lags = np.array(lags)
#         idx_best = np.nanargmax(np.abs(rs))
#         if abs(rs[idx_best]) >= thr_r:
#             resultados.append({
#                 "Var X": var_x,
#                 "Var Y": var_y,
#                 "Lag": int(lags[idx_best]),
#                 "r_max": float(rs[idx_best]),
#             })
#     if resultados:
#         df_res = (
#             pd.DataFrame(resultados)
#             .assign(abs_r=lambda d: d["r_max"].abs())
#             .sort_values("abs_r", ascending=False)
#             .head(top_n)
#         )
#         st.dataframe(df_res, hide_index=True, use_container_width=True)
#
#         # subplots para cada par
#         fig_top, axs_top = plt.subplots(top_n, 1, figsize=(10, 4 * top_n))
#         if top_n == 1:
#             axs_top = [axs_top]
#         for ax, (_, row) in zip(axs_top, df_res.iterrows()):
#             var_x, var_y, lag, rmax = row["Var X"], row["Var Y"], int(row["Lag"]), row["r_max"]
#             lags, rs = xcorr(df_interp[var_x], df_interp[var_y], max_lag)
#             ax.stem(lags, rs, basefmt=" ")
#             ax.axhline(thr_r, ls="--", color="gray", alpha=0.7)
#             ax.axhline(-thr_r, ls="--", color="gray", alpha=0.7)
#             ax.axvline(lag, color="red", ls=":" , alpha=0.6)
#             ax.set_ylabel("r(lag)")
#             ax.set_title(f"{var_x} ↔ {var_y} • rₘₐₓ={rmax:.2f}@lag={lag} d")
#             ax.grid(alpha=0.3)
#         plt.tight_layout(h_pad=0.5)
#         st.pyplot(fig_top, use_container_width=True)
#     else:
#         st.info("Nenhum par alcançou o |r| mínimo selecionado.")
#
# else:
#     st.info("Carregue um arquivo CSV para iniciar a análise.")
