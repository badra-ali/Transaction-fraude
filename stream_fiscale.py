import streamlit as st
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns
#from sklearn.model_selection import train_test_split
#from sklearn.linear_model import LinearRegression
#from sklearn.metrics import mean_squared_error

# Charger les donnéesst.cache_data
@st.cache_data
def load_data(uploaded_file):
    df=pd.read_excel(uploaded_file)
    return df
    

#st.image('Logo_bnetd_transparence.png',caption=' ')


#uploaded_file=st.file_uploader("Fichier Appel d'Offre",type=["xlsx","xls","csv"])
#if uploaded_file is not None:
#df = load_data(uploaded_file)
    
df=pd.read_excel("C:/Users/alidjou.bamba/Transaction-fraude/Base_de_donnee_Banque_Mondiale.xlsx")
    
# Titre de l'application
st.title('Analyse des appels d offres de 2023')
    
# Afficher un résumé des données
st.subheader('Résumé des données')
st.write(df.head())
st.write(df.info())
    
"""col1, col2, col3 = st.columns(3)
    with col1:
            st.subheader('Rapartition des AO par Pays')
            type_handicap = df['Pays']
    
            # Compter le nombre de AO pour chaque OC
            count_handicap_types = type_handicap.value_counts()
            count_handicap_types=count_handicap_types.sort_values()[-10:]
            # Créer un diagramme en secteurs
            fig=plt.figure(figsize=(8, 8))
            count_handicap_types.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['lightblue', 'lightcoral', 'lightgreen', 'lightyellow', 'lightsalmon'])
            plt.title('Pays')
            plt.ylabel('')  # Supprimer l'étiquette y
            st.pyplot(fig)
            
    with col1:
            st.subheader('Rapartition des AO par Projet')
            type_handicap = df['Titre']
    
            # Compter le nombre de AO pour chaque OC
            count_handicap_types = type_handicap.value_counts()
            count_handicap_types=count_handicap_types.sort_values()[-10:]
            # Créer un diagramme en secteurs
            fig=plt.figure(figsize=(5,5))
            count_handicap_types.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['lightblue', 'lightcoral', 'lightgreen', 'lightyellow', 'lightsalmon'])
            plt.title('Projet')
            plt.ylabel('')  # Supprimer l'étiquette y
            st.pyplot(fig)
        
    with col2:
        
            st.subheader('Rapartition des AO Statut')
            type_handicap = df['Statut']
    
            # Compter le nombre de AO pour chaque OC
            count_handicap_types = type_handicap.value_counts()
            count_handicap_types=count_handicap_types.sort_values()[-10:]
            # Créer un diagramme en secteurs
            fig=plt.figure(figsize=(8, 8))
            count_handicap_types.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['lightblue', 'lightcoral', 'lightgreen', 'lightyellow', 'lightsalmon'])
            plt.title('Rapartition des AO par Statut')
            plt.ylabel('')  # Supprimer l'étiquette y
            st.pyplot(fig)"""
    
    
st.write("BAMBA")



