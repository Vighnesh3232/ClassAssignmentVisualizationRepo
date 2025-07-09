
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load Data
@st.cache_data
def load_data():
    return pd.read_excel("happiness_data.xlsx")

df = load_data()

# Preprocessing
df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace(":", "").str.replace("+", "_plus_")
latest_year = df['year'].max()

# Sidebar
st.sidebar.title("🌍 Country Selector")
country = st.sidebar.selectbox("Select a Country", sorted(df['country_name'].unique()))

# Main Title
st.title("😊 Global Happiness Index Dashboard")

# Line Chart - Ladder Score Over Time
st.subheader(f"{country} - Happiness Score Over Time")
country_df = df[df['country_name'] == country].sort_values("year")
fig1 = px.line(country_df, x="year", y="ladder_score", markers=True)
st.plotly_chart(fig1, use_container_width=True)

# Radar Chart - Indicators (Latest Year)
st.subheader(f"{country} - Indicator Breakdown ({latest_year})")
indicators = [
    "explained_by_log_gdp_per_capita",
    "explained_by_social_support",
    "explained_by_healthy_life_expectancy",
    "explained_by_freedom_to_make_life_choices",
    "explained_by_generosity",
    "explained_by_perceptions_of_corruption"
]
latest_data = country_df[country_df["year"] == latest_year].iloc[0]
radar_fig = go.Figure()
radar_fig.add_trace(go.Scatterpolar(
    r=[latest_data[ind] for ind in indicators],
    theta=[ind.replace("explained_by_", "").replace("_", " ").title() for ind in indicators],
    fill='toself',
    name=country
))
radar_fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=False)
st.plotly_chart(radar_fig, use_container_width=True)

# Choropleth Map
st.subheader(f"World Happiness Map ({latest_year})")
map_df = df[df['year'] == latest_year]
map_fig = px.choropleth(
    map_df,
    locations="country_name",
    locationmode="country names",
    color="ladder_score",
    hover_name="country_name",
    color_continuous_scale="Viridis"
)
st.plotly_chart(map_fig, use_container_width=True)
