import streamlit as st 
from quienGanara import prediccion as predic
import csv
import pandas as pd 
import numpy as np 
import altair as alt

st.title("Enfrenta a dos Pokemon y descubre quién será el ganador")
num1 = st.number_input("Primer Pokemon", min_value=1, max_value=300)
st.write(num1)
num2 = st.number_input("Segundo Pokemon", min_value=1, max_value=300)
st.write(num2)



with open("datas/pokedex.csv", newline='') as csvfile:
    pokedex = csv.reader(csvfile) 
    next(pokedex)
    valores = predic(num1, num2,pokedex)
    st.write(valores)

