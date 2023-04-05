import statistics

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import openpyxl
from io import StringIO
import xlrd


# Set page config


st.set_page_config(page_title="My Streamlit App", page_icon=":guardsman:")





st.title("Analyse des résultats du Baccalauréat :blue[2021] session :yellow[complementaire]")
# Charger le fichier Excel
excel_file = 'resBac.xls'
sheet_name = 'SESSION'

df = pd.read_excel(excel_file,
             sheet_name,
            )
bac = df[['Numéro Bac', 'Nom', 'Ecole', 'Centre Examen', 'SERIE', 'Moy Session Compl','Decision']]

# Afficher le dataframe
#st.write(bac)


# Créer un champ de saisie de texte pour la recherche
search_term = st.text_input('Rechercher par numéro bac ou nom')

# Créer un espace réservé pour le dataframe filtré
filtered_df_placeholder = st.empty()

# Filtrer le dataframe en temps réel
with st.spinner('Recherche en cours...'):
    filtered_df = bac[bac[['Numéro Bac', 'Nom']].apply(lambda row: row.astype(str).str.contains(search_term).any(), axis=1)]
    # Afficher le dataframe filtré
    filtered_df_placeholder.write(filtered_df)



# Obtenir le nombre total des admis et ajournés
nombre_admis = bac['Decision'].value_counts()['Admis']
nombre_ajournés = bac['Decision'].value_counts()['Ajourné']
nb_total = bac['Decision'].count()
# Calculer le pourcentage de chaque catégorie
pourcentage_hommes = (nombre_admis / nb_total) * 100
pourcentage_femmes = (nombre_ajournés / nb_total) * 100

# Create some sample data
labels = ['Ajourné ', 'Admis ']
percentages = [pourcentage_hommes, pourcentage_femmes]

# Create a square chart with percentages
fig, ax = plt.subplots()
ax.pie(percentages, labels=labels, autopct='%1.1f%%', startangle=90)
ax.axis('equal')
ax.set_title('Pourcentage des admis et ajournés')

# Display the chart in Streamlit
st.pyplot(fig)



# Create a pivot table with center as the index, decision as the columns, and count as the values
center_counts = pd.pivot_table(bac, index="Centre Examen", columns="Decision", values="Numéro Bac", aggfunc="count", fill_value=0)

# Rename the columns to be more descriptive
center_counts.columns = ["Admis", "Ajournés"]
center_counts['Total'] = center_counts['Admis'] + center_counts['Ajournés']

center_counts['Moyenne d\'admission'] = (center_counts['Admis'] / center_counts['Total']) * 100


fig = px.scatter(center_counts, x='Admis', y='Ajournés', color=center_counts.index,size='Total',
                 title='Nombre d\'admis et d\'ajournés pour chaque centre d\'examen',width=900, height=700,
                 hover_name=center_counts.index, hover_data={'Total': True, 'Admis': True, 'Ajournés': True})

st.write(fig)
st.subheader("Information sur les centres d'examen")
st.write(center_counts)

# Créer un nouveau dataframe avec le nom de l'école et la moyenne générale de ses étudiants
#school_means = bac.groupby('Ecole')['Moy Session Compl'].mean().reset_index()
#school_means = school_means.rename(columns={'Moy Session Compl': 'Moyenne générale'})
#st.write(school_means)

center_infos = pd.pivot_table(bac, index=['Centre Examen','Ecole'], columns='SERIE', values='Moy Session Compl', aggfunc='mean').round(2)
st.write(center_infos)
st.markdown("Thanks for :blue[visiting]")
st.markdown("All Rights :red[reserved]")
st.write("Contact Us ")



