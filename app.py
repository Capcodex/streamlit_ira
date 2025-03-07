import streamlit as st
import pandas as pd
import plotly.express as px

# Charger les données
@st.cache_data  # Mise en cache pour optimiser les performances
def load_data():
    df = pd.read_csv("df_clean.csv")  # Remplace par ton vrai fichier
    return df

df = load_data()

# Calcul des métriques
num_artists = df["artist_id"].nunique()
ca_mean = df["ca"].mean()
main_medium = df["main_medium"].mode()[0]
most_represented_countries = df["main_country"].value_counts().head(5)
avg_rank = df["rank"].mean()
year_birth_desc = df["year_birth"].describe()

# Layout du tableau de bord
st.title("📊 Dashboard Artistes Insight")
st.write("Aperçu des principaux indicateurs du marché de l'art basé sur les artistes répertoriés.")

# 🏆 Cartes de métriques
col1, col2, col3 = st.columns(3)

col1.metric("🏆 Nombre total d'artistes", f"{num_artists:,}")
col2.metric("💰 Chiffre d’affaires moyen", f"${ca_mean:,.2f}")
col3.metric("🎨 Médium artistique le plus courant", main_medium)

col4, col5, col6 = st.columns(3)

col4.metric("📈 Classement moyen des artistes", f"{avg_rank:.2f}")
col5.metric("📆 Âge moyen des artistes (naissance)", f"{year_birth_desc['mean']:.0f}")
col6.metric("🔝 Pays les plus représentés", most_represented_countries.index[0])

# 🌍 Carte des pays les plus représentés
st.subheader("🌎 Répartition des artistes par pays")
country_counts = df["main_country"].value_counts().reset_index()
country_counts.columns = ["country", "count"]
country_counts["country_en"] = country_counts["country"].map({
    "Allemagne": "Germany", "France": "France", "États-Unis": "United States", "Royaume-Uni": "United Kingdom",
    "Italie": "Italy", "Espagne": "Spain", "Chine": "China", "Japon": "Japan", "Brésil": "Brazil"
})
country_counts["country_en"].fillna(country_counts["country"], inplace=True)

fig_map = px.choropleth(
    country_counts,
    locations="country_en",
    locationmode="country names",
    color="count",
    hover_name="country",
    title="Nombre d'artistes par pays"
)
st.plotly_chart(fig_map)

# 📆 Distribution des années de naissance
st.subheader("📆 Répartition des artistes par période de naissance")
fig = px.histogram(df, x="year_birth", nbins=1000, title="Distribution des années de naissance des artistes")
st.plotly_chart(fig)

# 🎭 Top des artistes
st.subheader("🏅 Top des artistes")

# Choix du tri
type_tri = st.radio("Trier par :", ["Chiffre d'affaires (CA)", "Classement (Rank)"])

# Sélecteur du pays
selected_country = st.selectbox("Choisir un pays", ["Tous"] + sorted(df["main_country"].dropna().unique().tolist()))

# Sélection des fourchettes pour le Rank et CA
col1, col2 = st.columns(2)
rank_min = col1.number_input("Rank minimum", min_value=int(df["rank"].min()), max_value=int(df["rank"].max()), value=int(df["rank"].min()))
rank_max = col2.number_input("Rank maximum", min_value=int(df["rank"].min()), max_value=int(df["rank"].max()), value=int(df["rank"].max()))

col3, col4 = st.columns(2)
ca_min = col3.number_input("Chiffre d'affaires minimum", min_value=float(df["ca"].min()), max_value=float(df["ca"].max()), value=float(df["ca"].min()))
ca_max = col4.number_input("Chiffre d'affaires maximum", min_value=float(df["ca"].min()), max_value=float(df["ca"].max()), value=float(df["ca"].max()))

# Filtrage des artistes
filtered_df = df.copy()
if selected_country != "Tous":
    filtered_df = filtered_df[filtered_df["main_country"] == selected_country]
filtered_df = filtered_df[(filtered_df["rank"] >= rank_min) & (filtered_df["rank"] <= rank_max)]
filtered_df = filtered_df[(filtered_df["ca"] >= ca_min) & (filtered_df["ca"] <= ca_max)]

# Tri des artistes
if type_tri == "Chiffre d'affaires (CA)":
    filtered_df = filtered_df.sort_values(by="ca", ascending=False)
else:
    filtered_df = filtered_df.sort_values(by="rank", ascending=True)

# Choix du nombre d'artistes à afficher
num_artists_display = st.slider("Nombre d'artistes à afficher", 1, 50, 10)
st.table(filtered_df[["artist_name", "main_country", "rank", "ca"]].head(num_artists_display))
