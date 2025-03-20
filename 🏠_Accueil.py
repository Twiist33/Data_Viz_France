"""

Ceci est la page principale du projet, veuillez trouver ci dessous une brève présentation du projet, ainsi que le mémoire associé.

"""

# Import des librairies
import matplotlib.pyplot as plt
import streamlit as st
import matplotlib.image as mpimg

# Charger les  fichiers PDF présent à la fin de la page d'acceuil
with open("Documentation/Documentation_Data_Viz_France.pdff", "rb") as file:
    cv_data = file.read()
with open("Mémoire/Mémoire_Romain_Traboul.pdf", "rb") as file:
    file_data = file.read()
with open("CV/CV_FR_Romain_Traboul.pdf", "rb") as file:
    cv_data = file.read()
with open("CV/CV_ENG_Romain_Traboul.pdf", "rb") as file:
    cv_data = file.read()

# Affichage du titre et du logo de l'application web
st.set_page_config(page_title="Data Viz ⚽ 🇫🇷", page_icon="📊", layout="centered")


# Titre de la page
st.markdown(
    "<h3 style='text-align: center;'>Projet de data visualisation sur les compétitions françaises de Romain Traboul</h3>", 
    unsafe_allow_html=True)

st.image("Image/logo_1.jpg") # Utilisation de la 1er bannière en image

# Sous-titre
st.markdown(
    "<h4 style='text-align: center;'>Présentation du projet</h4>", 
    unsafe_allow_html=True)

# Description du projet
st.markdown(
    """
    <div style="text-align: justify;">
    L'objectif de ce projet est de poursuivre le travail effectué lors de mon mémoire de M1 : <strong>Analyse comparative de 3 facteurs de performance dans le football : l'impact du 1er but, la distribution temporelle des buts et l’influence de l’avantage du terrain sur le match (domicile/extérieur) entre les équipes de jeunes (U17N et U19N)</strong>.  
    Ce mémoire s'articulant uniquement sur seulement 3 compétitions sur la saison 2022/2023, il m'a paru important d'étendre cette analyse en élargissant le nombre de compétitions et de saisons.  
    Ainsi, l'analyse prendra en compte les saisons récentes allant de 2021/2022 à 2024/2025 (lorsque cela est possible) et les compétitions suivantes : <strong>Ligue 1, Ligue 2, National 1, National 2, Championnat U19N, D1 Féminine et D2 Féminine</strong>.
    </div>
    <br>
    Plusieurs fonctionnalités seront disponibles au sein de cette application web : 
    <ul>
        <li><strong>📊 Analyse d'une Équipe</strong> : Analyse du club de votre choix à travers plusieurs statistiques</li>
        <li><strong>🥊 Confrontation entre Équipes</strong> : Analyse comparative entre 2 équipes de votre choix d'une même saison</li>
        <li><strong>📅 Analyse d'une Saison</strong> : Aperçu des tendances sur une saison entière</li>
        <li><strong>🏆 Analyse d'une Compétition</strong> : Comparaison des indicateurs statistiques pour les compétitions de votre choix</li>
    </ul>
    <br>
    Pour plus de détails sur ce projet, vous avez à votre disposition :  
    <ul>
        <li>La documentation du projet</li>
        <li><a href="https://github.com/Twiist33/Data_Viz_France">Le code associé à la création de l'application</a></li>
        <li>Mon mémoire de M1 : Analyse comparative de 3 facteurs de performance dans le football : l'impact du 1er but, la distribution temporelle des buts et de l'influence de l'avantage du terrain sur le match (domicile/extérieur) entre les équipes de jeunes (U17N et U19N) réalisé dans le cadre de mon Master 1 Science du Numérique et Sport en 2023 à Rennes</li>    
        <li>Et enfin mon CV (en français et anglais).</li>
        </ul>
    """, unsafe_allow_html=True
)

# Utilisation de st.columns pour afficher les 4 boutons côte à côte et centrés
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

# Utilisation du 1er bouton pour télécharger le mémoire de M1
with col1:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.download_button(
        label="Documentation",
        data=file_data,
        file_name="Documentation_Data_Viz_France.pdf",
        mime="application/pdf"
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Utilisation du 2ème bouton pour télécharger le mémoire de M1
with col2:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.download_button(
        label="Mon mémoire de M1",
        data=file_data,
        file_name="Mémoire_Romain_Traboul.pdf",
        mime="application/pdf"
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Utilisation du 3ème bouton pour télécharger le CV en français
with col3:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.download_button(
        label="Mon CV en français",
        data=cv_data,
        file_name="CV_FR_Romain_Traboul.pdf",
        mime="application/pdf"
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Utilisation du 4ème bouton pour télécharger le CV en anglais
with col4:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.download_button(
        label="Mon CV en anglais",
        data=cv_data,
        file_name="CV_ENG_Romain_Traboul.pdf",
        mime="application/pdf"
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.image("Image/logo_2.jpg") # Utilisation de la 2ème banière en fin de page
