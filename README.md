## 🌿 Análise Ambiental - I2A2 (Desafios na Amazônia)

### 🛍️ Contexto

O estado do Pará enfrenta um complexo e multifacetado desafio socioambiental, no qual a busca pelo desenvolvimento coexiste com a crescente degradação de seus recursos naturais. Os dados apresentam diversos indicadores de infraestrutura socioeconômica, bem como indicadores de degradação ambiental. Os dados expõem um dilema: **a presença de serviços básicos se traduz em sustentabilidade ambiental ou em melhorias socioeconômicas?**

### 🌟 Objetivos

Investigar, entender, encontrar insights e propor soluções para os desafios socioambientais enfrentados pelas comunidades amazônicas, com base em dados reais.

---

## 📁 Estrutura do Projeto

```bash
📆 projeto-i2a2-amazonia/
│
├── data/                 # Dados brutos, processados e fontes externas
│   ├── raw/              # Dados originais (sem modificação)
│   ├── processed/        # Dados limpos e prontos para análise
│
├── notebooks/            # Jupyter Notebooks com análises exploratórias e visuais
│
├── scripts/              # Scripts Python para ETL, modelagem ou visualização
│
├── outputs/              # Resultados: gráficos, mapas, relatórios
│
├── README.md             # Esta documentação
└── requirements.txt      # Dependências do projeto
```

---

## 📓 Descrição dos Dados

| Variável                 | Tipo       | Descrição                                   |
| ------------------------ | ---------- | ------------------------------------------- |
| `municipio`              | categórica | Nome da comunidade/localidade               |
| `desmatamento`           | numérica   | Área desmatada (hectares)                   |
| `queimadas`              | numérica   | Número de focos de calor registrados        |
| `cobertura_vegetal`      | percentual | Percentual de vegetação nativa remanescente |
| `renda_media`            | numérica   | Renda média domiciliar da comunidade        |
| `infra_agua`             | binária    | Acesso a água potável (0 = não, 1 = sim)    |
| `infra_esgoto`           | binária    | Acesso a esgotamento sanitário              |
| `infra_energia`          | binária    | Acesso à rede elétrica                      |
| `densidade_populacional` | numérica   | Habitantes por km²                          |
| `latitude`, `longitude`  | geográfica | Coordenadas geográficas da comunidade       |

> 💡 *Outras variáveis relevantes podem ser adicionadas conforme a análise avança.*

---

## 🔍 Metodologia

1. **Pré-processamento dos dados**

   * Limpeza, padronização e enriquecimento.

2. **Análise Exploratória (EDA)**

   * Distribuições, correlações e outliers.

3. **Visualizações geográficas e temporais**

   * Mapas interativos, séries históricas e comparações entre regiões.

4. **Modelagem e insights**

   * Identificação de padrões e agrupamentos de comunidades.

5. **Propostas e recomendações**

   * Soluções orientadas a dados.

---

## 📊 Ferramentas e Tecnologias

* Python (pandas, geopandas, matplotlib, seaborn, scikit-learn)
* Jupyter Notebook
* QGIS (opcional)
* Streamlit (para dashboards)
* Git + GitHub

---

## 🗌 Resultados Esperados

* Mapas temáticos com sobreposição de variáveis socioambientais
* Relatórios com análises quantitativas e qualitativas
* Gráficos interativos que expliquem a relação entre infraestrutura e degradação ambiental
* Repositório de dados limpos e organizados para reuso

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para colaborar:

1. Fork este repositório
2. Crie uma branch: `git checkout -b minha-analise`
3. Faça suas alterações
4. Envie um pull request

---

## 📝 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
