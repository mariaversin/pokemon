import streamlit as st 
from quienGanara import prediccion as predic
import csv
st.title("Enfrenta a dos Pokemon y descubre quién será el ganador")


with open("datas/pokedex.csv", newline='') as csvfile:
    pokedex = csv.reader(csvfile) 
    next(pokedex)
    valores = predic(268,518,pokedex)
    st.write(valores)