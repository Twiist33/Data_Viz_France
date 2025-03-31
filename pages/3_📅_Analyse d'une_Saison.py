# Import des libraries
import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
from supabase import create_client
from dotenv import load_dotenv
from decimal import Decimal

st.set_page_config(page_title="Data Viz ⚽ 🇫🇷", page_icon="📊", layout="wide") # Configuration de la page Streamlit

load_dotenv() # Chargement des variables d'environnement

# Connexion à la base de données Supabase
project_url = os.getenv("project_url")
api_key = os.getenv("api_key")
supabase = create_client(project_url, api_key)

# Fonction pour récupérer les compétitions disponibles
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

# Fonction pour récupérer les saisons disponibles pour une compétition donnée
def get_seasons_by_competition(competition_name):
    try:
        # Appel de la fonction RPC avec les paramètres dans le dictionnaire 'params'
        response = supabase.rpc("get_seasons_by_competition", params={"competition_name_input": competition_name}).execute()
        if response.data:
            seasons = response.data
        else:
            seasons = []
        return seasons
    except Exception as e:
        st.error(f"Erreur de connexion à Supabase : {e}")
        return []

### Fonction pour effectuer les requêtes des données des graphiques ou des tableaux

# Fonction pour récupérer les statistiques de moyenne de buts par match
def get_avg_goals_stats_by_competition():
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_avg_goals_stats_by_competition", params={}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des statistiques : {e}")
        return []

# Fonction pour récupérer les statistiques générales de la saison au niveau de la fréquence des scores
def get_frequent_score_by_season(season_name):
    try:
        # Appel de la fonction RPC avec le paramètre de l'équipe et de la saison
        response = supabase.rpc("get_frequent_score_by_season", {"season_name_input": season_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        print(f"Erreur lors de l'exécution de la fonction RPC : {e}")
        return None

# Fonction pour récupérer les information de buts inscrits sur une saison donnée
def get_goals_scored(season_name):
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_goals_scored", params={"season_name_input": season_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les information de buts concédés sur une saison donnée
def get_goals_conceded(season_name):
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_goals_conceded", params={"season_name_input": season_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer le nom des 5 équipes ayant obtenus les meilleurs taux de buts inscrits par match sur une saison donnée
def get_top5_goals_scored(competition_name):
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_top5_goals_scored", params={"competition_name_input": competition_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer le nom des 5 équipes ayant obtenus les meilleurs taux de buts concédés par match sur une saison donnée
def get_top5_goals_conceded(competition_name):
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_top5_goals_conceded", params={"competition_name_input": competition_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les statistiques sur le 1er but inscrit ou concédé sur une saison donnée
def get_first_goal_stats(season_name):
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_first_goal_stats", params={"season_name_input": season_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les statistiques sur le 1er but inscrit ou concédé, en comparaison des saisons provenant d'une même compétition
def get_first_goal_season(season_name):
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_first_goal_season", params={"season_name_input": season_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer le nom des 5 équipes ayant le meilleur taux de 1er but inscrit pour une compétition donnée
def get_top_teams_first_goal(competition_name):
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_top_teams_first_goal", params={"competition_name_input": competition_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer le nom des 5 équipes ayant le meilleur taux d'influence du 1er but inscrit pour une compétition donnée
def get_top_teams_first_goal_win(competition_name):
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_top_teams_first_goal_win", params={"competition_name_input": competition_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer le nom des 5 équipes ayant le meilleur taux de victoires après avoir concédé le 1er but pour une compétition donnée
def get_top_teams_first_goal_conceded_win(competition_name):
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_top_teams_first_goal_conceded_win", params={"competition_name_input": competition_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les statistiques générales de la saison au niveau de la distribution des buts
def get_distribution_goals(season_name):
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_distribution_goals", params={"season_name_input": season_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les statistiques générales de la saison au niveau de la distribution des buts (inscrits et concédés)
def get_distribution_goals_season(season_name):
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_distribution_goals_season", params={"season_name_input": season_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les meilleurs équipes en 1ère période sur une compétition donnée
def get_top_teams_1st_period(competition_name):
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_top_teams_1st_period", params={"competition_name_input": competition_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les meilleurs équipes en 2ème période sur une compétition donnée
def get_top_teams_2nd_period(competition_name):
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_top_teams_2nd_period", params={"competition_name_input": competition_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les meilleurs équipes durant les 15 dernières minutes sur une compétition donnée
def get_top_teams_last_minutes(competition_name):
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_top_teams_last_minutes", params={"competition_name_input": competition_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les statistiques générales de la saison au niveau de la proportion des résultats selon l'avantage du terrain
def get_home_away_advantage():
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_home_away_advantage", params={}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les statistiques générales de la saison au niveau du classement à domicile
def get_rank_home_season(season_name):
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_rank_home_season", params={"season_name_input": season_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les statistiques générales de la saison au niveau du classement à l'extérieur
def get_rank_away_season(season_name):
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_rank_away_season", params={"season_name_input": season_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction du top 5 des meilleurs équipes à domicile
def get_top5_home_rank_competition(competition_name):
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_top5_home_rank_competition", params={"competition_name_input": competition_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction du top 5 des meilleurs équipes à l'extérieur
def get_top5_away_rank_competition(competition_name):
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_top5_away_rank_competition", params={"competition_name_input": competition_name}).execute()
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
def highlight_selected_season(row):
    return ['background-color: lightcoral' if row["Saison"] == selected_season else '' for _ in row]

st.title("📅 Analyse d'une Saison") # Titre de l'application

# Vérifie si l'utilisateur a fait un choix (équipe, saison et section)
show_image = True  # Par défaut, on affiche l'image

image_path = os.path.join(os.path.dirname(__file__), "..", "Image", "banniere_saison.jpg") # Construction du chemin absolu

st.sidebar.header("🔍 Sélection de la compétition") # Sélection de la compétition en sidebar
competitions_available = get_competitions() # Récupèration de la liste des compétitions disponibles

# Selection des compétitions disponibles
if competitions_available:
    selected_competition = st.sidebar.selectbox("Choisissez une compétition :", ["Sélectionnez une compétition"] + competitions_available, index=0)
    
    if selected_competition != "Sélectionnez une compétition":
        st.sidebar.header("🔍 Sélection de la saison") # Sélection de la saison en fonction de la compétition choisie
        seasons_available = get_seasons_by_competition(selected_competition) # Récupèration des données
        
        # Selection des saisons disponibles
        if seasons_available:
            selected_season = st.sidebar.selectbox("Choisissez une saison :", ["Sélectionnez une saison"] + seasons_available, index=0)
            
            if selected_season != "Sélectionnez une saison":
                st.sidebar.header("📊 Sélectionnez une analyse")
                section = st.sidebar.radio("Sections", ["Statistiques générales", "1er but inscrit", "Distribution des buts", "Domicile / Extérieur", "Comparaison entre les saisons"])

                # Si une section est sélectionnée, on cache l’image
                if section:
                    show_image = False 

                st.subheader(f"📌 {section} - {selected_season}") # Récapitulatif des choix effectués

                # Affichage des graphiques relatifs à la section Statistiques Générales            
                if section == "Statistiques générales":

                    avg_goal_stats = get_avg_goals_stats_by_competition() # Récupération des statistiques de moyenne de but
                    if avg_goal_stats:
                        # Transformation des données en DataFrame avec les noms de colonnes
                        df_goals = pd.DataFrame([
                            {
                                "Compétition": item["competition_name"], "Saison": item["season_name"], "Buts/Match": item["avg_goals_per_match"],
                                "Buts Domicile": item["avg_home_goals"], "Buts Extérieur": item["avg_away_goals"]                            }
                            for item in avg_goal_stats
                        ])
                        # Détermination de l'échelle maximale en fonction des plus hautes valeurs observées
                        max_avg_goals = df_goals["Buts/Match"].max()
                        max_home_goals = df_goals["Buts Domicile"].max()
                        max_away_goals = df_goals["Buts Extérieur"].max()
                        
                        selected_data = df_goals[df_goals["Saison"] == selected_season] # Récupération des valeurs de la compétition sélectionnée

                        if not selected_data.empty:
                            # Mise en flottant des données
                            avg_goals = float(selected_data["Buts/Match"].values[0])
                            avg_home_goals = float(selected_data["Buts Domicile"].values[0])
                            avg_away_goals = float(selected_data["Buts Extérieur"].values[0])

                            # Conversion des valeurs max aussi (juste au cas où)
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

                    compare_goals_scored_data = get_goals_scored(selected_season) # On construit le tableau sur les buts inscrits en commençant par récupérer les données

                    if compare_goals_scored_data:
                        # Transformation des données en DataFrame avec les noms de colonne
                        df = pd.DataFrame([
                            {
                                "Équipe": item["team_name"], "Nbr. buts inscrits": item["total_goals_scored"], "Moy. buts inscrits": item["avg_goals_scored"],
                                "Nbr. buts inscrits (Domicile)": item["goals_scored_home"], "Moy. buts inscrits (Domicile)": item["avg_goals_scored_home"],
                                "Nbr. buts inscrits (Extérieur)": item["goals_scored_away"], "Moy. buts inscrits (Extérieur)": item["avg_goals_scored_away"]
                            }
                            for item in compare_goals_scored_data
                        ])
                        
                        numeric_columns = df.columns[1:]  # Sélectionne les colonnes numériques
                        df[numeric_columns] = df[numeric_columns].applymap(lambda x: int(x) if x == int(x) else round(x, 2))

                        df = df.sort_values(by=["Nbr. buts inscrits"], ascending=False) # On ordonne le tableau selon le Nbr. buts inscrits

                        # Appliquer le style de formatage
                        styled_df = (
                            df.style
                            .format({col: format_value for col in numeric_columns})  # Format personnalisé
                            .set_properties(**{"text-align": "center"}))  # Centrage du texte
                        st.subheader(f"Tableau sur les buts inscrits pour la saison {selected_season}") # On choisit le titre du tableau
                        st.dataframe(styled_df)
                    else:
                        st.warning("Aucune donnée disponible pour cette saison.")

                    compare_goals_conceded_data = get_goals_conceded(selected_season) # On construit le tableau sur les buts concédés en commençant par récupérer les données

                    if compare_goals_conceded_data:
                        # Transformation des données en DataFrame avec les noms de colonnes
                        df = pd.DataFrame([
                            {
                                "Équipe": item["team_name"], "Nbr. buts concédés": item["total_goals_conceded"], "Moy. buts concédés": item["avg_goals_conceded"],
                                "Nbr. buts concédés (Domicile)": item["goals_conceded_home"], "Moy. buts concédés (Domicile)": item["avg_goals_conceded_home"],
                                "Nbr. buts concédés (Extérieur)": item["goals_conceded_away"], "Moy. buts concédés (Extérieur)": item["avg_goals_conceded_away"]
                            }
                            for item in compare_goals_conceded_data
                        ])
                        
                        numeric_columns = df.columns[1:]  # Sélectionne les colonnes numériques
                        df[numeric_columns] = df[numeric_columns].applymap(lambda x: int(x) if x == int(x) else round(x, 2))

                        df = df.sort_values(by=["Nbr. buts concédés"], ascending=False) # On ordonne le tableau selon le Nbr. buts concédés

                        # Appliquer le style de formatage et la coloration en une seule fois
                        styled_df = (
                            df.style
                            .format({col: format_value for col in numeric_columns})  # Format personnalisé
                            .set_properties(**{"text-align": "center"})  # Centrage du texte
                        )

                        st.subheader(f"Tableau sur les buts concédés pour la saison {selected_season}") # On donne un titre
                        st.dataframe(styled_df) # On centre le titre

                    general_stats_data = get_frequent_score_by_season(selected_season) # Passage au tableau des scores fréquents (récupération des données)
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
                        ax.set_title(f"Répartition des scores pour {selected_season} (%)")
                        ax.set_xlabel("Score extérieur")
                        ax.set_ylabel("Score domicile")
                        st.pyplot(fig)

                # Affichage des graphiques relatifs à la section 1er but inscrit
                elif section == "1er but inscrit":
                    first_goal = get_first_goal_stats(selected_season) # Récupération des données
                    if first_goal:
                        # Transformation des données en DataFrame avec les noms de colonnes
                        first_goal = pd.DataFrame([
                            {
                                "Saison": item["season_name"], "Aucun but": item["proportion_no_goal"], "1er but inscrit - Domicile": item["proportion_1st_goal_home"],
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
                        axes[0, 0].pie(values_proportion, labels=labels_proportion, autopct='%1.2f%%', startangle=90,
                                    colors=["#95a5a6", "#3498db", "#e67e22"])
                        axes[0, 0].set_title("Proportion des équipes marquant en 1er")

                        # Données pour les autres graphiques circulaires
                        first_goal_data = [
                            (["1er but inscrit / Victoire", "1er but inscrit / Nul", "1er but inscrit / Défaite"],
                            "Proportion des résultats après avoir inscrit le 1er but"),
                            (["1er but inscrit / Domicile / Victoire", "1er but inscrit / Domicile / Nul", "1er but inscrit / Domicile / Défaite"],
                            "Proportion des résultats à domicile après avoir inscrit le 1er but"),
                            (["1er but inscrit / Extérieur / Victoire", "1er but inscrit / Extérieur / Nul", "1er but inscrit / Extérieur / Défaite"],
                            "Proportion des résultats à l'extérieur après avoir inscrit le 1er but")
                        ]

                        colors = ["#2ecc71", "#95a5a6", "#e74c3c"] # Couleurs des graphiques

                        # Boucle pour générer les autres graphiques circulaires
                        for ax, (cols, title) in zip(axes.flatten()[1:], first_goal_data):
                            values = first_goal.iloc[0][cols].values
                            ax.pie(values, labels=["Victoire", "Match nul", "Défaite"], autopct='%1.2f%%', startangle=90, colors=colors)
                            ax.set_title(title)

                        st.pyplot(fig) # Affichage de la figure

                    first_goal_season_data = get_first_goal_season(selected_season) # On construit le tableau sur les 1er buts inscrits en commençant par récupérer les données
                    if first_goal_season_data:
                        # Transformation des données en DataFrame avec les noms de colonnes
                        df = pd.DataFrame([
                            {
                                "Saison": item["season_name"], "Équipe": item["team_name"],
                                "1er but inscrit": item["proportion_1st_goal_for"], "Aucun but": item["proportion_no_goal"], "1er but encaissé": item["proportion_1st_goal_against"],
                                "Domicile / 1er but inscrit": item["proportion_1st_goal_home_for"],"Domicile / Aucun but": item["proportion_no_goal_home"], "Domicile / 1er but encaissé": item["proportion_1st_goal_home_against"],
                                "Extérieur / 1er but inscrit": item["proportion_1st_goal_away_for"], "Extérieur / Aucun but": item["proportion_no_goal_away"], "Extérieur / 1er but encaissé": item["proportion_1st_goal_away_against"],
                                "1er but inscrit / Victoire": item["first_goal_win"], "1er but inscrit / Nul": item["first_goal_draw"],"1er but inscrit / Défaite": item["first_goal_lose"],                    
                                "1er but inscrit / Domicile / Victoire": item["proportion_1st_goal_home_win"], "1er but inscrit / Domicile / Nul": item["proportion_1st_goal_home_draw"], "1er but inscrit / Domicile / Défaite": item["proportion_1st_goal_home_lose"],                            
                                "1er but inscrit / Extérieur / Victoire": item["proportion_1st_goal_away_win"], "1er but inscrit / Extérieur / Nul": item["proportion_1st_goal_away_draw"], "1er but inscrit / Extérieur / Défaite": item["proportion_1st_goal_away_lose"],                                
                                "1er but encaissé / Victoire": item["first_goal_conceded_win"],"1er but encaissé / Nul": item["first_goal_conceded_draw"], "1er but encaissé / Défaite": item["first_goal_conceded_lose"],                                
                                "1er but encaissé / Domicile / Victoire": item["proportion_1st_goal_conceded_home_win"], "1er but encaissé / Domicile / Nul": item["proportion_1st_goal_conceded_home_draw"], "1er but encaissé / Domicile / Défaite": item["proportion_1st_goal_conceded_home_lose"],
                                "1er but encaissé / Extérieur / Victoire": item["proportion_1st_goal_conceded_away_win"], "1er but encaissé / Extérieur / Nul": item["proportion_1st_goal_conceded_away_draw"], "1er but encaissé / Extérieur / Défaite": item["proportion_1st_goal_conceded_away_lose"]
                            }
                            for item in first_goal_season_data
                        ])

                        for col in df.columns:
                            if col != "Équipe":  # Exclure la colonne "Équipe" qui contient du texte
                                df[col] = pd.to_numeric(df[col], errors='coerce')

                        df = df.iloc[:, 1:]  # Supprime la colonne Saison

                        # On construit les tableaux sur le 1er but inscrit ou encaissé pour une saison donnée en faisant une catégorisation des sous-ensembles de colonnes
                        first_goal_columns = [
                            "Équipe", "1er but inscrit", "Aucun but", "1er but encaissé", "Domicile / 1er but inscrit", "Domicile / Aucun but", "Domicile / 1er but encaissé",
                            "Extérieur / 1er but inscrit", "Extérieur / Aucun but", "Extérieur / 1er but encaissé"
                        ]
                        first_goal_influence_columns = [
                            "Équipe", "1er but inscrit / Victoire", "1er but inscrit / Nul", "1er but inscrit / Défaite", "1er but inscrit / Domicile / Victoire",
                            "1er but inscrit / Domicile / Nul", "1er but inscrit / Domicile / Défaite","1er but inscrit / Extérieur / Victoire",
                            "1er but inscrit / Extérieur / Nul", "1er but inscrit / Extérieur / Défaite"
                        ]
                        first_goal_conceded_columns = [
                            "Équipe", "1er but encaissé / Victoire", "1er but encaissé / Nul", "1er but encaissé / Défaite",
                            "1er but encaissé / Domicile / Victoire", "1er but encaissé / Domicile / Nul", "1er but encaissé / Domicile / Défaite",
                            "1er but encaissé / Extérieur / Victoire", "1er but encaissé / Extérieur / Nul", "1er but encaissé / Extérieur / Défaite"
                        ]
                        
                        # Création des trois sous-tableaux
                        df_first_goal = df[first_goal_columns]
                        df_first_goal_influence = df[first_goal_influence_columns]
                        df_first_goal_conceded = df[first_goal_conceded_columns]
                        
                        # Tri des tableaux
                        df_first_goal = df_first_goal.sort_values(by=["1er but inscrit"], ascending=False)
                        df_first_goal_influence = df_first_goal_influence.sort_values(by=["1er but inscrit / Victoire"], ascending=False)
                        df_first_goal_conceded = df_first_goal_conceded.sort_values(by=["1er but encaissé / Victoire"], ascending=False)
                        
                        # Correction et multiplication des valeurs par 100
                        for df_subset in [df_first_goal, df_first_goal_influence, df_first_goal_conceded]:
                            numeric_columns = df_subset.columns[1:]  # Exclure "Équipe"
                            df_subset[numeric_columns] = df_subset[numeric_columns].astype(float)

                        # On ajuste les styles des 3 tableaux
                        style_df_first_goal = (
                            df_first_goal.style
                            .format({"Proportion du 1er but inscrit": format_value})
                            .set_properties(**{"text-align": "center"})  # Centrage du texte
                        )

                        style_df_first_goal_influence = (
                            df_first_goal_influence.style
                            .format({col: format_value for col in df_first_goal_influence.columns[1:]})  # Format personnalisé
                            .set_properties(**{"text-align": "center"})  # Centrage du texte
                        )

                        style_df_first_goal_conceded = (
                            df_first_goal_conceded.style
                            .format({col: format_value for col in df_first_goal_conceded.columns[1:]})  # Format personnalisé
                            .set_properties(**{"text-align": "center"})  # Centrage du texte
                        )
                        # Affichage des tableaux avec formatage conditionnel
                        st.subheader(f"Tableau sur le 1er but (inscrit ou encaissé) pour la saison {selected_season}")
                        st.dataframe(style_df_first_goal_influence)

                        st.subheader(f"Influence du 1er but inscrit pour la saison {selected_season}")
                        st.dataframe(style_df_first_goal_influence)

                        st.subheader(f"Influence du 1er but encaissé pour la saison {selected_season}")
                        st.dataframe(style_df_first_goal_conceded)

                # Affichage des graphiques relatifs à la section Distribution des buts
                elif section == "Distribution des buts":
                    distrib_goal = get_distribution_goals(selected_season) # On récupère les données
                    if distrib_goal:
                        # Transformation en dataframe en fonction des noms de colonnes
                        distrib_goal = pd.DataFrame([
                            {
                                "Saison": item["season_name"] ,"1ère période": item["proportion_buts_1ere_periode"],"2ème période": item["proportion_buts_2nde_periode"],
                                "0-15 min": item["proportion_buts_0_15"], "16-30 min": item["proportion_buts_16_30"],"31-45 min": item["proportion_buts_31_45"],
                                "46-60 min": item["proportion_buts_46_60"], "61-75 min": item["proportion_buts_61_75"], "76-90 min": item["proportion_buts_76_90"]

                            }
                            for item in distrib_goal
                        ])
                        distrib_goal = list(distrib_goal.iloc[0, 1:])  # Transforme en liste après avoir enlevé `season_name`
                
                        fig, axes = plt.subplots(1, 2, figsize=(15, 7)) # Création de la figure et des sous-graphiques

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

                   # On construit le tableau sur la distrbution des buts inscrits ou concédés en commençant par récupérer les données
                    distrib_goals_data = get_distribution_goals_season(selected_season)
                    if distrib_goals_data:
                        # Transformation des données en DataFrame avec les noms de colonnes
                        df = pd.DataFrame([
                            {
                                "Saison": item["season_name"], "Équipe": item["team_name"],"1ère période (Proportion Buts inscrits)": item["proportion_buts_inscrit_1ere_periode"],
                                "2ème période (Proportion Buts inscrits)": item["proportion_buts_inscrit_2nde_periode"], "0-15 min (Proportion Buts inscrits)": item["proportion_buts_0_15"],
                                "16-30 min (Proportion Buts inscrits)": item["proportion_buts_16_30"],"31-45 min (Proportion Buts inscrits)": item["proportion_buts_31_45"],
                                "46-60 min (Proportion Buts inscrits)": item["proportion_buts_46_60"], "61-75 min (Proportion Buts inscrits)": item["proportion_buts_61_75"],
                                "76-90 min (Proportion Buts inscrits)": item["proportion_buts_76_90"], "1ère période (Proportion Buts concédés)": item["proportion_buts_encaissés_1ere_periode"],                               
                                "2ème période (Proportion Buts concédés)": item["proportion_buts_encaissés_2nde_periode"], "0-15 min (Proportion Buts concédés)": item["proportion_buts_encaissés_0_15"],
                                "16-30 min (Proportion Buts concédés)": item["proportion_buts_encaissés_16_30"], "31-45 min (Proportion Buts concédés)": item["proportion_buts_encaissés_31_45"],
                                "46-60 min (Proportion Buts concédés)": item["proportion_buts_encaissés_46_60"], "61-75 min (Proportion Buts concédés)": item["proportion_buts_encaissés_61_75"],
                                "76-90 min (Proportion Buts concédés)": item["proportion_buts_encaissés_76_90"], "1ère période (Buts inscrits)": item["buts_inscrit_1ere_periode"],
                                "2ème période (Buts inscrits)": item["buts_inscrit_2nde_periode"], "0-15 min (Buts inscrits)": item["nbr_buts_0_15"],"16-30 min (Buts inscrits)": item["nbr_buts_16_30"],
                                "31-45 min (Buts inscrits)": item["nbr_buts_31_45"], "46-60 min (Buts inscrits)": item["nbr_buts_46_60"], "61-75 min (Buts inscrits)": item["nbr_buts_61_75"],
                                "76-90 min (Buts inscrits)": item["nbr_buts_76_90"], "1ère période (Buts concédés)": item["buts_encaissés_1ere_periode"],
                                "2ème période (Buts concédés)": item["buts_encaissés_2nde_periode"], "0-15 min (Buts concédés)": item["buts_encaissés_0_15"], "16-30 min (Buts concédés)": item["buts_encaissés_16_30"],
                                "31-45 min (Buts concédés)": item["buts_encaissés_31_45"], "46-60 min (Buts concédés)": item["buts_encaissés_46_60"],
                                "61-75 min (Buts concédés)": item["buts_encaissés_61_75"], "76-90 min (Buts concédés)": item["buts_encaissés_76_90"]

                            }
                            for item in distrib_goals_data
                        ])
                        for col in df.columns:
                            if col != "Équipe":  # Exclure la colonne "Équipe" qui contient du texte
                                df[col] = pd.to_numeric(df[col], errors='coerce')
                                df[col] = df[col].astype(float) # On transforme les données numériques en flottant

                        # Sélection des sous-ensembles de colonnes
                        distrib_goals_scored_columns = [
                            "Équipe", "1ère période (Proportion Buts inscrits)", "1ère période (Buts inscrits)", "2ème période (Proportion Buts inscrits)", "2ème période (Buts inscrits)",
                            "0-15 min (Proportion Buts inscrits)", "0-15 min (Buts inscrits)","16-30 min (Proportion Buts inscrits)", "16-30 min (Buts inscrits)",
                            "31-45 min (Proportion Buts inscrits)", "31-45 min (Buts inscrits)", "46-60 min (Proportion Buts inscrits)", "46-60 min (Buts inscrits)",
                            "61-75 min (Proportion Buts inscrits)", "61-75 min (Buts inscrits)", "76-90 min (Proportion Buts inscrits)" , "76-90 min (Buts inscrits)"
                        ]
                        distrib_goals_conceded_columns = [
                            "Équipe", "1ère période (Proportion Buts concédés)", "1ère période (Buts concédés)", "2ème période (Proportion Buts concédés)", "2ème période (Buts concédés)",
                            "0-15 min (Proportion Buts concédés)", "0-15 min (Buts concédés)","16-30 min (Proportion Buts concédés)", "16-30 min (Buts concédés)",
                            "31-45 min (Proportion Buts concédés)", "31-45 min (Buts concédés)", "46-60 min (Proportion Buts concédés)", "46-60 min (Buts concédés)",
                            "61-75 min (Proportion Buts concédés)", "61-75 min (Buts concédés)", "76-90 min (Proportion Buts concédés)" , "76-90 min (Buts concédés)"
                        ]
                        # Création des trois sous-tableaux
                        df_distrib_goals_scored = df[distrib_goals_scored_columns]
                        df_distrib_goals_conceded = df[distrib_goals_conceded_columns]
                        
                        # Tri des tableaux
                        df_distrib_goals_scored = df_distrib_goals_scored.sort_values(by=["1ère période (Proportion Buts inscrits)"], ascending=False)
                        df_distrib_goals_conceded = df_distrib_goals_conceded.sort_values(by=["1ère période (Proportion Buts concédés)"], ascending=False)

                        # Ajout de style des tableaux
                        style_df_distrib_goals_scored = (
                            df_distrib_goals_scored.style
                            .format({col: format_value for col in distrib_goals_scored_columns[1:]})  # Format personnalisé
                            .set_properties(**{"text-align": "center"})  # Centrage du texte
                        )

                        style_df_distrib_goals_conceded = (
                            df_distrib_goals_conceded.style
                            .format({col: format_value for col in distrib_goals_conceded_columns[1:]})
                            .set_properties(**{"text-align": "center"})  # Centrage du texte
                        )
                        # Affichage des deux tableaux avec formatage conditionnel
                        st.subheader(f"Tableau sur la distribution des buts inscrits pour la saison {selected_season}")
                        st.dataframe(style_df_distrib_goals_scored)

                        st.subheader(f"Tableau sur la distribution des buts concédés pour la saison {selected_season}")
                        st.dataframe(style_df_distrib_goals_conceded)

                # Affichage des graphiques relatifs à la section Domicile / Extérieur 
                elif section == "Domicile / Extérieur":
                    result_h_a = get_home_away_advantage() # Récupération des statistiques sur l'avantage du terrain

                    if result_h_a:
                        # Transformation des données en DataFrame avec les noms de colonnes
                        df_adv_home_away = pd.DataFrame([
                            {
                                "Saison": item["season_name"],"Victoire à Domicile": item["proportion_home_win"], "Match Nul": item["proportion_draw"],
                                "Victoire à l'Extérieur": item["proportion_away_win"], "Avantage du Terrain": item["home_advantage"]
                            }
                            for item in result_h_a
                        ])
                        # Détermination de l'échelle maximale en fonction des plus hautes valeurs observées
                        max_adv_home = df_adv_home_away["Avantage du Terrain"].max()
                        max_adv_home = float(max_adv_home)

                        selected_data = df_adv_home_away[df_adv_home_away["Saison"] == selected_season] # Récupération des valeurs de la compétition sélectionnée
                        
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

                    rank_home_data = get_rank_home_season(selected_season) # On construit le tableau sur le classement à domicile
                    if rank_home_data:
                        # Transformation des données en DataFrame avec les noms de colonnes
                        df = pd.DataFrame([
                            {
                                "Équipe": item["team_name"],"Matches joués": item["all_matches"],"Victoire (Domicile)": item["number_home_win"],
                                "Nul (Domicile)": item["number_home_draw"], "Défaite (Domicile)": item["number_home_lose"],"Point (Domicile)": item["home_points"],
                                "Points par match (Domicile)": item["avg_home_points"]
                            }
                            for item in rank_home_data
                        ])
                        for col in df.columns:
                            if col != "Équipe":  # Exclure la colonne "Équipe" qui contient du texte
                                df[col] = pd.to_numeric(df[col], errors='coerce')
                                df[col] = df[col].astype(float) # On tranforme les données en flottant

                        df_home_rank = df.sort_values(by=["Point (Domicile)"], ascending=False) # Tri des tableaux
                        # Application du style
                        style_df_home_rank = (
                            df_home_rank.style
                            .format({col: format_value for col in df_home_rank.columns[1:]})
                            .set_properties(**{"text-align": "center"})  # Centrage du texte
                        )
                        # Affichage des tableaux avec formatage conditionnel
                        st.subheader(f"Classement à domicile pour la saison de {selected_season}")
                        st.dataframe(style_df_home_rank)

                    rank_away_data = get_rank_away_season(selected_season) # On construit le tableau sur le classement à l'extérieur
                    if rank_away_data:
                        # Transformation des données en DataFrame avec les noms de colonnes
                        df = pd.DataFrame([
                            {
                                "Équipe": item["team_name"],"Matches joués": item["all_matches"],"Victoire (Extérieur)": item["number_away_win"],
                                "Nul (Extérieur)": item["number_away_draw"], "Défaite (Extérieur)": item["number_away_lose"],"Point (Extérieur)": item["away_points"],
                                "Points par match (Extérieur)": item["avg_away_points"]
                            }
                            for item in rank_away_data
                        ])
                        for col in df.columns:
                            if col != "Équipe":  # Exclure la colonne "Équipe" qui contient du texte
                                df[col] = pd.to_numeric(df[col], errors='coerce')
                                df[col] = df[col].astype(float) # On tranforme les données en flottant

                        df_away_rank = df.sort_values(by=["Point (Extérieur)"], ascending=False)  # Tri des tableaux
                        # Application du style
                        style_df_away_rank = (
                            df_away_rank.style
                            .format({col: format_value for col in df_away_rank.columns[1:]})
                            .set_properties(**{"text-align": "center"})  # Centrage du texte
                        )
                        # Affichage des tableaux avec formatage conditionnel
                        st.subheader(f"Classement à l'exterieur pour la saison de {selected_season}")
                        st.dataframe(style_df_away_rank)

                # On passe à la section Comparaison entre les saisons
                elif section == "Comparaison entre les saisons":
                    
                    compare_avg_goal_data = get_avg_goals_stats_by_competition() # On stocke les données sur le nombre de but moyen

                    if compare_avg_goal_data:
                        # Transformation des données en DataFrame avec les noms de colonnes
                        df = pd.DataFrame([
                            {
                                "Compétition": item["competition_name"], "Saison": item["season_name"], "Buts/Match": item["avg_goals_per_match"],
                                "Buts Domicile": item["avg_home_goals"], "Buts Extérieur": item["avg_away_goals"]                            }
                            for item in compare_avg_goal_data
                        ])                      
                        df = df[df["Compétition"] == selected_competition] # Récupération des valeurs de la compétition sélectionnée

                        df = df.drop(columns=["Compétition"]) # On enlève la colonne Compétition du tableau que l'on va afficher

                        # On traite les colonnes numériques de façon à les arrondir à 2 chiffres après la virgule si besoin
                        numeric_columns = df.columns[1:]
                        df[numeric_columns] = df[numeric_columns].applymap(lambda x: int(x) if x == int(x) else round(x, 2))

                        df = df.sort_values(by=numeric_columns.tolist(), ascending=False) # Assurer un tri numérique et non alphabétique

                        # Appliquer le style de formatage et la coloration en une seule fois
                        styled_df = (
                            df.style
                            .format({col: format_value for col in numeric_columns})  # Format personnalisé
                            .apply(highlight_selected_season, axis=1)  # Coloration personnalisée
                            .set_properties(**{"text-align": "center"})  # Centrage du texte
                        )
                        # Affichage du tableau mis en forme avec tri
                        st.subheader("⚽ Informations sur les statistiques générales (en moyenne)")
                        st.dataframe(styled_df)
                        
                        top5_goals_data = get_top5_goals_scored(selected_competition) # Récupération des données pour toutes les saisons de la compétition sélectionnée

                        if top5_goals_data:
                            # Transformation des données en DataFrame avec les noms de colonne
                            df = pd.DataFrame([
                                {
                                    "Équipe": item["team_name"], "Saison": item["season_name"], "Nbr. buts inscrits": item["total_goals_scored"], "Moy. buts inscrits": item["avg_goals_scored"],
                                    "Nbr. buts inscrits (Domicile)": item["goals_scored_home"], "Moy. buts inscrits (Domicile)": item["avg_goals_scored_home"],
                                    "Nbr. buts inscrits (Extérieur)": item["goals_scored_away"], "Moy. buts inscrits (Extérieur)": item["avg_goals_scored_away"]
                                }
                                for item in top5_goals_data
                            ])
                            
                            numeric_columns = df.columns[2:]  # Sélection des colonnes numériques
                            
                            for col in numeric_columns:
                                df[col] = pd.to_numeric(df[col], errors='coerce')  # Convertir en float
                            df[numeric_columns] = df[numeric_columns].applymap(lambda x: round(x, 2) if pd.notnull(x) else x) # On arrondit à 2 chiffres après la virgule si besoin

                            df = df.sort_values(by=["Saison", "Moy. buts inscrits"], ascending=[False, False]) # On ordonne selon la moyenne de buts inscrits

                            # Appliquer le style de formatage et la coloration en une seule fois
                            styled_df = (
                                df.style
                                .format({col: format_value for col in numeric_columns})  # Format personnalisé
                                .set_properties(**{"text-align": "center"})  # Centrage du texte
                            )
                            st.subheader(f"Top 5 des équipes ayant marqué le plus de buts pour {selected_competition} (toutes saisons)") # On affiche le titre
                            st.dataframe(styled_df)

                        top5_goals_conceded_data = get_top5_goals_conceded(selected_competition) # Récupération des données pour toutes les saisons de la compétition sélectionnée

                        if top5_goals_conceded_data:
                            # Transformation des données en DataFrame avec les noms de colonnes
                            df = pd.DataFrame([
                                {
                                    "Équipe": item["team_name"], "Saison": item["season_name"], "Nbr. buts concédés": item["total_goals_conceded"], "Moy. buts concédés": item["avg_goals_conceded"],
                                    "Nbr. buts concédés (Domicile)": item["goals_conceded_home"], "Moy. buts concédés (Domicile)": item["avg_goals_conceded_home"],
                                    "Nbr. buts concédés (Extérieur)": item["goals_conceded_away"], "Moy. buts concédés (Extérieur)": item["avg_goals_conceded_away"]
                                }
                                for item in top5_goals_conceded_data
                            ])
                            # Convertir les colonnes numériques en float
                            numeric_columns = df.columns[2:]  # Sélection des colonnes numériques
                            for col in numeric_columns:
                                df[col] = pd.to_numeric(df[col], errors='coerce')  # Convertir en float

                            df[numeric_columns] = df[numeric_columns].applymap(lambda x: round(x, 2) if pd.notnull(x) else x) # Arrondir à deux décimales

                            df = df.sort_values(by=["Saison", "Moy. buts concédés"], ascending=[False, True]) # On ordonne selon la moyenne de buts concédés
                            # Appliquer le style de formatage et la coloration en une seule fois
                            styled_df = (
                                df.style
                                .format({col: format_value for col in numeric_columns})  # Format personnalisé
                                .set_properties(**{"text-align": "center"})  # Centrage du texte
                            )
                            st.subheader(f"Top 5 des équipes ayant concédé le moins de buts pour {selected_competition} (toutes saisons)") # On donne un titre
                            st.dataframe(styled_df)

                    # Initialisation des variables de comparaison du 1er but inscrit et de la distribution des buts par saison
                    compare_first_goal_data = []
                    compare_distrib_goal_data = []
                    
                    # Création d'une boucle for pour récupérer la liste des saisons disponibles pour la compétition choisit par l'utilisateur
                    for season in seasons_available:
                        # Récupération des données
                        season_stats = get_first_goal_stats(season)
                        distrib_stats = get_distribution_goals(season)
                        distrib_stats = distrib_stats[0]

                        # Ajout des données saison par saison
                        if season_stats:
                            compare_first_goal_data.extend(season_stats)
                        if distrib_stats:
                            compare_distrib_goal_data.append(distrib_stats)

                    if compare_first_goal_data:
                        # Transformation des données en DataFrame avec les noms de colonnes
                        df = pd.DataFrame([
                            {
                                "Saison": item["season_name"], "Aucun but": item["proportion_no_goal"], "1er but inscrit - Domicile": item["proportion_1st_goal_home"],
                                "1er but inscrit - Extérieur": item["proportion_1st_goal_away"], "1er but inscrit / Victoire": item["first_goal_win"],
                                "1er but inscrit / Nul": item["first_goal_draw"],"1er but inscrit / Défaite": item["first_goal_lose"],                    
                                "1er but inscrit / Domicile / Victoire": item["first_goal_home_win"], "1er but inscrit / Domicile / Nul": item["first_goal_home_draw"],
                                "1er but inscrit / Domicile / Défaite": item["first_goal_home_lose"], "1er but inscrit / Extérieur / Victoire": item["first_goal_away_win"],
                                "1er but inscrit / Extérieur / Nul": item["first_goal_away_draw"], "1er but inscrit / Extérieur / Défaite": item["first_goal_away_lose"]                                
                            }
                            for item in compare_first_goal_data
                        ])
                        # Formatage des colonnes numériques
                        numeric_columns = df.columns[1:]
                        df[numeric_columns] = df[numeric_columns].astype(float)

                        df = df.sort_values(by=numeric_columns.tolist(), ascending=False) # Tri numérique

                        # Appliquer le style de formatage et la coloration en une seule fois
                        styled_df = (
                            df.style
                            .format({col: format_value for col in numeric_columns})  # Format personnalisé
                            .apply(highlight_selected_season, axis=1)  # Coloration personnalisée
                            .set_properties(**{"text-align": "center"})  # Centrage du texte
                        )
                        # Affichage du tableau
                        st.subheader("⚽ Informations sur le 1er but (inscrit ou encaissé) (en %)")
                        st.dataframe(styled_df)
                        
                        top5_first_goal_data = get_top_teams_first_goal(selected_competition) # Récupération des données pour toutes les saisons de la compétition sélectionnée

                        if top5_first_goal_data:
                            # Transformation des données en DataFrame avec les noms de colonnes
                            df = pd.DataFrame([
                                {
                                    "Saison": item["season_name"], "Équipe": item["team_name"], "Proportion du 1er but inscrit": item["proportion_1st_goal_for"]
                                }
                                for item in top5_first_goal_data
                            ])

                            df["Proportion du 1er but inscrit"] = df["Proportion du 1er but inscrit"].astype(float).map(format_value) # Convertir en flottant et dans le format souhaité
                            df = df.sort_values(by=["Équipe", "Proportion du 1er but inscrit"], ascending=[False, False]) # On ordonné selon la proportion du 1er but inscrit

                            # Appliquer le style de formatage et la coloration en une seule fois
                            styled_df = (
                                df.style
                                .set_properties(**{"text-align": "center"})  # Centrage du texte
                            )
                            st.subheader(f"Top 5 des équipes ayant les meilleurs taux de 1er but inscrit pour la {selected_competition} (toutes saisons)") # On écrit le titre
                            st.dataframe(styled_df)

                        top5_first_goal_win_data = get_top_teams_first_goal_win(selected_competition) # Récupération des données pour toutes les saisons de la compétition sélectionnée

                        if top5_first_goal_win_data:
                            # Transformation des données en DataFrame avec les noms de colonnes
                            df = pd.DataFrame([
                                {
                                    "Saison": item["season_name"], "Équipe": item["team_name"], "Proportion du 1er but inscrit apportant la victoire": item["first_goal_win"]
                                }
                                for item in top5_first_goal_win_data
                            ])
                            # Convertir en flottant et dans le format souhaité
                            df["Proportion du 1er but inscrit apportant la victoire"] = df["Proportion du 1er but inscrit apportant la victoire"].astype(float).map(format_value)

                            df = df.sort_values(by=["Équipe", "Proportion du 1er but inscrit apportant la victoire"], ascending=[False, False]) # On ordonne les données
                            
                            # Appliquer le style de formatage et la coloration en une seule fois
                            styled_df = (
                                df.style
                                .set_properties(**{"text-align": "center"})  # Centrage du texte
                            )
                            # On met un titre et on centre ce dernier
                            st.subheader(f"Top 5 des équipes ayant les meilleurs taux de 1er but inscrit apportant la victoire pour la {selected_competition} (toutes saisons)")
                            st.dataframe(styled_df)

                        # Récupération des données pour toutes les saisons de la compétition sélectionnée
                        top5_first_goal_conceded_win_data = get_top_teams_first_goal_conceded_win(selected_competition)

                        if top5_first_goal_conceded_win_data:
                            # Transformation des données en DataFrame avec les noms de colonnes
                            df = pd.DataFrame([
                                {
                                    "Saison": item["season_name"], "Équipe": item["team_name"], "Proportion du 1er but concédé mais avec la victoire finale": item["first_goal_conceded_win"]
                                }
                                for item in top5_first_goal_conceded_win_data
                            ])
                            # Convertir en flottant et dans le format souhaité
                            df["Proportion du 1er but concédé mais avec la victoire finale"] = df["Proportion du 1er but concédé mais avec la victoire finale"].astype(float).map(format_value)
                            df = df.sort_values(by=["Équipe", "Proportion du 1er but concédé mais avec la victoire finale"], ascending=[False, False]) # On ordonne les données

                            # Appliquer le style de formatage et la coloration en une seule fois
                            styled_df = (
                                df.style
                                .set_properties(**{"text-align": "center"})  # Centrage du texte
                            )
                            # On donne un titre et on centre ce dernier
                            st.subheader(f"Top 5 des équipes ayant les meilleurs taux de 1er but concédé mais avec la victoire finale pour la {selected_competition} (toutes saisons)")
                            st.dataframe(styled_df)

                    if compare_distrib_goal_data:
                        # Transformation en dataframe en fonction des noms de colonnes
                        df = pd.DataFrame([
                            {
                                "Saison": item["season_name"] ,"1ère période": item["proportion_buts_1ere_periode"],"2ème période": item["proportion_buts_2nde_periode"],
                                "0-15 min": item["proportion_buts_0_15"], "16-30 min": item["proportion_buts_16_30"],"31-45 min": item["proportion_buts_31_45"],
                                "46-60 min": item["proportion_buts_46_60"], "61-75 min": item["proportion_buts_61_75"], "76-90 min": item["proportion_buts_76_90"]

                            }
                            for item in compare_distrib_goal_data
                        ])
                        numeric_columns = df.columns[1:] # Traitement des données numériques
                        df[numeric_columns] = df[numeric_columns].astype(float)

                        df = df.sort_values(by=numeric_columns.tolist(), ascending=False) # Assurer un tri numérique et non alphabétique

                        styled_df = df.style.apply(highlight_selected_season, axis=1) # Appliquer la coloration par colonne
                        
                        styled_df = styled_df.format({col: "{:.2f}" for col in numeric_columns}) # Formatage propre des valeurs numériques avec deux chiffres après la virgule 

                        # Affichage du tableau mis en forme avec tri
                        st.subheader("⚽ Informations sur la distribution des buts par saison (en %)")
                        st.dataframe(styled_df.set_properties(**{"text-align": "center"}))
                    
                    top_teams_1st_period_data = get_top_teams_1st_period(selected_competition) # Récupération des données pour toutes les saisons de la compétition sélectionnée

                    if top_teams_1st_period_data:
                        # Transformation des données en DataFrame avec les noms de colonnes
                        df = pd.DataFrame([
                            {
                                "Saison": item["season_name"], "Équipe": item["team_name"],"Prop. Buts inscrits (1ère période)": item["proportion_buts_1ere_periode"],
                                "Nbr. Buts inscrits (1ère période)": item["nbr_buts_inscrit_1ere_periode"], "Prop. Buts inscrits (0-15 min)": item["proportion_buts_0_15"],
                                "Nbr. Buts inscrits (0-15 min)": item["nbr_buts_0_15"], "Prop. Buts inscrits (16-30 min)": item["proportion_buts_16_30"],
                                "Nbr. Buts inscrits (16-30 min)": item["nbr_buts_16_30"], "Prop. Buts inscrits (31-45 min)": item["proportion_buts_31_45"],
                                "Nbr. Buts inscrits (31-45 min)": item["nbr_buts_31_45"]

                            }
                            for item in top_teams_1st_period_data
                        ])    
                        numeric_columns = df.columns[2:]  # Sélection des colonnes numériques
                        for col in numeric_columns:
                            df[col] = pd.to_numeric(df[col], errors='coerce')  # Convertir en float

                        df = df.sort_values(by=["Saison", "Prop. Buts inscrits (1ère période)"], ascending=[False, False]) # On ordonne les données

                        # Appliquer le style de formatage et la coloration en une seule fois
                        styled_df = (
                            df.style
                            .format({col: format_value for col in numeric_columns})  # Format personnalisé
                            .set_properties(**{"text-align": "center"})  # Centrage du texte
                        )
                        # On donne un titre et on le centre
                        st.subheader(f"Top 5 des équipes ayant le plus haut taux de buts marqués en 1ère période pour la {selected_competition} (toutes saisons)")
                        st.dataframe(styled_df)

                    top_teams_2nd_period_data = get_top_teams_2nd_period(selected_competition) # Récupération des données pour toutes les saisons de la compétition sélectionnée

                    if top_teams_2nd_period_data:
                        # Transformation des données en DataFrame avec les noms de colonnes
                        df = pd.DataFrame([
                            {
                                "Saison": item["season_name"], "Équipe": item["team_name"],"Prop. Buts inscrits (2nd période)": item["proportion_buts_inscrit_2nde_periode"],
                                "Nbr. Buts inscrits (2nd période)": item["nbr_buts_inscrit_2nde_periode"], "Prop. Buts inscrits (46-60 min)": item["proportion_buts_46_60"],
                                "Nbr. Buts inscrits (46-60 min)": item["nbr_buts_46_60"], "Prop. Buts inscrits (61-75 min)": item["proportion_buts_61_75"],
                                "Nbr. Buts inscrits (61-75 min)": item["nbr_buts_61_75"], "Prop. Buts inscrits (76-90 min)": item["proportion_buts_76_90"],
                                "Nbr. Buts inscrits (76-90 min)": item["nbr_buts_76_90"]

                            }
                            for item in top_teams_2nd_period_data
                        ])    
                        numeric_columns = df.columns[2:]  # Sélection des colonnes numériques
                        for col in numeric_columns:
                            df[col] = pd.to_numeric(df[col], errors='coerce')  # Convertir en float

                        df = df.sort_values(by=["Saison", "Prop. Buts inscrits (2nd période)"], ascending=[False, False]) # On ordonne les données
                        # Appliquer le style de formatage et la coloration en une seule fois
                        styled_df = (
                            df.style
                            .format({col: format_value for col in numeric_columns})  # Format personnalisé
                            .set_properties(**{"text-align": "center"})  # Centrage du texte
                        )
                        # On met un titre et on centre ce dernier
                        st.subheader(f"Top 5 des équipes ayant le plus haut taux de buts marqués en 2ème période pour la {selected_competition} (toutes saisons)")
                        st.dataframe(styled_df)

                    top_teams_last_minutes_data = get_top_teams_last_minutes(selected_competition) # Récupération des données pour toutes les saisons de la compétition sélectionnée

                    if top_teams_last_minutes_data:
                        # Transformation des données en DataFrame avec les noms de colonnes
                        df = pd.DataFrame([
                            {
                                "Saison": item["season_name"], "Équipe": item["team_name"],"Prop. Buts inscrits (76-90 min)": item["proportion_buts_76_90"],
                                "Nbr. Buts inscrits (76-90 min)": item["nbr_buts_76_90"]
                            }
                            for item in top_teams_last_minutes_data
                        ])    
                            
                        numeric_columns = df.columns[2:]  # Sélection des colonnes numériques
                        for col in numeric_columns:
                            df[col] = pd.to_numeric(df[col], errors='coerce')  # Convertir en float

                        df = df.sort_values(by=["Saison", "Prop. Buts inscrits (76-90 min)"], ascending=[False, False]) # On ordonne les données
                        # Appliquer le style de formatage et la coloration en une seule fois
                        styled_df = (
                            df.style
                            .format({col: format_value for col in numeric_columns})  # Format personnalisé
                            .set_properties(**{"text-align": "center"})  # Centrage du texte
                        )
                        # On met un titre et on le centre
                        st.subheader(f"Top 5 des équipes ayant le plus haut taux de buts marqués dans les 15 dernières minutes pour la {selected_competition} (toutes saisons)")
                        st.dataframe(styled_df)

                    compare_home_away_adv_data = get_home_away_advantage() # On récupère les données par saison pour la saison
                    if compare_home_away_adv_data:
                        # Transformation des données en DataFrame avec les noms de colonnes
                        df = pd.DataFrame([
                            {
                                "Saison": item["season_name"],"Victoire à Domicile": item["proportion_home_win"], "Match Nul": item["proportion_draw"],
                                "Victoire à l'Extérieur": item["proportion_away_win"], "Avantage du Terrain": item["home_advantage"]
                            }
                            for item in compare_home_away_adv_data
                        ])
                        df = df[df["Saison"].isin(seasons_available)] # Filtrer uniquement les saisons présentes dans seasons_available
                        
                        # Traitement des colonnes numériques 
                        numeric_columns = df.columns[1:]
                        df[numeric_columns] = df[numeric_columns].astype(float)  # Conversion en flottant

                        df = df.sort_values(by=numeric_columns.tolist(), ascending=False) # Assurer un tri numérique et non alphabétique

                        # Appliquer le style de formatage et la coloration en une seule fois
                        styled_df = (
                            df.style
                            .format({col: format_value for col in numeric_columns})  # Format personnalisé
                            .apply(highlight_selected_season, axis=1)  # Coloration personnalisée
                            .set_properties(**{"text-align": "center"})  # Centrage du texte
                        )
                        # Affichage du tableau mis en forme avec tri
                        st.subheader(f"⚽ Informations sur l'influence du facteur Domicile/Extérieur pour la {selected_competition} (toutes saisons)")
                        st.dataframe(styled_df)

                    top5_home_rank_data = get_top5_home_rank_competition(selected_competition) # Récupération des données pour toutes les saisons de la compétition sélectionnée

                    if top5_home_rank_data:
                        # Transformation des données en DataFrame avec les noms de colonnes
                        df = pd.DataFrame([
                            {
                                "Saison": item["season_name"], "Équipe": item["team_name"],"Matches joués": item["all_matches"],"Victoire (Domicile)": item["number_home_win"],
                                "Nul (Domicile)": item["number_home_draw"], "Défaite (Domicile)": item["number_home_lose"],"Point (Domicile)": item["home_points"],
                                "Points par match (Domicile)": item["avg_home_points"]
                            }
                            for item in top5_home_rank_data
                        ])                         
                        df = df.sort_values(by=["Équipe", "Points par match (Domicile)"], ascending=[False, False]) # On ordonne les données
                        # Appliquer le style de formatage et la coloration en une seule fois
                        styled_df = (
                            df.style
                            .format({col: format_value for col in numeric_columns})  # Format personnalisé
                            .set_properties(**{"text-align": "center"})  # Centrage du texte
                        )
                        # On donne un titre et on centre ce dernier
                        st.subheader(f"Top 5 des équipes ayant le meilleur bilan à domicile pour la {selected_competition} (toutes saisons)")
                        st.dataframe(styled_df)

                    top5_away_rank_data = get_top5_away_rank_competition(selected_competition) # Récupération des données pour toutes les saisons de la compétition sélectionnée

                    if top5_away_rank_data:
                        # Transformation des données en DataFrame avec les noms de colonnes
                        df = pd.DataFrame([
                            {
                                "Saison": item["season_name"], "Équipe": item["team_name"],"Matches joués": item["all_matches"],"Victoire (Extérieur)": item["number_away_win"],
                                "Nul (Extérieur)": item["number_away_draw"], "Défaite (Extérieur)": item["number_away_lose"],"Point (Extérieur)": item["away_points"],
                                "Points par match (Extérieur)": item["avg_away_points"]
                            }
                            for item in top5_away_rank_data
                        ])   
                        df = df.sort_values(by=["Équipe", "Points par match (Extérieur)"], ascending=[False, False]) # On ordonne les données
                        # Appliquer le style de formatage et la coloration en une seule fois
                        styled_df = (
                            df.style
                            .format({col: format_value for col in numeric_columns})  # Format personnalisé
                            .set_properties(**{"text-align": "center"})  # Centrage du texte
                        )
                        # On donne un titre et on le centre
                        st.subheader(f"Top 5 des équipes ayant le meilleur bilan à l'extérieur pour la {selected_competition} (toutes saisons)")
                        st.dataframe(styled_df)

                    else:
                        st.warning("Aucune donnée disponible pour cette saison.")

# Affichage de l’image uniquement si aucun choix n'a été fait
if show_image:
    st.image(image_path)