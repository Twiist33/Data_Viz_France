"""

Ceci est la page principale du projet, veuillez trouver ci dessous une brève présentation du projet, ainsi que le mémoire associé.
This is the main page of the project, please find below a brief presentation of the project, as well as the associated brief.

"""

# Import des librairies / Importing libraries
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_option_menu import option_menu
import os
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
from supabase import create_client
from dotenv import load_dotenv
from decimal import Decimal
import numpy as np

# Charger les  fichiers PDF présent à la fin de la page d'acceuil / Load PDF files at the end of the home page
with open("Documentation/Documentation_Data_Viz_France.pdf", "rb") as file:
    doc = file.read()
with open("Documentation/Documentation_Data_Viz_France_English.pdf", "rb") as file:
    doc_eng = file.read()
with open("Mémoire/Mémoire_Romain_Traboul.pdf", "rb") as file:
    memoire = file.read()
with open("CV/CV_FR_Romain_Traboul.pdf", "rb") as file:
    cv_data_fr = file.read()
with open("CV/CV_ENG_Romain_Traboul.pdf", "rb") as file:
    cv_data_eng = file.read()

# Affichage du titre et du logo de l'application web / Display of web application title and logo
st.set_page_config(page_title="Data Viz ⚽ 🇫🇷", page_icon="📊", layout="centered")

load_dotenv() # Chargement des variables d'environnement / Loading environment variables

# Connexion à la base de données Supabase / Connection to the Supabase database
project_url = os.getenv("project_url")
api_key = os.getenv("api_key")
supabase = create_client(project_url, api_key)

# Langue dans session_state
if "lang" not in st.session_state:
    st.session_state["lang"] = "Français"

lang = st.sidebar.selectbox(
    "Choisissez votre langue / Choose your language", 
    ["Français", "English"]
)
st.session_state["lang"] = lang

# Création du menu horizontal / Horizontal menu at the top of the page /
menu = option_menu(
    menu_title=None,
    options=["Accueil", "Équipe", "Duel", "Saison", "Ligue"] if lang == "Français" else
            ["Home", "Team", "H2H", "Season", "League"],
    icons=["house", "person", "crosshair", "calendar", "trophy"],
    orientation="horizontal",
)

### Création des fonctions permettant de récuperer les informations de la base de données liées à l'analyse d'une équipe
### Creation of functions to retrieve information from the database relating to the analysis of a team

# Fonction pour récupérer les équipes disponibles dans la table team / Function for retrieving the teams available in the team table
def get_teams():
    try:
        # Appel de la fonction RPC avec params comme dictionnaire vide / Calling the RPC function with params as an empty dictionary
        response = supabase.rpc("get_teams", params={}).execute()
        if response.data:
            teams = response.data
        else:
            teams = []
        return teams
    except Exception as e:
        st.error(f"Erreur de connexion à Supabase : {e}")
        return []

# Fonction pour récupérer les saisons disponibles pour une équipe (au moins 5 matchs dans cette saison pour être comptabilisé)
# Function to retrieve the seasons available for a team (at least 5 matches in that season to be counted)
def get_seasons(team_name):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_seasons", params={"team_name_input": team_name}).execute()
        if response.data:
            seasons = response.data
        else:
            seasons = []
        return seasons
    except Exception as e:
        st.error(f"Erreur de connexion à Supabase : {e}")
        return []

# Fonction pour récupérer les statistiques de moyenne de buts par match pour une équipe donnée regroupé par saison (au moins 5 matchs dans cette saison pour être comptabilisé)
# Function to retrieve the average goals per match statistics for a given team grouped by season (at least 5 matches in that season to be counted).
def get_avg_goals_stats(season_name):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_avg_goals_stats", params={"season_name_input": season_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des statistiques : {e}")
        return []

# Fonction pour récupérer les information de buts inscrits par une équipe, regroupé par saison (au moins 5 matchs dans cette saison pour être comptabilisé)
# Function to retrieve information on goals scored by a team, grouped by season (at least 5 matches in that season to be counted).
def get_goals_scored(season_name):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_goals_scored", params={"season_name_input": season_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les information de buts concédés pour une équipe donnée, regroupé par saison
# Function to retrieve information on goals conceded for a given team, grouped by season
def get_goals_conceded(season_name):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_goals_conceded", params={"season_name_input": season_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer la fréquence des scores d'une équipe pour une saison donnée (au moins 5 matchs dans cette saison pour être comptabilisé)
# Function to retrieve a team's score frequency for a given season (at least 5 matches in that season to be counted)
def get_frequent_score(team_name, season_name):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_frequent_score", {
            "team_name_input": team_name, "season_name_input": season_name
        }).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        print(f"Erreur lors de l'exécution de la fonction RPC : {e}")
        return None

# Fonction pour récupérer les statistiques sur le 1er but inscrit ou concédé d'une équipe, en comparaison des saisons provenant d'une même compétition (au moins 5 matchs dans cette saison pour être comptabilisé)
# Function to retrieve statistics on the 1st goal scored or conceded by a team, in comparison with seasons from the same competition (at least 5 matches in that season to be counted).
def get_first_goal_season(season_name):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_first_goal_season", params={"season_name_input": season_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les statistiques générales de la saison au niveau de la distribution des buts (inscrits et concédés)
# Function to retrieve general statistics for the season in terms of the distribution of goals (scored and conceded)
def get_distribution_goals_season(season_name):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_distribution_goals_season", params={"season_name_input": season_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction sur les informations de la saison à domicile et à l'extérieur pour chaque équipe d'une saison donnée (au moins 5 matchs dans cette saison pour être comptabilisé)
# Function on home and away season information for each team in a given season (at least 5 matches in that season to be counted)
def get_rank_season(season_name):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_rank_season", params={"season_name_input": season_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction personnalisée pour le formatage conditionnel / Custom function for conditional formatting
def format_value(x):
    if pd.isnull(x):
        return "0"
    elif x == int(x):
        return str(int(x))  # Affiche sans décimales si entier / Displays without decimals if integer
    else:
        return f"{x:.2f}"   # Affiche avec 2 décimales sinon / Display with 2 decimal places otherwise

# Fonction pour construire les camemberts en omettant les labels vides / Function for constructing pie charts by omitting empty labels
def plot_pie_chart(ax, data, labels, title, colors):
    mask = data > 0  # Filtrer les catégories avec une valeur > 0 / Filter categories with a value > 0
    filtered_data = data[mask]
    filtered_labels = [label for label, m in zip(labels, mask) if m]
    filtered_colors = [color for color, m in zip(colors, mask) if m]

    if filtered_data.sum() > 0:
        ax.pie(filtered_data, labels=filtered_labels, autopct='%1.2f%%', startangle=90, colors=filtered_colors)
        ax.set_title(title)
    else:
        ax.axis('off')


### Création des fonctions permettant de récuperer les informations de la base de données liées à l'analyse des confrontations entre deux équipes
### Creation of functions to retrieve information from the database relating to the analysis of a head to head between two teams

# Fonction pour récupérer les équipes présents dans la saison de la 1ère équipe choisie / Function to retrieve the teams present in the season of the 1st team selected
def get_teams_in_season(season_name):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_teams_in_season", params={"season_name_input": season_name}).execute()
        if response.data:
            seasons = response.data
        else:
            seasons = []
        return seasons
    except Exception as e:
        st.error(f"Erreur de connexion à Supabase : {e}")
        return []

# Fonction pour récupérer les matchs opposant 2 équipes / Function to retrieve matches between 2 teams
def get_matches_between_teams(selected_team_home, selected_team_away):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_matches_between_teams", params={"selected_team_home_input": selected_team_home, "selected_team_away_input": selected_team_away}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour calculer la moyenne des buts inscrits lorsque deux équipes s'affrontent
# Function for calculating the average number of goals scored when two teams play each other
def get_avg_goals_stats_between_teams(selected_team_home, selected_team_away):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_avg_goals_stats_between_teams", params={"selected_team_home_input": selected_team_home, "selected_team_away_input": selected_team_away}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les informations du premier but inscrit entre deux équipes / Function to retrieve information about the first goal scored between two teams
def get_1st_goal_stats_between_teams(selected_team_home, selected_team_away):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_1st_goal_stats_between_teams", params={"selected_team_home_input": selected_team_home, "selected_team_away_input": selected_team_away}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les informations des proportions cumulées des buts inscrits / Function to retrieve information on the cumulative proportion of goals scored
def get_distrib_goal_between_teams(selected_team_home, selected_team_away):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_distrib_goal_between_teams", params={"selected_team_home_input": selected_team_home, "selected_team_away_input": selected_team_away}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récuperer les performances à face à face dans cette configurations entre deux équipes
# Function for recovering head-to-head performances in this configuration between two teams               
def get_home_away_selected_teams(selected_team_home, selected_team_away):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_home_away_selected_teams", params={"selected_team_home_input": selected_team_home, "selected_team_away_input": selected_team_away}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour colorer les jauges / Function to colour the gauges
def plot_gauge(value, max_value, title, inverse=False):
    # Calcul de la couleur en fonction du ratio valeur/max / Colour calculation based on the value/max ratio
    ratio = value / max_value
    if inverse:
        red = int(210 * ratio)  # Plus c'est haut, plus c'est rouge / The higher, the redder
        green = int(210 * (1 - ratio))
    else:
        red = int(210 * (1 - ratio))  # Plus c'est bas, plus c'est rouge / The lowher, the redder
        green = int(210 * ratio)
    color = f"rgb({red},{green},0)"

    # Création de la jauge / Creating the gauge
    return go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title, "font": {"size": 9}},
        gauge={
            "axis": {"range": [0, max_value]},
            "bar": {"color": color}  # Couleur dynamique / Dynamic color
        }
    ))

### Création des fonctions permettant de récuperer les informations de la base de données liées à l'analyse d'une saison
### Creation of functions to retrieve information from the database relating to the analysis of a season

# Fonction pour récupérer les compétitions disponibles / Function for retrieving available competitions
def get_competitions():
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_competitions", params={}).execute()
        if response.data:
            teams = response.data
        else:
            teams = []
        return teams
    except Exception as e:
        st.error(f"Erreur de connexion à Supabase : {e}")
        return []

# Fonction pour récupérer les saisons disponibles pour une compétition donnée / Function for retrieving the seasons available for a given competition
def get_seasons_by_competition(competition_name):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_seasons_by_competition", params={"competition_name_input": competition_name}).execute()
        if response.data:
            seasons = response.data
        else:
            seasons = []
        return seasons
    except Exception as e:
        st.error(f"Erreur de connexion à Supabase : {e}")
        return []

# Fonction pour récupérer les statistiques de moyenne de buts par match / Function for retrieving average goals per match statistics
def get_avg_goals_stats_by_competition():
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_avg_goals_stats_by_competition", params={}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des statistiques : {e}")
        return []

# Fonction pour récupérer les statistiques générales de la saison au niveau de la fréquence des scores
# Function to retrieve general statistics for the season in terms of scoring frequency
def get_frequent_score_by_season(season_name):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_frequent_score_by_season", {"season_name_input": season_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        print(f"Erreur lors de l'exécution de la fonction RPC : {e}")
        return None

# Fonction pour récupérer les information de buts inscrits sur une saison donnée / Function to retrieve information on goals scored in a given season
def get_goals_scored(season_name):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_goals_scored", params={"season_name_input": season_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les information de buts concédés sur une saison donnée / Function to retrieve information on goals conceded in a given season
def get_goals_conceded(season_name):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_goals_conceded", params={"season_name_input": season_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer le nom des 5 équipes ayant obtenus les meilleurs taux de buts inscrits par match sur une saison donnée
# Function to retrieve the names of the 5 teams with the best goals scored per match in a given season
def get_top5_goals_scored(competition_name):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_top5_goals_scored", params={"competition_name_input": competition_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer le nom des 5 équipes ayant obtenus les meilleurs taux de buts concédés par match sur une saison donnée
# Function to retrieve the names of the 5 teams with the best rate of goals conceded per match in a given season
def get_top5_goals_conceded(competition_name):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_top5_goals_conceded", params={"competition_name_input": competition_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les statistiques sur le 1er but inscrit ou concédé sur une saison donnée
# Function to retrieve statistics on the 1st goal scored or conceded in a given season
def get_first_goal_stats(season_name):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_first_goal_stats", params={"season_name_input": season_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les statistiques sur le 1er but inscrit ou concédé, en comparaison des saisons provenant d'une même compétition
# Function to retrieve statistics on the 1st goal scored or conceded, comparing seasons from the same competition
def get_first_goal_season(season_name):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_first_goal_season", params={"season_name_input": season_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer le nom des 5 équipes ayant le meilleur taux de 1er but inscrit pour une compétition donnée
# Function for retrieving the names of the 5 teams with the best rate of 1st goals scored in a given competition
def get_top_teams_first_goal(competition_name):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_top_teams_first_goal", params={"competition_name_input": competition_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer le nom des 5 équipes ayant le meilleur taux d'influence du 1er but inscrit pour une compétition donnée
# Function to retrieve the names of the 5 teams with the highest influence rate of the 1st goal scored in a given competition
def get_top_teams_first_goal_win(competition_name):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_top_teams_first_goal_win", params={"competition_name_input": competition_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer le nom des 5 équipes ayant le meilleur taux de victoires après avoir concédé le 1er but pour une compétition donnée
# Function for retrieving the names of the 5 teams with the best win rate after conceding the 1st goal in a given competition
def get_top_teams_first_goal_conceded_win(competition_name):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_top_teams_first_goal_conceded_win", params={"competition_name_input": competition_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les statistiques générales de la saison au niveau de la distribution des buts
# Fonction pour récupérer les statistiques générales de la saison au niveau de la distribution des buts
def get_distribution_goals(season_name):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_distribution_goals", params={"season_name_input": season_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les statistiques générales de la saison au niveau de la distribution des buts (inscrits et concédés)
# Function to retrieve general statistics for the season in terms of the distribution of goals (scored and conceded)
def get_distribution_goals_season(season_name):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_distribution_goals_season", params={"season_name_input": season_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les meilleurs équipes en 1ère période sur une compétition donnée / Function to retrieve the best teams in the 1st period of a given competition
def get_top_teams_1st_period(competition_name):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_top_teams_1st_period", params={"competition_name_input": competition_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les meilleurs équipes en 2ème période sur une compétition donnée / Function to retrieve the best teams in the 2nd half of a given competition
def get_top_teams_2nd_period(competition_name):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_top_teams_2nd_period", params={"competition_name_input": competition_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les meilleurs équipes durant les 15 dernières minutes sur une compétition donnée / Function to retrieve the best teams during the last 15 minutes of a given competition
def get_top_teams_last_minutes(competition_name):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_top_teams_last_minutes", params={"competition_name_input": competition_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les statistiques générales de la saison au niveau de la proportion des résultats selon l'avantage du terrain
# Function to retrieve general statistics for the season in terms of the proportion of results according to home advantage
def get_home_away_advantage():
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_home_away_advantage", params={}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les statistiques générales de la saison au niveau du classement à domicile / Function to retrieve overall statistics for the season in terms of home standings
def get_rank_home_season(season_name):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_rank_home_season", params={"season_name_input": season_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les statistiques générales de la saison au niveau du classement à l'extérieur / Function to retrieve overall statistics for the season in terms of away standings
def get_rank_away_season(season_name):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_rank_away_season", params={"season_name_input": season_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction du top 5 des meilleurs équipes à domicile / Function of the top 5 home teams
def get_top5_home_rank_competition(competition_name):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_top5_home_rank_competition", params={"competition_name_input": competition_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction du top 5 des meilleurs équipes à l'extérieur / Function of the top 5 away teams
def get_top5_away_rank_competition(competition_name):
    try:
        # Appel de la fonction RPC / Calling the RPC function
        response = supabase.rpc("get_top5_away_rank_competition", params={"competition_name_input": competition_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

### Création des fonctions permettant de récuperer les informations de la base de données liées à l'analyse d'une compétition
### Creation of functions to retrieve information from the database relating to the analysis of a competition

# Fonction pour récupérer les moyennes de buts par match, à domicile et à l'extérieur sur une compétition donnée
# Function to retrieve average goals per match, home and away, for a given competition
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
# Function for retrieving general competition statistics in terms of score frequency
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

# Fonction pour récupérer les statistiques sur le 1er but sur une compétition donnée / Function for retrieving statistics on the 1st goal in a given competition
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
# Function to retrieve general competition statistics in terms of goal distribution
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
# Function to retrieve general statistics for the competition in terms of the proportion of results according to home advantage
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

# Fonctions pour organiser ton code
def home():
    if lang == "Français":
        # Titre de la page
        st.markdown(
            "<h3 style='text-align: center;'>Projet de data visualisation sur les compétitions françaises de Romain Traboul</h3>", 
            unsafe_allow_html=True)

        st.image("image/logo_1.jpg") # Utilisation de la 1er bannière en image

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
                data=doc,
                file_name="Documentation_Data_Viz_France.pdf",
                mime="application/pdf"
            )
            st.markdown("</div>", unsafe_allow_html=True)

        # Utilisation du 2ème bouton pour télécharger le mémoire de M1
        with col2:
            st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
            st.download_button(
                label="Mon mémoire de M1",
                data=memoire,
                file_name="Mémoire_Romain_Traboul.pdf",
                mime="application/pdf"
            )
            st.markdown("</div>", unsafe_allow_html=True)

        # Utilisation du 3ème bouton pour télécharger le CV en français
        with col3:
            st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
            st.download_button(
                label="Mon CV en français",
                data=cv_data_fr,
                file_name="CV_FR_Romain_Traboul.pdf",
                mime="application/pdf"
            )
            st.markdown("</div>", unsafe_allow_html=True)

        # Utilisation du 4ème bouton pour télécharger le CV en anglais
        with col4:
            st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
            st.download_button(
                label="Mon CV en anglais",
                data=cv_data_eng,
                file_name="CV_ENG_Romain_Traboul.pdf",
                mime="application/pdf"
            )
            st.markdown("</div>", unsafe_allow_html=True)

    else:
        # Page title
        st.markdown(
            "<h3 style='text-align: center;'>Romain Traboul's data visualization project on French competitions</h3>", 
            unsafe_allow_html=True)

        st.image("image/logo_1.jpg") # Using the 1st image banner

        # Subtitle
        st.markdown(
            "<h4 style='text-align: center;'>Project presentation</h4>", 
            unsafe_allow_html=True)

        # Project description
        st.markdown(
            """
            <div style="text-align: justify;">
            The objective of this project is to build upon the work done during my first-year Master's dissertation: <strong>Comparative analysis of 3 performance factors in football: the impact of the first goal, the temporal distribution of goals, and the influence of home advantage on matches (home/away) among youth teams (U17N and U19N)</strong>.  
            Since this dissertation focused only on 3 competitions during the 2022/2023 season, it seemed important to extend the analysis by increasing the number of competitions and seasons considered.  
            Thus, the analysis will cover recent seasons from 2021/2022 to 2024/2025 (where available) and the following competitions: <strong>Ligue 1, Ligue 2, National 1, National 2, U19 National Championship, D1 Féminine, and D2 Féminine</strong>.
            </div>
            <br>
            Several features will be available within this web application: 
            <ul>
                <li><strong>📊 Team Analysis</strong>: Analyze the club of your choice through various statistics</li>
                <li><strong>🥊 Head-to-Head Analysis</strong>: Comparative analysis between two teams of your choice from the same season</li>
                <li><strong>📅 Season Analysis</strong>: Overview of trends across an entire season</li>
                <li><strong>🏆 Competition Analysis</strong>: Comparison of statistical indicators across competitions of your choice</li>
            </ul>
            <br>
            For more details about this project, you can refer to:  
            <ul>
                <li>The project documentation</li>
                <li><a href="https://github.com/Twiist33/Data_Viz_France">The source code used to create the application</a></li>
                <li>My Master's dissertation: Comparative analysis of 3 performance factors in football: the impact of the first goal, the temporal distribution of goals, and the influence of home advantage on matches (home/away) among youth teams (U17N and U19N), completed as part of my Master 1 in Digital Science and Sport in 2023 in Rennes</li>    
                <li>And finally, my resume (available in French and English).</li>
            </ul>
            """, unsafe_allow_html=True
        )


        # Use st.columns to display the 4 buttons side by side and centered
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

        # Use 1st button to download documentation
        with col1:
            st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
            st.download_button(
                label="Documentation",
                data=doc_eng,
                file_name="Documentation_Data_Viz_France_English.pdf",
                mime="application/pdf"
            )
            st.markdown("</div>", unsafe_allow_html=True)

        # Use 2nd button to download M1 dissertation
        with col2:
            st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
            st.download_button(
                label="My M1 dissertation",
                data=memoire,
                file_name="Mémoire_Romain_Traboul.pdf",
                mime="application/pdf"
            )
            st.markdown("</div>", unsafe_allow_html=True)

        # Use the 3rd button to download the French CV
        with col3:
            st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
            st.download_button(
                label="My CV in french",
                data=cv_data_fr,
                file_name="CV_FR_Romain_Traboul.pdf",
                mime="application/pdf"
            )
            st.markdown("</div>", unsafe_allow_html=True)

        # Use the 4th button to download the English CV
        with col4:
            st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
            st.download_button(
                label="My CV in english",
                data=cv_data_eng,
                file_name="CV_ENG_Romain_Traboul.pdf",
                mime="application/pdf"
            )
            st.markdown("</div>", unsafe_allow_html=True)

def team_analysis():
    if lang == "Français":

        st.title("📊 Analyse d'une Équipe") # Titre de l'application

        # Vérifie si l'utilisateur a fait un choix (équipe, saison et section)
        show_image = True  # Par défaut, on affiche l'image

        # Construction du chemin absolu
        image_path = os.path.join(os.path.dirname(__file__), "image", "banniere_equipe.jpg")

        st.sidebar.header("🔍 Sélection de l'équipe") # Sélection de la compétition en sidebar
        teams_available = get_teams()


        # Boucle pour selectionner l'équipe de son choix présent dans la base de données
        if teams_available:
            selected_team = st.sidebar.selectbox("Choisissez une équipe :", ["Sélectionnez une équipe"] + teams_available, index=0)
            
            if selected_team != "Sélectionnez une équipe":
                st.sidebar.header("🔍 Sélection de la saison") # Sélection de la saison en fonction de l'équipe choisie
                seasons_available = get_seasons(selected_team) # Récupération des données
                
                # Selection des saisons disponibles pour l'équipe de son choix (doit avoir au moins 5 matchs joué dans une saison pour être comptabilisé)
                if seasons_available:
                    selected_season = st.sidebar.selectbox("Choisissez une saison :", ["Sélectionnez une saison"] + seasons_available, index=0)
                    
                    # Selection de la section de notre choix
                    if selected_season != "Sélectionnez une saison":
                        st.sidebar.header("📊 Sélectionnez une analyse")
                        section = st.sidebar.radio("Sections", ["Statistiques générales", "1er but inscrit", "Distribution des buts", "Domicile / Extérieur", "Comparaison entre les saisons"])

                        # Si une section est sélectionnée, on cache l’image
                        if section:
                            show_image = False 

                        st.subheader(f"📌 {section} - {selected_team} - {selected_season}") # Récapitulatif des choix effectués

                        # Affichage des graphiques relatifs à la section Statistiques Générales            
                        if section == "Statistiques générales":

                            avg_goal_stats = get_avg_goals_stats(selected_season) # Récupération des statistiques de moyenne de but
                            if avg_goal_stats:
                                # Transformation des données en DataFrame avec les noms de colonnes
                                df_goals = pd.DataFrame([
                                    {
                                        "Saison": item["season_name"], "Équipe": item["team_name"], "Buts/Match": item["avg_goals_per_match"],
                                        "Buts inscrits/Match": item["avg_team_goals_per_match"], "Buts concédés/Match": item["avg_team_goals_conceded_per_match"],
                                        "Buts inscrits Domicile/Match": item["avg_team_home_goals"], "Buts inscrits Extérieur/Match": item["avg_team_away_goals"],
                                        "Buts concédés Domicile/Match": item["avg_conceded_home_goals"], "Buts concédés Extérieur/Match": item["avg_conceded_away_goals"]
                                    }
                                    for item in avg_goal_stats
                                ])
                                # Détermination de l'échelle maximale en fonction des plus hautes valeurs observées par catégorie
                                max_avg_goals = df_goals["Buts/Match"].max()
                                max_avg_goals_for = df_goals["Buts inscrits/Match"].max()
                                max_avg_goals_against = df_goals["Buts concédés/Match"].max()
                                max_home_goals_for = df_goals["Buts inscrits Domicile/Match"].max()
                                max_away_goals_for = df_goals["Buts inscrits Extérieur/Match"].max()
                                max_home_goals_against = df_goals["Buts concédés Domicile/Match"].max()
                                max_away_goals_against = df_goals["Buts concédés Extérieur/Match"].max()
                                
                                selected_data = df_goals[df_goals["Équipe"] == selected_team] # Récupération des valeurs de l'équipe souhaité pour la saison selectionné

                                if not selected_data.empty:

                                    # Mise en flottant des données
                                    avg_goals = float(selected_data["Buts/Match"].values[0])
                                    avg_goals_for = float(selected_data["Buts inscrits/Match"].values[0])
                                    avg_goals_against = float(selected_data["Buts concédés/Match"].values[0])
                                    avg_home_goals_for = float(selected_data["Buts inscrits Domicile/Match"].values[0])
                                    avg_away_goals_for = float(selected_data["Buts inscrits Extérieur/Match"].values[0])
                                    avg_home_goals_against = float(selected_data["Buts concédés Domicile/Match"].values[0])
                                    avg_away_goals_against = float(selected_data["Buts concédés Extérieur/Match"].values[0])

                                    # Conversion des valeurs max aussi (juste au cas où)
                                    max_avg_goals = float(max_avg_goals)
                                    max_avg_goals_for = float(max_avg_goals_for)
                                    max_avg_goals_against = float(max_avg_goals_against)
                                    max_home_goals_for = float(max_home_goals_for)
                                    max_away_goals_for = float(max_away_goals_for)
                                    max_home_goals_against = float(max_home_goals_against)
                                    max_away_goals_against = float(max_away_goals_against)


                                    # Fonction pour modifier la couleur de la jauge en fonction du taux de remplissage dans la catégorie spécifié
                                    def get_gauge_color(value, max_value, inverse=False):
                                        ratio = value / max_value
                                        if inverse:
                                            red = int(210 * ratio)  # Plus c'est haut, plus c'est rouge
                                            green = int(210 * (1 - ratio))
                                        else:
                                            red = int(210 * (1 - ratio))  # Plus c'est bas, plus c'est rouge
                                            green = int(210 * ratio)
                                        return f"rgb({red},{green},0)"

                                    st.subheader(f"Jauges générales sur les buts de {selected_team} pour la {selected_season}") # Titre des graphiques

                                    col1, col2, col3 = st.columns(3) # Première ligne de jauges

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
                                            value=avg_goals_for,
                                            title={"text": "Buts inscrits/Match"},
                                            gauge={
                                                "axis": {"range": [0, max_avg_goals_for]},
                                                "bar": {"color": get_gauge_color(avg_goals_for, max_avg_goals_for)}
                                            }
                                        ))
                                        st.plotly_chart(fig2)
                                    
                                    with col3:  # Inversion de la couleur
                                        fig3 = go.Figure(go.Indicator(
                                            mode="gauge+number",
                                            value=avg_goals_against,
                                            title={"text": "Buts concédés/Match"},
                                            gauge={
                                                "axis": {"range": [0, max_avg_goals_against]},
                                                "bar": {"color": get_gauge_color(avg_goals_against, max_avg_goals_against, inverse=True)}
                                            }
                                        ))
                                        st.plotly_chart(fig3)
                                                                
                                    st.subheader(f"Jauges spécifiques sur les buts inscrits de {selected_team} pour la {selected_season}") # Titre du graphique

                                    col4, col5 = st.columns(2) # Deuxième ligne de jauges

                                    with col4:
                                        fig4 = go.Figure(go.Indicator(
                                            mode="gauge+number",
                                            value=avg_home_goals_for,
                                            title={"text": "Buts inscrits Domicile/Match"},
                                            gauge={
                                                "axis": {"range": [0, max_home_goals_for]},
                                                "bar": {"color": get_gauge_color(avg_home_goals_for, max_home_goals_for)}
                                            }
                                        ))
                                        st.plotly_chart(fig4)

                                    with col5:  # Inversion de la couleur
                                        fig5 = go.Figure(go.Indicator(
                                            mode="gauge+number",
                                            value=avg_away_goals_for,
                                            title={"text": "Buts inscrits Extérieur/Match"},
                                            gauge={
                                                "axis": {"range": [0, max_away_goals_for]},
                                                "bar": {"color": get_gauge_color(avg_away_goals_for, max_away_goals_for)}
                                            }
                                        ))
                                        st.plotly_chart(fig5)

                                    st.subheader(f"Jauges spécifiques sur les buts concédés de {selected_team} pour la {selected_season}") # Titre du graphique

                                    col6, col7 = st.columns(2) # Troisième ligne de jauges

                                    with col6:  # Inversion de la couleur
                                        fig6 = go.Figure(go.Indicator(
                                            mode="gauge+number",
                                            value=avg_home_goals_against,
                                            title={"text": "Buts concédés Domicile/Match"},
                                            gauge={
                                                "axis": {"range": [0, max_home_goals_against]},
                                                "bar": {"color": get_gauge_color(avg_home_goals_against, max_home_goals_against, inverse=True)}
                                            }
                                        ))
                                        st.plotly_chart(fig6)

                                    with col7:  # Inversion de la couleur
                                        fig7 = go.Figure(go.Indicator(
                                            mode="gauge+number",
                                            value=avg_away_goals_against,
                                            title={"text": "Buts concédés Extérieur/Match"},
                                            gauge={
                                                "axis": {"range": [0, max_away_goals_against]},
                                                "bar": {"color": get_gauge_color(avg_away_goals_against, max_away_goals_against, inverse=True)}
                                            }
                                        ))
                                        st.plotly_chart(fig7)

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
                                # Arrondir et convertir les valeurs numériques
                                df[numeric_columns] = df[numeric_columns].apply(lambda col: col.apply(
                                    lambda x: int(x) if pd.notnull(x) and isinstance(x, (int, float)) and x == int(x) else (round(x, 2) if pd.notnull(x) else 0)
                                ))

                                # Trier par le nombre de buts inscrits
                                df = df.sort_values(by=["Nbr. buts inscrits"], ascending=False)
                                # Fonction pour colorer l'équipe sélectionnée / Function for colouring the selected team
                                def highlight_selected_squad(row):
                                    return ['background-color: lightcoral' if row["Équipe"] == selected_team else '' for _ in row]
                                # Appliquer le style de formatage et la coloration en une seule fois
                                styled_df = (
                                    df.style
                                    .format({col: format_value for col in numeric_columns})  # Format personnalisé
                                    .apply(highlight_selected_squad, axis=1)  # Coloration personnalisée
                                    .set_properties(**{"text-align": "center"})  # Centrage du texte
                                )
                                # Affichage du tableau
                                st.subheader(f"Tableau sur les buts inscrits pour la saison {selected_season}")
                                st.dataframe(styled_df)

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
                                
                                # Arrondir et convertir les valeurs numériques
                                df[numeric_columns] = df[numeric_columns].apply(lambda col: col.apply(
                                    lambda x: int(x) if pd.notnull(x) and isinstance(x, (int, float)) and x == int(x) else (round(x, 2) if pd.notnull(x) else 0)
                                ))
        
                                # Trier par le nombre de buts concédés
                                df = df.sort_values(by=["Nbr. buts concédés"], ascending=False)
                                # Fonction pour colorer l'équipe sélectionnée / Function for colouring the selected team
                                def highlight_selected_squad(row):
                                    return ['background-color: lightcoral' if row["Équipe"] == selected_team else '' for _ in row]
                                # Appliquer le style de formatage et la coloration en une seule fois
                                styled_df = (
                                    df.style
                                    .format({col: format_value for col in numeric_columns})  # Format personnalisé
                                    .apply(highlight_selected_squad, axis=1)  # Coloration personnalisée
                                    .set_properties(**{"text-align": "center"})  # Centrage du texte
                                )
                                
                                # Affichage du tableau
                                st.subheader(f"Tableau sur les buts concédés pour la saison {selected_season}")
                                st.dataframe(styled_df)

                            general_stats_data = get_frequent_score(selected_team, selected_season) # Passage au tableau des scores fréquents (récupération des données)
                            if general_stats_data:
                                # Transformation des données en DataFrame avec les noms de colonnes
                                df = pd.DataFrame([
                                    {
                                        "score_home": item["score_home"], "score_away": item["score_away"], "percentage": item["percentage"]
                                    }
                                    for item in general_stats_data
                                ])
                                df = df.groupby(["score_home", "score_away"], as_index=False).sum() # Agréger les données pour éviter les doublons (somme des fréquences)

                                pivot_table = df.pivot(index="score_home", columns="score_away", values="percentage").fillna(0) # Construction de la table pivot
                                pivot_table = pivot_table.apply(pd.to_numeric, errors='coerce').fillna(0) # Vérifier et convertir les valeurs en float

                                # Construction de la figure
                                fig, ax = plt.subplots(figsize=(10, 6))
                                sns.heatmap(pivot_table.astype(float), annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5, ax=ax)
                                ax.set_title(f"Répartition des scores pour {selected_team} pour la {selected_season} (%)")
                                ax.set_xlabel("Score extérieur")
                                ax.set_ylabel("Score domicile")

                                st.pyplot(fig) # On affiche la figure

                        # Affichage des graphiques relatifs à la section 1er but inscrit
                        elif section == "1er but inscrit":
                            first_goal = get_first_goal_season(selected_season) # On récupère les données
            
                            if first_goal:
                                # Transformation des données en DataFrame avec les noms de colonnes
                                first_goal_df = pd.DataFrame([
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
                                    for item in first_goal
                                ])
                                
                                for col in first_goal_df.columns:
                                    if col != "Équipe" and col != "Saison":  # Exclure la colonne "Équipe" et "Saison", contenant du texte
                                        first_goal_df[col] = pd.to_numeric(first_goal_df[col], errors='coerce') 
                                        first_goal_df[col] = first_goal_df[col].astype(float) # On transforme en flottant les valeurs numériques
                                
                                # On filtre les données selon l'équipe souhaité, et on se sépare ensuite des colonnes Saison et Équipe
                                first_goal_team = first_goal_df[first_goal_df["Équipe"] == selected_team].iloc[:, 2:]

                                graphs_to_plot = [
                                    (first_goal_team.iloc[0, :3], ["1er but inscrit", "Aucun but", "1er but encaissé"], f"Proportion du 1er but pour {selected_team} durant la {selected_season}"),
                                    (first_goal_team.iloc[0, 3:6], ["1er but inscrit", "Aucun but", "1er but encaissé"], "1er but à domicile"),
                                    (first_goal_team.iloc[0, 6:9], ["1er but inscrit", "Aucun but", "1er but encaissé"], "1er but à l'extérieur"),
                                    (first_goal_team.iloc[0, 9:12], ["Victoire", "Nul", "Défaite"], "Proportion des résultats après 1er but inscrit"),
                                    (first_goal_team.iloc[0, 12:15], ["Victoire", "Nul", "Défaite"], "Résultats à domicile après 1er but inscrit"),
                                    (first_goal_team.iloc[0, 15:18], ["Victoire", "Nul", "Défaite"], "Résultats à l'extérieur après 1er but inscrit"),
                                    (first_goal_team.iloc[0, 18:21], ["Victoire", "Nul", "Défaite"], "Proportion des résultats après 1er but encaissé"),
                                    (first_goal_team.iloc[0, 21:24], ["Victoire", "Nul", "Défaite"], "Résultats à domicile après 1er but encaissé"),
                                    (first_goal_team.iloc[0, 24:27], ["Victoire", "Nul", "Défaite"], "Résultats à l'extérieur après 1er but encaissé")
                                ]
                                
                                graphs_to_plot = [graph for graph in graphs_to_plot if graph[0].sum() > 0]
                                
                                num_graphs = len(graphs_to_plot)
                                num_rows = -(-num_graphs // 3)  # Équivalent à math.ceil(num_graphs / 3)
                                
                                if num_rows == 0:
                                    st.write("Aucune donnée disponible pour afficher les graphiques.")
                                else:
                                    fig, axes = plt.subplots(num_rows, 3, figsize=(18, 4 * num_rows))
                                    axes = np.atleast_2d(axes)  # Assurer une structure 2D
                                    
                                    for idx, (data, labels, title) in enumerate(graphs_to_plot):
                                        row, col = divmod(idx, 3)
                                        plot_pie_chart(axes[row, col], data, labels, title, ["#2ecc71", "#95a5a6", "#e74c3c"])
                                    
                                    for idx in range(num_graphs, num_rows * 3):
                                        row, col = divmod(idx, 3)
                                        axes[row, col].axis("off")
                                    
                                    plt.tight_layout()
                                    st.pyplot(fig)

                                # On passe au tableau du 1er but (inscrit ou concédé)
                                first_goal_df_season = first_goal_df.iloc[:, 1:]  # Supprime la colonne Saison
                                
                                # Définition des colonnes numériques à formater (excluant "Équipe" qui est textuel)
                                numeric_columns = [
                                    col for col in first_goal_df_season.columns if col != "Équipe"
                                ]
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
                                df_first_goal = first_goal_df_season[first_goal_columns]
                                df_first_goal_influence = first_goal_df_season[first_goal_influence_columns]
                                df_first_goal_conceded = first_goal_df_season[first_goal_conceded_columns]
                                
                                # Tri des tableaux
                                df_first_goal = df_first_goal.sort_values(by=["1er but inscrit"], ascending=False)
                                df_first_goal_influence = df_first_goal_influence.sort_values(by=["1er but inscrit / Victoire"], ascending=False)
                                df_first_goal_conceded = df_first_goal_conceded.sort_values(by=["1er but encaissé / Victoire"], ascending=False)
                                # Fonction pour colorer l'équipe sélectionnée / Function for colouring the selected team
                                def highlight_selected_squad(row):
                                    return ['background-color: lightcoral' if row["Équipe"] == selected_team else '' for _ in row]
                                # On ajuste les styles des 3 tableaux
                                style_df_first_goal = (
                                    df_first_goal.style
                                    .format({col: format_value for col in numeric_columns})  # Format personnalisé
                                    .apply(highlight_selected_squad, axis=1)  # Coloration personnalisée
                                    .set_properties(**{"text-align": "center"})  # Centrage du texte
                                )

                                style_df_first_goal_influence = (
                                    df_first_goal_influence.style
                                    .format({col: format_value for col in numeric_columns})  # Format personnalisé
                                    .apply(highlight_selected_squad, axis=1)  # Coloration personnalisée
                                    .set_properties(**{"text-align": "center"})  # Centrage du texte
                                )

                                style_df_first_goal_conceded = (
                                    df_first_goal_conceded.style
                                    .format({col: format_value for col in numeric_columns})  # Format personnalisé
                                    .apply(highlight_selected_squad, axis=1)  # Coloration personnalisée
                                    .set_properties(**{"text-align": "center"})  # Centrage du texte
                                )

                                # Affichage des tableaux avec formatage conditionnel
                                st.subheader(f"Tableau sur le 1er but (inscrit ou encaissé) pour la saison {selected_season} (en %)")
                                st.dataframe(style_df_first_goal)

                                st.subheader(f"Influence du 1er but inscrit pour la saison {selected_season} (en %)")
                                st.dataframe(style_df_first_goal_influence)

                                st.subheader(f"Influence du 1er but encaissé pour la saison {selected_season} (en %)")
                                st.dataframe(style_df_first_goal_conceded)

                        # Affichage des graphiques relatifs à la section Distribution des buts
                        elif section == "Distribution des buts":
                            distrib_goal_team = get_distribution_goals_season(selected_season) # On récupère nos données

                            if distrib_goal_team:
                                # Transformation des données en DataFrame avec les noms de colonnes
                                distrib_goal_team = pd.DataFrame([
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
                                    for item in distrib_goal_team
                                ])

                                distrib_goal_team  = distrib_goal_team.iloc[:, 1:]  # Suppression de la colonne "Saison"

                                for col in distrib_goal_team.columns:
                                    if col != "Équipe":  # Exclure la colonne "Équipe" qui contient du texte
                                        distrib_goal_team[col] = pd.to_numeric(distrib_goal_team[col], errors='coerce')
                                        distrib_goal_team[col] = distrib_goal_team[col].astype(float) # On transforme en flottant les valeurs numériques

                                # On crée un dataframe spécialement pour les graphiques et tableaux spécifiques à l'équipe sélectionné
                                distrib_goal_team_graph = distrib_goal_team[distrib_goal_team["Équipe"] == selected_team]
                                distrib_goal_team_graph = distrib_goal_team_graph.iloc[:, 1:]  # Suppression de la colonne "Équipe"
                                
                                fig, axes = plt.subplots(2, 2, figsize=(15, 10)) # Création de la figure et des axes
                                
                                # Proportions des buts inscrits par période
                                labels_proportion = ["1ère période", "2ème période"]
                                values_proportion_goal_scored = distrib_goal_team_graph.iloc[0, :2]
                                axes[0, 0].pie(values_proportion_goal_scored, labels=labels_proportion, autopct='%1.2f%%', startangle=90, colors=["lightblue", "lightcoral"])
                                axes[0, 0].set_title("Proportion des buts inscrits par période")
                                
                                # Proportions des buts concédés par période
                                values_proportion_goal_conceded = distrib_goal_team_graph.iloc[0, 8:10]
                                axes[0, 1].pie(values_proportion_goal_conceded, labels=labels_proportion, autopct='%1.2f%%', startangle=90, colors=["lightblue", "lightcoral"])
                                axes[0, 1].set_title("Proportion des buts concédés par période")
                                
                                # Proportions des buts inscrits par intervalle de 15 min
                                labels_intervals = ["0-15 min", "16-30 min", "31-45 min", "46-60 min", "61-75 min", "76-90 min"]
                                values_intervals_goal_scored = distrib_goal_team_graph.iloc[0, 2:8]
                                colors = ["#D4EFDF", "#A9DFBF", "#F9E79F", "#F5CBA7", "#E59866", "#DC7633"]
                                bars1 = axes[1, 0].bar(labels_intervals, values_intervals_goal_scored, color=colors)
                                axes[1, 0].set_title("Proportion des buts inscrits par intervalle de 15 min")
                                axes[1, 0].set_ylabel("%")
                                axes[1, 0].set_ylim(0, max(values_intervals_goal_scored) + 5)
                                
                                # Proportions des buts concédés par intervalle de 15 min
                                values_intervals_goal_conceded = distrib_goal_team_graph.iloc[0, 10:16]
                                bars2 = axes[1, 1].bar(labels_intervals, values_intervals_goal_conceded, color=colors)
                                axes[1, 1].set_title("Proportion des buts concédés par intervalle de 15 min")
                                axes[1, 1].set_ylabel("%")
                                axes[1, 1].set_ylim(0, max(values_intervals_goal_conceded) + 5)
                                
                                # Ajout des valeurs sur les barres
                                for bars in [bars1, bars2]:
                                    for bar in bars:
                                        yval = bar.get_height()
                                        axes[1, 0 if bars is bars1 else 1].text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval:.2f}%', ha='center', color='black')
                                
                                st.pyplot(fig) # Affichage de la figure

                                # On construit le tableau des distributions de buts sur la saison sélectionné en faisant une catégorisation des sous-ensembles de colonnes
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
                                df_distrib_goals_scored = distrib_goal_team[distrib_goals_scored_columns]
                                df_distrib_goals_conceded = distrib_goal_team[distrib_goals_conceded_columns]
                                
                                # Tri des tableaux
                                df_distrib_goals_scored = df_distrib_goals_scored.sort_values(by=["1ère période (Proportion Buts inscrits)"], ascending=False)
                                df_distrib_goals_conceded = df_distrib_goals_conceded.sort_values(by=["1ère période (Proportion Buts concédés)"], ascending=False)

                                # Appliquer des styles (coloration de l'équipe, format des chiffres, centrage du titre)
                                # Fonction pour colorer l'équipe sélectionnée / Function for colouring the selected team
                                def highlight_selected_squad(row):
                                    return ['background-color: lightcoral' if row["Équipe"] == selected_team else '' for _ in row]
                                style_df_distrib_goals_scored = (
                                    df_distrib_goals_scored.style
                                    .format({col: format_value for col in distrib_goals_scored_columns[1:]})  # Format personnalisé
                                    .apply(highlight_selected_squad, axis=1)  # Coloration personnalisée
                                    .set_properties(**{"text-align": "center"})  # Centrage du texte
                                )

                                style_df_distrib_goals_conceded = (
                                    df_distrib_goals_conceded.style
                                    .format({col: format_value for col in distrib_goals_conceded_columns[1:]})
                                    .apply(highlight_selected_squad, axis=1)  # Coloration personnalisée
                                    .set_properties(**{"text-align": "center"})  # Centrage du texte
                                )
                                # Affichage des tableaux avec formatage conditionnel
                                st.subheader(f"Tableau sur la distribution des buts inscrits pour la saison {selected_season}")
                                st.dataframe(style_df_distrib_goals_scored)

                                st.subheader(f"Tableau sur la distribution des buts concédés pour la saison {selected_season}")
                                st.dataframe(style_df_distrib_goals_conceded)

                        # Affichage des graphiques relatifs à la section Domicile / Extérieur 
                        elif section == "Domicile / Extérieur":
                            result_h_a = get_rank_season(selected_season) # Récupération des statistiques sur l'avantage du terrain

                            if result_h_a:
                                # Transformation des données en DataFrame avec les noms de colonnes
                                df_adv_home_away = pd.DataFrame([
                                    {
                                        "Type": item["type"], "Saison": item["season_name"], "Équipe": item["team_name"],"Matches joués": item["matches"],"Victoire": item["wins"],
                                        "Match Nul": item["draws"], "Défaite": item["losses"],"Points": item["points"], "Nbr de points moyen": item["avg_points"],
                                        "Avantage du Terrain": item["home_advantage"]
                                    }
                                    for item in result_h_a
                                ])
                                # Récupération des valeurs de la compétition sélectionnée
                                data_team = df_adv_home_away[df_adv_home_away["Équipe"] == selected_team]

                                if not data_team.empty:
                                    # Sélectionner uniquement les colonnes nécessaires et extraire les proportions en pourcentage
                                    data_team_home = data_team[data_team["Type"] == "Home"]
                                    total_home = data_team_home[["Victoire", "Match Nul", "Défaite"]].sum(axis=1).values[0]
                                    values_proportion_home = (data_team_home[["Victoire", "Match Nul", "Défaite"]].values.flatten() / total_home) * 100  

                                    data_team_away = data_team[data_team["Type"] == "Away"]
                                    total_away = data_team_away[["Victoire", "Match Nul", "Défaite"]].sum(axis=1).values[0]
                                    values_proportion_away = (data_team_away[["Victoire", "Match Nul", "Défaite"]].values.flatten() / total_away) * 100  

                                    # Détermination des valeurs maximales pour l'échelle des jauges
                                    max_adv_home = data_team_home["Avantage du Terrain"].max()
                                    max_adv_away = max_adv_home
                                    max_adv_home = float(max_adv_home)
                                    max_adv_away = float(max_adv_away)

                                    # Extraction et mise à l'échelle de l'avantage du terrain
                                    adv_home = float(data_team_home["Avantage du Terrain"].values[0])
                                    adv_away = float(data_team_away["Avantage du Terrain"].values[0])

                                    # Labels pour les diagrammes
                                    labels_proportion_home = ["Victoire à domicile", "Match Nul", "Défaite à domicile"]
                                    labels_proportion_away = ["Victoire à l'extérieur", "Match Nul", "Défaite à l'extérieur"]

                                    # Fonction pour la jauge de couleur
                                    def get_gauge_color(value, max_value, inverse=False):
                                        if max_value <= 0:
                                            raise ValueError("max_value doit être supérieur à 0")

                                        ratio = value / max_value
                                        if inverse:
                                            red = min(max(int(210 * ratio), 0), 255)  # Limiter à 0-255
                                            green = min(max(int(210 * (1 - ratio)), 0), 255)  # Limiter à 0-255
                                        else:
                                            red = min(max(int(210 * (1 - ratio)), 0), 255)  # Limiter à 0-255
                                            green = min(max(int(210 * ratio), 0), 255)  # Limiter à 0-255

                                        return f"rgb({red},{green},0)"

                                    col1, col2 = st.columns(2)  # Création des colonnes Streamlit à Domicile

                                    # Création du diagramme circulaire à domicile
                                    with col1:
                                        fig1, ax1 = plt.subplots(figsize=(7, 7))  
                                        plot_pie_chart(ax1, values_proportion_home, labels_proportion_home, "Proportion des résultats à Domicile", ["#2ecc71", "#95a5a6", "#e74c3c"])
                                        st.pyplot(fig1)  

                                    # Création de la jauge à domicile
                                    with col2:
                                        fig2 = go.Figure(go.Indicator(
                                            mode="gauge+number",
                                            value=adv_home,  
                                            title={"text": "Avantage du terrain à Domicile (en %)"},
                                            gauge={
                                                "axis": {"range": [0, max_adv_home]},
                                                "bar": {"color": get_gauge_color(adv_home, max_adv_home)}
                                            }
                                        ))
                                        st.plotly_chart(fig2)

                                    col3, col4 = st.columns(2)  # Création des colonnes Streamlit à l'Extérieur

                                    # Création du diagramme circulaire à l'extérieur
                                    with col3:
                                        fig3, ax3 = plt.subplots(figsize=(7, 7))  
                                        plot_pie_chart(ax3, values_proportion_away, labels_proportion_away, "Proportion des résultats à l'Extérieur", ["#2ecc71", "#95a5a6", "#e74c3c"])
                                        st.pyplot(fig3)  

                                    # Création de la jauge à l'extérieur
                                    with col4:
                                        fig4 = go.Figure(go.Indicator(
                                            mode="gauge+number",
                                            value=adv_away,  
                                            title={"text": "Avantage du terrain à l'Extérieur (en %)"},
                                            gauge={
                                                "axis": {"range": [0, max_adv_away]},
                                                "bar": {"color": get_gauge_color(adv_away, max_adv_away, inverse=True)}
                                            }
                                        ))
                                        st.plotly_chart(fig4)

                                # Classement à domicile
                                rank_home_data = df_adv_home_away[df_adv_home_away["Type"] == "Home"].copy()  # Copie explicite
                                if not rank_home_data.empty:
                                    for col in rank_home_data.columns:
                                        if col not in ["Équipe", "Saison", "Type"]:
                                            rank_home_data.loc[:, col] = pd.to_numeric(rank_home_data[col], errors='coerce')  # Assignation sécurisée

                                    rank_home_data = rank_home_data.drop(columns=["Saison", "Type"])
                                    rank_home_data = rank_home_data.sort_values(by=["Points"], ascending=False)
                                    # Fonction pour colorer l'équipe sélectionnée / Function for colouring the selected team
                                    def highlight_selected_squad(row):
                                        return ['background-color: lightcoral' if row["Équipe"] == selected_team else '' for _ in row]
                                    style_rank_home_data = (
                                        rank_home_data.style
                                        .format({col: format_value for col in rank_home_data.columns[1:]})
                                        .apply(highlight_selected_squad, axis=1)
                                        .set_properties(**{"text-align": "center"})
                                    )
                                    
                                    st.subheader(f"Classement à domicile pour la saison de {selected_season}")
                                    st.dataframe(style_rank_home_data)

                                # Classement à l'extérieur
                                rank_away_data = df_adv_home_away[df_adv_home_away["Type"] == "Away"].copy()  # Copie explicite
                                if not rank_away_data.empty:
                                    for col in rank_away_data.columns:
                                        if col not in ["Équipe", "Saison", "Type"]:
                                            rank_away_data.loc[:, col] = pd.to_numeric(rank_away_data[col], errors='coerce')  # Assignation sécurisée
                                    
                                    rank_away_data = rank_away_data.drop(columns=["Saison", "Type"])
                                    rank_away_data = rank_away_data.sort_values(by=["Points"], ascending=False)
                                    # Fonction pour colorer l'équipe sélectionnée / Function for colouring the selected team
                                    def highlight_selected_squad(row):
                                        return ['background-color: lightcoral' if row["Équipe"] == selected_team else '' for _ in row]
                                    style_rank_away_data = (
                                        rank_away_data.style
                                        .format({col: format_value for col in rank_away_data.columns[1:]})  # Correction ici aussi
                                        .apply(highlight_selected_squad, axis=1)
                                        .set_properties(**{"text-align": "center"})
                                    )
                                    
                                    st.subheader(f"Classement à l'extérieur pour la saison de {selected_season}")
                                    st.dataframe(style_rank_away_data)

                        elif section == "Comparaison entre les saisons":
                            with st.spinner("Chargement des données..."):
                                # Initialisation des variables de comparaison
                                compare_goals_season_team_data = []
                                compare_first_goal_team_data = []
                                compare_distrib_goal_data = []
                                compare_home_away_data = []

                                # Création d'une boucle for pour récupérer la liste des saisons disponibles pour la compétition choisit par l'utilisateur
                                for season in seasons_available:
                                    # On récupère les données
                                    goals_season_team_stats = get_avg_goals_stats(season)
                                    first_goal_season_stats = get_first_goal_season(season)
                                    distrib_stats = get_distribution_goals_season(season)
                                    home_away_stats = get_rank_season(season)

                                    # Si les données ne sont pas vides, on ajoute cela pour chaque saison disponible, en récupérant les informations associées
                                    if goals_season_team_stats:
                                        compare_goals_season_team_data.extend(goals_season_team_stats)

                                    if first_goal_season_stats:
                                        compare_first_goal_team_data.extend(first_goal_season_stats)
                                    
                                    if distrib_stats:
                                        compare_distrib_goal_data.extend(distrib_stats)    

                                    if home_away_stats:
                                        compare_home_away_data.extend(home_away_stats)            

                                if compare_goals_season_team_data:
                                    # Transformation des données en DataFrame avec les noms de colonnes
                                    df = pd.DataFrame([
                                        {
                                            "Saison": item["season_name"], "Équipe": item["team_name"], "Buts/Match": item["avg_goals_per_match"],
                                            "Buts inscrits/Match": item["avg_team_goals_per_match"], "Buts concédés/Match": item["avg_team_goals_conceded_per_match"],
                                            "Buts inscrits Domicile/Match": item["avg_team_home_goals"], "Buts inscrits Extérieur/Match": item["avg_team_away_goals"],
                                            "Buts concédés Domicile/Match": item["avg_conceded_home_goals"], "Buts concédés Extérieur/Match": item["avg_conceded_away_goals"]
                                        }
                                        for item in compare_goals_season_team_data
                                    ])
                                    df = df[df["Équipe"] == selected_team] # Récupération des valeurs de l'équipe sélectionnée

                                    df = df.drop(columns=["Équipe"]) # On enlève la colonne Équipe du tableau que l'on va afficher

                                    numeric_columns = df.columns[1:]  # Sélectionne les colonnes numériques
                                    # Arrondir et convertir les valeurs numériques
                                    df[numeric_columns] = df[numeric_columns].apply(lambda col: col.apply(lambda x: float(round(x, 2)) if pd.notnull(x) else 0.0))

                                    df = df.sort_values(by=numeric_columns.tolist(), ascending=False) # Trier le tableau
                                    # Fonction pour colorer la saison sélectionnée / Function for colouring the selected season
                                    def highlight_selected_season(row):
                                        return ['background-color: lightcoral' if row["Saison"] == selected_season else '' for _ in row]
                                    # Appliquer le style de formatage et la coloration en une seule fois
                                    styled_df = (
                                        df.style
                                        .format({col: format_value for col in numeric_columns})  # Format personnalisé
                                        .apply(highlight_selected_season, axis=1)  # Coloration personnalisée
                                        .set_properties(**{"text-align": "center"})  # Centrage du texte
                                    )
                                    # Affichage du tableau
                                    st.subheader("⚽ Informations sur les statistiques générales de buts (en moyenne)")
                                    st.dataframe(styled_df)

                                if compare_first_goal_team_data:
                                    # Transformation des données en DataFrame avec les noms de colonnes
                                    first_goal_season_data = pd.DataFrame([
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
                                        for item in compare_first_goal_team_data
                                    ])
                                    first_goal_season_data = first_goal_season_data[first_goal_season_data["Équipe"] == selected_team] # Récupération des valeurs de l'équipe sélectionnée

                                    for col in first_goal_season_data.columns:
                                        if col != "Équipe" and col != "Saison":  # Exclure la colonne "Équipe" qui contient du texte
                                            first_goal_season_data[col] = pd.to_numeric(first_goal_season_data[col], errors='coerce')

                                    first_goal_season_data = first_goal_season_data.drop(columns=["Équipe"]) # Suppression de la colonne Équipe

                                    first_goal_season_data = first_goal_season_data.sort_values(by=["1er but inscrit"], ascending=False) # Tri des tableaux

                                    numeric_columns = first_goal_season_data.columns[1:]  # Exclure "Saison"
                                        
                                    first_goal_season_data[numeric_columns] = first_goal_season_data[numeric_columns].astype(float) # Convertir en float
                                    # Fonction pour colorer la saison sélectionnée / Function for colouring the selected season
                                    def highlight_selected_season(row):
                                        return ['background-color: lightcoral' if row["Saison"] == selected_season else '' for _ in row]
                                    # On applique le style
                                    style_first_goal_season_data = (
                                        first_goal_season_data.style
                                        .format({col: format_value for col in numeric_columns})  # Format personnalisé
                                        .apply(highlight_selected_season, axis=1)  # Coloration personnalisée
                                        .set_properties(**{"text-align": "center"})  # Centrage du texte
                                    )
                                    # Affichage des tableaux avec formatage conditionnel
                                    st.subheader(f"⚽ Tableau sur le 1er but inscrit pour {selected_team} (en %)")
                                    st.dataframe(style_first_goal_season_data)

                                if compare_distrib_goal_data:
                                    distrib_goal_data = pd.DataFrame([
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
                                        for item in compare_distrib_goal_data
                                    ])
                                    
                                    distrib_goal_data = distrib_goal_data[distrib_goal_data["Équipe"] == selected_team] # Récupération des valeurs de l'équipe sélectionnée

                                    distrib_goal_data = distrib_goal_data.drop(columns=["Équipe"]) # On enlève la colonne Équipe

                                    numeric_columns = distrib_goal_data.columns[1:] # On traite les données numériques
                                    distrib_goal_data[numeric_columns] = distrib_goal_data[numeric_columns].astype(float).round(2)  # Arrondi à 2 décimales

                                    distrib_goal_data = distrib_goal_data.sort_values(by=numeric_columns.tolist(), ascending=False) # Assurer un tri numérique et non alphabétique
                                    # Fonction pour colorer la saison sélectionnée / Function for colouring the selected season
                                    def highlight_selected_season(row):
                                        return ['background-color: lightcoral' if row["Saison"] == selected_season else '' for _ in row]                                   
                                    # On applique le style
                                    styled_distrib_goal_data = (
                                        distrib_goal_data.style
                                        .format({col: format_value for col in numeric_columns})  # Format personnalisé
                                        .apply(highlight_selected_season, axis=1)  # Coloration personnalisée pour la saison sélectionné
                                        .set_properties(**{"text-align": "center"})  # Centrage du texte
                                    )

                                    # Affichage du tableau mis en forme avec tri
                                    st.subheader("⚽ Informations sur la distribution des buts par saison (en %)")
                                    st.dataframe(styled_distrib_goal_data)

                                if compare_home_away_data:
                                    # Transformation des données en DataFrame avec les noms de colonnes
                                    df_adv_home_away_complete = pd.DataFrame([
                                        {
                                            "Type": item["type"], "Saison": item["season_name"], "Équipe": item["team_name"], "Matches joués": item["matches"],
                                            "Victoire (en %)": item["wins"], "Match Nul (en %)": item["draws"], "Défaite (en %)": item["losses"],
                                            "Points": item["points"], "Nbr de points moyen": item["avg_points"], "Avantage du Terrain": item["home_advantage"]
                                        }
                                        for item in compare_home_away_data
                                    ])

                                    # Copie explicite pour éviter les warnings
                                    df_adv_home_away_team = df_adv_home_away_complete[df_adv_home_away_complete["Équipe"] == selected_team].copy()

                                    # Convertir les colonnes numériques en float et arrondir à 2 décimales
                                    numeric_columns = [col for col in df_adv_home_away_team.columns if col not in ["Équipe", "Saison", "Type"]]
                                    df_adv_home_away_team[numeric_columns] = df_adv_home_away_team[numeric_columns].astype(float).apply(
                                        lambda col: col.round(2).fillna(0)
                                    )

                                    # Récupération des valeurs selon le facteur Domicile/Extérieur avec copie explicite
                                    data_home = df_adv_home_away_team[df_adv_home_away_team["Type"] == "Home"].copy()
                                    data_away = df_adv_home_away_team[df_adv_home_away_team["Type"] == "Away"].copy()

                                    # Retrait des colonnes inutiles
                                    data_home = data_home.drop(columns=["Équipe", "Type"])
                                    data_away = data_away.drop(columns=["Équipe", "Type"])

                                    if not data_home.empty:
                                        # Calcul des pourcentages en évitant la division par 0
                                        for col in ["Victoire (en %)", "Match Nul (en %)", "Défaite (en %)"]:
                                            data_home[col] = (data_home[col] / data_home["Matches joués"].replace(0, np.nan)) * 100
                                            data_home[col] = data_home[col].round(2).fillna(0)
                                        # Fonction pour colorer la saison sélectionnée / Function for colouring the selected season
                                        def highlight_selected_season(row):
                                            return ['background-color: lightcoral' if row["Saison"] == selected_season else '' for _ in row]
                                        data_home = data_home.sort_values(by=["Points"], ascending=False)
                                        style_data_home = (
                                            data_home.style
                                            .format({col: format_value for col in data_home.columns[1:]})  # Format des nombres
                                            .apply(highlight_selected_season, axis=1)
                                            .set_properties(**{"text-align": "center"})
                                        )
                                        st.subheader(f"⚽ Informations sur les performances à domicile de {selected_team} (toutes saisons)")
                                        st.dataframe(style_data_home)

                                    if not data_away.empty:
                                        # Calcul des pourcentages en évitant la division par 0
                                        for col in ["Victoire (en %)", "Match Nul (en %)", "Défaite (en %)"]:
                                            data_away[col] = (data_away[col] / data_away["Matches joués"].replace(0, np.nan)) * 100
                                            data_away[col] = data_away[col].round(2).fillna(0)
                                        # Fonction pour colorer la saison sélectionnée / Function for colouring the selected season
                                        def highlight_selected_season(row):
                                            return ['background-color: lightcoral' if row["Saison"] == selected_season else '' for _ in row]
                                        data_away = data_away.sort_values(by=["Points"], ascending=False)
                                        style_data_away = (
                                            data_away.style
                                            .format({col: format_value for col in data_away.columns[1:]})  # Format des nombres
                                            .apply(highlight_selected_season, axis=1)
                                            .set_properties(**{"text-align": "center"})
                                        )
                                        st.subheader(f"⚽ Informations sur les performances à l'extérieur de {selected_team} (toutes saisons)")
                                        st.dataframe(style_data_away)

        # Affichage de l’image uniquement si aucun choix n'a été fait
        if show_image:
            st.image(image_path)

    else:
        st.title("📊 Team Analysis") # Page title

        # Checks whether the user has made a choice (team, season and section)
        show_image = True  # By default, we display the image

        # Build the path of image
        image_path = os.path.join(os.path.dirname(__file__), "image", "banniere_equipe.jpg")

        st.sidebar.header("🔍 Team selection") # Selection of the competition in the sidebar
        teams_available = get_teams()


        # Loop to select the team of your choice in the database
        if teams_available:
            selected_team = st.sidebar.selectbox("Choose a team :", ["Select a team"] + teams_available, index=0)
            
            if selected_team != "Select a team":
                st.sidebar.header("🔍 Team selection") # Selection of the season in fonction of the team chosen
                seasons_available = get_seasons(selected_team) # Recover the data
                
                # Selection of available seasons for the team of your choice (must have played at least 5 matches in a season to be counted)
                if seasons_available:
                    selected_season = st.sidebar.selectbox("Choose a season :", ["Select a season"] + seasons_available, index=0)
                    
                    # Selection of the section of our choice
                    if selected_season != "Select a season":
                        st.sidebar.header("📊 Select a analysys")
                        section = st.sidebar.radio("Sections", ["General statistics", "1st goal scored", "Goal distribution", "Home / Away", "Season comparison"])
                        # If the section is selected, we hide the image
                        if section:
                            show_image = False 

                        st.subheader(f"📌 {section} - {selected_team} - {selected_season}") # Summary of choices made

                        # Display of graphs relating to the General Statistics section            
                        if section == "General statistics":

                            avg_goal_stats = get_avg_goals_stats(selected_season) # Retrieving goal average statistics
                            if avg_goal_stats:
                                # Data transformation into DataFrame with column names
                                df_goals = pd.DataFrame([
                                    {
                                        "Season": item["season_name"], "Team": item["team_name"], "Goals/Match": item["avg_goals_per_match"],
                                        "Goals scored/Match": item["avg_team_goals_per_match"], "Goals conceded/Match": item["avg_team_goals_conceded_per_match"],
                                        "Goals scored Home/Match": item["avg_team_home_goals"], "Goals scored Away/Match": item["avg_team_away_goals"],
                                        "Goals conceded Home/Match": item["avg_conceded_home_goals"], "Goals conceded Away/Match": item["avg_conceded_away_goals"]
                                    }
                                    for item in avg_goal_stats
                                ])
                                # Determination of the maximum scale based on the highest values observed per category
                                max_avg_goals = df_goals["Goals/Match"].max()
                                max_avg_goals_for = df_goals["Goals scored/Match"].max()
                                max_avg_goals_against = df_goals["Goals conceded/Match"].max()
                                max_home_goals_for = df_goals["Goals scored Home/Match"].max()
                                max_away_goals_for = df_goals["Goals scored Away/Match"].max()
                                max_home_goals_against = df_goals["Goals conceded Home/Match"].max()
                                max_away_goals_against = df_goals["Goals conceded Away/Match"].max()
                                
                                selected_data = df_goals[df_goals["Team"] == selected_team] # Recovery of the team values desired for the selected season

                                if not selected_data.empty:

                                    # Floating data
                                    avg_goals = float(selected_data["Goals/Match"].values[0])
                                    avg_goals_for = float(selected_data["Goals scored/Match"].values[0])
                                    avg_goals_against = float(selected_data["Goals conceded/Match"].values[0])
                                    avg_home_goals_for = float(selected_data["Goals scored Home/Match"].values[0])
                                    avg_away_goals_for = float(selected_data["Goals scored Away/Match"].values[0])
                                    avg_home_goals_against = float(selected_data["Goals conceded Home/Match"].values[0])
                                    avg_away_goals_against = float(selected_data["Goals conceded Away/Match"].values[0])

                                    # Conversion of max values also
                                    max_avg_goals = float(max_avg_goals)
                                    max_avg_goals_for = float(max_avg_goals_for)
                                    max_avg_goals_against = float(max_avg_goals_against)
                                    max_home_goals_for = float(max_home_goals_for)
                                    max_away_goals_for = float(max_away_goals_for)
                                    max_home_goals_against = float(max_home_goals_against)
                                    max_away_goals_against = float(max_away_goals_against)

                                    # Function to change the color of the gauge according to the fill rate in the specified category
                                    def get_gauge_color(value, max_value, inverse=False):
                                        ratio = value / max_value
                                        if inverse:
                                            red = int(210 * ratio)  # The higher it is, the more red
                                            green = int(210 * (1 - ratio))
                                        else:
                                            red = int(210 * (1 - ratio))  # The lower it is, the more red
                                            green = int(210 * ratio)
                                        return f"rgb({red},{green},0)"

                                    st.subheader(f"{selected_team} goal gauges for the {selected_season}") # Charts title

                                    col1, col2, col3 = st.columns(3) # First line of gauge

                                    with col1:
                                        fig1 = go.Figure(go.Indicator(
                                            mode="gauge+number",
                                            value=avg_goals,
                                            title={"text": "Goals/Match"},
                                            gauge={
                                                "axis": {"range": [0, max_avg_goals]},
                                                "bar": {"color": get_gauge_color(avg_goals, max_avg_goals)}
                                            }
                                        ))
                                        st.plotly_chart(fig1)

                                    with col2:
                                        fig2 = go.Figure(go.Indicator(
                                            mode="gauge+number",
                                            value=avg_goals_for,
                                            title={"text": "Goals scored/Match"},
                                            gauge={
                                                "axis": {"range": [0, max_avg_goals_for]},
                                                "bar": {"color": get_gauge_color(avg_goals_for, max_avg_goals_for)}
                                            }
                                        ))
                                        st.plotly_chart(fig2)
                                    
                                    with col3:  # Inverting the color
                                        fig3 = go.Figure(go.Indicator(
                                            mode="gauge+number",
                                            value=avg_goals_against,
                                            title={"text": "Goals conceded/Match"},
                                            gauge={
                                                "axis": {"range": [0, max_avg_goals_against]},
                                                "bar": {"color": get_gauge_color(avg_goals_against, max_avg_goals_against, inverse=True)}
                                            }
                                        ))
                                        st.plotly_chart(fig3)
                                                                
                                    st.subheader(f"{selected_team} goals scored specific gauges for the {selected_season}") # Chart title

                                    col4, col5 = st.columns(2) # 2nd line of gauge

                                    with col4:
                                        fig4 = go.Figure(go.Indicator(
                                            mode="gauge+number",
                                            value=avg_home_goals_for,
                                            title={"text": "Goals scored Home/Match"},
                                            gauge={
                                                "axis": {"range": [0, max_home_goals_for]},
                                                "bar": {"color": get_gauge_color(avg_home_goals_for, max_home_goals_for)}
                                            }
                                        ))
                                        st.plotly_chart(fig4)

                                    with col5:  # Inverting the color
                                        fig5 = go.Figure(go.Indicator(
                                            mode="gauge+number",
                                            value=avg_away_goals_for,
                                            title={"text": "Goals scored Away/Match"},
                                            gauge={
                                                "axis": {"range": [0, max_away_goals_for]},
                                                "bar": {"color": get_gauge_color(avg_away_goals_for, max_away_goals_for)}
                                            }
                                        ))
                                        st.plotly_chart(fig5)

                                    st.subheader(f"{selected_team} goals conceded specific gauges for the {selected_season}") # Titre du graphique

                                    col6, col7 = st.columns(2) # Third line of gauge

                                    with col6:  # Inverting the color
                                        fig6 = go.Figure(go.Indicator(
                                            mode="gauge+number",
                                            value=avg_home_goals_against,
                                            title={"text": "Goals conceded Home/Match"},
                                            gauge={
                                                "axis": {"range": [0, max_home_goals_against]},
                                                "bar": {"color": get_gauge_color(avg_home_goals_against, max_home_goals_against, inverse=True)}
                                            }
                                        ))
                                        st.plotly_chart(fig6)

                                    with col7:  # Inverting the color
                                        fig7 = go.Figure(go.Indicator(
                                            mode="gauge+number",
                                            value=avg_away_goals_against,
                                            title={"text": "Goals conceded Away/Match"},
                                            gauge={
                                                "axis": {"range": [0, max_away_goals_against]},
                                                "bar": {"color": get_gauge_color(avg_away_goals_against, max_away_goals_against, inverse=True)}
                                            }
                                        ))
                                        st.plotly_chart(fig7)

                            compare_goals_scored_data = get_goals_scored(selected_season) # We build the table on goals scored starting with retrieving data

                            if compare_goals_scored_data:
                                # Transform the data into a DataFrame with column names
                                df = pd.DataFrame([
                                    {
                                        "Team": item["team_name"], 
                                        "Total Goals Scored": item["total_goals_scored"], 
                                        "Avg. Goals Scored": item["avg_goals_scored"],
                                        "Home Goals Scored": item["goals_scored_home"], 
                                        "Avg. Home Goals Scored": item["avg_goals_scored_home"],
                                        "Away Goals Scored": item["goals_scored_away"], 
                                        "Avg. Away Goals Scored": item["avg_goals_scored_away"]
                                    }
                                    for item in compare_goals_scored_data
                                ])
                                
                                numeric_columns = df.columns[1:]  # Select numeric columns
                                # Round and convert numeric values
                                df[numeric_columns] = df[numeric_columns].apply(lambda col: col.apply(
                                    lambda x: int(x) if pd.notnull(x) and isinstance(x, (int, float)) and x == int(x) else (round(x, 2) if pd.notnull(x) else 0)
                                ))

                                # Sort by the total goals scored
                                df = df.sort_values(by=["Total Goals Scored"], ascending=False)
                                
                                # Function for highlighting the selected team
                                def highlight_selected_squad(row):
                                    return ['background-color: lightcoral' if row["Team"] == selected_team else '' for _ in row]
                                
                                # Apply formatting style and highlighting at once
                                styled_df = (
                                    df.style
                                    .format({col: format_value for col in numeric_columns})  # Custom formatting
                                    .apply(highlight_selected_squad, axis=1)  # Custom highlighting
                                    .set_properties(**{"text-align": "center"})  # Center text
                                )
                                
                                # Display the table
                                st.subheader(f"Goals scored table for the {selected_season} season")
                                st.dataframe(styled_df)

                            compare_goals_conceded_data = get_goals_conceded(selected_season)  # Build the goals conceded table by first fetching the data

                            if compare_goals_conceded_data:
                                # Transform the data into a DataFrame with column names
                                df = pd.DataFrame([
                                    {
                                        "Team": item["team_name"], "Total Goals Conceded": item["total_goals_conceded"], "Avg. Goals Conceded": item["avg_goals_conceded"],
                                        "Home Goals Conceded": item["goals_conceded_home"], "Avg. Home Goals Conceded": item["avg_goals_conceded_home"],
                                        "Away Goals Conceded": item["goals_conceded_away"], "Avg. Away Goals Conceded": item["avg_goals_conceded_away"]
                                    }
                                    for item in compare_goals_conceded_data
                                ])
                                
                                numeric_columns = df.columns[1:]  # Select numeric columns
                                
                                # Round and convert numeric values
                                df[numeric_columns] = df[numeric_columns].apply(lambda col: col.apply(
                                    lambda x: int(x) if pd.notnull(x) and isinstance(x, (int, float)) and x == int(x) else (round(x, 2) if pd.notnull(x) else 0)
                                ))

                                # Sort by the total goals conceded
                                df = df.sort_values(by=["Total Goals Conceded"], ascending=False)
                                
                                # Function for highlighting the selected team
                                def highlight_selected_squad(row):
                                    return ['background-color: lightcoral' if row["Team"] == selected_team else '' for _ in row]
                                
                                # Apply formatting style and highlighting at once
                                styled_df = (
                                    df.style
                                    .format({col: format_value for col in numeric_columns})  # Custom formatting
                                    .apply(highlight_selected_squad, axis=1)  # Custom highlighting
                                    .set_properties(**{"text-align": "center"})  # Center text
                                )
                                
                                # Display the table
                                st.subheader(f"Goals conceded table for the {selected_season} season")
                                st.dataframe(styled_df)

                            general_stats_data = get_frequent_score(selected_team, selected_season)  # Move to the frequent scores table (fetch the data)

                            if general_stats_data:
                                # Transform the data into a DataFrame with column names
                                df = pd.DataFrame([
                                    {
                                        "score_home": item["score_home"], 
                                        "score_away": item["score_away"], 
                                        "percentage": item["percentage"]
                                    }
                                    for item in general_stats_data
                                ])
                                
                                df = df.groupby(["score_home", "score_away"], as_index=False).sum()  # Aggregate data to avoid duplicates (sum of frequencies)

                                pivot_table = df.pivot(index="score_home", columns="score_away", values="percentage").fillna(0)  # Build the pivot table
                                pivot_table = pivot_table.apply(pd.to_numeric, errors='coerce').fillna(0)  # Verify and convert values to float

                                # Build the figure
                                fig, ax = plt.subplots(figsize=(10, 6))
                                sns.heatmap(pivot_table.astype(float), annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5, ax=ax)
                                ax.set_title(f"Score distribution for {selected_team} in the {selected_season} season (%)")
                                ax.set_xlabel("Away score")
                                ax.set_ylabel("Home score")

                                st.pyplot(fig)  # Display the figure

                        # Display graphs related to the "First Goal Scored" section
                        elif section == "1st goal scored":
                            first_goal = get_first_goal_season(selected_season)  # Fetch the data
                            
                            if first_goal:
                                # Transform the data into a DataFrame with column names
                                first_goal_df = pd.DataFrame([
                                    {
                                        "Season": item["season_name"], "Team": item["team_name"],
                                        "First Goal Scored": item["proportion_1st_goal_for"], "No Goal": item["proportion_no_goal"], "First Goal Conceded": item["proportion_1st_goal_against"],
                                        "Home / First Goal Scored": item["proportion_1st_goal_home_for"], "Home / No Goal": item["proportion_no_goal_home"], "Home / First Goal Conceded": item["proportion_1st_goal_home_against"],
                                        "Away / First Goal Scored": item["proportion_1st_goal_away_for"], "Away / No Goal": item["proportion_no_goal_away"], "Away / First Goal Conceded": item["proportion_1st_goal_away_against"],
                                        "First Goal Scored / Win": item["first_goal_win"], "First Goal Scored / Draw": item["first_goal_draw"], "First Goal Scored / Loss": item["first_goal_lose"],
                                        "Home / First Goal Scored / Win": item["proportion_1st_goal_home_win"], "Home / First Goal Scored / Draw": item["proportion_1st_goal_home_draw"], "Home / First Goal Scored / Loss": item["proportion_1st_goal_home_lose"],
                                        "Away / First Goal Scored / Win": item["proportion_1st_goal_away_win"], "Away / First Goal Scored / Draw": item["proportion_1st_goal_away_draw"], "Away / First Goal Scored / Loss": item["proportion_1st_goal_away_lose"],
                                        "First Goal Conceded / Win": item["first_goal_conceded_win"], "First Goal Conceded / Draw": item["first_goal_conceded_draw"], "First Goal Conceded / Loss": item["first_goal_conceded_lose"],
                                        "Home / First Goal Conceded / Win": item["proportion_1st_goal_conceded_home_win"], "Home / First Goal Conceded / Draw": item["proportion_1st_goal_conceded_home_draw"], "Home / First Goal Conceded / Loss": item["proportion_1st_goal_conceded_home_lose"],
                                        "Away / First Goal Conceded / Win": item["proportion_1st_goal_conceded_away_win"], "Away / First Goal Conceded / Draw": item["proportion_1st_goal_conceded_away_draw"], "Away / First Goal Conceded / Loss": item["proportion_1st_goal_conceded_away_lose"]
                                    }
                                    for item in first_goal
                                ])
                                
                                for col in first_goal_df.columns:
                                    if col != "Team" and col != "Season":  # Exclude "Team" and "Season" columns which are text
                                        first_goal_df[col] = pd.to_numeric(first_goal_df[col], errors='coerce') 
                                        first_goal_df[col] = first_goal_df[col].astype(float)  # Convert numeric values to float
                                
                                # Filter the data by the selected team, then drop Season and Team columns
                                first_goal_team = first_goal_df[first_goal_df["Team"] == selected_team].iloc[:, 2:]

                                graphs_to_plot = [
                                    (first_goal_team.iloc[0, :3], ["First Goal Scored", "No Goal", "First Goal Conceded"], f"First Goal Proportion for {selected_team} in {selected_season}"),
                                    (first_goal_team.iloc[0, 3:6], ["First Goal Scored", "No Goal", "First Goal Conceded"], "Home First Goal"),
                                    (first_goal_team.iloc[0, 6:9], ["First Goal Scored", "No Goal", "First Goal Conceded"], "Away First Goal"),
                                    (first_goal_team.iloc[0, 9:12], ["Win", "Draw", "Loss"], "Results After Scoring First Goal"),
                                    (first_goal_team.iloc[0, 12:15], ["Win", "Draw", "Loss"], "Home Results After Scoring First Goal"),
                                    (first_goal_team.iloc[0, 15:18], ["Win", "Draw", "Loss"], "Away Results After Scoring First Goal"),
                                    (first_goal_team.iloc[0, 18:21], ["Win", "Draw", "Loss"], "Results After Conceding First Goal"),
                                    (first_goal_team.iloc[0, 21:24], ["Win", "Draw", "Loss"], "Home Results After Conceding First Goal"),
                                    (first_goal_team.iloc[0, 24:27], ["Win", "Draw", "Loss"], "Away Results After Conceding First Goal")
                                ]
                                
                                graphs_to_plot = [graph for graph in graphs_to_plot if graph[0].sum() > 0]
                                
                                num_graphs = len(graphs_to_plot)
                                num_rows = -(-num_graphs // 3)  # Equivalent to math.ceil(num_graphs / 3)
                                
                                if num_rows == 0:
                                    st.write("No data available to display charts.")
                                else:
                                    fig, axes = plt.subplots(num_rows, 3, figsize=(18, 4 * num_rows))
                                    axes = np.atleast_2d(axes)  # Ensure 2D structure
                                    
                                    for idx, (data, labels, title) in enumerate(graphs_to_plot):
                                        row, col = divmod(idx, 3)
                                        plot_pie_chart(axes[row, col], data, labels, title, ["#2ecc71", "#95a5a6", "#e74c3c"])
                                    
                                    for idx in range(num_graphs, num_rows * 3):
                                        row, col = divmod(idx, 3)
                                        axes[row, col].axis("off")
                                    
                                    plt.tight_layout()
                                    st.pyplot(fig)

                                # Move to the table of first goal (scored or conceded)
                                first_goal_df_season = first_goal_df.iloc[:, 1:]  # Remove the Season column
                                
                                # Define numeric columns to format (excluding "Team" which is text)
                                numeric_columns = [
                                    col for col in first_goal_df_season.columns if col != "Team"
                                ]
                                
                                # Build tables for first goal scored or conceded by category
                                first_goal_columns = [
                                    "Team", "First Goal Scored", "No Goal", "First Goal Conceded", "Home / First Goal Scored", "Home / No Goal", "Home / First Goal Conceded",
                                    "Away / First Goal Scored", "Away / No Goal", "Away / First Goal Conceded"
                                ]
                                first_goal_influence_columns = [
                                    "Team", "First Goal Scored / Win", "First Goal Scored / Draw", "First Goal Scored / Loss", "Home / First Goal Scored / Win",
                                    "Home / First Goal Scored / Draw", "Home / First Goal Scored / Loss", "Away / First Goal Scored / Win",
                                    "Away / First Goal Scored / Draw", "Away / First Goal Scored / Loss"
                                ]
                                first_goal_conceded_columns = [
                                    "Team", "First Goal Conceded / Win", "First Goal Conceded / Draw", "First Goal Conceded / Loss",
                                    "Home / First Goal Conceded / Win", "Home / First Goal Conceded / Draw", "Home / First Goal Conceded / Loss",
                                    "Away / First Goal Conceded / Win", "Away / First Goal Conceded / Draw", "Away / First Goal Conceded / Loss"
                                ]
                                
                                # Create the three subtables
                                df_first_goal = first_goal_df_season[first_goal_columns]
                                df_first_goal_influence = first_goal_df_season[first_goal_influence_columns]
                                df_first_goal_conceded = first_goal_df_season[first_goal_conceded_columns]
                                
                                # Sort the tables
                                df_first_goal = df_first_goal.sort_values(by=["First Goal Scored"], ascending=False)
                                df_first_goal_influence = df_first_goal_influence.sort_values(by=["First Goal Scored / Win"], ascending=False)
                                df_first_goal_conceded = df_first_goal_conceded.sort_values(by=["First Goal Conceded / Win"], ascending=False)
                                
                                # Function for highlighting the selected team
                                def highlight_selected_squad(row):
                                    return ['background-color: lightcoral' if row["Team"] == selected_team else '' for _ in row]
                                
                                # Adjust styles for the 3 tables
                                style_df_first_goal = (
                                    df_first_goal.style
                                    .format({col: format_value for col in numeric_columns})  # Custom formatting
                                    .apply(highlight_selected_squad, axis=1)  # Custom highlighting
                                    .set_properties(**{"text-align": "center"})  # Center text
                                )

                                style_df_first_goal_influence = (
                                    df_first_goal_influence.style
                                    .format({col: format_value for col in numeric_columns})  # Custom formatting
                                    .apply(highlight_selected_squad, axis=1)  # Custom highlighting
                                    .set_properties(**{"text-align": "center"})  # Center text
                                )

                                style_df_first_goal_conceded = (
                                    df_first_goal_conceded.style
                                    .format({col: format_value for col in numeric_columns})  # Custom formatting
                                    .apply(highlight_selected_squad, axis=1)  # Custom highlighting
                                    .set_properties(**{"text-align": "center"})  # Center text
                                )

                                # Display the formatted tables
                                st.subheader(f"First Goal (Scored or Conceded) Table for the {selected_season} season (%)")
                                st.dataframe(style_df_first_goal)

                                st.subheader(f"Impact of Scoring First Goal for the {selected_season} season (%)")
                                st.dataframe(style_df_first_goal_influence)

                                st.subheader(f"Impact of Conceding First Goal for the {selected_season} season (%)")
                                st.dataframe(style_df_first_goal_conceded)


                        # Display graphs related to the "Goal Distribution" section
                        elif section == "Goal distribution":
                            distrib_goal_team = get_distribution_goals_season(selected_season)  # Fetch the data

                            if distrib_goal_team:
                                # Transform the data into a DataFrame with column names
                                distrib_goal_team = pd.DataFrame([
                                    {
                                        "Season": item["season_name"], "Team": item["team_name"], "1st Half (Goal Scored Proportion)": item["proportion_buts_inscrit_1ere_periode"],
                                        "2nd Half (Goal Scored Proportion)": item["proportion_buts_inscrit_2nde_periode"], "0-15 min (Goal Scored Proportion)": item["proportion_buts_0_15"],
                                        "16-30 min (Goal Scored Proportion)": item["proportion_buts_16_30"], "31-45 min (Goal Scored Proportion)": item["proportion_buts_31_45"],
                                        "46-60 min (Goal Scored Proportion)": item["proportion_buts_46_60"], "61-75 min (Goal Scored Proportion)": item["proportion_buts_61_75"],
                                        "76-90 min (Goal Scored Proportion)": item["proportion_buts_76_90"], "1st Half (Goal Conceded Proportion)": item["proportion_buts_encaissés_1ere_periode"],
                                        "2nd Half (Goal Conceded Proportion)": item["proportion_buts_encaissés_2nde_periode"], "0-15 min (Goal Conceded Proportion)": item["proportion_buts_encaissés_0_15"],
                                        "16-30 min (Goal Conceded Proportion)": item["proportion_buts_encaissés_16_30"], "31-45 min (Goal Conceded Proportion)": item["proportion_buts_encaissés_31_45"],
                                        "46-60 min (Goal Conceded Proportion)": item["proportion_buts_encaissés_46_60"], "61-75 min (Goal Conceded Proportion)": item["proportion_buts_encaissés_61_75"],
                                        "76-90 min (Goal Conceded Proportion)": item["proportion_buts_encaissés_76_90"], "1st Half (Goals Scored)": item["buts_inscrit_1ere_periode"],
                                        "2nd Half (Goals Scored)": item["buts_inscrit_2nde_periode"], "0-15 min (Goals Scored)": item["nbr_buts_0_15"], "16-30 min (Goals Scored)": item["nbr_buts_16_30"],
                                        "31-45 min (Goals Scored)": item["nbr_buts_31_45"], "46-60 min (Goals Scored)": item["nbr_buts_46_60"], "61-75 min (Goals Scored)": item["nbr_buts_61_75"],
                                        "76-90 min (Goals Scored)": item["nbr_buts_76_90"], "1st Half (Goals Conceded)": item["buts_encaissés_1ere_periode"],
                                        "2nd Half (Goals Conceded)": item["buts_encaissés_2nde_periode"], "0-15 min (Goals Conceded)": item["buts_encaissés_0_15"], "16-30 min (Goals Conceded)": item["buts_encaissés_16_30"],
                                        "31-45 min (Goals Conceded)": item["buts_encaissés_31_45"], "46-60 min (Goals Conceded)": item["buts_encaissés_46_60"],
                                        "61-75 min (Goals Conceded)": item["buts_encaissés_61_75"], "76-90 min (Goals Conceded)": item["buts_encaissés_76_90"]
                                    }
                                    for item in distrib_goal_team
                                ])

                                distrib_goal_team = distrib_goal_team.iloc[:, 1:]  # Remove the "Season" column

                                for col in distrib_goal_team.columns:
                                    if col != "Team":  # Exclude "Team" column which is text
                                        distrib_goal_team[col] = pd.to_numeric(distrib_goal_team[col], errors='coerce')
                                        distrib_goal_team[col] = distrib_goal_team[col].astype(float)  # Convert numeric values to float

                                # Create a DataFrame for the selected team's graphs and tables
                                distrib_goal_team_graph = distrib_goal_team[distrib_goal_team["Team"] == selected_team]
                                distrib_goal_team_graph = distrib_goal_team_graph.iloc[:, 1:]  # Remove "Team" column

                                fig, axes = plt.subplots(2, 2, figsize=(15, 10))  # Create the figure and axes
                                
                                # Goal scored proportions by half
                                labels_proportion = ["1st Half", "2nd Half"]
                                values_proportion_goal_scored = distrib_goal_team_graph.iloc[0, :2]
                                axes[0, 0].pie(values_proportion_goal_scored, labels=labels_proportion, autopct='%1.2f%%', startangle=90, colors=["lightblue", "lightcoral"])
                                axes[0, 0].set_title("Proportion of Goals Scored by Half")
                                
                                # Goal conceded proportions by half
                                values_proportion_goal_conceded = distrib_goal_team_graph.iloc[0, 8:10]
                                axes[0, 1].pie(values_proportion_goal_conceded, labels=labels_proportion, autopct='%1.2f%%', startangle=90, colors=["lightblue", "lightcoral"])
                                axes[0, 1].set_title("Proportion of Goals Conceded by Half")
                                
                                # Goals scored by 15-min interval
                                labels_intervals = ["0-15 min", "16-30 min", "31-45 min", "46-60 min", "61-75 min", "76-90 min"]
                                values_intervals_goal_scored = distrib_goal_team_graph.iloc[0, 2:8]
                                colors = ["#D4EFDF", "#A9DFBF", "#F9E79F", "#F5CBA7", "#E59866", "#DC7633"]
                                bars1 = axes[1, 0].bar(labels_intervals, values_intervals_goal_scored, color=colors)
                                axes[1, 0].set_title("Proportion of Goals Scored by 15-Min Interval")
                                axes[1, 0].set_ylabel("%")
                                axes[1, 0].set_ylim(0, max(values_intervals_goal_scored) + 5)
                                
                                # Goals conceded by 15-min interval
                                values_intervals_goal_conceded = distrib_goal_team_graph.iloc[0, 10:16]
                                bars2 = axes[1, 1].bar(labels_intervals, values_intervals_goal_conceded, color=colors)
                                axes[1, 1].set_title("Proportion of Goals Conceded by 15-Min Interval")
                                axes[1, 1].set_ylabel("%")
                                axes[1, 1].set_ylim(0, max(values_intervals_goal_conceded) + 5)
                                
                                # Add values on bars
                                for bars in [bars1, bars2]:
                                    for bar in bars:
                                        yval = bar.get_height()
                                        axes[1, 0 if bars is bars1 else 1].text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval:.2f}%', ha='center', color='black')

                                st.pyplot(fig)  # Display the figure

                                # Build the goal distribution tables for the selected season
                                distrib_goals_scored_columns = [
                                    "Team", "1st Half (Goal Scored Proportion)", "1st Half (Goals Scored)", "2nd Half (Goal Scored Proportion)", "2nd Half (Goals Scored)",
                                    "0-15 min (Goal Scored Proportion)", "0-15 min (Goals Scored)", "16-30 min (Goal Scored Proportion)", "16-30 min (Goals Scored)",
                                    "31-45 min (Goal Scored Proportion)", "31-45 min (Goals Scored)", "46-60 min (Goal Scored Proportion)", "46-60 min (Goals Scored)",
                                    "61-75 min (Goal Scored Proportion)", "61-75 min (Goals Scored)", "76-90 min (Goal Scored Proportion)", "76-90 min (Goals Scored)"
                                ]
                                distrib_goals_conceded_columns = [
                                    "Team", "1st Half (Goal Conceded Proportion)", "1st Half (Goals Conceded)", "2nd Half (Goal Conceded Proportion)", "2nd Half (Goals Conceded)",
                                    "0-15 min (Goal Conceded Proportion)", "0-15 min (Goals Conceded)", "16-30 min (Goal Conceded Proportion)", "16-30 min (Goals Conceded)",
                                    "31-45 min (Goal Conceded Proportion)", "31-45 min (Goals Conceded)", "46-60 min (Goal Conceded Proportion)", "46-60 min (Goals Conceded)",
                                    "61-75 min (Goal Conceded Proportion)", "61-75 min (Goals Conceded)", "76-90 min (Goal Conceded Proportion)", "76-90 min (Goals Conceded)"
                                ]

                                # Create subtables
                                df_distrib_goals_scored = distrib_goal_team[distrib_goals_scored_columns]
                                df_distrib_goals_conceded = distrib_goal_team[distrib_goals_conceded_columns]
                                
                                # Sort tables
                                df_distrib_goals_scored = df_distrib_goals_scored.sort_values(by=["1st Half (Goal Scored Proportion)"], ascending=False)
                                df_distrib_goals_conceded = df_distrib_goals_conceded.sort_values(by=["1st Half (Goal Conceded Proportion)"], ascending=False)

                                # Apply styles (highlight selected team, format numbers, center text)
                                def highlight_selected_squad(row):
                                    return ['background-color: lightcoral' if row["Team"] == selected_team else '' for _ in row]
                                
                                style_df_distrib_goals_scored = (
                                    df_distrib_goals_scored.style
                                    .format({col: format_value for col in distrib_goals_scored_columns[1:]})
                                    .apply(highlight_selected_squad, axis=1)
                                    .set_properties(**{"text-align": "center"})
                                )

                                style_df_distrib_goals_conceded = (
                                    df_distrib_goals_conceded.style
                                    .format({col: format_value for col in distrib_goals_conceded_columns[1:]})
                                    .apply(highlight_selected_squad, axis=1)
                                    .set_properties(**{"text-align": "center"})
                                )

                                # Display the formatted tables
                                st.subheader(f"Goals Scored Distribution Table for the {selected_season} Season")
                                st.dataframe(style_df_distrib_goals_scored)

                                st.subheader(f"Goals Conceded Distribution Table for the {selected_season} Season")
                                st.dataframe(style_df_distrib_goals_conceded)


                        # Display graphs related to the "Home / Away" section
                        elif section == "Home / Away":
                            result_h_a = get_rank_season(selected_season)  # Fetch home advantage statistics

                            if result_h_a:
                                # Transform the data into a DataFrame with column names
                                df_adv_home_away = pd.DataFrame([
                                    {
                                        "Type": item["type"], "Season": item["season_name"], "Team": item["team_name"], "Matches Played": item["matches"], "Wins": item["wins"],
                                        "Draws": item["draws"], "Losses": item["losses"], "Points": item["points"], "Avg. Points": item["avg_points"],
                                        "Home Advantage": item["home_advantage"]
                                    }
                                    for item in result_h_a
                                ])

                                # Filter for the selected team
                                data_team = df_adv_home_away[df_adv_home_away["Team"] == selected_team]

                                if not data_team.empty:
                                    # Select necessary columns and compute proportions
                                    data_team_home = data_team[data_team["Type"] == "Home"]
                                    total_home = data_team_home[["Wins", "Draws", "Losses"]].sum(axis=1).values[0]
                                    values_proportion_home = (data_team_home[["Wins", "Draws", "Losses"]].values.flatten() / total_home) * 100

                                    data_team_away = data_team[data_team["Type"] == "Away"]
                                    total_away = data_team_away[["Wins", "Draws", "Losses"]].sum(axis=1).values[0]
                                    values_proportion_away = (data_team_away[["Wins", "Draws", "Losses"]].values.flatten() / total_away) * 100

                                    # Determine maximum values for gauge scaling
                                    max_adv_home = float(data_team_home["Home Advantage"].max())
                                    max_adv_away = float(max_adv_home)

                                    # Extract and scale home advantage values
                                    adv_home = float(data_team_home["Home Advantage"].values[0])
                                    adv_away = float(data_team_away["Home Advantage"].values[0])

                                    # Labels for the pie charts
                                    labels_proportion_home = ["Home Win", "Draw", "Home Loss"]
                                    labels_proportion_away = ["Away Win", "Draw", "Away Loss"]

                                    # Function to determine gauge color
                                    def get_gauge_color(value, max_value, inverse=False):
                                        if max_value <= 0:
                                            raise ValueError("max_value must be greater than 0")

                                        ratio = value / max_value
                                        if inverse:
                                            red = min(max(int(210 * ratio), 0), 255)
                                            green = min(max(int(210 * (1 - ratio)), 0), 255)
                                        else:
                                            red = min(max(int(210 * (1 - ratio)), 0), 255)
                                            green = min(max(int(210 * ratio), 0), 255)

                                        return f"rgb({red},{green},0)"

                                    col1, col2 = st.columns(2)  # Create Streamlit columns for Home

                                    # Create home pie chart
                                    with col1:
                                        fig1, ax1 = plt.subplots(figsize=(7, 7))
                                        plot_pie_chart(ax1, values_proportion_home, labels_proportion_home, "Result Proportions at Home", ["#2ecc71", "#95a5a6", "#e74c3c"])
                                        st.pyplot(fig1)

                                    # Create home gauge
                                    with col2:
                                        fig2 = go.Figure(go.Indicator(
                                            mode="gauge+number",
                                            value=adv_home,
                                            title={"text": "Home Advantage (%)"},
                                            gauge={
                                                "axis": {"range": [0, max_adv_home]},
                                                "bar": {"color": get_gauge_color(adv_home, max_adv_home)}
                                            }
                                        ))
                                        st.plotly_chart(fig2)

                                    col3, col4 = st.columns(2)  # Create Streamlit columns for Away

                                    # Create away pie chart
                                    with col3:
                                        fig3, ax3 = plt.subplots(figsize=(7, 7))
                                        plot_pie_chart(ax3, values_proportion_away, labels_proportion_away, "Result Proportions Away", ["#2ecc71", "#95a5a6", "#e74c3c"])
                                        st.pyplot(fig3)

                                    # Create away gauge
                                    with col4:
                                        fig4 = go.Figure(go.Indicator(
                                            mode="gauge+number",
                                            value=adv_away,
                                            title={"text": "Away Advantage (%)"},
                                            gauge={
                                                "axis": {"range": [0, max_adv_away]},
                                                "bar": {"color": get_gauge_color(adv_away, max_adv_away, inverse=True)}
                                            }
                                        ))
                                        st.plotly_chart(fig4)

                                # Home ranking
                                rank_home_data = df_adv_home_away[df_adv_home_away["Type"] == "Home"].copy()
                                if not rank_home_data.empty:
                                    for col in rank_home_data.columns:
                                        if col not in ["Team", "Season", "Type"]:
                                            rank_home_data.loc[:, col] = pd.to_numeric(rank_home_data[col], errors='coerce')

                                    rank_home_data = rank_home_data.drop(columns=["Season", "Type"])
                                    rank_home_data = rank_home_data.sort_values(by=["Points"], ascending=False)

                                    # Function to highlight the selected team
                                    def highlight_selected_squad(row):
                                        return ['background-color: lightcoral' if row["Team"] == selected_team else '' for _ in row]

                                    style_rank_home_data = (
                                        rank_home_data.style
                                        .format({col: format_value for col in rank_home_data.columns[1:]})
                                        .apply(highlight_selected_squad, axis=1)
                                        .set_properties(**{"text-align": "center"})
                                    )

                                    st.subheader(f"Home Ranking for the {selected_season} Season")
                                    st.dataframe(style_rank_home_data)

                                # Away ranking
                                rank_away_data = df_adv_home_away[df_adv_home_away["Type"] == "Away"].copy()
                                if not rank_away_data.empty:
                                    for col in rank_away_data.columns:
                                        if col not in ["Team", "Season", "Type"]:
                                            rank_away_data.loc[:, col] = pd.to_numeric(rank_away_data[col], errors='coerce')

                                    rank_away_data = rank_away_data.drop(columns=["Season", "Type"])
                                    rank_away_data = rank_away_data.sort_values(by=["Points"], ascending=False)

                                    # Function to highlight the selected team
                                    style_rank_away_data = (
                                        rank_away_data.style
                                        .format({col: format_value for col in rank_away_data.columns[1:]})
                                        .apply(highlight_selected_squad, axis=1)
                                        .set_properties(**{"text-align": "center"})
                                    )

                                    st.subheader(f"Away Ranking for the {selected_season} Season")
                                    st.dataframe(style_rank_away_data)


                        elif section == "Season comparison":
                            with st.spinner("Loading data..."):
                                # Initialize comparison variables
                                compare_goals_season_team_data = []
                                compare_first_goal_team_data = []
                                compare_distrib_goal_data = []
                                compare_home_away_data = []

                                # Loop to fetch the list of available seasons for the selected competition
                                for season in seasons_available:
                                    # Fetch data
                                    goals_season_team_stats = get_avg_goals_stats(season)
                                    first_goal_season_stats = get_first_goal_season(season)
                                    distrib_stats = get_distribution_goals_season(season)
                                    home_away_stats = get_rank_season(season)

                                    # Add available data to comparison lists
                                    if goals_season_team_stats:
                                        compare_goals_season_team_data.extend(goals_season_team_stats)

                                    if first_goal_season_stats:
                                        compare_first_goal_team_data.extend(first_goal_season_stats)

                                    if distrib_stats:
                                        compare_distrib_goal_data.extend(distrib_stats)

                                    if home_away_stats:
                                        compare_home_away_data.extend(home_away_stats)

                                if compare_goals_season_team_data:
                                    # Transform the data into a DataFrame with column names
                                    df = pd.DataFrame([
                                        {
                                            "Season": item["season_name"], "Team": item["team_name"], "Goals/Match": item["avg_goals_per_match"],
                                            "Goals Scored/Match": item["avg_team_goals_per_match"], "Goals Conceded/Match": item["avg_team_goals_conceded_per_match"],
                                            "Home Goals Scored/Match": item["avg_team_home_goals"], "Away Goals Scored/Match": item["avg_team_away_goals"],
                                            "Home Goals Conceded/Match": item["avg_conceded_home_goals"], "Away Goals Conceded/Match": item["avg_conceded_away_goals"]
                                        }
                                        for item in compare_goals_season_team_data
                                    ])
                                    df = df[df["Team"] == selected_team]  # Filter for the selected team

                                    df = df.drop(columns=["Team"])  # Remove the Team column

                                    numeric_columns = df.columns[1:]  # Select numeric columns
                                    # Round and convert numeric values
                                    df[numeric_columns] = df[numeric_columns].apply(lambda col: col.apply(lambda x: float(round(x, 2)) if pd.notnull(x) else 0.0))

                                    df = df.sort_values(by=numeric_columns.tolist(), ascending=False)  # Sort the table
                                    # Function to highlight the selected season
                                    def highlight_selected_season(row):
                                        return ['background-color: lightcoral' if row["Season"] == selected_season else '' for _ in row]
                                    # Apply styling and highlighting
                                    styled_df = (
                                        df.style
                                        .format({col: format_value for col in numeric_columns})
                                        .apply(highlight_selected_season, axis=1)
                                        .set_properties(**{"text-align": "center"})
                                    )
                                    # Display the table
                                    st.subheader("⚽ General Goal Statistics (Average)")
                                    st.dataframe(styled_df)

                                if compare_first_goal_team_data:
                                    # Transform the data into a DataFrame with column names
                                    first_goal_season_data = pd.DataFrame([
                                        {
                                            "Season": item["season_name"], "Team": item["team_name"],
                                            "First Goal Scored": item["proportion_1st_goal_for"], "No Goal": item["proportion_no_goal"], "First Goal Conceded": item["proportion_1st_goal_against"],
                                            "Home / First Goal Scored": item["proportion_1st_goal_home_for"], "Home / No Goal": item["proportion_no_goal_home"], "Home / First Goal Conceded": item["proportion_1st_goal_home_against"],
                                            "Away / First Goal Scored": item["proportion_1st_goal_away_for"], "Away / No Goal": item["proportion_no_goal_away"], "Away / First Goal Conceded": item["proportion_1st_goal_away_against"],
                                            "First Goal Scored / Win": item["first_goal_win"], "First Goal Scored / Draw": item["first_goal_draw"], "First Goal Scored / Loss": item["first_goal_lose"],
                                            "Home / First Goal Scored / Win": item["proportion_1st_goal_home_win"], "Home / First Goal Scored / Draw": item["proportion_1st_goal_home_draw"], "Home / First Goal Scored / Loss": item["proportion_1st_goal_home_lose"],
                                            "Away / First Goal Scored / Win": item["proportion_1st_goal_away_win"], "Away / First Goal Scored / Draw": item["proportion_1st_goal_away_draw"], "Away / First Goal Scored / Loss": item["proportion_1st_goal_away_lose"],
                                            "First Goal Conceded / Win": item["first_goal_conceded_win"], "First Goal Conceded / Draw": item["first_goal_conceded_draw"], "First Goal Conceded / Loss": item["first_goal_conceded_lose"],
                                            "Home / First Goal Conceded / Win": item["proportion_1st_goal_conceded_home_win"], "Home / First Goal Conceded / Draw": item["proportion_1st_goal_conceded_home_draw"], "Home / First Goal Conceded / Loss": item["proportion_1st_goal_conceded_home_lose"],
                                            "Away / First Goal Conceded / Win": item["proportion_1st_goal_conceded_away_win"], "Away / First Goal Conceded / Draw": item["proportion_1st_goal_conceded_away_draw"], "Away / First Goal Conceded / Loss": item["proportion_1st_goal_conceded_away_lose"]
                                        }
                                        for item in compare_first_goal_team_data
                                    ])
                                    first_goal_season_data = first_goal_season_data[first_goal_season_data["Team"] == selected_team]  # Filter for the selected team

                                    for col in first_goal_season_data.columns:
                                        if col not in ["Team", "Season"]:  # Exclude text columns
                                            first_goal_season_data[col] = pd.to_numeric(first_goal_season_data[col], errors='coerce')

                                    first_goal_season_data = first_goal_season_data.drop(columns=["Team"])  # Remove Team column

                                    first_goal_season_data = first_goal_season_data.sort_values(by=["First Goal Scored"], ascending=False)  # Sort

                                    numeric_columns = first_goal_season_data.columns[1:]  # Exclude "Season"
                                    first_goal_season_data[numeric_columns] = first_goal_season_data[numeric_columns].astype(float)

                                    # Function to highlight the selected season
                                    def highlight_selected_season(row):
                                        return ['background-color: lightcoral' if row["Season"] == selected_season else '' for _ in row]
                                    # Apply styling
                                    style_first_goal_season_data = (
                                        first_goal_season_data.style
                                        .format({col: format_value for col in numeric_columns})
                                        .apply(highlight_selected_season, axis=1)
                                        .set_properties(**{"text-align": "center"})
                                    )
                                    # Display the table
                                    st.subheader(f"⚽ First Goal Statistics for {selected_team} (in %)")
                                    st.dataframe(style_first_goal_season_data)

                                if compare_distrib_goal_data:
                                    distrib_goal_data = pd.DataFrame([
                                        {
                                            "Season": item["season_name"], "Team": item["team_name"], "1st Half (Proportion Goals Scored)": item["proportion_buts_inscrit_1ere_periode"],
                                            "2nd Half (Proportion Goals Scored)": item["proportion_buts_inscrit_2nde_periode"], "0-15 min (Proportion Goals Scored)": item["proportion_buts_0_15"],
                                            "16-30 min (Proportion Goals Scored)": item["proportion_buts_16_30"], "31-45 min (Proportion Goals Scored)": item["proportion_buts_31_45"],
                                            "46-60 min (Proportion Goals Scored)": item["proportion_buts_46_60"], "61-75 min (Proportion Goals Scored)": item["proportion_buts_61_75"],
                                            "76-90 min (Proportion Goals Scored)": item["proportion_buts_76_90"], "1st Half (Proportion Goals Conceded)": item["proportion_buts_encaissés_1ere_periode"],
                                            "2nd Half (Proportion Goals Conceded)": item["proportion_buts_encaissés_2nde_periode"], "0-15 min (Proportion Goals Conceded)": item["proportion_buts_encaissés_0_15"],
                                            "16-30 min (Proportion Goals Conceded)": item["proportion_buts_encaissés_16_30"], "31-45 min (Proportion Goals Conceded)": item["proportion_buts_encaissés_31_45"],
                                            "46-60 min (Proportion Goals Conceded)": item["proportion_buts_encaissés_46_60"], "61-75 min (Proportion Goals Conceded)": item["proportion_buts_encaissés_61_75"],
                                            "76-90 min (Proportion Goals Conceded)": item["proportion_buts_encaissés_76_90"], "1st Half (Goals Scored)": item["buts_inscrit_1ere_periode"],
                                            "2nd Half (Goals Scored)": item["buts_inscrit_2nde_periode"], "0-15 min (Goals Scored)": item["nbr_buts_0_15"], "16-30 min (Goals Scored)": item["nbr_buts_16_30"],
                                            "31-45 min (Goals Scored)": item["nbr_buts_31_45"], "46-60 min (Goals Scored)": item["nbr_buts_46_60"], "61-75 min (Goals Scored)": item["nbr_buts_61_75"],
                                            "76-90 min (Goals Scored)": item["nbr_buts_76_90"], "1st Half (Goals Conceded)": item["buts_encaissés_1ere_periode"],
                                            "2nd Half (Goals Conceded)": item["buts_encaissés_2nde_periode"], "0-15 min (Goals Conceded)": item["buts_encaissés_0_15"], "16-30 min (Goals Conceded)": item["buts_encaissés_16_30"],
                                            "31-45 min (Goals Conceded)": item["buts_encaissés_31_45"], "46-60 min (Goals Conceded)": item["buts_encaissés_46_60"],
                                            "61-75 min (Goals Conceded)": item["buts_encaissés_61_75"], "76-90 min (Goals Conceded)": item["buts_encaissés_76_90"]
                                        }
                                        for item in compare_distrib_goal_data
                                    ])

                                    distrib_goal_data = distrib_goal_data[distrib_goal_data["Team"] == selected_team]  # Retrieve the selected team's values

                                    distrib_goal_data = distrib_goal_data.drop(columns=["Team"])  # Remove the Team column

                                    numeric_columns = distrib_goal_data.columns[1:]  # Handle numeric data
                                    distrib_goal_data[numeric_columns] = distrib_goal_data[numeric_columns].astype(float).round(2)  # Round to 2 decimals

                                    distrib_goal_data = distrib_goal_data.sort_values(by=numeric_columns.tolist(), ascending=False)  # Ensure numerical sorting
                                    # Function to highlight the selected season
                                    def highlight_selected_season(row):
                                        return ['background-color: lightcoral' if row["Season"] == selected_season else '' for _ in row]

                                    # Apply style
                                    styled_distrib_goal_data = (
                                        distrib_goal_data.style
                                        .format({col: format_value for col in numeric_columns})
                                        .apply(highlight_selected_season, axis=1)  # Custom highlighting for the selected season
                                        .set_properties(**{"text-align": "center"})  # Center the text
                                    )

                                    # Display the formatted and sorted table
                                    st.subheader("⚽ Goal Distribution Information by Season (%)")
                                    st.dataframe(styled_distrib_goal_data)

                                if compare_home_away_data:
                                    # Transform the data into a DataFrame with column names
                                    df_adv_home_away_complete = pd.DataFrame([
                                        {
                                            "Type": item["type"], "Season": item["season_name"], "Team": item["team_name"], "Matches Played": item["matches"],
                                            "Win (%)": item["wins"], "Draw (%)": item["draws"], "Loss (%)": item["losses"],
                                            "Points": item["points"], "Avg. Points": item["avg_points"], "Home Advantage": item["home_advantage"]
                                        }
                                        for item in compare_home_away_data
                                    ])

                                    # Explicit copy to avoid warnings
                                    df_adv_home_away_team = df_adv_home_away_complete[df_adv_home_away_complete["Team"] == selected_team].copy()

                                    # Convert numeric columns to float and round to 2 decimals
                                    numeric_columns = [col for col in df_adv_home_away_team.columns if col not in ["Team", "Season", "Type"]]
                                    df_adv_home_away_team[numeric_columns] = df_adv_home_away_team[numeric_columns].astype(float).apply(lambda col: col.round(2).fillna(0))

                                    # Retrieve Home/Away values with explicit copies
                                    data_home = df_adv_home_away_team[df_adv_home_away_team["Type"] == "Home"].copy()
                                    data_away = df_adv_home_away_team[df_adv_home_away_team["Type"] == "Away"].copy()

                                    # Drop unnecessary columns
                                    data_home = data_home.drop(columns=["Team", "Type"])
                                    data_away = data_away.drop(columns=["Team", "Type"])

                                    if not data_home.empty:
                                        # Calculate percentages safely
                                        for col in ["Win (%)", "Draw (%)", "Loss (%)"]:
                                            data_home[col] = (data_home[col] / data_home["Matches Played"].replace(0, np.nan)) * 100
                                            data_home[col] = data_home[col].round(2).fillna(0)
                                        # Function to highlight the selected season
                                        def highlight_selected_season(row):
                                            return ['background-color: lightcoral' if row["Season"] == selected_season else '' for _ in row]

                                        data_home = data_home.sort_values(by=["Points"], ascending=False)
                                        style_data_home = (
                                            data_home.style
                                            .format({col: format_value for col in data_home.columns[1:]})
                                            .apply(highlight_selected_season, axis=1)
                                            .set_properties(**{"text-align": "center"})
                                        )
                                        st.subheader(f"⚽ Home Performance Information for {selected_team} (all seasons)")
                                        st.dataframe(style_data_home)

                                    if not data_away.empty:
                                        # Calculate percentages safely
                                        for col in ["Win (%)", "Draw (%)", "Loss (%)"]:
                                            data_away[col] = (data_away[col] / data_away["Matches Played"].replace(0, np.nan)) * 100
                                            data_away[col] = data_away[col].round(2).fillna(0)
                                        # Function to highlight the selected season
                                        def highlight_selected_season(row):
                                            return ['background-color: lightcoral' if row["Season"] == selected_season else '' for _ in row]
                                        data_away = data_away.sort_values(by=["Points"], ascending=False)
                                        style_data_away = (
                                            data_away.style
                                            .format({col: format_value for col in data_away.columns[1:]})
                                            .apply(highlight_selected_season, axis=1)
                                            .set_properties(**{"text-align": "center"})
                                        )
                                        st.subheader(f"⚽ Away Performance Information for {selected_team} (all seasons)")
                                        st.dataframe(style_data_away)

        # Image display only if no selection was made
        if show_image:
            st.image(image_path)


def team_head_to_head_analysis():
    if lang == "Français":
        st.title("🥊 Confrontation entre Équipes") # Titre de l'application

        # Vérifie si l'utilisateur a fait un choix (équipe, saison et section)
        show_image = True  # Par défaut, on affiche l'image

        image_path = os.path.join(os.path.dirname(__file__), "image", "banniere_confrontation.jpg") # Construction du chemin absolu

        st.sidebar.header("🔍 Sélection de l'équipe") # Sélection de la compétition en sidebar
        teams_available = get_teams() # Récupération des équipes disponibles

        # Boucle pour selectionner les équipes de son choix présent dans la base de données
        if teams_available:
            selected_team_home = st.sidebar.selectbox("Choisissez une équipe (Domicile) :", ["Sélectionnez une équipe"] + teams_available, index=0)
            
            if selected_team_home != "Sélectionnez une équipe":
                seasons_available = get_seasons(selected_team_home)
                
                if seasons_available: # Sélection de la saison
                    selected_season = st.sidebar.selectbox("Choisissez une saison :", ["Sélectionnez une saison"] + seasons_available, index=0)
                    
                    if selected_season != "Sélectionnez une saison":
                        teams_in_season = get_teams_in_season(selected_season)

                        teams_in_season = [
                            team['team_name'] 
                            for team in get_teams_in_season(selected_season) 
                            if team['team_name'] != selected_team_home
                        ]
                        
                        if teams_in_season: # Sélection de la 2ème équipe
                            selected_team_away = st.sidebar.selectbox("Choisissez une équipe (Extérieur) :", ["Sélectionnez une équipe"] + teams_in_season, index=0)
                            
                            if selected_team_away != "Sélectionnez une équipe":
                                st.sidebar.header("📊 Sélectionnez une analyse")
                                section = st.sidebar.radio("sections", ["Statistiques générales", "1er but inscrit", "Distribution des buts", "Domicile / Extérieur", "Précédentes confrontations"])

                                # Si une section est sélectionnée, on cache l’image
                                if section:
                                    show_image = False 
                                st.subheader(f"📌 {section} - {selected_team_home} (Domicile) vs {selected_team_away} (Extérieur) - {selected_season}") # Récapitulatif des choix
                        
                                # Affichage des graphiques relatifs à la section Statistiques Générales            
                                if section == "Statistiques générales":
                                    avg_goal_stats = get_avg_goals_stats(selected_season) # Récupération des données
                                    if avg_goal_stats:
                                        # Transformation des données en DataFrame avec les noms de colonnes
                                        df_goals = pd.DataFrame([
                                            {
                                                "Saison": item["season_name"], "Équipe": item["team_name"], "Buts/Match": item["avg_goals_per_match"],
                                                "Buts inscrits/Match": item["avg_team_goals_per_match"], "Buts concédés/Match": item["avg_team_goals_conceded_per_match"],
                                                "Buts inscrits Domicile/Match": item["avg_team_home_goals"], "Buts inscrits Extérieur/Match": item["avg_team_away_goals"],
                                                "Buts concédés Domicile/Match": item["avg_conceded_home_goals"], "Buts concédés Extérieur/Match": item["avg_conceded_away_goals"]
                                            }
                                            for item in avg_goal_stats
                                        ])
                                        # Filtrage des données par équipe
                                        df_home = df_goals[df_goals["Équipe"] == selected_team_home]
                                        df_away = df_goals[df_goals["Équipe"] == selected_team_away]
                                        
                                        if not df_home.empty and not df_away.empty:
                                            # On affiche le titre
                                            st.markdown(
                                                f"<h3 style='text-align: center;'>{selected_team_home} vs {selected_team_away} : Buts (inscrits ou concédés)</h3>",
                                                unsafe_allow_html=True
                                            )
                                            col1, col2, col3, col4 = st.columns(4) # 1ère ligne des graphiques sur les buts inscrits et concédés
                                            with col1:
                                                st.plotly_chart(plot_gauge(df_home["Buts inscrits/Match"].values[0], df_goals["Buts inscrits/Match"].max(), f"{selected_team_home} : Buts inscrits"))
                                            with col2:
                                                st.plotly_chart(plot_gauge(df_home["Buts concédés/Match"].values[0], df_goals["Buts concédés/Match"].max(), f"{selected_team_home} : Buts concédés", inverse=True))
                                            with col3:
                                                st.plotly_chart(plot_gauge(df_away["Buts inscrits/Match"].values[0], df_goals["Buts inscrits/Match"].max(), f" {selected_team_away} : Buts inscrits"))
                                            with col4:
                                                st.plotly_chart(plot_gauge(df_away["Buts concédés/Match"].values[0], df_goals["Buts concédés/Match"].max(), f"{selected_team_away} : Buts concédés", inverse=True))
                                            
                                            st.markdown(
                                                f"<h3 style='text-align: center;'>Performance à domicile pour {selected_team_home} et {selected_team_away} à l'extérieur</h3>",
                                                unsafe_allow_html=True
                                            )
                                            col5, col6, col7, col8 = st.columns(4) # 2ème ligne des graphiques sur les buts inscrits et concédés selon le facteur Domicile/Extérieur
                                            with col5:
                                                st.plotly_chart(plot_gauge(df_home["Buts inscrits Domicile/Match"].values[0], df_goals["Buts inscrits Domicile/Match"].max(), f"{selected_team_home} : Buts inscrits Dom"))
                                            with col6:
                                                st.plotly_chart(plot_gauge(df_home["Buts concédés Domicile/Match"].values[0], df_goals["Buts concédés Domicile/Match"].max(), f"{selected_team_home} : Buts concédés Dom", inverse=True))
                                            with col7:
                                                st.plotly_chart(plot_gauge(df_away["Buts inscrits Extérieur/Match"].values[0], df_goals["Buts inscrits Extérieur/Match"].max(), f"{selected_team_away} : Buts inscrits Ext"))
                                            with col8:
                                                st.plotly_chart(plot_gauge(df_away["Buts concédés Extérieur/Match"].values[0], df_goals["Buts concédés Extérieur/Match"].max(), f" {selected_team_away} : Buts concédés Ext", inverse=True))
                                                
                                # Affichage des graphiques relatifs à la section 1er but          
                                if section == "1er but inscrit":
                                    first_goal_stats = get_first_goal_season(selected_season) # Récupération des données
                                    if first_goal_stats:
                                        # Transformation des données en DataFrame avec les noms de colonnes
                                        df_first_goal = pd.DataFrame([
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
                                            for item in first_goal_stats
                                        ])
                                        # Conversion des valeurs en float
                                        for col in df_first_goal.columns:
                                            if col != "Équipe" and col != "Saison":  # Exclure la colonne "Équipe" et "Saison", contenant du texte
                                                df_first_goal[col] = pd.to_numeric(df_first_goal[col], errors='coerce') 
                                                df_first_goal[col] = df_first_goal[col].astype(float) # On transforme en flottant les valeurs numériques
                                                                    
                                        
                                        # Séparation des données pour domicile et extérieur
                                        df_home = df_first_goal[df_first_goal["Équipe"] == selected_team_home].iloc[:, 2:]
                                        df_away = df_first_goal[df_first_goal["Équipe"] == selected_team_away].iloc[:, 2:]

                                        # Liste des graphiques non vides
                                        graphs_to_plot = [
                                            (df_home.iloc[0, :3], ["1er but inscrit", "Aucun but", "1er but encaissé"], f"1er but - {selected_team_home}"),
                                            (df_home.iloc[0, 9:12], ["Victoire", "Nul", "Défaite"], f"Résultats après 1er but inscrit - {selected_team_home}"),
                                            (df_home.iloc[0, 18:21], ["Victoire", "Nul", "Défaite"], f"Résultats après 1er but encaissé - {selected_team_home}"),
                                            (df_home.iloc[0, 3:6], ["1er but inscrit", "Aucun but", "1er but encaissé"], f"Résultats à domicile - {selected_team_home}"),
                                            (df_home.iloc[0, 12:15], ["Domicile / Victoire", "Domicile / Nul", "Domicile / Défaite"], f"Domicile après 1er but inscrit - {selected_team_home}"),
                                            (df_home.iloc[0, 21:24], ["Victoire", "Nul", "Défaite"], f"Domicile après 1er but encaissé - {selected_team_home}"),
                                            (df_away.iloc[0, :3], ["1er but inscrit", "Aucun but", "1er but encaissé"], f"1er but - {selected_team_away}"),
                                            (df_away.iloc[0, 9:12], ["Victoire", "Nul", "Défaite"], f"Résultats après 1er but inscrit - {selected_team_away}"),
                                            (df_away.iloc[0, 18:21], ["Victoire", "Nul", "Défaite"], f"Résultats après 1er but encaissé - {selected_team_away}"),
                                            (df_away.iloc[0, 6:9], ["1er but inscrit", "Aucun but", "1er but encaissé"], f"Résultats à l'extérieur - {selected_team_away}"),
                                            (df_away.iloc[0, 15:18], ["Extérieur / Victoire", "Extérieur / Nul", "Extérieur / Défaite"], f"Extérieur après 1er but inscrit - {selected_team_away}"),
                                            (df_away.iloc[0, 24:], ["Victoire", "Nul", "Défaite"], f"Extérieur après 1er but encaissé - {selected_team_away}")
                                        ]

                                        # Filtrer les graphiques avec des données non nulles
                                        graphs_to_plot = [graph for graph in graphs_to_plot if graph[0].sum() > 0]

                                        # Déterminer le nombre de lignes nécessaires (3 graphiques par ligne)
                                        num_graphs = len(graphs_to_plot)
                                        num_rows = -(-num_graphs // 3)  # Équivalent à math.ceil(num_graphs / 3)

                                        if num_rows == 0:
                                            st.write("Aucune donnée disponible pour afficher les graphiques.")
                                        else:
                                            # Création des subplots
                                            fig, axes = plt.subplots(num_rows, 3, figsize=(18, 4 * num_rows))
                                            axes = np.atleast_2d(axes)  # Garantir une structure 2D même si num_rows == 1

                                            # Remplissage des subplots
                                            for idx, (data, labels, title) in enumerate(graphs_to_plot):
                                                row, col = divmod(idx, 3)  # Convertir index en position (ligne, colonne)
                                                plot_pie_chart(axes[row, col], data, labels, title, ["#2ecc71", "#95a5a6", "#e74c3c"])
                                            
                                            # Masquer les axes restants non utilisés
                                            for idx in range(num_graphs, num_rows * 3):
                                                row, col = divmod(idx, 3)
                                                axes[row, col].axis("off")

                                            # Ajustement du layout
                                            plt.tight_layout()
                                            st.pyplot(fig)


                                # Affichage des graphiques relatifs à la section Distribution des buts
                                elif section == "Distribution des buts":
                                    distrib_goal_team = get_distribution_goals_season(selected_season) # On récupère nos données

                                    if distrib_goal_team:
                                        # Transformation des données en DataFrame avec les noms de colonnes
                                        distrib_goal_team = pd.DataFrame([
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
                                            for item in distrib_goal_team
                                        ])
                                        distrib_goal_team = distrib_goal_team.iloc[:, 1:]  # Suppression de la colonne "Saison"

                                        for col in distrib_goal_team.columns:
                                            if col != "Équipe":  # Exclure la colonne "Équipe"
                                                distrib_goal_team[col] = pd.to_numeric(distrib_goal_team[col], errors='coerce').astype(float)

                                        # Séparation des données pour l'équipe à domicile et à l'extérieur
                                        distrib_goal_home = distrib_goal_team[distrib_goal_team["Équipe"] == selected_team_home].iloc[:, 1:]
                                        distrib_goal_away = distrib_goal_team[distrib_goal_team["Équipe"] == selected_team_away].iloc[:, 1:]

                                        # Création d'une fonction pour construire les graphiques de distribution de buts par équipe (dans le cas où des buts sont inscrits)
                                        def plot_distribution_graphs(data, title_prefix):
                                            # Vérifier la présence de données non nulles pour chaque graphique
                                            has_goal_scored_half = data.iloc[0, :2].sum() > 0
                                            has_goal_conceded_half = data.iloc[0, 8:10].sum() > 0
                                            has_goal_scored_intervals = data.iloc[0, 2:8].sum() > 0
                                            has_goal_conceded_intervals = data.iloc[0, 10:16].sum() > 0
                                            
                                            # Déterminer le nombre de graphiques à afficher
                                            graphs = [
                                                has_goal_scored_half,
                                                has_goal_conceded_half,
                                                has_goal_scored_intervals,
                                                has_goal_conceded_intervals
                                            ]
                                            
                                            num_graphs = sum(graphs)  # Nombre de graphiques valides
                                            num_rows = (num_graphs + 1) // 2  # Nombre de lignes nécessaires (2 graphiques max par ligne)
                                            
                                            if num_graphs == 0:
                                                st.write(f"Aucune donnée disponible pour {title_prefix}.")
                                                return  # Arrêter la fonction si aucun graphique n'est valide

                                            # Création dynamique des sous-graphiques
                                            fig, axes = plt.subplots(num_rows, 2, figsize=(15, 5 * num_rows))
                                            axes = axes.flatten()  # Transformer la grille en une liste d'axes

                                            idx = 0  # Index pour positionner chaque graphique
                                            
                                            # 1️⃣ Proportion des buts inscrits par période
                                            if has_goal_scored_half:
                                                labels_proportion = ["1ère période", "2ème période"]
                                                values_proportion_goal_scored = data.iloc[0, :2]
                                                axes[idx].pie(values_proportion_goal_scored, labels=labels_proportion, autopct='%1.2f%%', startangle=90, colors=["lightblue", "lightcoral"])
                                                axes[idx].set_title(f"{title_prefix} - Proportion des buts inscrits par période")
                                                idx += 1

                                            # 2️⃣ Proportion des buts concédés par période
                                            if has_goal_conceded_half:
                                                values_proportion_goal_conceded = data.iloc[0, 8:10]
                                                axes[idx].pie(values_proportion_goal_conceded, labels=labels_proportion, autopct='%1.2f%%', startangle=90, colors=["lightblue", "lightcoral"])
                                                axes[idx].set_title(f"{title_prefix} - Proportion des buts concédés par période")
                                                idx += 1

                                            # 3️⃣ Proportion des buts inscrits par intervalle de 15 min
                                            if has_goal_scored_intervals:
                                                labels_intervals = ["0-15 min", "16-30 min", "31-45 min", "46-60 min", "61-75 min", "76-90 min"]
                                                values_intervals_goal_scored = data.iloc[0, 2:8]
                                                colors = ["#D4EFDF", "#A9DFBF", "#F9E79F", "#F5CBA7", "#E59866", "#DC7633"]
                                                bars1 = axes[idx].bar(labels_intervals, values_intervals_goal_scored, color=colors)
                                                axes[idx].set_title(f"{title_prefix} - Proportion des buts inscrits par intervalle de 15 min")
                                                axes[idx].set_ylabel("%")
                                                axes[idx].set_ylim(0, max(values_intervals_goal_scored) + 5)
                                                idx += 1

                                            # 4️⃣ Proportion des buts concédés par intervalle de 15 min
                                            if has_goal_conceded_intervals:
                                                values_intervals_goal_conceded = data.iloc[0, 10:16]
                                                bars2 = axes[idx].bar(labels_intervals, values_intervals_goal_conceded, color=colors)
                                                axes[idx].set_title(f"{title_prefix} - Proportion des buts concédés par intervalle de 15 min")
                                                axes[idx].set_ylabel("%")
                                                axes[idx].set_ylim(0, max(values_intervals_goal_conceded) + 5)
                                                idx += 1

                                            # Supprimer les axes restants s'ils existent
                                            while idx < len(axes):
                                                fig.delaxes(axes[idx])
                                                idx += 1

                                            st.pyplot(fig)  # Affichage du graphique

                                        # Affichage des graphiques dans l'ordre souhaité (équipe à domicile puis celle à l'extérieur)
                                        plot_distribution_graphs(distrib_goal_home, f"{selected_team_home}")
                                        plot_distribution_graphs(distrib_goal_away, f"{selected_team_away}")

                                # Affichage des graphiques relatifs à la section Domicile / Extérieur 
                                elif section == "Domicile / Extérieur":
                                    result_h_a = get_rank_season(selected_season) # Récupération des statistiques sur l'avantage du terrain

                                    if result_h_a:
                                        # Transformation des données en DataFrame avec les noms de colonnes
                                        df_adv_home_away = pd.DataFrame([
                                            {
                                                "Type": item["type"], "Saison": item["season_name"], "Équipe": item["team_name"],"Matches joués": item["matches"],"Victoire": item["wins"],
                                                "Match Nul": item["draws"], "Défaite": item["losses"],"Points": item["points"], "Nbr de points moyen": item["avg_points"],
                                                "Avantage du Terrain": item["home_advantage"]
                                            }
                                            for item in result_h_a
                                        ])

                                        if not df_adv_home_away.empty:
                                            # Sélectionner uniquement les colonnes nécessaires et extraire les proportions en pourcentage
                                            data_team_home = df_adv_home_away[(df_adv_home_away["Type"] == "Home") & (df_adv_home_away["Équipe"] == selected_team_home)]
                                            total_home = data_team_home[["Victoire", "Match Nul", "Défaite"]].sum(axis=1).values[0]
                                            values_proportion_home = (data_team_home[["Victoire", "Match Nul", "Défaite"]].values.flatten() / total_home) * 100  

                                            data_team_away = df_adv_home_away[(df_adv_home_away["Type"] == "Away") & (df_adv_home_away["Équipe"] == selected_team_away)]
                                            total_away = data_team_away[["Victoire", "Match Nul", "Défaite"]].sum(axis=1).values[0]
                                            values_proportion_away = (data_team_away[["Victoire", "Match Nul", "Défaite"]].values.flatten() / total_away) * 100  

                                            # Détermination des valeurs maximales pour l'échelle des jauges
                                            max_adv_home = df_adv_home_away["Avantage du Terrain"].max()
                                            max_adv_away = max_adv_home
                                            max_adv_home = float(max_adv_home)
                                            max_adv_away = float(max_adv_away)

                                            # Extraction et mise à l'échelle de l'avantage du terrain
                                            adv_home = float(data_team_home["Avantage du Terrain"].values[0])
                                            adv_away = float(data_team_away["Avantage du Terrain"].values[0])

                                            # Labels pour les diagrammes
                                            labels_proportion_home = ["Victoire à domicile", "Match Nul", "Défaite à domicile"]
                                            labels_proportion_away = ["Victoire à l'extérieur", "Match Nul", "Défaite à l'extérieur"]

                                            col1, col2 = st.columns(2) # Création des colonnes Streamlit à Domicile

                                            # Fonction pour la jauge de couleur
                                            def get_gauge_color(value, max_value, inverse=False):
                                                if max_value <= 0:
                                                    raise ValueError("max_value doit être supérieur à 0")

                                                ratio = value / max_value
                                                if inverse:
                                                    red = min(max(int(210 * ratio), 0), 255)  # Limiter à 0-255
                                                    green = min(max(int(210 * (1 - ratio)), 0), 255)  # Limiter à 0-255
                                                else:
                                                    red = min(max(int(210 * (1 - ratio)), 0), 255)  # Limiter à 0-255
                                                    green = min(max(int(210 * ratio), 0), 255)  # Limiter à 0-255

                                                return f"rgb({red},{green},0)"

                                            # Création du diagramme circulaire
                                            with col1:
                                                fig1, ax1 = plt.subplots(figsize=(7, 7))  
                                                plot_pie_chart(ax1, values_proportion_home, labels_proportion_home, "Proportion des résultats à Domicile", ["#2ecc71", "#95a5a6", "#e74c3c"])
                                                st.pyplot(fig1)  

                                            # Création de la jauge à domicile
                                            with col2:
                                                fig2 = go.Figure(go.Indicator(
                                                    mode="gauge+number",
                                                    value=adv_home,  
                                                    title={"text": f"Avantage du terrain à Domicile (en %) - {selected_team_home}","font": {"size": 12}},
                                                    gauge={
                                                        "axis": {"range": [0, max_adv_home]},
                                                        "bar": {"color": get_gauge_color(adv_home, max_adv_home)}
                                                    }
                                                ))
                                                st.plotly_chart(fig2)

                                            col3, col4 = st.columns(2) # Création des colonnes Streamlit à l'Extérieur

                                            # Création du diagramme circulaire
                                            with col3:
                                                fig3, ax3 = plt.subplots(figsize=(7, 7))  
                                                plot_pie_chart(ax3, values_proportion_away, labels_proportion_away, "Proportion des résultats à l'Extérieur", ["#2ecc71", "#95a5a6", "#e74c3c"])
                                                st.pyplot(fig3)  

                                            # Création de la jauge à l'extérieur
                                            with col4:
                                                fig4 = go.Figure(go.Indicator(
                                                    mode="gauge+number",
                                                    value=adv_away,  
                                                    title={"text": f"Avantage du terrain à l'Extérieur (en %) - {selected_team_away}" ,"font": {"size": 12}},
                                                    gauge={
                                                        "axis": {"range": [0, max_adv_away]},
                                                        "bar": {"color": get_gauge_color(adv_away, max_adv_away, inverse=True)}
                                                    }
                                                ))
                                                st.plotly_chart(fig4)

                                # Affichage des graphiques relatifs à la section Précédentes confrontations
                                elif section == "Précédentes confrontations":
                                    df_confrontation = get_matches_between_teams(selected_team_home, selected_team_away) # On récupère les données

                                    if df_confrontation:  # Vérifie si la liste n'est pas vide
                                        # Transformation des données en DataFrame avec les noms de colonnes
                                        df_confrontation = pd.DataFrame([
                                            {
                                                "Saison": item["season_name"], "Équipe (Domicile": item["home_team_name"], "Équipe (Extérieur)": item["away_team_name"],
                                                "Score (Domicile)": item["score_home"],"Score (Extérieur)": item["score_away"],"Date du match": item["match_date"]
                                            }
                                            for item in df_confrontation
                                        ])

                                        st.subheader(f"Liste des matchs opposant {selected_team_home} et {selected_team_away}")  # Titre du tableau
                                        st.dataframe(df_confrontation.style.set_properties(**{"text-align": "center"})) # On centre le titre

                                        df_avg_goals_confrontation = get_avg_goals_stats_between_teams(selected_team_home, selected_team_away) # Récupérons les données

                                        df_avg_goals_confrontation = pd.DataFrame([
                                            {
                                                f"Moy. but {selected_team_home}": item["avg_goals_selected_home"], f"Moy. but {selected_team_away}": item["avg_goals_selected_away"],
                                                f"Moy. but {selected_team_home} à domicile": item["avg_goals_home_at_home"],
                                                f"Moy. but {selected_team_away} à l'extérieur": item["avg_goals_away_at_away"]
                                            }
                                            for item in df_avg_goals_confrontation
                                        ])
                                        # Récupérer les valeurs des moyennes en utilisant les noms de colonnes
                                        avg_goals_selected_home = df_avg_goals_confrontation[f"Moy. but {selected_team_home}"].iloc[0]
                                        avg_goals_selected_away = df_avg_goals_confrontation[f"Moy. but {selected_team_away}"].iloc[0]
                                        avg_goals_home_at_home = df_avg_goals_confrontation[f"Moy. but {selected_team_home} à domicile"].iloc[0]
                                        avg_goals_away_at_away = df_avg_goals_confrontation[f"Moy. but {selected_team_away} à l'extérieur"].iloc[0]


                                        # Vérifier si les valeurs sont None, et les remplacer par 0.0 si c'est le cas
                                        avg_goals_selected_home = float(avg_goals_selected_home) if avg_goals_selected_home is not None else 0.0
                                        avg_goals_selected_away = float(avg_goals_selected_away) if avg_goals_selected_away is not None else 0.0
                                        avg_goals_home_at_home = float(avg_goals_home_at_home) if avg_goals_home_at_home is not None else 0.0
                                        avg_goals_away_at_away = float(avg_goals_away_at_away) if avg_goals_away_at_away is not None else 0.0

                                        max_value = max(avg_goals_selected_home, avg_goals_selected_away, avg_goals_home_at_home, avg_goals_away_at_away) # Calculer les limites des jauges

                                        # Fonction pour obtenir la couleur de la jauge (dégradé du rouge au vert)
                                        def get_gauge_color(value, max_value):
                                            ratio = value / max_value
                                            red = int(210 * (1 - ratio))  # Plus la valeur est faible, plus le rouge est intense
                                            green = int(210 * ratio)  # Plus la valeur est haute, plus le vert est intense
                                            return f"rgb({red},{green},0)"  # Retourner la couleur dans le format RGB

                                        col1, col2 = st.columns(2)  # Création des colonnes Streamlit

                                        # Jauge 1: Moyenne des buts inscrits par selected_team_home
                                        with col1:
                                            fig1 = go.Figure(go.Indicator(
                                                mode="gauge+number",
                                                value=avg_goals_selected_home,
                                                gauge={
                                                    "axis": {"range": [None, max_value]},  # Plage de la jauge
                                                    "bar": {"color": get_gauge_color(avg_goals_selected_home, max_value)},  # Utiliser la fonction de couleur
                                                    "steps": [
                                                        {"range": [0, avg_goals_selected_home], "color": get_gauge_color(avg_goals_selected_home, max_value)},  # Partie colorée en fonction de la valeur
                                                        {"range": [avg_goals_selected_home, max_value], "color": 'white'}  # Partie vide pour le reste
                                                    ]
                                                },
                                                title={"text": f"<b style='font-size: 16px;'>{selected_team_home} - Moyenne des buts</b>"},
                                                number={"suffix": " buts", "font": {"size": 20}}  # Afficher la valeur au centre
                                            ))
                                            st.plotly_chart(fig1)

                                        # Jauge 2: Moyenne des buts inscrits par selected_team_away
                                        with col2:
                                            fig2 = go.Figure(go.Indicator(
                                                mode="gauge+number",
                                                value=avg_goals_selected_away,
                                                gauge={
                                                    "axis": {"range": [None, max_value]},  # Plage de la jauge
                                                    "bar": {"color": get_gauge_color(avg_goals_selected_away, max_value)},  # Utiliser la fonction de couleur
                                                    "steps": [
                                                        {"range": [0, avg_goals_selected_away], "color": get_gauge_color(avg_goals_selected_away, max_value)},  # Partie colorée en fonction de la valeur
                                                        {"range": [avg_goals_selected_away, max_value], "color": 'white'}  # Partie vide pour le reste
                                                    ]
                                                },
                                                title={"text": f"<b style='font-size: 16px;'>{selected_team_away} - Moyenne des buts</b>"},
                                                number={"suffix": " buts", "font": {"size": 20}}  # Afficher la valeur au centre
                                            ))
                                            st.plotly_chart(fig2)

                                        # Jauge 3: Moyenne des buts inscrits par selected_team_home contre selected_team_away chez selected_team_home
                                        with col1:
                                            fig3 = go.Figure(go.Indicator(
                                                mode="gauge+number",
                                                value=avg_goals_home_at_home,
                                                gauge={
                                                    "axis": {"range": [None, max_value]},  # Plage de la jauge
                                                    "bar": {"color": get_gauge_color(avg_goals_home_at_home, max_value)},  # Utiliser la fonction de couleur
                                                    "steps": [
                                                        {"range": [0, avg_goals_home_at_home], "color": get_gauge_color(avg_goals_home_at_home, max_value)},  # Partie colorée en fonction de la valeur
                                                        {"range": [avg_goals_home_at_home, max_value], "color": 'white'}  # Partie vide pour le reste
                                                    ]
                                                },
                                                title={"text": f"<b style='font-size: 16px;'>{selected_team_home} - Moyenne des buts à domicile</b>"},
                                                number={"suffix": " buts", "font": {"size": 20}}  # Afficher la valeur au centre
                                            ))
                                            st.plotly_chart(fig3)

                                        # Jauge 4: Moyenne des buts inscrits par selected_team_away contre selected_team_home chez selected_team_away
                                        with col2:
                                            fig4 = go.Figure(go.Indicator(
                                                mode="gauge+number",
                                                value=avg_goals_away_at_away,
                                                gauge={
                                                    "axis": {"range": [None, max_value]},  # Plage de la jauge
                                                    "bar": {"color": get_gauge_color(avg_goals_away_at_away, max_value)},  # Utiliser la fonction de couleur
                                                    "steps": [
                                                        {"range": [0, avg_goals_away_at_away], "color": get_gauge_color(avg_goals_away_at_away, max_value)},  # Partie colorée en fonction de la valeur
                                                        {"range": [avg_goals_away_at_away, max_value], "color": 'white'}  # Partie vide pour le reste
                                                    ]
                                                },
                                                title={"text": f"<b style='font-size: 16px;'>{selected_team_away} - Moyenne des buts à l'extérieur</b>"},
                                                number={"suffix": " buts", "font": {"size": 20}}  # Afficher la valeur au centre
                                            ))
                                            st.plotly_chart(fig4)

                                        
                                        df_first_goal_confrontation = get_1st_goal_stats_between_teams(selected_team_home, selected_team_away) # On récupére les données

                                        if df_first_goal_confrontation :
                                            # Transformation du dataframe en fonction du nom des colonnes
                                            df_first_goal_confrontation = pd.DataFrame([
                                                {
                                                    "Équipe": item["team"], f"{selected_team_home} - 1er but inscrit": item["proportion_1st_goal_for"],"Aucun but": item["proportion_no_goal"],
                                                    f"{selected_team_away} - 1er but inscrit": item["proportion_1st_goal_against"],
                                                    f"{selected_team_home} - 1er but inscrit / Victoire": item["proportion_1st_goal_win"],
                                                    f"{selected_team_home} - 1er but inscrit / Nul": item["proportion_1st_goal_draw"],
                                                    f"{selected_team_home} - 1er but inscrit / Défaite": item["proportion_1st_goal_lose"],                                           
                                                    f"{selected_team_home} - 1er but encaissé / Victoire": item["proportion_1st_goal_conceded_win"],
                                                    f"{selected_team_home} - 1er but encaissé / Nul": item["proportion_1st_goal_conceded_draw"],
                                                    f"{selected_team_home} - 1er but encaissé / Défaite": item["proportion_1st_goal_conceded_lose"],
                                                }
                                                for item in df_first_goal_confrontation
                                            ])
                                            # Conversion des valeurs en float
                                            for col in df_first_goal_confrontation.columns:
                                                if col != "Équipe":  # Exclure la colonne "Équipe"
                                                    df_first_goal_confrontation[col] = pd.to_numeric(df_first_goal_confrontation[col], errors='coerce') 
                                                    df_first_goal_confrontation[col] = df_first_goal_confrontation[col].astype(float).mul(100) # Transformation en flottant

                                            # Séparation des données pour domicile et extérieur
                                            df_home = df_first_goal_confrontation[df_first_goal_confrontation["Équipe"] == selected_team_home].iloc[:, 1:] 

                                            fig, axes = plt.subplots(1, 3, figsize=(15, 7))  # 1 ligne et 3 colonnes

                                            # Graphique 1 : 1er but inscrit
                                            plot_pie_chart(
                                                axes[0],
                                                df_home.iloc[0, :3],
                                                ["1er but inscrit", "Aucun but", "1er but encaissé"],
                                                f"{selected_team_home} - 1er but inscrit",
                                                ["#2ecc71", "#95a5a6", "#e74c3c"]
                                            )

                                            # Graphique 2 : Résultats après 1er but inscrit
                                            plot_pie_chart(
                                                axes[1],
                                                df_home.iloc[0, 3:6],
                                                ["Victoire", "Nul", "Défaite"],
                                                f"{selected_team_home} - Résultats après 1er but inscrit",
                                                ["#2ecc71", "#f1c40f", "#e74c3c"]
                                            )

                                            # Graphique 3 : Résultats après 1er but encaissé
                                            plot_pie_chart(
                                                axes[2],
                                                df_home.iloc[0, 6:],
                                                ["Victoire", "Nul", "Défaite"],
                                                f"{selected_team_home} - Résultats après 1er but encaissé",
                                                ["#2ecc71", "#f1c40f", "#e74c3c"]
                                            )

                                            plt.tight_layout()  # Ajuste l'affichage pour éviter les chevauchements
                                            st.pyplot(fig)  # Afficher la figure

                                        distrib_goal_between_team = get_distrib_goal_between_teams(selected_team_home, selected_team_away) # On récupère nos données

                                        if distrib_goal_between_team:
                                            # Transformation du dataframe en fonction du nom des colonnes
                                            distrib_goal_between_team = pd.DataFrame([
                                                {
                                                    "Équipe": item["team"], "1ère période (Buts inscrits)": item["proportion_0_45"],"2ème période (Buts inscrits)": item["proportion_46_90"],
                                                    "0-15 min (Buts inscrits)": item["proportion_0_15"], "16-30 min (Buts inscrits)": item["proportion_16_30"],
                                                    "31-45 min (Buts inscrits)": item["proportion_31_45"], "46-60 min (Buts inscrits)": item["proportion_46_60"],                                           
                                                    "61-75 min (Buts inscrits)": item["proportion_61_75"], "76-90 min (Buts inscrits)": item["proportion_76_90"]                                        }
                                                for item in distrib_goal_between_team
                                            ])
                                            for col in distrib_goal_between_team.columns:
                                                if col != "Équipe":  # Exclure la colonne "Équipe"
                                                    distrib_goal_between_team[col] = pd.to_numeric(distrib_goal_between_team[col], errors='coerce').astype(float)

                                            # Séparation des données pour l'équipe à domicile et à l'extérieur
                                            distrib_goal_team_home = distrib_goal_between_team[distrib_goal_between_team["Équipe"] == selected_team_home].iloc[:, 1:]
                                            distrib_goal_team_away = distrib_goal_between_team[distrib_goal_between_team["Équipe"] == selected_team_away].iloc[:, 1:]
                                            
                                            # Création d'une fonction pour générer les graphiques de distribution de buts par équipe
                                            def plot_distribution_graphs(data, title_prefix):
                                                total_goals = data.sum().sum()
                                                
                                                # Si aucun but n'est inscrit, on n'affiche pas de tableau de buts
                                                if total_goals == 0:
                                                    return

                                                fig, axes = plt.subplots(1, 2, figsize=(15, 5))
                                                
                                                # Proportions des buts inscrits par période
                                                labels_proportion = ["1ère période", "2ème période"]
                                                values_proportion_goal_scored = data.iloc[0, :2]
                                                axes[0].pie(values_proportion_goal_scored, labels=labels_proportion, autopct='%1.2f%%', startangle=90, colors=["lightblue", "lightcoral"])
                                                axes[0].set_title(f"{title_prefix} - Proportion des buts inscrits par période")
                                                
                                                # Proportions des buts inscrits par intervalle de 15 min
                                                labels_intervals = ["0-15 min", "16-30 min", "31-45 min", "46-60 min", "61-75 min", "76-90 min"]
                                                values_intervals_goal_scored = data.iloc[0, 2:8]
                                                colors = ["#D4EFDF", "#A9DFBF", "#F9E79F", "#F5CBA7", "#E59866", "#DC7633"]
                                                bars = axes[1].bar(labels_intervals, values_intervals_goal_scored, color=colors)
                                                axes[1].set_title(f"{title_prefix} - Proportion des buts inscrits par intervalle de 15 min")
                                                axes[1].set_ylabel("%")
                                                axes[1].set_ylim(0, max(values_intervals_goal_scored) + 5)
                                                
                                                # Ajout des valeurs sur les barres
                                                for bar in bars:
                                                    yval = bar.get_height()
                                                    axes[1].text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval:.2f}%', ha='center', color='black')
                                                
                                                st.pyplot(fig) # Affichage du tableau

                                            # Affichage des graphiques dans l'ordre souhaité (équipe à domicile puis celle à l'extérieur)
                                            plot_distribution_graphs(distrib_goal_team_home, f"{selected_team_home}")
                                            plot_distribution_graphs(distrib_goal_team_away, f"{selected_team_away}")

                                        result_h_a_between_teams = get_home_away_selected_teams(selected_team_home, selected_team_away) # Récupération des statistiques sur l'avantage du terrain

                                        if result_h_a_between_teams:
                                            # Transformation du dataframe en fonction des noms de colonnes
                                            df_adv_home_away_team = pd.DataFrame([
                                                {
                                                    "Équipe": item["team_name"], "Victoire à Domicile": item["home_win"],"Match Nul à Domicile": item["home_draws"],
                                                    "Défaite à Domicile": item["home_losses"], "Avantage du Terrain": item["home_advantage"],
                                                    "Victoire": item["total_wins"], "Match Nul": item["total_draws"], "Défaite": item["total_losses"]                                      }
                                                for item in result_h_a_between_teams
                                            ])
                                            df_adv_home_away_team = df_adv_home_away_team[df_adv_home_away_team["Équipe"] == selected_team_home].iloc[:, 1:] # On filtre pour l'équipe cible

                                            if not df_adv_home_away_team.empty:
                                                # Sélectionner uniquement les colonnes nécessaires et extraire les proportions en pourcentage
                                                total = df_adv_home_away_team[["Victoire", "Match Nul", "Défaite"]].sum(axis=1).values[0]
                                                values_proportion = (df_adv_home_away_team[["Victoire", "Match Nul", "Défaite"]].values.flatten() / total) * 100  

                                                total_home = df_adv_home_away_team[["Victoire à Domicile", "Match Nul à Domicile", "Défaite à Domicile"]].sum(axis=1).values[0]
                                                values_proportion_home = (df_adv_home_away_team[["Victoire à Domicile", "Match Nul à Domicile", "Défaite à Domicile"]].values.flatten() / total_home) * 100  

                                                adv_home = float(df_adv_home_away_team["Avantage du Terrain"].values[0]) # Extraction et mise à l'échelle de l'avantage du terrain

                                                # Fonction pour construire les camemberts en omettant les labels vides
                                                def plot_filtered_pie(ax, values, labels, title, colors, text_size=6):
                                                    mask = values > 0  # Filtrer les catégories avec une valeur > 0
                                                    filtered_values = values[mask]
                                                    filtered_labels = [label for label, m in zip(labels, mask) if m]
                                                    filtered_colors = [color for color, m in zip(colors, mask) if m]  # Garder les bonnes couleurs

                                                    if filtered_values.sum() > 0:
                                                        wedges, texts, autotexts = ax.pie(
                                                            filtered_values, labels=filtered_labels, autopct='%1.2f%%', startangle=90, colors=filtered_colors,
                                                            textprops={'fontsize': text_size}
                                                        )
                                                        for text in texts:
                                                            text.set_fontsize(text_size)
                                                        for autotext in autotexts:
                                                            autotext.set_fontsize(text_size)

                                                        ax.set_title(title, fontsize=text_size)
                                                    else:
                                                        ax.axis('off')  # Masquer l'axe si aucune donnée n'est disponible

                                                # Première ligne : Diagramme circulaire général
                                                with st.container():
                                                    col1 = st.columns(1)  
                                                    with col1[0]:
                                                        fig1, ax1 = plt.subplots(figsize=(3, 3))
                                                        plot_filtered_pie(
                                                            ax1,
                                                            values_proportion,
                                                            ["Victoire", "Match Nul", "Défaite"],
                                                            f"Proportion des résultats de {selected_team_home} contre {selected_team_away} (tous matchs confondus)",
                                                            ["#2ecc71", "#95a5a6", "#e74c3c"]
                                                        )
                                                        st.pyplot(fig1)

                                                # Deuxième ligne : Résultats à domicile + Jauge
                                                if total_home != 0:  # Vérifier si les statistiques à domicile existent
                                                    with st.container():
                                                        col2, col3 = st.columns(2)

                                                        with col2:
                                                            fig2, ax2 = plt.subplots(figsize=(7, 7))
                                                            plot_filtered_pie(
                                                                ax2,
                                                                values_proportion_home,
                                                                ["Victoire à domicile", "Match Nul", "Défaite à domicile"],
                                                                f"Proportion des résultats à Domicile de {selected_team_home} contre {selected_team_away}",
                                                                ["#2ecc71", "#95a5a6", "#e74c3c"]
                                                            )
                                                            st.pyplot(fig2)

                                                        def get_gauge_color(value):
                                                            if not (0 <= value <= 100):
                                                                raise ValueError("La valeur doit être comprise entre 0 et 100")
                                                            ratio = value / 100
                                                            red = int(210 * (1 - ratio))
                                                            green = int(210 * ratio)
                                                            return f"rgb({red},{green},0)"

                                                        with col3:
                                                            fig3 = go.Figure(go.Indicator(
                                                                mode="gauge+number",
                                                                value=adv_home,
                                                                title={"text": f"Avantage du terrain à Domicile (en %) de {selected_team_home} contre {selected_team_away}", "font": {"size": 10}},
                                                                gauge={"axis": {"range": [0, 100]}, "bar": {"color": get_gauge_color(adv_home)}}
                                                            ))
                                                            st.plotly_chart(fig3)

                                    else:
                                        st.warning(f"Aucun match opposant {selected_team_home} et {selected_team_away} dans la base de données.")

        # Affichage de l’image uniquement si aucun choix n'a été fait
        if show_image:
            st.image(image_path)

    else:
        st.title("🥊 H2H analysis") # Title

        # Checks if the user has made a selection (team, season and section)
        show_image = True  # By default, we display the image

        image_path = os.path.join(os.path.dirname(__file__), "image", "banniere_confrontation.jpg") # Bulding the path

        st.sidebar.header("🔍 Team selection") # Selecting the competition in the sidebar
        teams_available = get_teams() # Retrieving teams available

        # Loop to select the teams of his choice present in the database
        if teams_available:
            selected_team_home = st.sidebar.selectbox("Choose a team (Home) :", ["Select a team"] + teams_available, index=0)
            
            if selected_team_home != "Select a team":
                seasons_available = get_seasons(selected_team_home)
                
                if seasons_available: # Selection of the season
                    selected_season = st.sidebar.selectbox("Choose a season :", ["Select a season"] + seasons_available, index=0)
                    
                    if selected_season != "Select a season":
                        teams_in_season = get_teams_in_season(selected_season)

                        teams_in_season = [
                            team['team_name'] 
                            for team in get_teams_in_season(selected_season) 
                            if team['team_name'] != selected_team_home
                        ]
                        
                        if teams_in_season: # Selecting the 2nd team
                            selected_team_away = st.sidebar.selectbox("Choose a team (Away) :", ["Select a team"] + teams_in_season, index=0)
                            
                            if selected_team_away != "Select a team":
                                st.sidebar.header("📊 Select a analysis")
                                section = st.sidebar.radio("Sections", ["General statistics", "1st goal scored", "Goal distribution", "Home / Away", "Previous confrontations"])

                                # If a section is selected, we hide the image
                                if section:
                                    show_image = False 
                                st.subheader(f"📌 {section} - {selected_team_home} (Domicile) vs {selected_team_away} (Extérieur) - {selected_season}") # Summary choices
                        
                                # Display of graphs related to the General Statistics section
                                if section == "General statistics":
                                    avg_goal_stats = get_avg_goals_stats(selected_season) # Fetching data
                                    if avg_goal_stats:
                                        # Transforming data into a DataFrame with column names
                                        df_goals = pd.DataFrame([
                                            {
                                                "Season": item["season_name"], "Team": item["team_name"], "Goals/Match": item["avg_goals_per_match"],
                                                "Goals Scored/Match": item["avg_team_goals_per_match"], "Goals Conceded/Match": item["avg_team_goals_conceded_per_match"],
                                                "Home Goals Scored/Match": item["avg_team_home_goals"], "Away Goals Scored/Match": item["avg_team_away_goals"],
                                                "Home Goals Conceded/Match": item["avg_conceded_home_goals"], "Away Goals Conceded/Match": item["avg_conceded_away_goals"]
                                            }
                                            for item in avg_goal_stats
                                        ])
                                        # Filtering data by team
                                        df_home = df_goals[df_goals["Team"] == selected_team_home]
                                        df_away = df_goals[df_goals["Team"] == selected_team_away]
                                        
                                        if not df_home.empty and not df_away.empty:
                                            # Display the title
                                            st.markdown(
                                                f"<h3 style='text-align: center;'>{selected_team_home} vs {selected_team_away}: Goals (Scored or Conceded)</h3>",
                                                unsafe_allow_html=True
                                            )
                                            col1, col2, col3, col4 = st.columns(4) # 1st row of graphs on goals scored and conceded
                                            with col1:
                                                st.plotly_chart(plot_gauge(df_home["Goals Scored/Match"].values[0], df_goals["Goals Scored/Match"].max(), f"{selected_team_home}: Goals Scored"))
                                            with col2:
                                                st.plotly_chart(plot_gauge(df_home["Goals Conceded/Match"].values[0], df_goals["Goals Conceded/Match"].max(), f"{selected_team_home}: Goals Conceded", inverse=True))
                                            with col3:
                                                st.plotly_chart(plot_gauge(df_away["Goals Scored/Match"].values[0], df_goals["Goals Scored/Match"].max(), f"{selected_team_away}: Goals Scored"))
                                            with col4:
                                                st.plotly_chart(plot_gauge(df_away["Goals Conceded/Match"].values[0], df_goals["Goals Conceded/Match"].max(), f"{selected_team_away}: Goals Conceded", inverse=True))
                                            
                                            st.markdown(
                                                f"<h3 style='text-align: center;'>Home Performance for {selected_team_home} and Away Performance for {selected_team_away}</h3>",
                                                unsafe_allow_html=True
                                            )
                                            col5, col6, col7, col8 = st.columns(4) # 2nd row of graphs on goals scored and conceded depending on Home/Away
                                            with col5:
                                                st.plotly_chart(plot_gauge(df_home["Home Goals Scored/Match"].values[0], df_goals["Home Goals Scored/Match"].max(), f"{selected_team_home}: Home Goals Scored"))
                                            with col6:
                                                st.plotly_chart(plot_gauge(df_home["Home Goals Conceded/Match"].values[0], df_goals["Home Goals Conceded/Match"].max(), f"{selected_team_home}: Home Goals Conceded", inverse=True))
                                            with col7:
                                                st.plotly_chart(plot_gauge(df_away["Away Goals Scored/Match"].values[0], df_goals["Away Goals Scored/Match"].max(), f"{selected_team_away}: Away Goals Scored"))
                                            with col8:
                                                st.plotly_chart(plot_gauge(df_away["Away Goals Conceded/Match"].values[0], df_goals["Away Goals Conceded/Match"].max(), f"{selected_team_away}: Away Goals Conceded", inverse=True))

                                # Display of graphs related to the First Goal section
                                if section == "1st goal scored":
                                    first_goal_stats = get_first_goal_season(selected_season) # Fetching data
                                    if first_goal_stats:
                                        # Transforming data into a DataFrame with column names
                                        df_first_goal = pd.DataFrame([
                                            {
                                                "Season": item["season_name"], "Team": item["team_name"],
                                                "First Goal Scored": item["proportion_1st_goal_for"], "No Goal": item["proportion_no_goal"], "First Goal Conceded": item["proportion_1st_goal_against"],
                                                "Home / First Goal Scored": item["proportion_1st_goal_home_for"], "Home / No Goal": item["proportion_no_goal_home"], "Home / First Goal Conceded": item["proportion_1st_goal_home_against"],
                                                "Away / First Goal Scored": item["proportion_1st_goal_away_for"], "Away / No Goal": item["proportion_no_goal_away"], "Away / First Goal Conceded": item["proportion_1st_goal_away_against"],
                                                "First Goal Scored / Win": item["first_goal_win"], "First Goal Scored / Draw": item["first_goal_draw"], "First Goal Scored / Loss": item["first_goal_lose"],
                                                "Home / First Goal Scored / Win": item["proportion_1st_goal_home_win"], "Home / First Goal Scored / Draw": item["proportion_1st_goal_home_draw"], "Home / First Goal Scored / Loss": item["proportion_1st_goal_home_lose"],
                                                "Away / First Goal Scored / Win": item["proportion_1st_goal_away_win"], "Away / First Goal Scored / Draw": item["proportion_1st_goal_away_draw"], "Away / First Goal Scored / Loss": item["proportion_1st_goal_away_lose"],
                                                "First Goal Conceded / Win": item["first_goal_conceded_win"], "First Goal Conceded / Draw": item["first_goal_conceded_draw"], "First Goal Conceded / Loss": item["first_goal_conceded_lose"],
                                                "Home / First Goal Conceded / Win": item["proportion_1st_goal_conceded_home_win"], "Home / First Goal Conceded / Draw": item["proportion_1st_goal_conceded_home_draw"], "Home / First Goal Conceded / Loss": item["proportion_1st_goal_conceded_home_lose"],
                                                "Away / First Goal Conceded / Win": item["proportion_1st_goal_conceded_away_win"], "Away / First Goal Conceded / Draw": item["proportion_1st_goal_conceded_away_draw"], "Away / First Goal Conceded / Loss": item["proportion_1st_goal_conceded_away_lose"]
                                            }
                                            for item in first_goal_stats
                                        ])
                                        # Converting values to float
                                        for col in df_first_goal.columns:
                                            if col != "Team" and col != "Season":  # Exclude text columns "Team" and "Season"
                                                df_first_goal[col] = pd.to_numeric(df_first_goal[col], errors='coerce')
                                                df_first_goal[col] = df_first_goal[col].astype(float) # Transform numerical values to float
                                        
                                        # Separating data for home and away teams
                                        df_home = df_first_goal[df_first_goal["Team"] == selected_team_home].iloc[:, 2:]
                                        df_away = df_first_goal[df_first_goal["Team"] == selected_team_away].iloc[:, 2:]

                                        # List of non-empty graphs
                                        graphs_to_plot = [
                                            (df_home.iloc[0, :3], ["First Goal Scored", "No Goal", "First Goal Conceded"], f"First Goal - {selected_team_home}"),
                                            (df_home.iloc[0, 9:12], ["Win", "Draw", "Loss"], f"Results After First Goal Scored - {selected_team_home}"),
                                            (df_home.iloc[0, 18:21], ["Win", "Draw", "Loss"], f"Results After First Goal Conceded - {selected_team_home}"),
                                            (df_home.iloc[0, 3:6], ["First Goal Scored", "No Goal", "First Goal Conceded"], f"Home Results - {selected_team_home}"),
                                            (df_home.iloc[0, 12:15], ["Home / Win", "Home / Draw", "Home / Loss"], f"Home After First Goal Scored - {selected_team_home}"),
                                            (df_home.iloc[0, 21:24], ["Win", "Draw", "Loss"], f"Home After First Goal Conceded - {selected_team_home}"),
                                            (df_away.iloc[0, :3], ["First Goal Scored", "No Goal", "First Goal Conceded"], f"First Goal - {selected_team_away}"),
                                            (df_away.iloc[0, 9:12], ["Win", "Draw", "Loss"], f"Results After First Goal Scored - {selected_team_away}"),
                                            (df_away.iloc[0, 18:21], ["Win", "Draw", "Loss"], f"Results After First Goal Conceded - {selected_team_away}"),
                                            (df_away.iloc[0, 6:9], ["First Goal Scored", "No Goal", "First Goal Conceded"], f"Away Results - {selected_team_away}"),
                                            (df_away.iloc[0, 15:18], ["Away / Win", "Away / Draw", "Away / Loss"], f"Away After First Goal Scored - {selected_team_away}"),
                                            (df_away.iloc[0, 24:], ["Win", "Draw", "Loss"], f"Away After First Goal Conceded - {selected_team_away}")
                                        ]

                                        # Filter graphs with non-null data
                                        graphs_to_plot = [graph for graph in graphs_to_plot if graph[0].sum() > 0]

                                        # Determine the number of rows needed (3 graphs per row)
                                        num_graphs = len(graphs_to_plot)
                                        num_rows = -(-num_graphs // 3)  # Equivalent to math.ceil(num_graphs / 3)

                                        if num_rows == 0:
                                            st.write("No data available to display the charts.")
                                        else:
                                            # Create subplots
                                            fig, axes = plt.subplots(num_rows, 3, figsize=(18, 4 * num_rows))
                                            axes = np.atleast_2d(axes)  # Ensure a 2D structure even if num_rows == 1

                                            # Fill the subplots
                                            for idx, (data, labels, title) in enumerate(graphs_to_plot):
                                                row, col = divmod(idx, 3)  # Convert index to (row, column) position
                                                plot_pie_chart(axes[row, col], data, labels, title, ["#2ecc71", "#95a5a6", "#e74c3c"])
                                            
                                            # Hide unused axes
                                            for idx in range(num_graphs, num_rows * 3):
                                                row, col = divmod(idx, 3)
                                                axes[row, col].axis("off")

                                            # Adjust layout
                                            plt.tight_layout()
                                            st.pyplot(fig)

                                # Display of graphs related to the Goal Distribution section
                                elif section == "Goal distribution":
                                    distrib_goal_team = get_distribution_goals_season(selected_season) # Fetching data

                                    if distrib_goal_team:
                                        # Transforming data into a DataFrame with column names
                                        distrib_goal_team = pd.DataFrame([
                                            {
                                                "Season": item["season_name"], "Team": item["team_name"], "1st Half (Proportion Goals Scored)": item["proportion_buts_inscrit_1ere_periode"],
                                                "2nd Half (Proportion Goals Scored)": item["proportion_buts_inscrit_2nde_periode"], "0-15 min (Proportion Goals Scored)": item["proportion_buts_0_15"],
                                                "16-30 min (Proportion Goals Scored)": item["proportion_buts_16_30"], "31-45 min (Proportion Goals Scored)": item["proportion_buts_31_45"],
                                                "46-60 min (Proportion Goals Scored)": item["proportion_buts_46_60"], "61-75 min (Proportion Goals Scored)": item["proportion_buts_61_75"],
                                                "76-90 min (Proportion Goals Scored)": item["proportion_buts_76_90"], "1st Half (Proportion Goals Conceded)": item["proportion_buts_encaissés_1ere_periode"],
                                                "2nd Half (Proportion Goals Conceded)": item["proportion_buts_encaissés_2nde_periode"], "0-15 min (Proportion Goals Conceded)": item["proportion_buts_encaissés_0_15"],
                                                "16-30 min (Proportion Goals Conceded)": item["proportion_buts_encaissés_16_30"], "31-45 min (Proportion Goals Conceded)": item["proportion_buts_encaissés_31_45"],
                                                "46-60 min (Proportion Goals Conceded)": item["proportion_buts_encaissés_46_60"], "61-75 min (Proportion Goals Conceded)": item["proportion_buts_encaissés_61_75"],
                                                "76-90 min (Proportion Goals Conceded)": item["proportion_buts_encaissés_76_90"], "1st Half (Goals Scored)": item["buts_inscrit_1ere_periode"],
                                                "2nd Half (Goals Scored)": item["buts_inscrit_2nde_periode"], "0-15 min (Goals Scored)": item["nbr_buts_0_15"], "16-30 min (Goals Scored)": item["nbr_buts_16_30"],
                                                "31-45 min (Goals Scored)": item["nbr_buts_31_45"], "46-60 min (Goals Scored)": item["nbr_buts_46_60"], "61-75 min (Goals Scored)": item["nbr_buts_61_75"],
                                                "76-90 min (Goals Scored)": item["nbr_buts_76_90"], "1st Half (Goals Conceded)": item["buts_encaissés_1ere_periode"],
                                                "2nd Half (Goals Conceded)": item["buts_encaissés_2nde_periode"], "0-15 min (Goals Conceded)": item["buts_encaissés_0_15"], "16-30 min (Goals Conceded)": item["buts_encaissés_16_30"],
                                                "31-45 min (Goals Conceded)": item["buts_encaissés_31_45"], "46-60 min (Goals Conceded)": item["buts_encaissés_46_60"],
                                                "61-75 min (Goals Conceded)": item["buts_encaissés_61_75"], "76-90 min (Goals Conceded)": item["buts_encaissés_76_90"]
                                            }
                                            for item in distrib_goal_team
                                        ])
                                        distrib_goal_team = distrib_goal_team.iloc[:, 1:]  # Removing the "Season" column

                                        for col in distrib_goal_team.columns:
                                            if col != "Team":  # Exclude "Team" column
                                                distrib_goal_team[col] = pd.to_numeric(distrib_goal_team[col], errors='coerce').astype(float)

                                        # Separating data for home and away teams
                                        distrib_goal_home = distrib_goal_team[distrib_goal_team["Team"] == selected_team_home].iloc[:, 1:]
                                        distrib_goal_away = distrib_goal_team[distrib_goal_team["Team"] == selected_team_away].iloc[:, 1:]

                                        # Creating a function to build goal distribution graphs by team (if goals are scored)
                                        def plot_distribution_graphs(data, title_prefix):
                                            # Check for non-null data for each graph
                                            has_goal_scored_half = data.iloc[0, :2].sum() > 0
                                            has_goal_conceded_half = data.iloc[0, 8:10].sum() > 0
                                            has_goal_scored_intervals = data.iloc[0, 2:8].sum() > 0
                                            has_goal_conceded_intervals = data.iloc[0, 10:16].sum() > 0
                                            
                                            # Determine how many graphs to display
                                            graphs = [
                                                has_goal_scored_half,
                                                has_goal_conceded_half,
                                                has_goal_scored_intervals,
                                                has_goal_conceded_intervals
                                            ]
                                            
                                            num_graphs = sum(graphs)  # Number of valid graphs
                                            num_rows = (num_graphs + 1) // 2  # Number of rows needed (2 graphs max per row)
                                            
                                            if num_graphs == 0:
                                                st.write(f"No data available for {title_prefix}.")
                                                return  # Stop the function if no valid graph

                                            # Dynamic creation of subplots
                                            fig, axes = plt.subplots(num_rows, 2, figsize=(15, 5 * num_rows))
                                            axes = axes.flatten()  # Flatten the grid into a list of axes

                                            idx = 0  # Index for positioning each graph
                                            
                                            # 1️⃣ Proportion of goals scored per half
                                            if has_goal_scored_half:
                                                labels_proportion = ["1st Half", "2nd Half"]
                                                values_proportion_goal_scored = data.iloc[0, :2]
                                                axes[idx].pie(values_proportion_goal_scored, labels=labels_proportion, autopct='%1.2f%%', startangle=90, colors=["lightblue", "lightcoral"])
                                                axes[idx].set_title(f"{title_prefix} - Proportion of Goals Scored per Half")
                                                idx += 1

                                            # 2️⃣ Proportion of goals conceded per half
                                            if has_goal_conceded_half:
                                                values_proportion_goal_conceded = data.iloc[0, 8:10]
                                                axes[idx].pie(values_proportion_goal_conceded, labels=labels_proportion, autopct='%1.2f%%', startangle=90, colors=["lightblue", "lightcoral"])
                                                axes[idx].set_title(f"{title_prefix} - Proportion of Goals Conceded per Half")
                                                idx += 1

                                            # 3️⃣ Proportion of goals scored by 15-minute intervals
                                            if has_goal_scored_intervals:
                                                labels_intervals = ["0-15 min", "16-30 min", "31-45 min", "46-60 min", "61-75 min", "76-90 min"]
                                                values_intervals_goal_scored = data.iloc[0, 2:8]
                                                colors = ["#D4EFDF", "#A9DFBF", "#F9E79F", "#F5CBA7", "#E59866", "#DC7633"]
                                                axes[idx].bar(labels_intervals, values_intervals_goal_scored, color=colors)
                                                axes[idx].set_title(f"{title_prefix} - Proportion of Goals Scored per 15-Minute Interval")
                                                axes[idx].set_ylabel("%")
                                                axes[idx].set_ylim(0, max(values_intervals_goal_scored) + 5)
                                                idx += 1

                                            # 4️⃣ Proportion of goals conceded by 15-minute intervals
                                            if has_goal_conceded_intervals:
                                                values_intervals_goal_conceded = data.iloc[0, 10:16]
                                                axes[idx].bar(labels_intervals, values_intervals_goal_conceded, color=colors)
                                                axes[idx].set_title(f"{title_prefix} - Proportion of Goals Conceded per 15-Minute Interval")
                                                axes[idx].set_ylabel("%")
                                                axes[idx].set_ylim(0, max(values_intervals_goal_conceded) + 5)
                                                idx += 1

                                            # Hide remaining empty axes
                                            while idx < len(axes):
                                                fig.delaxes(axes[idx])
                                                idx += 1

                                            st.pyplot(fig)  # Display the figure

                                        # Display graphs in the desired order (home team first, then away team)
                                        plot_distribution_graphs(distrib_goal_home, f"{selected_team_home}")
                                        plot_distribution_graphs(distrib_goal_away, f"{selected_team_away}")

                                # Display of graphs related to the Home / Away section
                                elif section == "Home / Away":
                                    result_h_a = get_rank_season(selected_season) # Fetching home advantage statistics

                                    if result_h_a:
                                        # Transforming data into a DataFrame with column names
                                        df_adv_home_away = pd.DataFrame([
                                            {
                                                "Type": item["type"], "Season": item["season_name"], "Team": item["team_name"], "Matches Played": item["matches"], "Wins": item["wins"],
                                                "Draws": item["draws"], "Losses": item["losses"], "Points": item["points"], "Average Points": item["avg_points"],
                                                "Home Advantage": item["home_advantage"]
                                            }
                                            for item in result_h_a
                                        ])

                                        if not df_adv_home_away.empty:
                                            # Select only the necessary columns and extract percentages
                                            data_team_home = df_adv_home_away[(df_adv_home_away["Type"] == "Home") & (df_adv_home_away["Team"] == selected_team_home)]
                                            total_home = data_team_home[["Wins", "Draws", "Losses"]].sum(axis=1).values[0]
                                            values_proportion_home = (data_team_home[["Wins", "Draws", "Losses"]].values.flatten() / total_home) * 100

                                            data_team_away = df_adv_home_away[(df_adv_home_away["Type"] == "Away") & (df_adv_home_away["Team"] == selected_team_away)]
                                            total_away = data_team_away[["Wins", "Draws", "Losses"]].sum(axis=1).values[0]
                                            values_proportion_away = (data_team_away[["Wins", "Draws", "Losses"]].values.flatten() / total_away) * 100

                                            # Determine maximum values for gauge scales
                                            max_adv_home = df_adv_home_away["Home Advantage"].max()
                                            max_adv_away = max_adv_home
                                            max_adv_home = float(max_adv_home)
                                            max_adv_away = float(max_adv_away)

                                            # Extract and scale home advantage
                                            adv_home = float(data_team_home["Home Advantage"].values[0])
                                            adv_away = float(data_team_away["Home Advantage"].values[0])

                                            # Labels for pie charts
                                            labels_proportion_home = ["Home Win", "Draw", "Home Loss"]
                                            labels_proportion_away = ["Away Win", "Draw", "Away Loss"]

                                            col1, col2 = st.columns(2) # Creating Streamlit columns for Home

                                            # Function for gauge color
                                            def get_gauge_color(value, max_value, inverse=False):
                                                if max_value <= 0:
                                                    raise ValueError("max_value must be greater than 0")

                                                ratio = value / max_value
                                                if inverse:
                                                    red = min(max(int(210 * ratio), 0), 255)
                                                    green = min(max(int(210 * (1 - ratio)), 0), 255)
                                                else:
                                                    red = min(max(int(210 * (1 - ratio)), 0), 255)
                                                    green = min(max(int(210 * ratio), 0), 255)

                                                return f"rgb({red},{green},0)"

                                            # Create Home pie chart
                                            with col1:
                                                fig1, ax1 = plt.subplots(figsize=(7, 7))
                                                plot_pie_chart(ax1, values_proportion_home, labels_proportion_home, "Home Results Proportion", ["#2ecc71", "#95a5a6", "#e74c3c"])
                                                st.pyplot(fig1)

                                            # Create Home advantage gauge
                                            with col2:
                                                fig2 = go.Figure(go.Indicator(
                                                    mode="gauge+number",
                                                    value=adv_home,
                                                    title={"text": f"Home Advantage (%) - {selected_team_home}", "font": {"size": 12}},
                                                    gauge={
                                                        "axis": {"range": [0, max_adv_home]},
                                                        "bar": {"color": get_gauge_color(adv_home, max_adv_home)}
                                                    }
                                                ))
                                                st.plotly_chart(fig2)

                                            col3, col4 = st.columns(2) # Creating Streamlit columns for Away

                                            # Create Away pie chart
                                            with col3:
                                                fig3, ax3 = plt.subplots(figsize=(7, 7))
                                                plot_pie_chart(ax3, values_proportion_away, labels_proportion_away, "Away Results Proportion", ["#2ecc71", "#95a5a6", "#e74c3c"])
                                                st.pyplot(fig3)

                                            # Create Away advantage gauge
                                            with col4:
                                                fig4 = go.Figure(go.Indicator(
                                                    mode="gauge+number",
                                                    value=adv_away,
                                                    title={"text": f"Away Advantage (%) - {selected_team_away}", "font": {"size": 12}},
                                                    gauge={
                                                        "axis": {"range": [0, max_adv_away]},
                                                        "bar": {"color": get_gauge_color(adv_away, max_adv_away, inverse=True)}
                                                    }
                                                ))
                                                st.plotly_chart(fig4)


                                # Display of graphs related to the Previous Meetings section
                                elif section == "Previous confrontations":
                                    df_confrontation = get_matches_between_teams(selected_team_home, selected_team_away) # Fetching data

                                    if df_confrontation:  # Check if the list is not empty
                                        # Transforming data into a DataFrame with column names
                                        df_confrontation = pd.DataFrame([
                                            {
                                                "Season": item["season_name"], "Home Team": item["home_team_name"], "Away Team": item["away_team_name"],
                                                "Home Score": item["score_home"], "Away Score": item["score_away"], "Match Date": item["match_date"]
                                            }
                                            for item in df_confrontation
                                        ])

                                        st.subheader(f"List of matches between {selected_team_home} and {selected_team_away}")  # Table title
                                        st.dataframe(df_confrontation.style.set_properties(**{"text-align": "center"}))  # Center the text

                                        df_avg_goals_confrontation = get_avg_goals_stats_between_teams(selected_team_home, selected_team_away)  # Fetch data

                                        df_avg_goals_confrontation = pd.DataFrame([
                                            {
                                                f"Avg. Goals {selected_team_home}": item["avg_goals_selected_home"],
                                                f"Avg. Goals {selected_team_away}": item["avg_goals_selected_away"],
                                                f"Avg. Goals {selected_team_home} at Home": item["avg_goals_home_at_home"],
                                                f"Avg. Goals {selected_team_away} Away": item["avg_goals_away_at_away"]
                                            }
                                            for item in df_avg_goals_confrontation
                                        ])

                                        # Retrieve average goal values using column names
                                        avg_goals_selected_home = df_avg_goals_confrontation[f"Avg. Goals {selected_team_home}"].iloc[0]
                                        avg_goals_selected_away = df_avg_goals_confrontation[f"Avg. Goals {selected_team_away}"].iloc[0]
                                        avg_goals_home_at_home = df_avg_goals_confrontation[f"Avg. Goals {selected_team_home} at Home"].iloc[0]
                                        avg_goals_away_at_away = df_avg_goals_confrontation[f"Avg. Goals {selected_team_away} Away"].iloc[0]

                                        # Replace None values with 0.0 if necessary
                                        avg_goals_selected_home = float(avg_goals_selected_home) if avg_goals_selected_home is not None else 0.0
                                        avg_goals_selected_away = float(avg_goals_selected_away) if avg_goals_selected_away is not None else 0.0
                                        avg_goals_home_at_home = float(avg_goals_home_at_home) if avg_goals_home_at_home is not None else 0.0
                                        avg_goals_away_at_away = float(avg_goals_away_at_away) if avg_goals_away_at_away is not None else 0.0

                                        max_value = max(avg_goals_selected_home, avg_goals_selected_away, avg_goals_home_at_home, avg_goals_away_at_away)  # Compute gauge limits

                                        # Function to get gauge color (gradient from red to green)
                                        def get_gauge_color(value, max_value):
                                            ratio = value / max_value
                                            red = int(210 * (1 - ratio))
                                            green = int(210 * ratio)
                                            return f"rgb({red},{green},0)"

                                        col1, col2 = st.columns(2)  # Create Streamlit columns

                                        # Gauge 1: Average goals scored by selected_team_home
                                        with col1:
                                            fig1 = go.Figure(go.Indicator(
                                                mode="gauge+number",
                                                value=avg_goals_selected_home,
                                                gauge={
                                                    "axis": {"range": [None, max_value]},
                                                    "bar": {"color": get_gauge_color(avg_goals_selected_home, max_value)},
                                                    "steps": [
                                                        {"range": [0, avg_goals_selected_home], "color": get_gauge_color(avg_goals_selected_home, max_value)},
                                                        {"range": [avg_goals_selected_home, max_value], "color": 'white'}
                                                    ]
                                                },
                                                title={"text": f"<b style='font-size: 16px;'>{selected_team_home} - Average Goals</b>"},
                                                number={"suffix": " goals", "font": {"size": 20}}
                                            ))
                                            st.plotly_chart(fig1)

                                        # Gauge 2: Average goals scored by selected_team_away
                                        with col2:
                                            fig2 = go.Figure(go.Indicator(
                                                mode="gauge+number",
                                                value=avg_goals_selected_away,
                                                gauge={
                                                    "axis": {"range": [None, max_value]},
                                                    "bar": {"color": get_gauge_color(avg_goals_selected_away, max_value)},
                                                    "steps": [
                                                        {"range": [0, avg_goals_selected_away], "color": get_gauge_color(avg_goals_selected_away, max_value)},
                                                        {"range": [avg_goals_selected_away, max_value], "color": 'white'}
                                                    ]
                                                },
                                                title={"text": f"<b style='font-size: 16px;'>{selected_team_away} - Average Goals</b>"},
                                                number={"suffix": " goals", "font": {"size": 20}}
                                            ))
                                            st.plotly_chart(fig2)

                                        # Gauge 3: Average goals by selected_team_home at home
                                        with col1:
                                            fig3 = go.Figure(go.Indicator(
                                                mode="gauge+number",
                                                value=avg_goals_home_at_home,
                                                gauge={
                                                    "axis": {"range": [None, max_value]},
                                                    "bar": {"color": get_gauge_color(avg_goals_home_at_home, max_value)},
                                                    "steps": [
                                                        {"range": [0, avg_goals_home_at_home], "color": get_gauge_color(avg_goals_home_at_home, max_value)},
                                                        {"range": [avg_goals_home_at_home, max_value], "color": 'white'}
                                                    ]
                                                },
                                                title={"text": f"<b style='font-size: 16px;'>{selected_team_home} - Average Goals at Home</b>"},
                                                number={"suffix": " goals", "font": {"size": 20}}
                                            ))
                                            st.plotly_chart(fig3)

                                        # Gauge 4: Average goals by selected_team_away away
                                        with col2:
                                            fig4 = go.Figure(go.Indicator(
                                                mode="gauge+number",
                                                value=avg_goals_away_at_away,
                                                gauge={
                                                    "axis": {"range": [None, max_value]},
                                                    "bar": {"color": get_gauge_color(avg_goals_away_at_away, max_value)},
                                                    "steps": [
                                                        {"range": [0, avg_goals_away_at_away], "color": get_gauge_color(avg_goals_away_at_away, max_value)},
                                                        {"range": [avg_goals_away_at_away, max_value], "color": 'white'}
                                                    ]
                                                },
                                                title={"text": f"<b style='font-size: 16px;'>{selected_team_away} - Average Goals Away</b>"},
                                                number={"suffix": " goals", "font": {"size": 20}}
                                            ))
                                            st.plotly_chart(fig4)

                                        df_first_goal_confrontation = get_1st_goal_stats_between_teams(selected_team_home, selected_team_away) # Fetch first goal stats

                                        if df_first_goal_confrontation:
                                            # Transform dataframe with correct column names
                                            df_first_goal_confrontation = pd.DataFrame([
                                                {
                                                    "Team": item["team"],
                                                    f"{selected_team_home} - First Goal Scored": item["proportion_1st_goal_for"],
                                                    "No Goal": item["proportion_no_goal"],
                                                    f"{selected_team_away} - First Goal Conceded": item["proportion_1st_goal_against"],
                                                    f"{selected_team_home} - First Goal Scored / Win": item["proportion_1st_goal_win"],
                                                    f"{selected_team_home} - First Goal Scored / Draw": item["proportion_1st_goal_draw"],
                                                    f"{selected_team_home} - First Goal Scored / Loss": item["proportion_1st_goal_lose"],
                                                    f"{selected_team_home} - First Goal Conceded / Win": item["proportion_1st_goal_conceded_win"],
                                                    f"{selected_team_home} - First Goal Conceded / Draw": item["proportion_1st_goal_conceded_draw"],
                                                    f"{selected_team_home} - First Goal Conceded / Loss": item["proportion_1st_goal_conceded_lose"]
                                                }
                                                for item in df_first_goal_confrontation
                                            ])

                                            # Convert values to float
                                            for col in df_first_goal_confrontation.columns:
                                                if col != "Team":
                                                    df_first_goal_confrontation[col] = pd.to_numeric(df_first_goal_confrontation[col], errors='coerce').astype(float).mul(100)

                                            # Separate data for home team
                                            df_home = df_first_goal_confrontation[df_first_goal_confrontation["Team"] == selected_team_home].iloc[:, 1:]

                                            fig, axes = plt.subplots(1, 3, figsize=(15, 7))  # 1 row, 3 columns

                                            # Chart 1: First Goal Scored
                                            plot_pie_chart(
                                                axes[0],
                                                df_home.iloc[0, :3],
                                                ["First Goal Scored", "No Goal", "First Goal Conceded"],
                                                f"{selected_team_home} - First Goal Scored",
                                                ["#2ecc71", "#95a5a6", "#e74c3c"]
                                            )

                                            # Chart 2: Results After First Goal Scored
                                            plot_pie_chart(
                                                axes[1],
                                                df_home.iloc[0, 3:6],
                                                ["Win", "Draw", "Loss"],
                                                f"{selected_team_home} - Results After First Goal Scored",
                                                ["#2ecc71", "#f1c40f", "#e74c3c"]
                                            )

                                            # Chart 3: Results After First Goal Conceded
                                            plot_pie_chart(
                                                axes[2],
                                                df_home.iloc[0, 6:],
                                                ["Win", "Draw", "Loss"],
                                                f"{selected_team_home} - Results After First Goal Conceded",
                                                ["#2ecc71", "#f1c40f", "#e74c3c"]
                                            )

                                            plt.tight_layout()  # Adjust layout to prevent overlap
                                            st.pyplot(fig)  # Display the figure

                                        distrib_goal_between_team = get_distrib_goal_between_teams(selected_team_home, selected_team_away) # Fetching data

                                        if distrib_goal_between_team:
                                            # Transforming the DataFrame with proper column names
                                            distrib_goal_between_team = pd.DataFrame([
                                                {
                                                    "Team": item["team"],
                                                    "1st Half (Goals Scored)": item["proportion_0_45"],
                                                    "2nd Half (Goals Scored)": item["proportion_46_90"],
                                                    "0-15 min (Goals Scored)": item["proportion_0_15"],
                                                    "16-30 min (Goals Scored)": item["proportion_16_30"],
                                                    "31-45 min (Goals Scored)": item["proportion_31_45"],
                                                    "46-60 min (Goals Scored)": item["proportion_46_60"],
                                                    "61-75 min (Goals Scored)": item["proportion_61_75"],
                                                    "76-90 min (Goals Scored)": item["proportion_76_90"]
                                                }
                                                for item in distrib_goal_between_team
                                            ])
                                            for col in distrib_goal_between_team.columns:
                                                if col != "Team":
                                                    distrib_goal_between_team[col] = pd.to_numeric(distrib_goal_between_team[col], errors='coerce').astype(float)

                                            # Separate data for home and away teams
                                            distrib_goal_team_home = distrib_goal_between_team[distrib_goal_between_team["Team"] == selected_team_home].iloc[:, 1:]
                                            distrib_goal_team_away = distrib_goal_between_team[distrib_goal_between_team["Team"] == selected_team_away].iloc[:, 1:]

                                            # Function to generate goal distribution charts
                                            def plot_distribution_graphs(data, title_prefix):
                                                total_goals = data.sum().sum()

                                                if total_goals == 0:
                                                    return

                                                fig, axes = plt.subplots(1, 2, figsize=(15, 5))

                                                # Proportion of goals scored per half
                                                labels_proportion = ["1st Half", "2nd Half"]
                                                values_proportion_goal_scored = data.iloc[0, :2]
                                                axes[0].pie(values_proportion_goal_scored, labels=labels_proportion, autopct='%1.2f%%', startangle=90, colors=["lightblue", "lightcoral"])
                                                axes[0].set_title(f"{title_prefix} - Proportion of Goals Scored per Half")

                                                # Proportion of goals scored per 15-minute interval
                                                labels_intervals = ["0-15 min", "16-30 min", "31-45 min", "46-60 min", "61-75 min", "76-90 min"]
                                                values_intervals_goal_scored = data.iloc[0, 2:8]
                                                colors = ["#D4EFDF", "#A9DFBF", "#F9E79F", "#F5CBA7", "#E59866", "#DC7633"]
                                                bars = axes[1].bar(labels_intervals, values_intervals_goal_scored, color=colors)
                                                axes[1].set_title(f"{title_prefix} - Proportion of Goals Scored per 15-Minute Interval")
                                                axes[1].set_ylabel("%")
                                                axes[1].set_ylim(0, max(values_intervals_goal_scored) + 5)

                                                # Adding values on the bars
                                                for bar in bars:
                                                    yval = bar.get_height()
                                                    axes[1].text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval:.2f}%', ha='center', color='black')

                                                st.pyplot(fig)

                                            # Display the charts for both teams
                                            plot_distribution_graphs(distrib_goal_team_home, f"{selected_team_home}")
                                            plot_distribution_graphs(distrib_goal_team_away, f"{selected_team_away}")

                                        result_h_a_between_teams = get_home_away_selected_teams(selected_team_home, selected_team_away) # Fetching home advantage stats

                                        if result_h_a_between_teams:
                                            # Transforming the DataFrame with proper column names
                                            df_adv_home_away_team = pd.DataFrame([
                                                {
                                                    "Team": item["team_name"],
                                                    "Home Wins": item["home_win"],
                                                    "Home Draws": item["home_draws"],
                                                    "Home Losses": item["home_losses"],
                                                    "Home Advantage": item["home_advantage"],
                                                    "Total Wins": item["total_wins"],
                                                    "Total Draws": item["total_draws"],
                                                    "Total Losses": item["total_losses"]
                                                }
                                                for item in result_h_a_between_teams
                                            ])
                                            df_adv_home_away_team = df_adv_home_away_team[df_adv_home_away_team["Team"] == selected_team_home].iloc[:, 1:]

                                            if not df_adv_home_away_team.empty:
                                                # Select the necessary columns and extract percentages
                                                total = df_adv_home_away_team[["Total Wins", "Total Draws", "Total Losses"]].sum(axis=1).values[0]
                                                values_proportion = (df_adv_home_away_team[["Total Wins", "Total Draws", "Total Losses"]].values.flatten() / total) * 100

                                                total_home = df_adv_home_away_team[["Home Wins", "Home Draws", "Home Losses"]].sum(axis=1).values[0]
                                                values_proportion_home = (df_adv_home_away_team[["Home Wins", "Home Draws", "Home Losses"]].values.flatten() / total_home) * 100

                                                adv_home = float(df_adv_home_away_team["Home Advantage"].values[0])

                                                # Function to create filtered pie charts
                                                def plot_filtered_pie(ax, values, labels, title, colors, text_size=6):
                                                    mask = values > 0
                                                    filtered_values = values[mask]
                                                    filtered_labels = [label for label, m in zip(labels, mask) if m]
                                                    filtered_colors = [color for color, m in zip(colors, mask) if m]

                                                    if filtered_values.sum() > 0:
                                                        wedges, texts, autotexts = ax.pie(
                                                            filtered_values, labels=filtered_labels, autopct='%1.2f%%', startangle=90, colors=filtered_colors,
                                                            textprops={'fontsize': text_size}
                                                        )
                                                        for text in texts:
                                                            text.set_fontsize(text_size)
                                                        for autotext in autotexts:
                                                            autotext.set_fontsize(text_size)

                                                        ax.set_title(title, fontsize=text_size)
                                                    else:
                                                        ax.axis('off')  # Hide axis if no data

                                                # First row: Overall results pie chart
                                                with st.container():
                                                    col1 = st.columns(1)
                                                    with col1[0]:
                                                        fig1, ax1 = plt.subplots(figsize=(3, 3))
                                                        plot_filtered_pie(
                                                            ax1,
                                                            values_proportion,
                                                            ["Win", "Draw", "Loss"],
                                                            f"Result Proportions of {selected_team_home} against {selected_team_away} (All Matches)",
                                                            ["#2ecc71", "#95a5a6", "#e74c3c"]
                                                        )
                                                        st.pyplot(fig1)

                                                # Second row: Home results + Home advantage gauge
                                                if total_home != 0:
                                                    with st.container():
                                                        col2, col3 = st.columns(2)

                                                        with col2:
                                                            fig2, ax2 = plt.subplots(figsize=(7, 7))
                                                            plot_filtered_pie(
                                                                ax2,
                                                                values_proportion_home,
                                                                ["Home Win", "Draw", "Home Loss"],
                                                                f"Home Results of {selected_team_home} against {selected_team_away}",
                                                                ["#2ecc71", "#95a5a6", "#e74c3c"]
                                                            )
                                                            st.pyplot(fig2)

                                                        def get_gauge_color(value):
                                                            if not (0 <= value <= 100):
                                                                raise ValueError("Value must be between 0 and 100")
                                                            ratio = value / 100
                                                            red = int(210 * (1 - ratio))
                                                            green = int(210 * ratio)
                                                            return f"rgb({red},{green},0)"

                                                        with col3:
                                                            fig3 = go.Figure(go.Indicator(
                                                                mode="gauge+number",
                                                                value=adv_home,
                                                                title={"text": f"Home Advantage (%) of {selected_team_home} against {selected_team_away}", "font": {"size": 10}},
                                                                gauge={"axis": {"range": [0, 100]}, "bar": {"color": get_gauge_color(adv_home)}}
                                                            ))
                                                            st.plotly_chart(fig3)


                                    else:
                                        st.warning(f"No matches between {selected_team_home} and {selected_team_away} in the database.")

        # Image display only if no selection was made
        if show_image:
            st.image(image_path)

def season_analysis():
    if lang == "Français":
        st.title("📅 Analyse d'une Saison") # Titre de l'application

        # Vérifie si l'utilisateur a fait un choix (équipe, saison et section)
        show_image = True  # Par défaut, on affiche l'image

        image_path = os.path.join(os.path.dirname(__file__), "image", "banniere_saison.jpg") # Construction du chemin absolu

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
                                df[numeric_columns] = df[numeric_columns].apply(lambda col: col.apply(lambda x: float(round(x, 2)) if pd.notnull(x) else 0.0))

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
                                df[numeric_columns] = df[numeric_columns].apply(lambda col: col.apply(lambda x: float(round(x, 2)) if pd.notnull(x) else 0.0))


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
                                df[numeric_columns] = df[numeric_columns].apply(lambda col: col.apply(lambda x: float(round(x, 2)) if pd.notnull(x) else 0.0))


                                df = df.sort_values(by=numeric_columns.tolist(), ascending=False) # Assurer un tri numérique et non alphabétique
                                # Fonction pour colorer la saison sélectionnée / Function for colouring the selected season
                                def highlight_selected_season(row):
                                    return ['background-color: lightcoral' if row["Saison"] == selected_season else '' for _ in row]
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
                                    df[numeric_columns] = df[numeric_columns].apply(lambda col: col.apply(lambda x: float(round(x, 2)) if pd.notnull(x) else 0.0))
                                    # On arrondit à 2 chiffres après la virgule si besoin

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

                                    df[numeric_columns] = df[numeric_columns].apply(lambda col: col.apply(lambda x: float(round(x, 2)) if pd.notnull(x) else 0.0))

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
                                # Fonction pour colorer la saison sélectionnée / Function for colouring the selected season
                                def highlight_selected_season(row):
                                    return ['background-color: lightcoral' if row["Saison"] == selected_season else '' for _ in row]
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
                                # Fonction pour colorer la saison sélectionnée / Function for colouring the selected season
                                def highlight_selected_season(row):
                                    return ['background-color: lightcoral' if row["Saison"] == selected_season else '' for _ in row]
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
                                # Fonction pour colorer la saison sélectionnée / Function for colouring the selected season
                                def highlight_selected_season(row):
                                    return ['background-color: lightcoral' if row["Saison"] == selected_season else '' for _ in row]
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

        # Affichage de l’image uniquement si aucun choix n'a été fait
        if show_image:
            st.image(image_path)
    else:
        st.title("📅 Analysis of a season") # Title

        # Checks if the user has made a selection (team, season and section)
        show_image = True  # By default, we display the image

        image_path = os.path.join(os.path.dirname(__file__), "image", "banniere_saison.jpg") # Build the path

        st.sidebar.header("🔍 Competition selection") # Competition selection in the sidebar
        competitions_available = get_competitions() # Retrieving the list of available competitions

        # Selection of competitions available
        if competitions_available:
            selected_competition = st.sidebar.selectbox("Choose a competition :", ["Select a competition"] + competitions_available, index=0)
            
            if selected_competition != "Select a competition":
                st.sidebar.header("🔍 Season selection") # Selection of the season according to the chosen competition
                seasons_available = get_seasons_by_competition(selected_competition) # Recover data
                
                # Selection of available seasons
                if seasons_available:
                    selected_season = st.sidebar.selectbox("Choose a season :", ["Select a season"] + seasons_available, index=0)
                    
                    if selected_season != "Select a season":
                        st.sidebar.header("📊 Select a analysis")
                        section = st.sidebar.radio("Sections", ["General statistics", "1st goal scored", "Goal distribution", "Home / Away", "Season comparison"])

                        # If a section is selected, we hide the imahe
                        if section:
                            show_image = False 

                        st.subheader(f"📌 {section} - {selected_season}") # Summary

                        # Display of graphs related to the General Statistics section           
                        if section == "General statistics":

                            avg_goal_stats = get_avg_goals_stats_by_competition()  # Fetching average goals statistics
                            if avg_goal_stats:
                                # Transforming the data into a DataFrame with column names
                                df_goals = pd.DataFrame([
                                    {
                                        "Competition": item["competition_name"], "Season": item["season_name"], "Goals/Match": item["avg_goals_per_match"],
                                        "Home Goals": item["avg_home_goals"], "Away Goals": item["avg_away_goals"]
                                    }
                                    for item in avg_goal_stats
                                ])

                                # Determine maximum scale for gauges
                                max_avg_goals = df_goals["Goals/Match"].max()
                                max_home_goals = df_goals["Home Goals"].max()
                                max_away_goals = df_goals["Away Goals"].max()

                                selected_data = df_goals[df_goals["Season"] == selected_season]  # Filter selected season

                                if not selected_data.empty:
                                    avg_goals = float(selected_data["Goals/Match"].values[0])
                                    avg_home_goals = float(selected_data["Home Goals"].values[0])
                                    avg_away_goals = float(selected_data["Away Goals"].values[0])

                                    max_avg_goals = float(max_avg_goals)
                                    max_home_goals = float(max_home_goals)
                                    max_away_goals = float(max_away_goals)

                                    col1, col2, col3 = st.columns(3)  # Create columns for the gauges

                                    # Function to calculate gauge color
                                    def get_gauge_color(value, max_value):
                                        ratio = value / max_value
                                        red = int(210 * (1 - ratio))
                                        green = int(210 * ratio)
                                        return f"rgb({red},{green},0)"

                                    with col1:
                                        fig1 = go.Figure(go.Indicator(
                                            mode="gauge+number",
                                            value=avg_goals,
                                            title={"text": "Goals/Match"},
                                            gauge={"axis": {"range": [0, max_avg_goals]}, "bar": {"color": get_gauge_color(avg_goals, max_avg_goals)}}
                                        ))
                                        st.plotly_chart(fig1)

                                    with col2:
                                        fig2 = go.Figure(go.Indicator(
                                            mode="gauge+number",
                                            value=avg_home_goals,
                                            title={"text": "Home Goals"},
                                            gauge={"axis": {"range": [0, max_home_goals]}, "bar": {"color": get_gauge_color(avg_home_goals, max_home_goals)}}
                                        ))
                                        st.plotly_chart(fig2)

                                    with col3:
                                        fig3 = go.Figure(go.Indicator(
                                            mode="gauge+number",
                                            value=avg_away_goals,
                                            title={"text": "Away Goals"},
                                            gauge={"axis": {"range": [0, max_away_goals]}, "bar": {"color": get_gauge_color(avg_away_goals, max_away_goals)}}
                                        ))
                                        st.plotly_chart(fig3)

                            # Table of goals scored
                            compare_goals_scored_data = get_goals_scored(selected_season)
                            if compare_goals_scored_data:
                                df = pd.DataFrame([
                                    {
                                        "Team": item["team_name"], "Total Goals Scored": item["total_goals_scored"], "Avg Goals Scored": item["avg_goals_scored"],
                                        "Home Goals Scored": item["goals_scored_home"], "Avg Home Goals": item["avg_goals_scored_home"],
                                        "Away Goals Scored": item["goals_scored_away"], "Avg Away Goals": item["avg_goals_scored_away"]
                                    }
                                    for item in compare_goals_scored_data
                                ])

                                numeric_columns = df.columns[1:]
                                df[numeric_columns] = df[numeric_columns].apply(lambda col: col.apply(lambda x: float(round(x, 2)) if pd.notnull(x) else 0.0))

                                df = df.sort_values(by=["Total Goals Scored"], ascending=False)

                                styled_df = df.style.format({col: "{:.2f}" for col in numeric_columns}).set_properties(**{"text-align": "center"})
                                st.subheader(f"Goals Scored Table for {selected_season}")
                                st.dataframe(styled_df)
                            else:
                                st.warning("No data available for this season.")

                            # Table of goals conceded
                            compare_goals_conceded_data = get_goals_conceded(selected_season)
                            if compare_goals_conceded_data:
                                df = pd.DataFrame([
                                    {
                                        "Team": item["team_name"], "Total Goals Conceded": item["total_goals_conceded"], "Avg Goals Conceded": item["avg_goals_conceded"],
                                        "Home Goals Conceded": item["goals_conceded_home"], "Avg Home Goals Conceded": item["avg_goals_conceded_home"],
                                        "Away Goals Conceded": item["goals_conceded_away"], "Avg Away Goals Conceded": item["avg_goals_conceded_away"]
                                    }
                                    for item in compare_goals_conceded_data
                                ])

                                numeric_columns = df.columns[1:]
                                df[numeric_columns] = df[numeric_columns].apply(lambda col: col.apply(lambda x: float(round(x, 2)) if pd.notnull(x) else 0.0))

                                df = df.sort_values(by=["Total Goals Conceded"], ascending=False)

                                styled_df = df.style.format({col: "{:.2f}" for col in numeric_columns}).set_properties(**{"text-align": "center"})
                                st.subheader(f"Goals Conceded Table for {selected_season}")
                                st.dataframe(styled_df)

                            # Table of frequent scores
                            general_stats_data = get_frequent_score_by_season(selected_season)
                            if general_stats_data:
                                df = pd.DataFrame([
                                    {
                                        "Home Score": item["score_home"], "Away Score": item["score_away"], "Percentage": item["percentage"]
                                    }
                                    for item in general_stats_data
                                ])

                                pivot_table = df.pivot(index="Home Score", columns="Away Score", values="Percentage").fillna(0)
                                pivot_table = pivot_table.apply(pd.to_numeric, errors='coerce').fillna(0)

                                fig, ax = plt.subplots(figsize=(10, 6))
                                sns.heatmap(pivot_table, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5, ax=ax)
                                ax.set_title(f"Score Distribution for {selected_season} (%)")
                                ax.set_xlabel("Away Score")
                                ax.set_ylabel("Home Score")
                                st.pyplot(fig)

                        # Display of graphs related to the First Goal Scored section
                        elif section == "1st goal scored":
                            first_goal = get_first_goal_stats(selected_season)  # Fetching data
                            if first_goal:
                                # Transforming data into a DataFrame with column names
                                first_goal = pd.DataFrame([
                                    {
                                        "Season": item["season_name"], "No Goal": item["proportion_no_goal"], "First Goal - Home": item["proportion_1st_goal_home"],
                                        "First Goal - Away": item["proportion_1st_goal_away"], "First Goal / Win": item["first_goal_win"],
                                        "First Goal / Draw": item["first_goal_draw"], "First Goal / Loss": item["first_goal_lose"],
                                        "First Goal / Home / Win": item["first_goal_home_win"], "First Goal / Home / Draw": item["first_goal_home_draw"],
                                        "First Goal / Home / Loss": item["first_goal_home_lose"], "First Goal / Away / Win": item["first_goal_away_win"],
                                        "First Goal / Away / Draw": item["first_goal_away_draw"], "First Goal / Away / Loss": item["first_goal_away_lose"]
                                    }
                                    for item in first_goal
                                ])

                                # Extract values for pie chart
                                values_proportion = first_goal.iloc[0][["No Goal", "First Goal - Home", "First Goal - Away"]].values
                                labels_proportion = ["No Goal", "Home", "Away"]

                                fig, axes = plt.subplots(2, 2, figsize=(15, 10))

                                # First pie chart: Teams scoring first
                                axes[0, 0].pie(values_proportion, labels=labels_proportion, autopct='%1.2f%%', startangle=90,
                                            colors=["#95a5a6", "#3498db", "#e67e22"])
                                axes[0, 0].set_title("Proportion of Teams Scoring First")

                                # Data for the other pie charts
                                first_goal_data = [
                                    (["First Goal / Win", "First Goal / Draw", "First Goal / Loss"],
                                    "Results after Scoring the First Goal"),
                                    (["First Goal / Home / Win", "First Goal / Home / Draw", "First Goal / Home / Loss"],
                                    "Home Results after Scoring the First Goal"),
                                    (["First Goal / Away / Win", "First Goal / Away / Draw", "First Goal / Away / Loss"],
                                    "Away Results after Scoring the First Goal")
                                ]

                                colors = ["#2ecc71", "#95a5a6", "#e74c3c"]

                                # Loop for other pie charts
                                for ax, (cols, title) in zip(axes.flatten()[1:], first_goal_data):
                                    values = first_goal.iloc[0][cols].values
                                    ax.pie(values, labels=["Win", "Draw", "Loss"], autopct='%1.2f%%', startangle=90, colors=colors)
                                    ax.set_title(title)

                                st.pyplot(fig)

                            # Building the table for First Goal by team
                            first_goal_season_data = get_first_goal_season(selected_season)
                            if first_goal_season_data:
                                df = pd.DataFrame([
                                    {
                                        "Season": item["season_name"], "Team": item["team_name"],
                                        "First Goal Scored": item["proportion_1st_goal_for"], "No Goal": item["proportion_no_goal"], "First Goal Conceded": item["proportion_1st_goal_against"],
                                        "Home / First Goal Scored": item["proportion_1st_goal_home_for"], "Home / No Goal": item["proportion_no_goal_home"], "Home / First Goal Conceded": item["proportion_1st_goal_home_against"],
                                        "Away / First Goal Scored": item["proportion_1st_goal_away_for"], "Away / No Goal": item["proportion_no_goal_away"], "Away / First Goal Conceded": item["proportion_1st_goal_away_against"],
                                        "First Goal Scored / Win": item["first_goal_win"], "First Goal Scored / Draw": item["first_goal_draw"], "First Goal Scored / Loss": item["first_goal_lose"],
                                        "Home / First Goal Scored / Win": item["proportion_1st_goal_home_win"], "Home / First Goal Scored / Draw": item["proportion_1st_goal_home_draw"], "Home / First Goal Scored / Loss": item["proportion_1st_goal_home_lose"],
                                        "Away / First Goal Scored / Win": item["proportion_1st_goal_away_win"], "Away / First Goal Scored / Draw": item["proportion_1st_goal_away_draw"], "Away / First Goal Scored / Loss": item["proportion_1st_goal_away_lose"],
                                        "First Goal Conceded / Win": item["first_goal_conceded_win"], "First Goal Conceded / Draw": item["first_goal_conceded_draw"], "First Goal Conceded / Loss": item["first_goal_conceded_lose"],
                                        "Home / First Goal Conceded / Win": item["proportion_1st_goal_conceded_home_win"], "Home / First Goal Conceded / Draw": item["proportion_1st_goal_conceded_home_draw"], "Home / First Goal Conceded / Loss": item["proportion_1st_goal_conceded_home_lose"],
                                        "Away / First Goal Conceded / Win": item["proportion_1st_goal_conceded_away_win"], "Away / First Goal Conceded / Draw": item["proportion_1st_goal_conceded_away_draw"], "Away / First Goal Conceded / Loss": item["proportion_1st_goal_conceded_away_lose"]
                                    }
                                    for item in first_goal_season_data
                                ])

                                for col in df.columns:
                                    if col != "Team":
                                        df[col] = pd.to_numeric(df[col], errors='coerce')

                                df = df.iloc[:, 1:]  # Drop Season column

                                # Building sub-tables
                                first_goal_columns = [
                                    "Team", "First Goal Scored", "No Goal", "First Goal Conceded", "Home / First Goal Scored", "Home / No Goal", "Home / First Goal Conceded",
                                    "Away / First Goal Scored", "Away / No Goal", "Away / First Goal Conceded"
                                ]
                                first_goal_influence_columns = [
                                    "Team", "First Goal Scored / Win", "First Goal Scored / Draw", "First Goal Scored / Loss",
                                    "Home / First Goal Scored / Win", "Home / First Goal Scored / Draw", "Home / First Goal Scored / Loss",
                                    "Away / First Goal Scored / Win", "Away / First Goal Scored / Draw", "Away / First Goal Scored / Loss"
                                ]
                                first_goal_conceded_columns = [
                                    "Team", "First Goal Conceded / Win", "First Goal Conceded / Draw", "First Goal Conceded / Loss",
                                    "Home / First Goal Conceded / Win", "Home / First Goal Conceded / Draw", "Home / First Goal Conceded / Loss",
                                    "Away / First Goal Conceded / Win", "Away / First Goal Conceded / Draw", "Away / First Goal Conceded / Loss"
                                ]

                                df_first_goal = df[first_goal_columns].sort_values(by=["First Goal Scored"], ascending=False)
                                df_first_goal_influence = df[first_goal_influence_columns].sort_values(by=["First Goal Scored / Win"], ascending=False)
                                df_first_goal_conceded = df[first_goal_conceded_columns].sort_values(by=["First Goal Conceded / Win"], ascending=False)

                                for df_subset in [df_first_goal, df_first_goal_influence, df_first_goal_conceded]:
                                    numeric_columns = df_subset.columns[1:]
                                    df_subset[numeric_columns] = df_subset[numeric_columns].astype(float)

                                # Styling the tables
                                style_df_first_goal = (
                                    df_first_goal.style
                                    .format({col: "{:.2f}" for col in df_first_goal.columns[1:]})
                                    .set_properties(**{"text-align": "center"})
                                )

                                style_df_first_goal_influence = (
                                    df_first_goal_influence.style
                                    .format({col: "{:.2f}" for col in df_first_goal_influence.columns[1:]})
                                    .set_properties(**{"text-align": "center"})
                                )

                                style_df_first_goal_conceded = (
                                    df_first_goal_conceded.style
                                    .format({col: "{:.2f}" for col in df_first_goal_conceded.columns[1:]})
                                    .set_properties(**{"text-align": "center"})
                                )

                                # Display tables
                                st.subheader(f"First Goal (Scored or Conceded) Table for {selected_season}")
                                st.dataframe(style_df_first_goal)

                                st.subheader(f"Impact of First Goal Scored for {selected_season}")
                                st.dataframe(style_df_first_goal_influence)

                                st.subheader(f"Impact of First Goal Conceded for {selected_season}")
                                st.dataframe(style_df_first_goal_conceded)


                        # Display of graphs related to the Goal Distribution section
                        elif section == "Goal distribution":
                            distrib_goal = get_distribution_goals(selected_season)  # Fetching data
                            if distrib_goal:
                                # Transform the data into a DataFrame with column names
                                distrib_goal = pd.DataFrame([
                                    {
                                        "Season": item["season_name"], "1st Half": item["proportion_buts_1ere_periode"], "2nd Half": item["proportion_buts_2nde_periode"],
                                        "0-15 min": item["proportion_buts_0_15"], "16-30 min": item["proportion_buts_16_30"], "31-45 min": item["proportion_buts_31_45"],
                                        "46-60 min": item["proportion_buts_46_60"], "61-75 min": item["proportion_buts_61_75"], "76-90 min": item["proportion_buts_76_90"]
                                    }
                                    for item in distrib_goal
                                ])
                                distrib_goal = list(distrib_goal.iloc[0, 1:])  # Convert to list (remove 'Season')

                                fig, axes = plt.subplots(1, 2, figsize=(15, 7))  # Create figure and subplots

                                # Pie chart for goal distribution per half
                                labels_proportion = ["1st Half", "2nd Half"]
                                values_proportion = distrib_goal[:2]
                                axes[0].pie(values_proportion, labels=labels_proportion, autopct='%1.2f%%', startangle=90, colors=["lightblue", "lightcoral"])
                                axes[0].set_title("Goal Distribution per Half")

                                # Bar chart for goal distribution per 15-minute interval
                                labels_intervals = ["0-15 min", "16-30 min", "31-45 min", "46-60 min", "61-75 min", "76-90 min"]
                                values_intervals = list(map(float, distrib_goal[2:]))
                                colors = ["#D4EFDF", "#A9DFBF", "#F9E79F", "#F5CBA7", "#E59866", "#DC7633"]
                                bars = axes[1].bar(labels_intervals, values_intervals, color=colors)
                                axes[1].set_title("Goal Distribution per 15-Minute Interval")
                                axes[1].set_ylabel("%")
                                axes[1].set_xlabel("Time Interval")
                                axes[1].set_ylim(0, max(values_intervals) + 5)

                                # Add values on top of bars
                                for bar in bars:
                                    yval = bar.get_height()
                                    axes[1].text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval:.2f}%', ha='center', color='black')

                                st.pyplot(fig)

                            # Building the table for goals scored/conceded distribution
                            distrib_goals_data = get_distribution_goals_season(selected_season)
                            if distrib_goals_data:
                                df = pd.DataFrame([
                                    {
                                        "Season": item["season_name"], "Team": item["team_name"], "1st Half (Scored %)": item["proportion_buts_inscrit_1ere_periode"],
                                        "2nd Half (Scored %)": item["proportion_buts_inscrit_2nde_periode"], "0-15 min (Scored %)": item["proportion_buts_0_15"],
                                        "16-30 min (Scored %)": item["proportion_buts_16_30"], "31-45 min (Scored %)": item["proportion_buts_31_45"],
                                        "46-60 min (Scored %)": item["proportion_buts_46_60"], "61-75 min (Scored %)": item["proportion_buts_61_75"],
                                        "76-90 min (Scored %)": item["proportion_buts_76_90"], "1st Half (Conceded %)": item["proportion_buts_encaissés_1ere_periode"],
                                        "2nd Half (Conceded %)": item["proportion_buts_encaissés_2nde_periode"], "0-15 min (Conceded %)": item["proportion_buts_encaissés_0_15"],
                                        "16-30 min (Conceded %)": item["proportion_buts_encaissés_16_30"], "31-45 min (Conceded %)": item["proportion_buts_encaissés_31_45"],
                                        "46-60 min (Conceded %)": item["proportion_buts_encaissés_46_60"], "61-75 min (Conceded %)": item["proportion_buts_encaissés_61_75"],
                                        "76-90 min (Conceded %)": item["proportion_buts_encaissés_76_90"], "1st Half (Goals Scored)": item["buts_inscrit_1ere_periode"],
                                        "2nd Half (Goals Scored)": item["buts_inscrit_2nde_periode"], "0-15 min (Goals Scored)": item["nbr_buts_0_15"],
                                        "16-30 min (Goals Scored)": item["nbr_buts_16_30"], "31-45 min (Goals Scored)": item["nbr_buts_31_45"],
                                        "46-60 min (Goals Scored)": item["nbr_buts_46_60"], "61-75 min (Goals Scored)": item["nbr_buts_61_75"],
                                        "76-90 min (Goals Scored)": item["nbr_buts_76_90"], "1st Half (Goals Conceded)": item["buts_encaissés_1ere_periode"],
                                        "2nd Half (Goals Conceded)": item["buts_encaissés_2nde_periode"], "0-15 min (Goals Conceded)": item["buts_encaissés_0_15"],
                                        "16-30 min (Goals Conceded)": item["buts_encaissés_16_30"], "31-45 min (Goals Conceded)": item["buts_encaissés_31_45"],
                                        "46-60 min (Goals Conceded)": item["buts_encaissés_46_60"], "61-75 min (Goals Conceded)": item["buts_encaissés_61_75"],
                                        "76-90 min (Goals Conceded)": item["buts_encaissés_76_90"]
                                    }
                                    for item in distrib_goals_data
                                ])

                                for col in df.columns:
                                    if col != "Team":
                                        df[col] = pd.to_numeric(df[col], errors='coerce')
                                        df[col] = df[col].astype(float)

                                # Subsets of columns
                                distrib_goals_scored_columns = [
                                    "Team", "1st Half (Scored %)", "1st Half (Goals Scored)", "2nd Half (Scored %)", "2nd Half (Goals Scored)",
                                    "0-15 min (Scored %)", "0-15 min (Goals Scored)", "16-30 min (Scored %)", "16-30 min (Goals Scored)",
                                    "31-45 min (Scored %)", "31-45 min (Goals Scored)", "46-60 min (Scored %)", "46-60 min (Goals Scored)",
                                    "61-75 min (Scored %)", "61-75 min (Goals Scored)", "76-90 min (Scored %)", "76-90 min (Goals Scored)"
                                ]
                                distrib_goals_conceded_columns = [
                                    "Team", "1st Half (Conceded %)", "1st Half (Goals Conceded)", "2nd Half (Conceded %)", "2nd Half (Goals Conceded)",
                                    "0-15 min (Conceded %)", "0-15 min (Goals Conceded)", "16-30 min (Conceded %)", "16-30 min (Goals Conceded)",
                                    "31-45 min (Conceded %)", "31-45 min (Goals Conceded)", "46-60 min (Conceded %)", "46-60 min (Goals Conceded)",
                                    "61-75 min (Conceded %)", "61-75 min (Goals Conceded)", "76-90 min (Conceded %)", "76-90 min (Goals Conceded)"
                                ]

                                # Create sub-tables
                                df_distrib_goals_scored = df[distrib_goals_scored_columns].sort_values(by=["1st Half (Scored %)"], ascending=False)
                                df_distrib_goals_conceded = df[distrib_goals_conceded_columns].sort_values(by=["1st Half (Conceded %)"], ascending=False)

                                # Apply style
                                style_df_distrib_goals_scored = (
                                    df_distrib_goals_scored.style
                                    .format({col: "{:.2f}" for col in distrib_goals_scored_columns[1:]})
                                    .set_properties(**{"text-align": "center"})
                                )

                                style_df_distrib_goals_conceded = (
                                    df_distrib_goals_conceded.style
                                    .format({col: "{:.2f}" for col in distrib_goals_conceded_columns[1:]})
                                    .set_properties(**{"text-align": "center"})
                                )

                                # Display styled tables
                                st.subheader(f"Goals Scored Distribution Table for {selected_season}")
                                st.dataframe(style_df_distrib_goals_scored)

                                st.subheader(f"Goals Conceded Distribution Table for {selected_season}")
                                st.dataframe(style_df_distrib_goals_conceded)

                        # Display of graphs related to the Home / Away section
                        elif section == "Home / Away":
                            result_h_a = get_home_away_advantage()  # Fetch home advantage statistics

                            if result_h_a:
                                # Transforming data into a DataFrame with column names
                                df_adv_home_away = pd.DataFrame([
                                    {
                                        "Season": item["season_name"], "Home Win": item["proportion_home_win"], "Draw": item["proportion_draw"],
                                        "Away Win": item["proportion_away_win"], "Home Advantage": item["home_advantage"]
                                    }
                                    for item in result_h_a
                                ])

                                # Determine the maximum scale based on highest observed values
                                max_adv_home = df_adv_home_away["Home Advantage"].max()
                                max_adv_home = float(max_adv_home)

                                selected_data = df_adv_home_away[df_adv_home_away["Season"] == selected_season]  # Retrieve the selected season's data

                                if not selected_data.empty:
                                    # Select only the necessary columns and extract as list
                                    values_proportion = selected_data[["Home Win", "Draw", "Away Win"]].values.flatten()

                                    labels_proportion = ["Home Win", "Draw", "Away Win"]

                                    col1, col2 = st.columns(2)  # Streamlit columns

                                    # Create pie chart
                                    with col1:
                                        fig1, ax1 = plt.subplots(figsize=(7, 7))
                                        ax1.pie(values_proportion, labels=labels_proportion, autopct='%1.2f%%', startangle=90, colors=["#3498db", "#95a5a6", "#e67e22"])
                                        ax1.set_title("Results Proportion by Home/Away Factor")
                                        st.pyplot(fig1)

                                    adv_home = float(selected_data["Home Advantage"].values[0])

                                    # Function to compute the color based on the fill ratio
                                    def get_gauge_color(value, max_value):
                                        if max_value == 0:
                                            return "rgb(210,0,0)"
                                        ratio = max(0, min(value / max_value, 1))
                                        red = int(210 * (1 - ratio))
                                        green = int(210 * ratio)
                                        return f"rgb({red},{green},0)"

                                    # Create gauge chart
                                    with col2:
                                        fig2 = go.Figure(go.Indicator(
                                            mode="gauge+number",
                                            value=adv_home,
                                            title={"text": "Home Advantage (%)"},
                                            gauge={
                                                "axis": {"range": [0, max_adv_home]},
                                                "bar": {"color": get_gauge_color(adv_home, max_adv_home)}
                                            }
                                        ))
                                        st.plotly_chart(fig2)

                            rank_home_data = get_rank_home_season(selected_season)  # Build the table for home ranking
                            if rank_home_data:
                                df = pd.DataFrame([
                                    {
                                        "Team": item["team_name"], "Matches Played": item["all_matches"], "Home Wins": item["number_home_win"],
                                        "Home Draws": item["number_home_draw"], "Home Losses": item["number_home_lose"], "Home Points": item["home_points"],
                                        "Average Home Points": item["avg_home_points"]
                                    }
                                    for item in rank_home_data
                                ])
                                for col in df.columns:
                                    if col != "Team":
                                        df[col] = pd.to_numeric(df[col], errors='coerce')
                                        df[col] = df[col].astype(float)

                                df_home_rank = df.sort_values(by=["Home Points"], ascending=False)
                                style_df_home_rank = (
                                    df_home_rank.style
                                    .format({col: format_value for col in df_home_rank.columns[1:]})
                                    .set_properties(**{"text-align": "center"})
                                )

                                st.subheader(f"Home Ranking for the {selected_season} Season")
                                st.dataframe(style_df_home_rank)

                            rank_away_data = get_rank_away_season(selected_season)  # Build the table for away ranking
                            if rank_away_data:
                                df = pd.DataFrame([
                                    {
                                        "Team": item["team_name"], "Matches Played": item["all_matches"], "Away Wins": item["number_away_win"],
                                        "Away Draws": item["number_away_draw"], "Away Losses": item["number_away_lose"], "Away Points": item["away_points"],
                                        "Average Away Points": item["avg_away_points"]
                                    }
                                    for item in rank_away_data
                                ])
                                for col in df.columns:
                                    if col != "Team":
                                        df[col] = pd.to_numeric(df[col], errors='coerce')
                                        df[col] = df[col].astype(float)

                                df_away_rank = df.sort_values(by=["Away Points"], ascending=False)
                                style_df_away_rank = (
                                    df_away_rank.style
                                    .format({col: format_value for col in df_away_rank.columns[1:]})
                                    .set_properties(**{"text-align": "center"})
                                )

                                st.subheader(f"Away Ranking for the {selected_season} Season")
                                st.dataframe(style_df_away_rank)


                        # Moving to the section "Season comparison"
                        elif section == "Season comparison":
                            
                            compare_avg_goal_data = get_avg_goals_stats_by_competition()  # Fetch average goals data

                            if compare_avg_goal_data:
                                # Transforming data into a DataFrame with column names
                                df = pd.DataFrame([
                                    {
                                        "Competition": item["competition_name"], "Season": item["season_name"], "Goals/Match": item["avg_goals_per_match"],
                                        "Home Goals": item["avg_home_goals"], "Away Goals": item["avg_away_goals"]
                                    }
                                    for item in compare_avg_goal_data
                                ])                      
                                df = df[df["Competition"] == selected_competition]  # Select values for the chosen competition

                                df = df.drop(columns=["Competition"])  # Remove Competition column for display

                                # Format numeric columns to 2 decimal places
                                numeric_columns = df.columns[1:]
                                df[numeric_columns] = df[numeric_columns].apply(lambda col: col.apply(lambda x: float(round(x, 2)) if pd.notnull(x) else 0.0))

                                df = df.sort_values(by=numeric_columns.tolist(), ascending=False)

                                # Function to highlight the selected season
                                def highlight_selected_season(row):
                                    return ['background-color: lightcoral' if row["Season"] == selected_season else '' for _ in row]

                                # Apply formatting and highlighting
                                styled_df = (
                                    df.style
                                    .format({col: format_value for col in numeric_columns})
                                    .apply(highlight_selected_season, axis=1)
                                    .set_properties(**{"text-align": "center"})
                                )
                                st.subheader("⚽ General Statistics (Averages)")
                                st.dataframe(styled_df)

                                top5_goals_data = get_top5_goals_scored(selected_competition)

                                if top5_goals_data:
                                    df = pd.DataFrame([
                                        {
                                            "Team": item["team_name"], "Season": item["season_name"], "Total Goals": item["total_goals_scored"], "Avg Goals": item["avg_goals_scored"],
                                            "Home Goals": item["goals_scored_home"], "Avg Home Goals": item["avg_goals_scored_home"],
                                            "Away Goals": item["goals_scored_away"], "Avg Away Goals": item["avg_goals_scored_away"]
                                        }
                                        for item in top5_goals_data
                                    ])
                                    numeric_columns = df.columns[2:]

                                    for col in numeric_columns:
                                        df[col] = pd.to_numeric(df[col], errors='coerce')
                                    df[numeric_columns] = df[numeric_columns].apply(lambda col: col.apply(lambda x: float(round(x, 2)) if pd.notnull(x) else 0.0))

                                    df = df.sort_values(by=["Season", "Avg Goals"], ascending=[False, False])

                                    styled_df = (
                                        df.style
                                        .format({col: format_value for col in numeric_columns})
                                        .set_properties(**{"text-align": "center"})
                                    )
                                    st.subheader(f"Top 5 Teams by Goals Scored for {selected_competition} (All Seasons)")
                                    st.dataframe(styled_df)

                                top5_goals_conceded_data = get_top5_goals_conceded(selected_competition)

                                if top5_goals_conceded_data:
                                    df = pd.DataFrame([
                                        {
                                            "Team": item["team_name"], "Season": item["season_name"], "Total Goals Conceded": item["total_goals_conceded"], "Avg Goals Conceded": item["avg_goals_conceded"],
                                            "Home Goals Conceded": item["goals_conceded_home"], "Avg Home Goals Conceded": item["avg_goals_conceded_home"],
                                            "Away Goals Conceded": item["goals_conceded_away"], "Avg Away Goals Conceded": item["avg_goals_conceded_away"]
                                        }
                                        for item in top5_goals_conceded_data
                                    ])
                                    numeric_columns = df.columns[2:]
                                    for col in numeric_columns:
                                        df[col] = pd.to_numeric(df[col], errors='coerce')

                                    df[numeric_columns] = df[numeric_columns].apply(lambda col: col.apply(lambda x: float(round(x, 2)) if pd.notnull(x) else 0.0))

                                    df = df.sort_values(by=["Season", "Avg Goals Conceded"], ascending=[False, True])

                                    styled_df = (
                                        df.style
                                        .format({col: format_value for col in numeric_columns})
                                        .set_properties(**{"text-align": "center"})
                                    )
                                    st.subheader(f"Top 5 Teams by Least Goals Conceded for {selected_competition} (All Seasons)")
                                    st.dataframe(styled_df)

                            # Initialization for comparison of First Goal Scored and Goals Distribution
                            compare_first_goal_data = []
                            compare_distrib_goal_data = []
                            
                            for season in seasons_available:
                                season_stats = get_first_goal_stats(season)
                                distrib_stats = get_distribution_goals(season)
                                distrib_stats = distrib_stats[0]

                                if season_stats:
                                    compare_first_goal_data.extend(season_stats)
                                if distrib_stats:
                                    compare_distrib_goal_data.append(distrib_stats)

                            if compare_first_goal_data:
                                # We bulding a dataframe
                                df = pd.DataFrame([
                                    {
                                        "Season": item["season_name"], "No Goal": item["proportion_no_goal"], "First Goal Home": item["proportion_1st_goal_home"],
                                        "First Goal Away": item["proportion_1st_goal_away"], "First Goal / Win": item["first_goal_win"],
                                        "First Goal / Draw": item["first_goal_draw"], "First Goal / Loss": item["first_goal_lose"],
                                        "First Goal Home / Win": item["first_goal_home_win"], "First Goal Home / Draw": item["first_goal_home_draw"],
                                        "First Goal Home / Loss": item["first_goal_home_lose"], "First Goal Away / Win": item["first_goal_away_win"],
                                        "First Goal Away / Draw": item["first_goal_away_draw"], "First Goal Away / Loss": item["first_goal_away_lose"]
                                    }
                                    for item in compare_first_goal_data
                                ])
                                numeric_columns = df.columns[1:]
                                df[numeric_columns] = df[numeric_columns].astype(float)

                                df = df.sort_values(by=numeric_columns.tolist(), ascending=False)
                                # Creation of the function for coloring the season selected
                                def highlight_selected_season(row):
                                    return ['background-color: lightcoral' if row["Season"] == selected_season else '' for _ in row]

                                styled_df = (
                                    df.style
                                    .format({col: format_value for col in numeric_columns})
                                    .apply(highlight_selected_season, axis=1)
                                    .set_properties(**{"text-align": "center"})
                                )
                                st.subheader("⚽ First Goal Scored or Conceded Information (in %)")
                                st.dataframe(styled_df)

                                top5_first_goal_data = get_top_teams_first_goal(selected_competition) # Retrieving data associated

                                if top5_first_goal_data:
                                    df = pd.DataFrame([
                                        {
                                            "Season": item["season_name"], "Team": item["team_name"], "First Goal Scored %": item["proportion_1st_goal_for"]
                                        }
                                        for item in top5_first_goal_data
                                    ])

                                    df["First Goal Scored %"] = df["First Goal Scored %"].astype(float).map(format_value) # Float
                                    df = df.sort_values(by=["Team", "First Goal Scored %"], ascending=[False, False]) # Sort
                                    # Applying style
                                    styled_df = (
                                        df.style
                                        .set_properties(**{"text-align": "center"})
                                    )
                                    st.subheader(f"Top 5 Teams with Best First Goal Scored Rate for {selected_competition} (All Seasons)")
                                    st.dataframe(styled_df)

                                top5_first_goal_win_data = get_top_teams_first_goal_win(selected_competition)# Retrieving data

                                if top5_first_goal_win_data:
                                    df = pd.DataFrame([
                                        {
                                            "Season": item["season_name"], "Team": item["team_name"], "First Goal Win %": item["first_goal_win"]
                                        }
                                        for item in top5_first_goal_win_data
                                    ])

                                    df["First Goal Win %"] = df["First Goal Win %"].astype(float).map(format_value) # Float
                                    df = df.sort_values(by=["Team", "First Goal Win %"], ascending=[False, False]) # Sort
                                    # Style
                                    styled_df = (
                                        df.style
                                        .set_properties(**{"text-align": "center"})
                                    )
                                    st.subheader(f"Top 5 Teams with Best First Goal Leading to Win Rate for {selected_competition} (All Seasons)")
                                    st.dataframe(styled_df)


                                # Retrieving data for all seasons of the selected competition
                                top5_first_goal_conceded_win_data = get_top_teams_first_goal_conceded_win(selected_competition)

                                if top5_first_goal_conceded_win_data:
                                    # Transforming data into a DataFrame
                                    df = pd.DataFrame([
                                        {
                                            "Season": item["season_name"], "Team": item["team_name"], "1st Goal Conceded but Final Win %": item["first_goal_conceded_win"]
                                        }
                                        for item in top5_first_goal_conceded_win_data
                                    ])
                                    # Convert to float and format
                                    df["1st Goal Conceded but Final Win %"] = df["1st Goal Conceded but Final Win %"].astype(float).map(format_value)
                                    df = df.sort_values(by=["Team", "1st Goal Conceded but Final Win %"], ascending=[False, False])

                                    # Apply formatting and centering
                                    styled_df = (
                                        df.style
                                        .set_properties(**{"text-align": "center"})
                                    )
                                    # Display the table with title
                                    st.subheader(f"Top 5 Teams - 1st Goal Conceded but Final Win for {selected_competition} (All Seasons)")
                                    st.dataframe(styled_df)

                                # Display table on goals distribution
                                if compare_distrib_goal_data:
                                    # Transforming data into a DataFrame
                                    df = pd.DataFrame([
                                        {
                                            "Season": item["season_name"], "1st Half": item["proportion_buts_1ere_periode"], "2nd Half": item["proportion_buts_2nde_periode"],
                                            "0-15 min": item["proportion_buts_0_15"], "16-30 min": item["proportion_buts_16_30"], "31-45 min": item["proportion_buts_31_45"],
                                            "46-60 min": item["proportion_buts_46_60"], "61-75 min": item["proportion_buts_61_75"], "76-90 min": item["proportion_buts_76_90"]
                                        }
                                        for item in compare_distrib_goal_data
                                    ])
                                    numeric_columns = df.columns[1:]
                                    df[numeric_columns] = df[numeric_columns].astype(float)

                                    df = df.sort_values(by=numeric_columns.tolist(), ascending=False)

                                    # Function to highlight the selected season
                                    def highlight_selected_season(row):
                                        return ['background-color: lightcoral' if row["Season"] == selected_season else '' for _ in row]

                                    styled_df = df.style.apply(highlight_selected_season, axis=1)
                                    styled_df = styled_df.format({col: "{:.2f}" for col in numeric_columns})

                                    # Display the formatted table
                                    st.subheader("⚽ Goals Distribution by Season (in %)")
                                    st.dataframe(styled_df.set_properties(**{"text-align": "center"}))

                                # Display table on best first half goal rates
                                top_teams_1st_period_data = get_top_teams_1st_period(selected_competition)

                                if top_teams_1st_period_data:
                                    # Transforming data into a DataFrame
                                    df = pd.DataFrame([
                                        {
                                            "Season": item["season_name"], "Team": item["team_name"], "1st Half Goals %": item["proportion_buts_1ere_periode"],
                                            "1st Half Goals": item["nbr_buts_inscrit_1ere_periode"], "0-15 min Goals %": item["proportion_buts_0_15"],
                                            "0-15 min Goals": item["nbr_buts_0_15"], "16-30 min Goals %": item["proportion_buts_16_30"],
                                            "16-30 min Goals": item["nbr_buts_16_30"], "31-45 min Goals %": item["proportion_buts_31_45"],
                                            "31-45 min Goals": item["nbr_buts_31_45"]
                                        }
                                        for item in top_teams_1st_period_data
                                    ])
                                    numeric_columns = df.columns[2:]
                                    df[numeric_columns] = df[numeric_columns].astype(float)

                                    df = df.sort_values(by=["Season", "1st Half Goals %"], ascending=[False, False])

                                    styled_df = (
                                        df.style
                                        .format({col: format_value for col in numeric_columns})
                                        .set_properties(**{"text-align": "center"})
                                    )
                                    st.subheader(f"Top 5 Teams - Best 1st Half Goal Rates for {selected_competition} (All Seasons)")
                                    st.dataframe(styled_df)

                                # Display table on best second half goal rates
                                top_teams_2nd_period_data = get_top_teams_2nd_period(selected_competition)

                                if top_teams_2nd_period_data:
                                    # Transforming data into a DataFrame
                                    df = pd.DataFrame([
                                        {
                                            "Season": item["season_name"], "Team": item["team_name"], "2nd Half Goals %": item["proportion_buts_inscrit_2nde_periode"],
                                            "2nd Half Goals": item["nbr_buts_inscrit_2nde_periode"], "46-60 min Goals %": item["proportion_buts_46_60"],
                                            "46-60 min Goals": item["nbr_buts_46_60"], "61-75 min Goals %": item["proportion_buts_61_75"],
                                            "61-75 min Goals": item["nbr_buts_61_75"], "76-90 min Goals %": item["proportion_buts_76_90"],
                                            "76-90 min Goals": item["nbr_buts_76_90"]
                                        }
                                        for item in top_teams_2nd_period_data
                                    ])
                                    numeric_columns = df.columns[2:]
                                    df[numeric_columns] = df[numeric_columns].astype(float)

                                    df = df.sort_values(by=["Season", "2nd Half Goals %"], ascending=[False, False])

                                    styled_df = (
                                        df.style
                                        .format({col: format_value for col in numeric_columns})
                                        .set_properties(**{"text-align": "center"})
                                    )
                                    st.subheader(f"Top 5 Teams - Best 2nd Half Goal Rates for {selected_competition} (All Seasons)")
                                    st.dataframe(styled_df)

                                # Display table on goals scored in the last 15 minutes
                                top_teams_last_minutes_data = get_top_teams_last_minutes(selected_competition)

                                if top_teams_last_minutes_data:
                                    # Transforming data into a DataFrame
                                    df = pd.DataFrame([
                                        {
                                            "Season": item["season_name"], "Team": item["team_name"], "76-90 min Goals %": item["proportion_buts_76_90"],
                                            "76-90 min Goals": item["nbr_buts_76_90"]
                                        }
                                        for item in top_teams_last_minutes_data
                                    ])
                                    numeric_columns = df.columns[2:]
                                    df[numeric_columns] = df[numeric_columns].astype(float)

                                    df = df.sort_values(by=["Season", "76-90 min Goals %"], ascending=[False, False])

                                    styled_df = (
                                        df.style
                                        .format({col: format_value for col in numeric_columns})
                                        .set_properties(**{"text-align": "center"})
                                    )
                                    st.subheader(f"Top 5 Teams - Best Goal Rate in the Last 15 Minutes for {selected_competition} (All Seasons)")
                                    st.dataframe(styled_df)

                                # Display table on home/away advantage across seasons
                                compare_home_away_adv_data = get_home_away_advantage()

                                if compare_home_away_adv_data:
                                    df = pd.DataFrame([
                                        {
                                            "Season": item["season_name"], "Home Wins": item["proportion_home_win"], "Draws": item["proportion_draw"],
                                            "Away Wins": item["proportion_away_win"], "Home Advantage": item["home_advantage"]
                                        }
                                        for item in compare_home_away_adv_data
                                    ])
                                    df = df[df["Season"].isin(seasons_available)]

                                    numeric_columns = df.columns[1:]
                                    df[numeric_columns] = df[numeric_columns].astype(float)

                                    df = df.sort_values(by=numeric_columns.tolist(), ascending=False)

                                    def highlight_selected_season(row):
                                        return ['background-color: lightcoral' if row["Season"] == selected_season else '' for _ in row]

                                    styled_df = (
                                        df.style
                                        .format({col: format_value for col in numeric_columns})
                                        .apply(highlight_selected_season, axis=1)
                                        .set_properties(**{"text-align": "center"})
                                    )
                                    st.subheader(f"⚽ Home/Away Factor Influence for {selected_competition} (All Seasons)")
                                    st.dataframe(styled_df)

                                # Display tables for top home/away teams
                                top5_home_rank_data = get_top5_home_rank_competition(selected_competition)

                                if top5_home_rank_data:
                                    df = pd.DataFrame([
                                        {
                                            "Season": item["season_name"], "Team": item["team_name"], "Matches Played": item["all_matches"], "Home Wins": item["number_home_win"],
                                            "Home Draws": item["number_home_draw"], "Home Losses": item["number_home_lose"], "Home Points": item["home_points"],
                                            "Avg Home Points": item["avg_home_points"]
                                        }
                                        for item in top5_home_rank_data
                                    ])
                                    df = df.sort_values(by=["Team", "Avg Home Points"], ascending=[False, False])

                                    styled_df = (
                                        df.style
                                        .format({col: format_value for col in numeric_columns})
                                        .set_properties(**{"text-align": "center"})
                                    )
                                    st.subheader(f"Top 5 Teams - Best Home Records for {selected_competition} (All Seasons)")
                                    st.dataframe(styled_df)

                                top5_away_rank_data = get_top5_away_rank_competition(selected_competition)

                                if top5_away_rank_data:
                                    df = pd.DataFrame([
                                        {
                                            "Season": item["season_name"], "Team": item["team_name"], "Matches Played": item["all_matches"], "Away Wins": item["number_away_win"],
                                            "Away Draws": item["number_away_draw"], "Away Losses": item["number_away_lose"], "Away Points": item["away_points"],
                                            "Avg Away Points": item["avg_away_points"]
                                        }
                                        for item in top5_away_rank_data
                                    ])
                                    df = df.sort_values(by=["Team", "Avg Away Points"], ascending=[False, False])

                                    styled_df = (
                                        df.style
                                        .format({col: format_value for col in numeric_columns})
                                        .set_properties(**{"text-align": "center"})
                                    )
                                    st.subheader(f"Top 5 Teams - Best Away Records for {selected_competition} (All Seasons)")
                                    st.dataframe(styled_df)

        # Image display only if no selection was made
        if show_image:
            st.image(image_path)

def competition_analysis():
    if lang == "Français":
        st.title("🏆 Analyse d'une Compétition") # Titre de l'interface Streamlit associé

        # Vérifie si l'utilisateur a fait un choix (équipe, saison et section)
        show_image = True  # Par défaut, on affiche l'image

        image_path = os.path.join(os.path.dirname(__file__), "image", "banniere_competition.jpg") # Construction du chemin absolu


        st.sidebar.header("🔍 Sélection de la compétition") # Utilisation de la sélection de la compétition en sidebar
        competition_available = get_competitions() # Récupération de la liste des compétitions

        # Dans le cas où la compétition sélectionné est disponibles, on passe au début de l'analyse
        if competition_available:
            selected_competition = st.sidebar.selectbox("Choisissez une compétition :", ["Sélectionnez une compétition"] + competition_available, index=0)
            
            if selected_competition != "Sélectionnez une compétition":
                st.sidebar.header("📊 Sélectionnez une analyse")
                # Affichage des types de sections disponibles
                section = st.sidebar.radio("Sections", ["Statistiques générales", "1er but inscrit", "Distribution des buts", "Domicile / Extérieur","Comparaison entre les compétitions"])

                # Si une section est sélectionnée, on cache l’image
                if section:
                    show_image = False

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
                        # Fonction pour colorer la compétition sélectionnée / Function to colour the selected competition
                        def highlight_selected_competition(row):
                            return ['background-color: lightcoral' if row["Compétition"] == selected_competition else '' for _ in row]
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
                        # Fonction pour colorer la compétition sélectionnée / Function to colour the selected competition
                        def highlight_selected_competition(row):
                            return ['background-color: lightcoral' if row["Compétition"] == selected_competition else '' for _ in row]
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
                        # Fonction pour colorer la compétition sélectionnée / Function to colour the selected competition
                        def highlight_selected_competition(row):
                            return ['background-color: lightcoral' if row["Compétition"] == selected_competition else '' for _ in row]
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
                        # Fonction pour colorer la compétition sélectionnée / Function to colour the selected competition
                        def highlight_selected_competition(row):
                            return ['background-color: lightcoral' if row["Compétition"] == selected_competition else '' for _ in row]
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


        # Affichage de l’image uniquement si aucun choix n'a été fait
        if show_image:
            st.image(image_path)
    else:
        st.title("🏆 Analysis of a competition") # Title

        # Checks if the user has made a selection (team, season and section)
        show_image = True  # By default, we display the image

        image_path = os.path.join(os.path.dirname(__file__), "image", "banniere_competition.jpg") # Build path


        st.sidebar.header("🔍 Competition selection") # Using the competition selection in sidebar
        competition_available = get_competitions() # Retrieve the list of competitions

        # In case the selected competition is available, we go to the beginning of the analysis
        if competition_available:
            selected_competition = st.sidebar.selectbox("Choose a competition :", ["Select a competition"] + competition_available, index=0)
            
            if selected_competition != "Select a competition":
                st.sidebar.header("📊 Select a analysis")
                # Display of available section types
                section = st.sidebar.radio("Sections", ["General statistics", "1st goal scored", "Goal distribution", "Home / Away", "Competition comparison"])

                # If a section is selected, we hide the image
                if section:
                    show_image = False

                st.subheader(f"📌 {section} - {selected_competition}") # Summary
                
                # Display of graphs related to the General Statistics section
                if section == "General statistics":
                    # Retrieving average goals statistics
                    avg_goal_stats = get_avg_goals_stats_by_competition_2()
                    if avg_goal_stats:
                        # Transforming data into a DataFrame with column names
                        df_goals = pd.DataFrame([
                            {
                                "Competition": item["competition_name"], "Goals/Match": item["avg_goals_per_match"],
                                "Home Goals": item["avg_home_goals"], "Away Goals": item["avg_away_goals"]
                            }
                            for item in avg_goal_stats
                        ])
                        # Determining the maximum scale based on the highest observed values
                        max_avg_goals = df_goals["Goals/Match"].max()
                        max_home_goals = df_goals["Home Goals"].max()
                        max_away_goals = df_goals["Away Goals"].max()

                        selected_data = df_goals[df_goals["Competition"] == selected_competition]  # Retrieving the selected competition values

                        if not selected_data.empty:
                            # Converting data to float
                            avg_goals = float(selected_data["Goals/Match"].values[0])
                            avg_home_goals = float(selected_data["Home Goals"].values[0])
                            avg_away_goals = float(selected_data["Away Goals"].values[0])
                            max_avg_goals = float(max_avg_goals)
                            max_home_goals = float(max_home_goals)
                            max_away_goals = float(max_away_goals)

                            col1, col2, col3 = st.columns(3)  # Creating columns to display gauges side by side

                            # Function to calculate color based on the fill rate
                            def get_gauge_color(value, max_value):
                                ratio = value / max_value
                                red = int(210 * (1 - ratio))
                                green = int(210 * ratio)
                                return f"rgb({red},{green},0)"

                            col1, col2, col3 = st.columns(3)  # Creating the gauges again

                            with col1:
                                fig1 = go.Figure(go.Indicator(
                                    mode="gauge+number",
                                    value=avg_goals,
                                    title={"text": "Goals/Match"},
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
                                    title={"text": "Home Goals"},
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
                                    title={"text": "Away Goals"},
                                    gauge={
                                        "axis": {"range": [0, max_away_goals]},
                                        "bar": {"color": get_gauge_color(avg_away_goals, max_away_goals)}
                                    }
                                ))
                                st.plotly_chart(fig3)

                    # Moving on to the frequent scores table (retrieving data)
                    general_stats_data = get_frequent_score_by_competition(selected_competition)
                    if general_stats_data:
                        # Transforming data into a DataFrame with column names
                        df = pd.DataFrame([
                            {
                                "score_home": item["score_home"], "score_away": item["score_away"], "percentage": item["percentage"]
                            }
                            for item in general_stats_data
                        ])
                        # Building the pivot table
                        pivot_table = df.pivot(index="score_home", columns="score_away", values="percentage").fillna(0)
                        pivot_table = pivot_table.apply(pd.to_numeric, errors='coerce').fillna(0)
                        # Creating the figure
                        fig, ax = plt.subplots(figsize=(10, 6))
                        sns.heatmap(pivot_table, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5, ax=ax)
                        ax.set_title(f"Score distribution for {selected_competition} (%)")
                        ax.set_xlabel("Away Score")
                        ax.set_ylabel("Home Score")
                        st.pyplot(fig)

                elif section == "1st goal scored":
                    # Retrieving data for the first goal statistics
                    first_goal = get_first_goal_stats_by_competition(selected_competition)
                    if first_goal:
                        # Transforming data into a DataFrame with column names
                        first_goal = pd.DataFrame([
                            {
                                "Competition": item["competition_name"], "No Goal": item["proportion_no_goal"], "1st Goal - Home": item["proportion_1st_goal_home"],
                                "1st Goal - Away": item["proportion_1st_goal_away"], "1st Goal/Win": item["first_goal_win"],
                                "1st Goal/Draw": item["first_goal_draw"], "1st Goal/Loss": item["first_goal_lose"],
                                "Home 1st Goal/Win": item["first_goal_home_win"], "Home 1st Goal/Draw": item["first_goal_home_draw"],
                                "Home 1st Goal/Loss": item["first_goal_home_lose"], "Away 1st Goal/Win": item["first_goal_away_win"],
                                "Away 1st Goal/Draw": item["first_goal_away_draw"], "Away 1st Goal/Loss": item["first_goal_away_lose"]
                            }
                            for item in first_goal
                        ])

                        # Extracting values for the pie chart of the first team scoring
                        values_proportion = first_goal.iloc[0][["No Goal", "1st Goal - Home", "1st Goal - Away"]].values
                        labels_proportion = ["No Goal", "Home", "Away"]

                        fig, axes = plt.subplots(2, 2, figsize=(15, 10))  # Creating subplots

                        # First pie chart: Proportion of teams scoring first
                        axes[0, 0].pie(values_proportion, labels=labels_proportion, autopct='%1.2f%%', startangle=90,
                                    colors=["#95a5a6", "#3498db", "#e67e22"])
                        axes[0, 0].set_title("Proportion of Teams Scoring First")

                        # Preparing data for the other pie charts
                        first_goal_data = [
                            (["1st Goal/Win", "1st Goal/Draw", "1st Goal/Loss"], "Results after scoring the 1st Goal"),
                            (["Home 1st Goal/Win", "Home 1st Goal/Draw", "Home 1st Goal/Loss"], "Home results after scoring the 1st Goal"),
                            (["Away 1st Goal/Win", "Away 1st Goal/Draw", "Away 1st Goal/Loss"], "Away results after scoring the 1st Goal")
                        ]

                        colors = ["#2ecc71", "#95a5a6", "#e74c3c"]  # Pie chart colors

                        # Loop to generate other pie charts
                        for ax, (cols, title) in zip(axes.flatten()[1:], first_goal_data):
                            values = first_goal.iloc[0][cols].values
                            ax.pie(values, labels=["Win", "Draw", "Loss"], autopct='%1.2f%%', startangle=90, colors=colors)
                            ax.set_title(title)

                        st.pyplot(fig)  # Display the figure

                elif section == "Goal distribution":
                    # Retrieving goal distribution data
                    distrib_goal = get_distribution_goals_by_competition(selected_competition)
                    if distrib_goal:
                        # Transforming into a DataFrame with column names
                        distrib_goal = pd.DataFrame([
                            {
                                "Competition": item["competition_name"], "1st Half": item["proportion_buts_1ere_periode"], "2nd Half": item["proportion_buts_2nde_periode"],
                                "0-15 min": item["proportion_buts_0_15"], "16-30 min": item["proportion_buts_16_30"], "31-45 min": item["proportion_buts_31_45"],
                                "46-60 min": item["proportion_buts_46_60"], "61-75 min": item["proportion_buts_61_75"], "76-90 min": item["proportion_buts_76_90"]
                            }
                            for item in distrib_goal
                        ])
                        distrib_goal = list(distrib_goal.iloc[0, 1:])  # Converting into a list after removing `competition_name`

                        # Creating figure and subplots
                        fig, axes = plt.subplots(1, 2, figsize=(15, 7))  # 1 row, 2 columns

                        # Pie chart: Proportion of goals by half
                        labels_proportion = ["1st Half", "2nd Half"]
                        values_proportion = distrib_goal[:2]
                        axes[0].pie(values_proportion, labels=labels_proportion, autopct='%1.2f%%', startangle=90, colors=["lightblue", "lightcoral"])
                        axes[0].set_title("Proportion of Goals by Half")

                        # Bar chart: Proportion of goals by 15-min intervals
                        labels_intervals = ["0-15 min", "16-30 min", "31-45 min", "46-60 min", "61-75 min", "76-90 min"]
                        values_intervals = list(map(float, distrib_goal[2:]))
                        colors = ["#D4EFDF", "#A9DFBF", "#F9E79F", "#F5CBA7", "#E59866", "#DC7633"]
                        bars = axes[1].bar(labels_intervals, values_intervals, color=colors)
                        axes[1].set_title("Proportion of Goals by 15-Minute Interval")
                        axes[1].set_ylabel("%")
                        axes[1].set_xlabel("Time Interval")
                        axes[1].set_ylim(0, max(values_intervals) + 5)

                        # Adding values above bars
                        for bar in bars:
                            yval = bar.get_height()
                            axes[1].text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval:.2f}%', ha='center', color='black')

                        st.pyplot(fig)  # Display the figure

                # Displaying graphs related to the Home/Away section
                elif section == "Home / Away":
                    result_h_a = get_home_away_advantage_by_competition()  # Retrieving home advantage statistics

                    if result_h_a:
                        # Transforming data into a DataFrame with column names
                        df_adv_home_away = pd.DataFrame([
                            {
                                "Competition": item["competition_name"], "Home Win": item["proportion_home_win"], "Draw": item["proportion_draw"],
                                "Away Win": item["proportion_away_win"], "Home Advantage": item["home_advantage"]
                            }
                            for item in result_h_a
                        ])
                        max_adv_home = df_adv_home_away["Home Advantage"].max()  # Determining the maximum scale
                        max_adv_home = float(max_adv_home)  # Converting to float

                        selected_data = df_adv_home_away[df_adv_home_away["Competition"] == selected_competition]  # Retrieving the selected competition values

                        if not selected_data.empty:
                            # Selecting necessary columns and extracting values as a list
                            values_proportion = selected_data[["Home Win", "Draw", "Away Win"]].values.flatten()

                            labels_proportion = ["Home Win", "Draw", "Away Win"]  # Labels for the pie chart

                            col1, col2 = st.columns(2)  # Creating Streamlit columns

                            # Creating the pie chart
                            with col1:
                                fig1, ax1 = plt.subplots(figsize=(7, 7))
                                ax1.pie(values_proportion, labels=labels_proportion, autopct='%1.2f%%', startangle=90,
                                        colors=["#3498db", "#95a5a6", "#e67e22"])
                                ax1.set_title("Proportion of results by Home/Away factor")
                                st.pyplot(fig1)

                            adv_home = float(selected_data["Home Advantage"].values[0])  # Extracting home advantage value

                            # Function to calculate color based on the fill rate
                            def get_gauge_color(value, max_value):
                                if max_value == 0:  # Avoid division by zero
                                    return "rgb(210,0,0)"
                                ratio = max(0, min(value / max_value, 1))  # Ensure the ratio is between 0 and 1
                                red = int(210 * (1 - ratio))
                                green = int(210 * ratio)
                                return f"rgb({red},{green},0)"

                            # Creating the gauge chart
                            with col2:
                                fig2 = go.Figure(go.Indicator(
                                    mode="gauge+number",
                                    value=adv_home,
                                    title={"text": "Home Advantage (%)"},
                                    gauge={
                                        "axis": {"range": [0, max_adv_home]},
                                        "bar": {"color": get_gauge_color(adv_home, max_adv_home)}
                                    }
                                ))
                                st.plotly_chart(fig2)

                # Displaying graphs related to the Comparison between Competitions section
                elif section == "Competition comparison":

                    # Initializing comparison variables
                    compare_first_goal_data = []
                    compare_distrib_goal_data = []

                    # Storing average goal statistics and Home/Away influence data
                    compare_avg_goal_data = get_avg_goals_stats_by_competition_2()
                    compare_home_away_adv_data = get_home_away_advantage_by_competition()

                    # Retrieving first goal and goal distribution information
                    for competition in competition_available:
                        compare_first_goal_stats = get_first_goal_stats_by_competition(competition)
                        if compare_first_goal_stats:
                            compare_first_goal_data.extend(compare_first_goal_stats)  # Storing all data by competition
                        compare_distrib_goal_stats = get_distribution_goals_by_competition(competition)
                        compare_distrib_goal_stats = compare_distrib_goal_stats[0]
                        if compare_distrib_goal_stats:
                            compare_distrib_goal_data.append(compare_distrib_goal_stats)  # Storing all data by competition

                    if compare_avg_goal_data:
                        # Transforming data into a DataFrame with column names
                        df = pd.DataFrame([
                            {
                                "Competition": item["competition_name"], "Goals/Match": item["avg_goals_per_match"],
                                "Home Goals": item["avg_home_goals"], "Away Goals": item["avg_away_goals"]
                            }
                            for item in compare_avg_goal_data
                        ])

                        numeric_columns = df.columns[1:]  # Processing numeric data
                        df[numeric_columns] = df[numeric_columns].astype(float).round(2)

                        df = df.sort_values(by=numeric_columns.tolist(), ascending=False)  # Ensure numerical sorting

                        # Function to highlight the selected competition
                        def highlight_selected_competition(row):
                            return ['background-color: lightcoral' if row["Competition"] == selected_competition else '' for _ in row]

                        # Applying formatting and custom highlighting
                        styled_df = (
                            df.style
                            .format({col: format_value for col in numeric_columns})
                            .apply(highlight_selected_competition, axis=1)
                            .set_properties(**{"text-align": "center"})
                        )

                        st.subheader("⚽ General statistics information (average)")
                        st.dataframe(styled_df)

                    if compare_first_goal_data:
                        # Transforming data into a DataFrame with column names
                        df = pd.DataFrame([
                            {
                                "Competition": item["competition_name"], "No Goal": item["proportion_no_goal"], "1st Goal - Home": item["proportion_1st_goal_home"],
                                "1st Goal - Away": item["proportion_1st_goal_away"], "1st Goal/Win": item["first_goal_win"],
                                "1st Goal/Draw": item["first_goal_draw"], "1st Goal/Loss": item["first_goal_lose"],
                                "Home 1st Goal/Win": item["first_goal_home_win"], "Home 1st Goal/Draw": item["first_goal_home_draw"],
                                "Home 1st Goal/Loss": item["first_goal_home_lose"], "Away 1st Goal/Win": item["first_goal_away_win"],
                                "Away 1st Goal/Draw": item["first_goal_away_draw"], "Away 1st Goal/Loss": item["first_goal_away_lose"]
                            }
                            for item in compare_first_goal_data
                        ])
                        numeric_columns = df.columns[1:]  # Processing numeric data
                        df[numeric_columns] = df[numeric_columns].astype(float)

                        df = df.sort_values(by=numeric_columns.tolist(), ascending=False)  # Ensure numerical sorting

                        styled_df = (
                            df.style
                            .format({col: format_value for col in numeric_columns})
                            .apply(highlight_selected_competition, axis=1)
                            .set_properties(**{"text-align": "center"})
                        )

                        st.subheader("⚽ Information on the 1st goal scored (in %)")
                        st.dataframe(styled_df)

                    if compare_distrib_goal_data:
                        # Transforming into a DataFrame based on column names
                        df = pd.DataFrame([
                            {
                                "Competition": item["competition_name"], "1st Half": item["proportion_buts_1ere_periode"], "2nd Half": item["proportion_buts_2nde_periode"],
                                "0-15 min": item["proportion_buts_0_15"], "16-30 min": item["proportion_buts_16_30"], "31-45 min": item["proportion_buts_31_45"],
                                "46-60 min": item["proportion_buts_46_60"], "61-75 min": item["proportion_buts_61_75"], "76-90 min": item["proportion_buts_76_90"]
                            }
                            for item in compare_distrib_goal_data
                        ])
                        numeric_columns = df.columns[1:]  # Processing numeric data
                        df[numeric_columns] = df[numeric_columns].astype(float)

                        df = df.sort_values(by=numeric_columns.tolist(), ascending=False)

                        styled_df = (
                            df.style
                            .format({col: format_value for col in numeric_columns})
                            .apply(highlight_selected_competition, axis=1)
                            .set_properties(**{"text-align": "center"})
                        )

                        st.subheader("⚽ Information on goal distribution (in %)")
                        st.dataframe(styled_df)

                    if compare_home_away_adv_data:
                        # Transforming data into a DataFrame with column names
                        df = pd.DataFrame([
                            {
                                "Competition": item["competition_name"], "Home Win": item["proportion_home_win"], "Draw": item["proportion_draw"],
                                "Away Win": item["proportion_away_win"], "Home Advantage": item["home_advantage"]
                            }
                            for item in compare_home_away_adv_data
                        ])
                        numeric_columns = df.columns[1:]
                        df[numeric_columns] = df[numeric_columns].astype(float)

                        df = df.sort_values(by=numeric_columns.tolist(), ascending=False)

                        styled_df = (
                            df.style
                            .format({col: format_value for col in numeric_columns})
                            .apply(highlight_selected_competition, axis=1)
                            .set_properties(**{"text-align": "center"})
                        )

                        st.subheader("⚽ Information on the influence of the Home/Away factor (in %)")
                        st.dataframe(styled_df)

        # Image display only if no selection was made
        if show_image:
            st.image(image_path)

# Appel de la bonne fonction
if menu in ["Accueil", "Home"]:
    home()
elif menu in ["Équipe", "Team"]:
    team_analysis()
elif menu in ["Duel", "H2H"]:
    team_head_to_head_analysis()
elif menu in ["Saison", "Season"]:
    season_analysis()
elif menu in ["Ligue", "League"]:
    competition_analysis()
