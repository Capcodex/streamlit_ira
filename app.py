import streamlit as st
import pandas as pd
import plotly.express as px

# Charger les données
@st.cache_data
def load_data():
    df = pd.read_csv("df_clean.csv")  # Remplace par ton fichier
    return df

df = load_data()

# Dictionnaire de conversion des noms de pays
country_translation = {
    "Afrique du Sud": "South Africa", "Allemagne": "Germany", "Argentine": "Argentina", "Australie": "Australia", "Autriche": "Austria",
    "Belgique": "Belgium", "Brésil": "Brazil", "Bulgarie": "Bulgaria", "Canada": "Canada", "Chine": "China", "Chypre": "Cyprus",
    "Colombie": "Colombia", "Corée du Sud": "South Korea", "Croatie": "Croatia", "Danemark": "Denmark", "Ecosse (Royaume-Uni)": "Scotland",
    "Espagne": "Spain", "Estonie": "Estonia", "Finlande": "Finland", "France": "France", "Grèce": "Greece", "Hong Kong": "Hong Kong",
    "Hongrie": "Hungary", "Inde": "India", "Indonésie": "Indonesia", "Iran": "Iran", "Irlande": "Ireland", "Irlande du Nord (Royaume-Uni)": "Northern Ireland",
    "Israël": "Israel", "Italie": "Italy", "Japon": "Japan", "Kenya": "Kenya", "Lettonie": "Latvia", "Liban": "Lebanon", "Lituanie": "Lithuania",
    "Luxembourg": "Luxembourg", "Malaisie": "Malaysia", "Maroc": "Morocco", "Mexique": "Mexico", "Monaco": "Monaco", "Norvège": "Norway",
    "Nouvelle-Zélande": "New Zealand", "Pays de Galles (Royaume-Uni)": "Wales", "Pays-Bas": "Netherlands", "Philippines": "Philippines",
    "Pologne": "Poland", "Portugal": "Portugal", "Qatar": "Qatar", "Roumanie": "Romania", "Royaume-Uni": "United Kingdom", "Russie": "Russia",
    "Serbie": "Serbia", "Singapour": "Singapore", "Slovaquie": "Slovakia", "Suisse": "Switzerland", "Suède": "Sweden", "Taïwan": "Taiwan",
    "Tchéquie": "Czech Republic", "Thaïlande": "Thailand", "Turquie": "Turkey", "Ukraine": "Ukraine", "Uruguay": "Uruguay", "Viêt Nam": "Vietnam",
    "Émirats arabes unis": "United Arab Emirates", "États-Unis": "United States"
}

# Appliquer la conversion des noms de pays
df["main_country_en"] = df["main_country"].map(country_translation)

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

# 🌍 Carte du monde avec Plotly
st.subheader("🌍 Répartition des artistes par pays")
country_counts = df["main_country_en"].value_counts().reset_index()
country_counts.columns = ["Country", "Artist Count"]

fig = px.choropleth(
    country_counts,
    locations="Country",
    locationmode="country names",
    color="Artist Count",
    title="Répartition des artistes par pays",
    color_continuous_scale="viridis"
)

st.plotly_chart(fig)

# 📆 Distribution des années de naissance
st.subheader("📆 Répartition des artistes par période de naissance")
fig = px.histogram(df, x="year_birth", nbins=1000, title="Distribution des années de naissance des artistes")
st.plotly_chart(fig)
