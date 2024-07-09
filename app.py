import streamlit as st
import pandas as pd
import sqlite3
import json

db = sqlite3.connect('database.sqlite')
cursor = db.cursor()
mínimo = st.number_input('Digite o valor mínimo do ativo')

statement = 'SELECT details FROM ativos'
fetchall = cursor.execute(statement).fetchall()

Abertura = []
Volume = []
ExtremosDia = []
Variacao = []

for index, row in enumerate(fetchall):
    data = json.loads(row[0])
    x = float(data.get('Abertura').replace(',','.'))
    if x < mínimo:  
      Abertura.append(x)
      Volume.append(data.get('Volume'))
      ExtremosDia.append(data.get('Mín — Máx (Dia)'))
      Variacao.append(data.get('Variação (Dia)'))

st.table({'Abertura': Abertura, 'Volume': Volume, 'ExtremosDia': ExtremosDia, 'Variacao': Variacao})

st.bar_chart(pd.DataFrame({'Abertura': Abertura}))