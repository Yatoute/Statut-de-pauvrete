import pandas as pd
import numpy as np
import pickle
import streamlit as st
import sklearn
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
# loading in the model to predict on the data
pickle_in = open("C://Users//HP//app//model.pkl", 'rb')
model = pickle.load(pickle_in)

# Message de bienvenue
def welcome():
    return "Bienvenue sur  la page d'évaluation de la vulnérabilité des ménages au Sénégal"

# defining the function which will make the prediction using the data which the user inputs
def prediction(s01q01, s01q07, s01q10, s00q01, s00q04, Taill_men, s02q33, s04q39):  
    prediction = model.predict( [[s01q01, s01q07, s01q10, s00q01, s00q04, Taill_men, s02q33, s04q39]])
    print(prediction)
    return prediction

# This is the main function in which we define our webpage 
def main():
    
    # here we define some of the front end elements of the web page like 
    # the font and background color, the padding and the text to be displayed
    html_temp = """
    <div style ="background-color:yellow;padding:13px">
    <h1 style ="color:black;text-align:center;">Evaluation de la vulnérabilité des ménages </h1>
    </div>
    """
    # this line allows us to display the front end aspects we have defined in the above code
    st.markdown(html_temp, unsafe_allow_html = True)
    
    # the following lines create text boxes in which the user can enter the data required to make the prediction
    ## Région
    Regions = ["Dakar", "Ziguinchor", "Diourbel", "Saint-Louis", "Tambacounda", "Kaolack", "Thiès", "Louga", "Fatick", "Kolda", "Matam", "Kaffrine", "Kédougou", "Sédhiou"]
    s00q01 = st.sidebar.selectbox("Votre région",Regions,index =10)
    
    ## Milieu de résidence
    Milieu = ["Urbain", "Rural"]
    s00q04 = st.sidebar.selectbox("Votre milieu de résidence", Milieu)
    
    ## Taille du ménage (après il faut mettre toutes les tailles supérieures à 20 à 20)
    Taill_men = st.text_input("Votre ménage compte t-il combien de personnes ?","",2)
    
    ## Sexe du chef de ménage
    Genre = ["Homme", "Femme"]
    s01q01 = st.sidebar.selectbox("Votre ménage est-il dirigé par un homme ou une femme ?", Genre)
    
    ## Situation matrimoniale du CM
    SMCM = ["Célibataire ou union libre", "Marié(e) monogame", "Marié(e) polygame", "Divorcé(e) ou séparé(e)", "Veuf(ve)"]
    s01q07 = st.sidebar.selectbox("Situation matrimoniale de votre chef de ménage", SMCM)
  
    ## Age du chef de ménage à son premier mariage (à recoder par classe après après )
    s01q10 = st.text_input("Quel âge avait votre chef de ménage à son premier mariage ?", "",2)
    
    ## Niveau d'instruction du chef de ménage
    Niv_inst = ["Aucun niveau", "CEP/CFEE", "BEPC/BFEM", "CAP, BT", "BAC", "DEUG, DUT, BTS", "Licence, Maitrice", "Master/DEA/DESS", "Doctorat/Phd" ]
    s02q33 = st.sidebar.selectbox("Quel est le niveau d'instruction de votre chef de ménage", Niv_inst )
    
    ## Catégorie socioprofessionnelle du chef de ménage
    Categorie =["Cadre supérieur", "Cadre moyen/agent de maîtrise", "Ouvrier ou employé qualifié", "Ouvrier ou employé non qualifié", "Manœuvre, aide ménagère", "Stagiaire", "Travailleur familial contribuant à une entreprise familiale", "Travailleur pour compte propre", "Patron", "Sans profession ou catégorie non classée"]
    s04q39 = st.sidebar.selectbox("Catégorie socioprofessionnelle de votre chef de ménage", Categorie,index=1)

    result =""
    # the below line ensures that when the button called 'Predict' is clicked, 
    # the prediction function defined above is called to make the prediction 
    # and store it in the variable result
    if st.button("Predict") :
        if Taill_men !="" and s01q10 !="" :
            # limité la taille de ménage à 20
            if int(Taill_men) > 20: 
                Taill_men =20
            # Recodage de l'âge
            if int(s01q10) < 25 :
                s01q10 = "moins de 25 ans" 
            elif int(s01q10) < 30 :
                s01q10 = "25 à 30 ans" 
            elif int(s01q10) < 40 :
                s01q10 = "30 à 40 ans"
            else : 
                s01q10 = "40 ans et plus"
            Tranche_age = ["moins de 25 ans", "25 à 30 ans", "30 à 40 ans","40 ans et plus" ]
        # Transformer les données en numérique
            s00q01 = encoder.fit_transform(Regions)[Regions.index(s00q01)]
            s00q04 = encoder.fit_transform(Milieu)[Milieu.index(s00q04)]
            s01q01 = encoder.fit_transform(Genre)[Genre.index(s01q01)]
            s01q07 = encoder.fit_transform(SMCM)[SMCM.index(s01q07)]
            s02q33 = encoder.fit_transform(Niv_inst)[Niv_inst.index(s02q33)]
            s04q39 = encoder.fit_transform(Categorie)[Categorie.index(s04q39)]
            s01q10 = encoder.fit_transform(Tranche_age)[Tranche_age.index(s01q10)]
            result = prediction(s01q01, s01q07, s01q10, s00q01, s00q04, Taill_men, s02q33, s04q39)
            if result == 1 : 
                result = "Ménage vulnérable"
            if result == 0 : 
                result = "Ménage non vulnérable"
            st.success(result)
        else :
            st.success("Assurez vous d'avoir rempli tous les champs")
    
if __name__=='__main__':
    main()
    

    
    
    