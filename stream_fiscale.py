import numpy as np
import altair as alt
import streamlit as st
from datetime import time, datetime,date
#from fastapi import FastAPI
from scipy.optimize import newton
import math
import time
from keras.models import load_model
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Model
from keras.layers import Input, Dense

class Traitement_data:
    def __init__(self,data_tansaction):
        
        self.data_tansaction=data_tansaction
        self.Data_copie=self.data_tansaction.copy()
    
    def Traitement_de_la_data(self):
        

        #supprimer les colonnes moins importantes
        self.data_tansaction=self.data_tansaction.drop(
        ['IdStructure','IdSociete','TauxCSS','TauxIRVM','TauxActuarial','FraisIRVM','FraisCSS','OrigineImportation','DateJouissance','IdOrdreExecuteImporte', 'ReferenceDcbr', 'DateExecutionDcbr','DateValidation', 'HeureValidation', 
               'DateAnnulation', 'HeureAnnulation', 'MotifAnnulation','NameAnnuleur','LoginAnnuleur','TauxSgi','CoursSgi','Marge'], axis=1)

        #remplaçons les NAN par la valeur suivante ou précédente si le pourcentage de la valeur manquante dans la colonne est inférieur ou égale à 5%
        threshold = 0.05
        for col in self.data_tansaction.columns:
            nan_proportion = self.data_tansaction[col].isna().sum() / len(self.data_tansaction)
            if 0 < nan_proportion <= threshold:
                self.data_tansaction[col].fillna(method='ffill', inplace=True)
                self.data_tansaction[col].fillna(method='bfill', inplace=True)


        # Liste des colonnes à traiter
        columns_to_fill = ['InteretsCourus', 'MontantTotal', 'CouponCouru', 'TauxObligation']

        # Remplacer les valeurs NaN par 0 dans les colonnes spécifiées
        self.data_tansaction[columns_to_fill] = self.data_tansaction[columns_to_fill].fillna(0)



        # Remplacer les valeurs 'Oui' par 1 et les valeurs 'Non' par 0 dans la colonne spécifiée
        column_to_replace = 'Valider'
        self.data_tansaction[column_to_replace] = self.data_tansaction[column_to_replace].replace({'Oui': 1, 'Non': 0})


        Feature_to_encode=[]
        for chaine in self.data_tansaction.columns:
            if (chaine.startswith("Date")) or (chaine.startswith("Heure")) or (type(self.data_tansaction[chaine][0])==str) :
                Feature_to_encode.append(chaine)
        print(Feature_to_encode)               
        from sklearn.preprocessing import LabelEncoder

        label_encoder = LabelEncoder()
        for columns in Feature_to_encode:
            self.data_tansaction[columns] = label_encoder.fit_transform(self.data_tansaction[columns])
         
        self.data_tansaction = self.data_tansaction.drop(['ValiderPar', 'AnnulerPar'], axis=1)
        
        X = self.data_tansaction #.drop(columns=["Fraude","DateJournee","InteretsCourusReel"])  # Remplacez "target" par le nom de la colonne cible, si elle existe
        columns_missing_values=X.columns[X.isnull().all()]
        X=X.drop(columns_missing_values,axis=1)
        # Standardiser les données pour les mettre à l'échelle
        scaler = StandardScaler()


        X_scaled = scaler.fit_transform(X)

        Data_copie=self.Data_copie[self.data_tansaction.columns]
        
        return X_scaled,Data_copie

#Importation du modèle

autoencoder = load_model('autoencoders.h5')

# Présentation avec Streamlit

col1, col2, col3 = st.columns(3)
with col1:
    st.image('Marche-Financier.png',caption='Les Valeurs du Marché')
with col2:
    st.image('Marche-Financier.png',caption='Les Valeurs du Marché')
    
with col3:
    st.image('Marche-Financier.png',caption='Les Valeurs du Marché')
    

    with col1:
        user_name = st.text_input('Seuil_tolerence')
    with col2:
        uploaded_file=st.file_uploader("Fichier Transaction",type=["xlsx","xls","csv"])
        if uploaded_file is not None:
            data = pd.read_excel(uploaded_file)
            Traitement_dat=Traitement_data(data)
            data,X=Traitement_dat.Traitement_de_la_data()
            
    with col1:
      if user_name != '':
        st.write(f'Le Seuil  de tolerence est {user_name}!')
      else:
        st.write('👆🏿  SVP Entrez le **Taux de marché**!')

    with col2:
     if uploaded_file is None:
        st.write('SVP Selectionnez le Fichier Transaction')


if user_name != '':
        if (uploaded_file is not None) :
            test=autoencoder.predict(data)
            st.write(data)
            
            mse = np.mean(np.power(data- test, 2), axis=1)
            threshold = float(user_name)
            anomalies = mse > threshold
            X["anomalies"]=anomalies
            X=X.loc[X["anomalies"]==1]
            Xgrouped = X.groupby('IdCompte')
            for name, group in Xgrouped:
                st.write("Compte", {name})
                st.write(group)
                st.write('\n')







