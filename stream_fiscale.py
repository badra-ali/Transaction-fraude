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

import schedule
import time
import requests
from bs4 import BeautifulSoup

def retrieve_data():
    data_pays=[]
    data_Entite_contractante=[]
    data_pays_titre=[]
    data_projet=[]
    data_lancement=[]
    data_statut=[]
    data_limite=[]
    data_NAO=[]
    stock_price_pays=[]
    stock_price_Entite_contractante=[]
    stock_price_projet=[]
    stock_price_lancement=[]
    stock_price_statut=[]
    stock_price_limite=[]
    stock_price_NAO=[]
    for i in range(30):
        url = f"https://devbusiness.un.org/site-search?page={i}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        price_element_pays = soup.findAll("span",class_="card__countries-country")
        if price_element_pays:
            for element in price_element_pays:
                stock_price_pays.append(element.text)

        price_element_Entite_contractante = soup.findAll("span",class_="card__institution")
        if price_element_Entite_contractante:
            for element in price_element_Entite_contractante:
                stock_price_Entite_contractante.append(element.text)

        price_element_titre = soup.findAll("h3",class_="heading card-search-result__title")
        if price_element_titre:
            stock_price_titre=[]
            for element in price_element_titre:
                stock_price_titre.append(element.text)

        price_element_projet = soup.findAll("div",class_="col-sm-6 card__content-wrapper")
        if price_element_projet:
            for element in price_element_projet:
                stock_price_projet.append(element.text)

        price_element_lancement = soup.findAll("div",class_="col-sm-2 card__date-posted")
        if price_element_lancement:
            for element in price_element_lancement:
                stock_price_lancement.append(element.text)

        price_element_statut = soup.findAll("div",class_="col-sm-2 card__status")
        if price_element_statut:
            for element in price_element_statut:
                stock_price_statut.append(element.text)

        price_element_limite = soup.findAll("div",class_="col-sm-6")
        if price_element_limite:
            for element in price_element_limite:
                stock_price_limite.append(element.text)
        else:
            stock_price_limite.append(0)

        price_element_NAO = soup.findAll("div",class_="col-sm-2 card__db-ref")
        if price_element_NAO:
            for element in price_element_NAO:
                stock_price_NAO.append(element.text+"\n\n"+str(i))

    data_pays.append(stock_price_pays)
    data_Entite_contractante.append(stock_price_Entite_contractante)
    data_pays_titre.append(stock_price_titre)
    data_lancement.append(stock_price_lancement)
    data_statut.append(stock_price_statut)
    data_limite.append(stock_price_limite)
    data_NAO.append(stock_price_NAO)

    data_pays=pd.DataFrame(stock_price_pays)
    data_Entite_contractante=pd.DataFrame(stock_price_Entite_contractante)
    data_pays_titre=pd.DataFrame(stock_price_titre)
    data_projet=pd.DataFrame(stock_price_projet)
    data_lancement=pd.DataFrame(stock_price_lancement)
    data_statut=pd.DataFrame(stock_price_statut)
    data_limite=pd.DataFrame(stock_price_limite)
    data_NAO=pd.DataFrame(stock_price_NAO)

    data_NAO.to_excel("Data_NAO.xlsx")
    data_projet.to_excel("data_projet.xlsx")
    data_pays.to_excel("data_pays.xlsx")
    data_Entite_contractante.to_excel("data_Entite_contractante.xlsx")
    data_pays_titre.to_excel("data_pays_titre.xlsx")
    data_limite.to_excel("data_limite.xlsx")
    data_statut.to_excel("data_statut.xlsx")
    data_lancement.to_excel("data_lancement.xlsx")

    print("ok ok")
# Planification de l'exécution toutes les heures
schedule.every(3).minutes.do(lambda: retrieve_data())
print("ok ok ok")
#data_pays,data_Entite_contractante,data_pays_titre,data_lancement,data_statut,data_limite,data_NAO=retrieve_data()
# Boucle d'exécution continue
while True:
      schedule.run_pending()
      time.sleep(1)

import pandas as pd
import numpy as np

# Définir la taille de la base de données
nb_lignes = 1000

# Générer des données aléatoires pour chaque colonne
noms = ['Alice', 'Bob', 'Charlie', 'David', 'Eve']
ages = np.random.randint(18, 70, size=nb_lignes)
salaires = np.random.randint(20000, 100000, size=nb_lignes)
ville = np.random.choice(['Paris', 'Londres', 'New York', 'Tokyo'], size=nb_lignes)

# Créer un DataFrame Pandas avec les données générées
data = {
    'Nom': np.random.choice(noms, size=nb_lignes),
    'Age': ages,
    'Salaire': salaires,
    'Ville': ville
}
df = pd.DataFrame(data)
    
#df=pd.read_excel("C:/Users/alidjou.bamba/Transaction-fraude/Base_de_donnee_Banque_Mondiale.xlsx")
    
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



