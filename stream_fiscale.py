#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
from datetime import time, datetime,date
from fastapi import FastAPI
from scipy.optimize import newton
import math
import time

from keras.models import load_model

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Model
from keras.layers import Input, Dense

class Traitement_data:
    def __init__(self,data_tansaction):
        
        self.data_tansaction=data_tansaction
    
    def Traitement_de_la_data(self):
        # Identifiez les colonnes avec des valeurs manquantes
        columns_missing_values = self.data_tansaction.columns[self.data_tansaction.isnull().any()]
    
        #le pourcentage de valeurs manquantes pour chaque colone
        percentage=self.data_tansaction[columns_missing_values].isnull().mean()*100
        
        #supprimer les colonnes moins importantes
        self.data_tansaction=self.data_tansaction.drop(['IdStructure','IsDeletedOld','IdSociete',  'TauxCSS','TauxIRVM','TauxActuarial','FraisIRVM','FraisCSS','CanCalculateInterets','OrigineImportation','DateJouissance','IdOrdreExecuteImporte', 'ReferenceDcbr', 'DateExecutionDcbr','DateValidation', 'HeureValidation', 
       'DateAnnulation', 'HeureAnnulation', 'MotifAnnulation','ValiderPar', 'AnnulerPar'], axis=1)
        
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
        
        
        column_to_replace = 'Valider'

        # Remplacer les valeurs 'Oui' par 1 et les valeurs 'Non' par 0 dans la colonne spécifiée
        self.data_tansaction[column_to_replace] = self.data_tansaction[column_to_replace].replace({'Oui': 1, 'Non': 0})
        
    
        Feature_to_encode=[]
        for chaine in self.data_tansaction.columns:
            if (chaine.startswith("Date")) or (chaine.startswith("Heure")) or (type(self.data_tansaction[chaine][0])==str) :
                Feature_to_encode.append(chaine)
                
        from sklearn.preprocessing import LabelEncoder

        label_encoder = LabelEncoder()
        for columns in Feature_to_encode:
            self.data_tansaction[columns] = label_encoder.fit_transform(self.data_tansaction[columns])
            
        X = self.data_tansaction #.drop(columns=["Fraude","DateJournee","InteretsCourusReel"])  # Remplacez "target" par le nom de la colonne cible, si elle existe

        # Standardiser les données pour les mettre à l'échelle
        scaler = StandardScaler()

        
        X_scaled = scaler.fit_transform(X)
        
        #X_train, X_test = train_test_split(X_scaled, test_size=0.2, random_state=42)
        # Enregistrer le DataFrame traité dans un fichier CSV
        #pd.DataFrame(X_test).to_excel('daf.xlsx', index=True)
        
        return X_scaled,X

autoencoder = load_model('autoencoders.h5')

# Présentation avec Streamlit

col1, col2, col3 = st.columns(3)
with col1:
    st.image('Marche-Financier.png',caption='Les Valeurs du Marché')
with col2:
    st.image('Marche-Financier.png',caption='Les Valeurs du Marché')
    
with col3:
    st.image('Marche-Financier.png',caption='Les Valeurs du Marché')
    
    
    #st.header('Visualiser Vos Données')

    #with st.expander('En Savoir Plus'):
    #  st.write('This app shows the various ways on how you can layout your Streamlit app.')
    # st.image('https://www.eslsca.fr/blog/gestion-du-patrimoine-tout-ce-quil-faut-savoir.png', width=250)

    with col1:
        user_name = st.text_input('Seuil_tolerence')
    with col2:
        uploaded_file=st.file_uploader("please upload file",type=["xlsx","csv"])
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
        st.write('SVP Selectionnez un fichier')


if user_name != '':
        if (uploaded_file is not None) :
            #data=np.array(data)[1:1000,:]
            #X=X.iloc[1:1000,:]
            test=autoencoder.predict(data)
            mse = np.mean(np.power(data- test, 2), axis=1)
            dif=data - test
            threshold = float(user_name)
            anomalies = mse > threshold
            dif=pd.DataFrame(dif)
            dif.columns=X.columns
            #Variable_name=pd.DataFrame(Variable_name)
            dif["anomalies"]=anomalies
            X["anomalies"]=anomalies
            dif=dif.loc[dif["anomalies"]==1]
            X=X.loc[X["anomalies"]==1]
            #dif=pd.concat((dif.iloc[:,:-1],X),axis=0)
            st.write(dif)
            st.write(X)
            st.write("le nombre de transaction anormales est:",dif.shape[0])







