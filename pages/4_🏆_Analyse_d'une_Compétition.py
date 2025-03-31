# Import des librairies
import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
from supabase import create_client
from dotenv import load_dotenv
from decimal import Decimal

st.set_page_config(page_title="Data Viz ⚽ 🇫🇷", page_icon="📊", layout="wide") # Affichage du titre et du logo et l'application web

load_dotenv() # Chargement des variables d'environnement

# Connexion à la base de données Supabase
project_url = os.getenv("project_url")
api_key = os.getenv("api_key")
supabase = create_client(project_url, api_key)

### Fonctions pour l'affichage des graphiques et des tableaux

# Fonction pour récupérer les compétitions disponible
def get_competitions():
    try:
        # Appel de la fonction RPC avec params comme dictionnaire vide
        response = supabase.rpc("get_competitions", params={}).execute()
        if response.data:
            teams = response.data
        else:
            teams = []
        return teams
    except Exception as e:
        st.error(f"Erreur de connexion à Supabase : {e}")
        return []

# Fonction pour récupérer les moyennes de buts par match, à domicile et à l'extérieur sur une compétition donnée
def get_avg_goals_stats_by_competition_2():
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_avg_goals_stats_by_competition_2", params={}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des statistiques : {e}")
        return []

# Fonction pour récupérer les statistiques générales de la compétition au niveau de la fréquence des scores
def get_frequent_score_by_competition(competition_name):
    try:
        # Appel de la fonction RPC avec le paramètre de l'équipe et de la saison
        response = supabase.rpc("get_frequent_score_by_competition", {"competition_name_input": competition_name
        }).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        print(f"Erreur lors de l'exécution de la fonction RPC : {e}")
        return None

# Fonction pour récupérer les statistiques sur le 1er but sur une compétition donnée
def get_first_goal_stats_by_competition(competition_name):
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_first_goal_stats_by_competition", params={"competition_name_input": competition_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les statistiques générales de la compétition au niveau de la distribution des buts
def get_distribution_goals_by_competition(competition_name):
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_distribution_goals_by_competition", params={"competition_name_input": competition_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les statistiques générales de la compétition au niveau de la proportion des résultats selon l'avantage du terrain
def get_home_away_advantage_by_competition():
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_home_away_advantage_by_competition", params={}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction personnalisée pour le formatage conditionnel
def format_value(x):
    if pd.isnull(x):
        return "0"
    elif x == int(x):
        return str(int(x))  # Affiche sans décimales si entier
    else:
        return f"{x:.2f}"   # Affiche avec 2 décimales sinon

# Fonction pour colorer la compétition sélectionnée
def highlight_selected_competition(row):
    return ['background-color: lightcoral' if row["Compétition"] == selected_competition else '' for _ in row]

st.title("🏆 Analyse d'une Compétition") # Titre de l'interface Streamlit associé

if "selected_competition" not in st.session_state or st.session_state.get("selected_competition") == "Sélectionnez une compétition":
    st.image(os.path.abspath("../Image/banniere_competition.jpg"))


st.sidebar.header("🔍 Sélection de la compétition") # Utilisation de la sélection de la compétition en sidebar
competition_available = get_competitions() # Récupération de la liste des compétitions

# Dans le cas où la compétition sélectionné est disponibles, on passe au début de l'analyse
if competition_available:
    selected_competition = st.sidebar.selectbox("Choisissez une compétition :", ["Sélectionnez une compétition"] + competition_available, index=0)
    
    if selected_competition != "Sélectionnez une compétition":
        st.sidebar.header("📊 Sélectionnez une analyse")
        # Affichage des types de sections disponibles
        section = st.sidebar.radio("Sections", ["Statistiques générales", "1er but inscrit", "Distribution des buts", "Domicile / Extérieur","Comparaison entre les compétitions"])
        
        st.subheader(f"📌 {section} - {selected_competition}") # Récapitulatif des choix effectués
        
        # Affichage des graphiques relatifs à la section Statistiques Générales
        if section == "Statistiques générales":
            # Récupération des statistiques de moyenne de but
            avg_goal_stats = get_avg_goals_stats_by_competition_2()
            if avg_goal_stats:
                # Transformation des données en DataFrame avec les noms de colonnes
                df_goals = pd.DataFrame([
                    {
                        "Compétition": item["competition_name"], "Buts/Match": item["avg_goals_per_match"],
                        "Buts Domicile": item["avg_home_goals"], "Buts Extérieur": item["avg_away_goals"]                            }
                    for item in avg_goal_stats
                ])
                # Détermination de l'échelle maximale en fonction des plus hautes valeurs observées
                max_avg_goals = df_goals["Buts/Match"].max()
                max_home_goals = df_goals["Buts Domicile"].max()
                max_away_goals = df_goals["Buts Extérieur"].max()

                selected_data = df_goals[df_goals["Compétition"] == selected_competition] # Récupération des valeurs de la compétition sélectionnée

                if not selected_data.empty:
                    # Mise en flottant des données
                    avg_goals = float(selected_data["Buts/Match"].values[0])
                    avg_home_goals = float(selected_data["Buts Domicile"].values[0])
                    avg_away_goals = float(selected_data["Buts Extérieur"].values[0])
                    max_avg_goals = float(max_avg_goals)
                    max_home_goals = float(max_home_goals)
                    max_away_goals = float(max_away_goals)

                    col1, col2, col3 = st.columns(3) # Création des colonnes pour afficher les jauges côte à côte

                    # Fonction pour calculer la couleur en fonction du taux de remplissage
                    def get_gauge_color(value, max_value):
                        ratio = value / max_value
                        red = int(210 * (1 - ratio))
                        green = int(210 * ratio)
                        return f"rgb({red},{green},0)"

                    col1, col2, col3 = st.columns(3) # Création des jauges

                    with col1:
                        fig1 = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=avg_goals,
                            title={"text": "Buts/Match"},
                            gauge={
                                "axis": {"range": [0, max_avg_goals]},
                                "bar": {"color": get_gauge_color(avg_goals, max_avg_goals)}
                            }
                        ))
                        st.plotly_chart(fig1)

                    with col2:
                        fig2 = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=avg_home_goals,
                            title={"text": "Buts Domicile"},
                            gauge={
                                "axis": {"range": [0, max_home_goals]},
                                "bar": {"color": get_gauge_color(avg_home_goals, max_home_goals)}
                            }
                        ))
                        st.plotly_chart(fig2)

                    with col3:
                        fig3 = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=avg_away_goals,
                            title={"text": "Buts Extérieur"},
                            gauge={
                                "axis": {"range": [0, max_away_goals]},
                                "bar": {"color": get_gauge_color(avg_away_goals, max_away_goals)}
                            }
                        ))
                        st.plotly_chart(fig3)

            # Passage au tableau des scores fréquents (récupération des données)
            general_stats_data = get_frequent_score_by_competition(selected_competition)
            if general_stats_data:
                # Transformation des données en DataFrame avec les noms de colonnes
                df = pd.DataFrame([
                    {
                        "score_home": item["score_home"], "score_away": item["score_away"], "percentage": item["percentage"]
                    }
                    for item in general_stats_data
                ])
                # Construction de la table pivot
                pivot_table = df.pivot(index="score_home", columns="score_away", values="percentage").fillna(0)
                pivot_table = pivot_table.apply(pd.to_numeric, errors='coerce').fillna(0)
                # Construction de la figure
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.heatmap(pivot_table, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5, ax=ax)
                ax.set_title(f"Répartition des scores pour {selected_competition} (%)")
                ax.set_xlabel("Score extérieur")
                ax.set_ylabel("Score domicile")
                st.pyplot(fig)

        # Affichage des graphiques relatifs à la section 1er but inscrit
        elif section == "1er but inscrit":
            first_goal = get_first_goal_stats_by_competition(selected_competition) # On récupère les données
            if first_goal:
                # Transformation des données en DataFrame avec les noms de colonnes
                first_goal = pd.DataFrame([
                    {
                        "Compétition": item["competition_name"], "Aucun but": item["proportion_no_goal"], "1er but inscrit - Domicile": item["proportion_1st_goal_home"],
                        "1er but inscrit - Extérieur": item["proportion_1st_goal_away"], "1er but inscrit / Victoire": item["first_goal_win"],
                        "1er but inscrit / Nul": item["first_goal_draw"], "1er but inscrit / Défaite": item["first_goal_lose"],
                        "1er but inscrit / Domicile / Victoire": item["first_goal_home_win"], "1er but inscrit / Domicile / Nul": item["first_goal_home_draw"],
                        "1er but inscrit / Domicile / Défaite": item["first_goal_home_lose"], "1er but inscrit / Extérieur / Victoire": item["first_goal_away_win"],
                        "1er but inscrit / Extérieur / Nul": item["first_goal_away_draw"], "1er but inscrit / Extérieur / Défaite": item["first_goal_away_lose"]
                    }
                    for item in first_goal
                ])

                # Extraction des valeurs pour le graphique de la proportion des équipes marquant en premier
                values_proportion = first_goal.iloc[0][["Aucun but", "1er but inscrit - Domicile", "1er but inscrit - Extérieur"]].values
                labels_proportion = ["Aucun but", "Domicile", "Extérieur"]

                fig, axes = plt.subplots(2, 2, figsize=(15, 10)) # Création des sous-graphes

                # Premier graphique circulaire : Proportion des équipes marquant en 1er
                axes[0, 0].pie(values_proportion, labels=labels_proportion, autopct='%1.2f%%', startangle=90,colors=["#95a5a6", "#3498db", "#e67e22"])
                axes[0, 0].set_title("Proportion des équipes marquant en 1er")

                # Données pour les autres graphiques circulaires
                first_goal_data = [
                    (["1er but inscrit / Victoire", "1er but inscrit / Nul", "1er but inscrit / Défaite"], "Proportion des résultats après avoir inscrit le 1er but"),
                    (["1er but inscrit / Domicile / Victoire", "1er but inscrit / Domicile / Nul", "1er but inscrit / Domicile / Défaite"],
                    "Proportion des résultats à domicile après avoir inscrit le 1er but"), (["1er but inscrit / Extérieur / Victoire", "1er but inscrit / Extérieur / Nul",
                    "1er but inscrit / Extérieur / Défaite"], "Proportion des résultats à l'extérieur après avoir inscrit le 1er but")
                ]

                colors = ["#2ecc71", "#95a5a6", "#e74c3c"] # Couleurs des graphiques

                # Boucle pour générer les autres graphiques circulaires
                for ax, (cols, title) in zip(axes.flatten()[1:], first_goal_data):
                    values = first_goal.iloc[0][cols].values
                    ax.pie(values, labels=["Victoire", "Match nul", "Défaite"], autopct='%1.2f%%', startangle=90, colors=colors)
                    ax.set_title(title)

                st.pyplot(fig) # Affichage de la figure

        # Affichage des graphiques relatifs à la section Distribution des buts
        elif section == "Distribution des buts":
            distrib_goal = get_distribution_goals_by_competition(selected_competition) # On récupère les données associés
            if distrib_goal:
                # Transformation en dataframe en fonction des noms de colonnes
                distrib_goal = pd.DataFrame([
                    {
                        "Compétition": item["competition_name"] ,"1ère période": item["proportion_buts_1ere_periode"],"2ème période": item["proportion_buts_2nde_periode"],
                        "0-15 min": item["proportion_buts_0_15"], "16-30 min": item["proportion_buts_16_30"],"31-45 min": item["proportion_buts_31_45"],
                        "46-60 min": item["proportion_buts_46_60"], "61-75 min": item["proportion_buts_61_75"], "76-90 min": item["proportion_buts_76_90"]
                    }
                    for item in distrib_goal
                ])
                distrib_goal = list(distrib_goal.iloc[0, 1:])  # Transforme en liste après avoir enlevé `competition_name`
                # Création de la figure et des sous-graphiques
                fig, axes = plt.subplots(1, 2, figsize=(15, 7))  # 1 ligne, 2 colonnes
                # Construction du diagramme circulaire pour la proportion des buts inscrits par période
                labels_proportion = ["1ère période", "2ème période"]
                values_proportion = distrib_goal[:2]  # Extraction des valeurs
                axes[0].pie(values_proportion, labels=labels_proportion, autopct='%1.2f%%', startangle=90, colors=["lightblue", "lightcoral"])
                axes[0].set_title("Proportion des buts inscrits par période")

                # Construction de l'histogramme pour la proportion des buts inscrits par intervalle de 15 min
                labels_intervals = ["0-15 min", "16-30 min", "31-45 min", "46-60 min", "61-75 min", "76-90 min"]
                values_intervals = list(map(float, distrib_goal[2:]))  # Convertir les valeurs en float
                colors = ["#D4EFDF", "#A9DFBF", "#F9E79F", "#F5CBA7", "#E59866", "#DC7633"]
                bars = axes[1].bar(labels_intervals, values_intervals, color=colors)
                axes[1].set_title("Proportion des buts inscrits par intervalle de 15 min")
                axes[1].set_ylabel("%")
                axes[1].set_xlabel("Intervalle de temps")
                axes[1].set_ylim(0, max(values_intervals) + 5)

                # Ajout des valeurs sur les barres
                for bar in bars:
                    yval = bar.get_height()  # Hauteur de chaque barre
                    axes[1].text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval:.2f}%', ha='center', color='black')

                st.pyplot(fig) # Affichage avec Streamlit

        # Affichage des graphiques relatifs à la section Domicile / Extérieur 
        elif section == "Domicile / Extérieur":
            result_h_a = get_home_away_advantage_by_competition() # Récupération des statistiques sur l'avantage du terrain

            if result_h_a:
                # Transformation des données en DataFrame avec les noms de colonnes
                df_adv_home_away = pd.DataFrame([
                    {
                        "Compétition": item["competition_name"],"Victoire à Domicile": item["proportion_home_win"], "Match Nul": item["proportion_draw"],
                        "Victoire à l'Extérieur": item["proportion_away_win"], "Avantage du Terrain": item["home_advantage"]
                    }
                    for item in result_h_a
                ])
                max_adv_home = df_adv_home_away["Avantage du Terrain"].max() # Détermination de l'échelle maximale en fonction des plus hautes valeurs observées
                max_adv_home = float(max_adv_home) # Convertion en floattant

                selected_data = df_adv_home_away[df_adv_home_away["Compétition"] == selected_competition] # Récupération des valeurs de la compétition sélectionnée
                
                if not selected_data.empty:
                    # Sélectionner uniquement les colonnes nécessaires et extraire les valeurs sous forme de liste
                    values_proportion = selected_data[["Victoire à Domicile", "Match Nul", "Victoire à l'Extérieur"]].values.flatten()

                    labels_proportion = ["Victoire à domicile", "Match Nul", "Victoire à l'extérieur"] # Labels pour le diagramme

                    col1, col2 = st.columns(2) # Création des colonnes Streamlit

                    # Création du diagramme circulaire
                    with col1:
                        fig1, ax1 = plt.subplots(figsize=(7, 7))  
                        ax1.pie(values_proportion, labels=labels_proportion, autopct='%1.2f%%', startangle=90, colors=["#3498db", "#95a5a6", "#e67e22"])
                        ax1.set_title("Proportion des résultats selon le facteur Domicile/Extérieur")
                        st.pyplot(fig1)  

                    adv_home = float(selected_data["Avantage du Terrain"].values[0]) # Extraction de l'avantage du terrain

                    # Fonction pour calculer la couleur en fonction du taux de remplissage
                    def get_gauge_color(value, max_value):
                        if max_value == 0:  # Éviter une division par zéro
                            return "rgb(210,0,0)"
                        ratio = max(0, min(value / max_value, 1))  # S'assurer que le ratio est entre 0 et 1
                        red = int(210 * (1 - ratio))
                        green = int(210 * ratio)
                        return f"rgb({red},{green},0)"

                    # Création de la jauge
                    with col2:
                        fig2 = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=adv_home,  
                            title={"text": "Avantage du terrain (en %)"},
                            gauge={
                                "axis": {"range": [0, max_adv_home]},
                                "bar": {"color": get_gauge_color(adv_home, max_adv_home)}
                            }
                        ))
                        st.plotly_chart(fig2)  

                else:
                    st.warning("Aucune donnée disponible pour cette compétition.")

        # Affichage des graphiques relatifs à la section Comparaison entre les compétitions
        elif section == "Comparaison entre les compétitions":
            
            # Initialisation des variables de comparaison
            compare_first_goal_data = []
            compare_distrib_goal_data = []

            # On stocke les données sur le nombre de but moyen et de l'influence du facteur Domicile Extérieur
            compare_avg_goal_data = get_avg_goals_stats_by_competition_2()
            compare_home_away_adv_data = get_home_away_advantage_by_competition()

            # Récupération des informations obtenues pour le 1er but inscrit, et de la distribution des buts
            for competition in competition_available:
                compare_first_goal_stats = get_first_goal_stats_by_competition(competition)
                if compare_first_goal_stats:
                    compare_first_goal_data.extend(compare_first_goal_stats) # On stocke toutes les données par compétition
                compare_distrib_goal_stats = get_distribution_goals_by_competition(competition)
                compare_distrib_goal_stats = compare_distrib_goal_stats[0]
                if compare_distrib_goal_stats:
                    compare_distrib_goal_data.append(compare_distrib_goal_stats) # On stocke toutes les données par compétition

            if compare_avg_goal_data:
                # Transformation des données en DataFrame avec les noms de colonnes
                df = pd.DataFrame([
                        {
                            "Compétition": item["competition_name"], "Buts/Match": item["avg_goals_per_match"],
                            "Buts Domicile": item["avg_home_goals"], "Buts Extérieur": item["avg_away_goals"]                            }
                        for item in compare_avg_goal_data
                ])
                
                numeric_columns = df.columns[1:] # On traite les données numériques
                df[numeric_columns] = df[numeric_columns].astype(float).round(2)  # Arrondi à 2 décimales

                df = df.sort_values(by=numeric_columns.tolist(), ascending=False) # Assurer un tri numérique et non alphabétique

                # Appliquer le style de formatage et la coloration en une seule fois
                styled_df = (
                    df.style
                    .format({col: format_value for col in numeric_columns})  # Format personnalisé
                    .apply(highlight_selected_competition, axis=1)  # Coloration personnalisée
                    .set_properties(**{"text-align": "center"})  # Centrage du texte
                )
                # Affichage du tableau mis en forme avec tri
                st.subheader("⚽ Informations sur les statistiques générales (en moyenne)")
                st.dataframe(styled_df)

            if compare_first_goal_data:
                # Transformation des données en DataFrame avec les noms de colonnes
                df = pd.DataFrame([
                    {
                        "Compétition": item["competition_name"], "Aucun but": item["proportion_no_goal"], "1er but inscrit - Domicile": item["proportion_1st_goal_home"],
                        "1er but inscrit - Extérieur": item["proportion_1st_goal_away"], "1er but inscrit / Victoire": item["first_goal_win"],
                        "1er but inscrit / Nul": item["first_goal_draw"], "1er but inscrit / Défaite": item["first_goal_lose"],
                        "1er but inscrit / Domicile / Victoire": item["first_goal_home_win"], "1er but inscrit / Domicile / Nul": item["first_goal_home_draw"],
                        "1er but inscrit / Domicile / Défaite": item["first_goal_home_lose"], "1er but inscrit / Extérieur / Victoire": item["first_goal_away_win"],
                        "1er but inscrit / Extérieur / Nul": item["first_goal_away_draw"], "1er but inscrit / Extérieur / Défaite": item["first_goal_away_lose"]
                    }
                    for item in compare_first_goal_data
                ])
                numeric_columns = df.columns[1:] # On traite les données numériques
                df[numeric_columns] = df[numeric_columns].astype(float) # Convertion en flottant

                df = df.sort_values(by=numeric_columns.tolist(), ascending=False) # Assurer un tri numérique et non alphabétique

                # Appliquer le style de formatage et la coloration en une seule fois
                styled_df = (
                    df.style
                    .format({col: format_value for col in numeric_columns})  # Format personnalisé
                    .apply(highlight_selected_competition, axis=1)  # Coloration personnalisée
                    .set_properties(**{"text-align": "center"})  # Centrage du texte
                )
                # Affichage du tableau mis en forme avec tri
                st.subheader("⚽ Informations sur le 1er inscrit (en %)")
                st.dataframe(styled_df)
            
            if compare_distrib_goal_data:
                # Transformation en dataframe en fonction des noms de colonnes
                df = pd.DataFrame([
                    {
                        "Compétition": item["competition_name"] ,"1ère période": item["proportion_buts_1ere_periode"],"2ème période": item["proportion_buts_2nde_periode"],
                        "0-15 min": item["proportion_buts_0_15"], "16-30 min": item["proportion_buts_16_30"],"31-45 min": item["proportion_buts_31_45"],
                        "46-60 min": item["proportion_buts_46_60"], "61-75 min": item["proportion_buts_61_75"], "76-90 min": item["proportion_buts_76_90"]
                    }
                    for item in compare_distrib_goal_data
                ])
                numeric_columns = df.columns[1:] # On traite les données numériques
                df[numeric_columns] = df[numeric_columns].astype(float) # Convertir en flottant

                df = df.sort_values(by=numeric_columns.tolist(), ascending=False) # Assurer un tri numérique et non alphabétique
                # Appliquer le style de formatage et la coloration en une seule fois
                styled_df = (
                    df.style
                    .format({col: format_value for col in numeric_columns})  # Format personnalisé
                    .apply(highlight_selected_competition, axis=1)  # Coloration personnalisée
                    .set_properties(**{"text-align": "center"})  # Centrage du texte
                )
                # Affichage du tableau mis en forme avec tri
                st.subheader("⚽ Informations sur la distribution des buts (en %)")
                st.dataframe(styled_df)

            if compare_home_away_adv_data:
                # Transformation des données en DataFrame avec les noms de colonnes
                df = pd.DataFrame([
                    {
                        "Compétition": item["competition_name"],"Victoire à Domicile": item["proportion_home_win"], "Match Nul": item["proportion_draw"],
                        "Victoire à l'Extérieur": item["proportion_away_win"], "Avantage du Terrain": item["home_advantage"]
                    }
                    for item in compare_home_away_adv_data
                ])              
                numeric_columns = df.columns[1:] # On traite les données numériques
                df[numeric_columns] = df[numeric_columns].astype(float) # Convertion en flottant

                df = df.sort_values(by=numeric_columns.tolist(), ascending=False) # Assurer un tri numérique et non alphabétique
                # Appliquer le style de formatage et la coloration en une seule fois
                styled_df = (
                    df.style
                    .format({col: format_value for col in numeric_columns})  # Format personnalisé
                    .apply(highlight_selected_competition, axis=1)  # Coloration personnalisée
                    .set_properties(**{"text-align": "center"})  # Centrage du texte
                )
                # Affichage du tableau mis en forme avec tri
                st.subheader("⚽ Informations sur l'influence du facteur Domicile/Extérieur (en %)")
                st.dataframe(styled_df)
            else:
                st.warning("Aucune donnée disponible pour comparaison.")