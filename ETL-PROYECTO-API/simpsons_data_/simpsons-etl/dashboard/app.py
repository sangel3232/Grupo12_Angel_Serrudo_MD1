import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:1234@localhost:5432/Simpsons_db")

st.title("📊 Simpsons Data Dashboard")

query = "SELECT * FROM dim_characters"
df = pd.read_sql(query, engine)

st.subheader("Personajes")

st.dataframe(df)

st.subheader("Personajes por género")

gender_count = df["gender"].value_counts()

st.bar_chart(gender_count)

st.subheader("Top ocupaciones")

occupation_count = df["occupation"].value_counts().head(10)

st.bar_chart(occupation_count)