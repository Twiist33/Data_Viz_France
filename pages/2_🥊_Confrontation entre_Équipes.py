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
import plotly.express as px

st.set_page_config(page_title="Data Viz ⚽ 🇫🇷", page_icon="📊", layout="wide") # Configuration de la page Streamlit

load_dotenv() # Chargement des variables d'environnement

# Connexion à la base de données Supabase
project_url = os.getenv("project_url")
api_key = os.getenv("api_key")
supabase = create_client(project_url, api_key)

# Fonction pour récupérer les équipes disponibles dans la table team
def get_teams():
    try:
        # Appel de la fonction RPC avec params comme dictionnaire vide
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
def get_seasons(team_name):
    try:
        # Appel de la fonction RPC avec les paramètres dans le dictionnaire 'params'
        response = supabase.rpc("get_seasons", params={"team_name_input": team_name}).execute()
        if response.data:
            seasons = response.data
        else:
            seasons = []
        return seasons
    except Exception as e:
        st.error(f"Erreur de connexion à Supabase : {e}")
        return []

# Fonction pour récupérer les équipes présents dans la saison de la 1ère équipe choisi
def get_teams_in_season(season_name):
    try:
        # Appel de la fonction RPC avec les paramètres dans le dictionnaire 'params'
        response = supabase.rpc("get_teams_in_season", params={"season_name_input": season_name}).execute()
        if response.data:
            seasons = response.data
        else:
            seasons = []
        return seasons
    except Exception as e:
        st.error(f"Erreur de connexion à Supabase : {e}")
        return []

# Fonction pour récupérer les statistiques de moyenne de buts par match pour deux équipes donnée regroupé par saison (au moins 5 matchs dans cette saison pour être comptabilisé)
def get_avg_goals_stats(season_name):
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_avg_goals_stats", params={"season_name_input": season_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des statistiques : {e}")
        return []

# Fonction pour récupérer les statistiques sur le 1er but inscrit ou concédé entre deux équipes
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

# Fonction sur les informations de la saison à domicile et à l'extérieur pour 2 équipes d'une saison donnée (au moins 5 matchs dans cette saison pour être comptabilisé)
def get_rank_season(season_name):
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_rank_season", params={"season_name_input": season_name}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les matchs opposant 2 équipes
def get_matches_between_teams(selected_team_home, selected_team_away):
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_matches_between_teams", params={"selected_team_home_input": selected_team_home, "selected_team_away_input": selected_team_away}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour calculer la moyenne des buts inscrits lorsque deux équipes s'affrontent
def get_avg_goals_stats_between_teams(selected_team_home, selected_team_away):
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_avg_goals_stats_between_teams", params={"selected_team_home_input": selected_team_home, "selected_team_away_input": selected_team_away}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les informations du premier but inscrit entre deux équipes
def get_1st_goal_stats_between_teams(selected_team_home, selected_team_away):
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_1st_goal_stats_between_teams", params={"selected_team_home_input": selected_team_home, "selected_team_away_input": selected_team_away}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récupérer les informations des proportions cumulées des buts inscrits
def get_distrib_goal_between_teams(selected_team_home, selected_team_away):
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_distrib_goal_between_teams", params={"selected_team_home_input": selected_team_home, "selected_team_away_input": selected_team_away}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour récuperer les performances à face à face dans cette configurations entre deux équipes               
def get_home_away_selected_teams(selected_team_home, selected_team_away):
    try:
        # Appel de la fonction RPC avec le paramètre de la saison
        response = supabase.rpc("get_home_away_selected_teams", params={"selected_team_home_input": selected_team_home, "selected_team_away_input": selected_team_away}).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Fonction pour colorer les jauges
def plot_gauge(value, max_value, title, inverse=False):
    # Calcul de la couleur en fonction du ratio valeur/max
    ratio = value / max_value
    if inverse:
        red = int(210 * ratio)  # Plus c'est haut, plus c'est rouge
        green = int(210 * (1 - ratio))
    else:
        red = int(210 * (1 - ratio))  # Plus c'est bas, plus c'est rouge
        green = int(210 * ratio)
    color = f"rgb({red},{green},0)"

    # Création de la jauge
    return go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title, "font": {"size": 9}},  # Réduction de la taille du titre
        gauge={
            "axis": {"range": [0, max_value]},
            "bar": {"color": color}  # Couleur dynamique
        }
    ))

st.title("🥊 Confrontation entre Équipes") # Titre de l'application

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

                                fig, axes = plt.subplots(4, 3, figsize=(18, 16))  # 4 lignes et 3 colonnes
                                    
                                # Graphiques pour l'équipe à domicile
                                # 1ère ligne
                                axes[0, 0].pie(df_home.iloc[0, :3], labels=["1er but inscrit", "Aucun but", "1er but encaissé"],
                                                autopct='%1.2f%%', startangle=90, colors=["#2ecc71", "#95a5a6", "#e74c3c"])
                                axes[0, 0].set_title(f"1er but - {selected_team_home}")

                                axes[0, 1].pie(df_home.iloc[0, 9:12], labels=["Victoire", "Nul", "Défaite"],
                                                autopct='%1.2f%%', startangle=90, colors=["#2ecc71", "#f1c40f", "#e74c3c"])
                                axes[0, 1].set_title(f"Résultats après 1er but inscrit - {selected_team_home}")

                                axes[0, 2].pie(df_home.iloc[0, 18:21], labels=["Victoire", "Nul", "Défaite"],
                                                autopct='%1.2f%%', startangle=90, colors=["#2ecc71", "#f1c40f", "#e74c3c"])
                                axes[0, 2].set_title(f"Résultats après 1er but encaissé - {selected_team_home}")

                                # 2ème ligne
                                axes[1, 0].pie(df_home.iloc[0, 3:6], labels=["Domicile / 1er but inscrit", "Domicile / Aucun but", "Domicile / 1er but encaissé"],
                                                autopct='%1.2f%%', startangle=90, colors=["#2ecc71", "#95a5a6", "#e74c3c"])
                                axes[1, 0].set_title(f"Résultats à domicile - {selected_team_home}")
                                    
                                axes[1, 1].pie(df_home.iloc[0, 12:15], labels=["Domicile / Victoire", "Domicile / Nul", "Domicile / Défaite"],
                                                autopct='%1.2f%%', startangle=90, colors=["#2ecc71", "#f1c40f", "#e74c3c"])
                                axes[1, 1].set_title(f"Domicile après 1er but inscrit - {selected_team_home}")

                                axes[1, 2].pie(df_home.iloc[0, 21:24], labels=["Victoire", "Nul", "Défaite"],
                                                autopct='%1.2f%%', startangle=90, colors=["#2ecc71", "#f1c40f", "#e74c3c"])
                                axes[1, 2].set_title(f"Domicile après 1er but encaissé - {selected_team_home}")

                                # Graphiques pour l'équipe à l'extérieur
                                # 3ème ligne
                                axes[2, 0].pie(df_away.iloc[0, :3], labels=["1er but inscrit", "Aucun but", "1er but encaissé"],
                                                autopct='%1.2f%%', startangle=90, colors=["#2ecc71", "#95a5a6", "#e74c3c"])
                                axes[2, 0].set_title(f"1er but - {selected_team_away}")

                                axes[2, 1].pie(df_away.iloc[0, 9:12], labels=["Victoire", "Nul", "Défaite"],
                                                autopct='%1.2f%%', startangle=90, colors=["#2ecc71", "#f1c40f", "#e74c3c"])
                                axes[2, 1].set_title(f"Résultats après 1er but inscrit - {selected_team_away}")

                                axes[2, 2].pie(df_away.iloc[0, 18:21], labels=["Victoire", "Nul", "Défaite"],
                                                autopct='%1.2f%%', startangle=90, colors=["#2ecc71", "#f1c40f", "#e74c3c"])
                                axes[2, 2].set_title(f"Résultats après 1er but encaissé - {selected_team_away}")                               

                                # 4ème ligne
                                axes[3, 0].pie(df_away.iloc[0, 6:9], labels=["Extérieur / 1er but inscrit", "Extérieur / Aucun but", "Extérieur / 1er but encaissé"],
                                                autopct='%1.2f%%', startangle=90, colors=["#2ecc71", "#95a5a6", "#e74c3c"])
                                axes[3, 0].set_title(f"Résultats à l'extérieur - {selected_team_away}")
                                    
                                axes[3, 1].pie(df_away.iloc[0, 15:18], labels=["Extérieur / Victoire", "Extérieur / Nul", "Extérieur / Défaite"],
                                                    autopct='%1.2f%%', startangle=90, colors=["#2ecc71", "#f1c40f", "#e74c3c"])
                                axes[3, 1].set_title(f"Extérieur après 1er but inscrit - {selected_team_away}")

                                axes[3, 2].pie(df_away.iloc[0, 24:], labels=["Victoire", "Nul", "Défaite"],
                                                autopct='%1.2f%%', startangle=90, colors=["#2ecc71", "#f1c40f", "#e74c3c"])
                                axes[3, 2].set_title(f"Extérieur après 1er but encaissé - {selected_team_away}")                           

                                plt.tight_layout() # On affiche les graphiques
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
                                
                                # Création d'une fonction pour générer les graphiques de distribution de buts par équipe
                                def plot_distribution_graphs(data, title_prefix):
                                    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
                                    
                                    # Proportions des buts inscrits par période
                                    labels_proportion = ["1ère période", "2ème période"]
                                    values_proportion_goal_scored = data.iloc[0, :2]
                                    axes[0, 0].pie(values_proportion_goal_scored, labels=labels_proportion, autopct='%1.2f%%', startangle=90, colors=["lightblue", "lightcoral"])
                                    axes[0, 0].set_title(f"{title_prefix} - Proportion des buts inscrits par période")
                                    
                                    # Proportions des buts concédés par période
                                    values_proportion_goal_conceded = data.iloc[0, 8:10]
                                    axes[0, 1].pie(values_proportion_goal_conceded, labels=labels_proportion, autopct='%1.2f%%', startangle=90, colors=["lightblue", "lightcoral"])
                                    axes[0, 1].set_title(f"{title_prefix} - Proportion des buts concédés par période")
                                    
                                    # Proportions des buts inscrits par intervalle de 15 min
                                    labels_intervals = ["0-15 min", "16-30 min", "31-45 min", "46-60 min", "61-75 min", "76-90 min"]
                                    values_intervals_goal_scored = data.iloc[0, 2:8]
                                    colors = ["#D4EFDF", "#A9DFBF", "#F9E79F", "#F5CBA7", "#E59866", "#DC7633"]
                                    bars1 = axes[1, 0].bar(labels_intervals, values_intervals_goal_scored, color=colors)
                                    axes[1, 0].set_title(f"{title_prefix} - Proportion des buts inscrits par intervalle de 15 min")
                                    axes[1, 0].set_ylabel("%")
                                    axes[1, 0].set_ylim(0, max(values_intervals_goal_scored) + 5)
                                    
                                    # Proportions des buts concédés par intervalle de 15 min
                                    values_intervals_goal_conceded = data.iloc[0, 10:16]
                                    bars2 = axes[1, 1].bar(labels_intervals, values_intervals_goal_conceded, color=colors)
                                    axes[1, 1].set_title(f"{title_prefix} - Proportion des buts concédés par intervalle de 15 min")
                                    axes[1, 1].set_ylabel("%")
                                    axes[1, 1].set_ylim(0, max(values_intervals_goal_conceded) + 5)
                                    
                                    # Ajout des valeurs sur les barres
                                    for bars in [bars1, bars2]:
                                        for bar in bars:
                                            yval = bar.get_height()
                                            axes[1, 0 if bars is bars1 else 1].text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval:.2f}%', ha='center', color='black')
                                    
                                    st.pyplot(fig) # Affichage du tableau
                                
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

                                    # Création du diagramme circulaire
                                    with col1:
                                        fig1, ax1 = plt.subplots(figsize=(7, 7))  
                                        ax1.pie(values_proportion_home, labels=labels_proportion_home, autopct='%1.2f%%', startangle=90, colors=["#2ecc71", "#95a5a6", "#e74c3c"])
                                        ax1.set_title(f"Proportion des résultats à Domicile - {selected_team_home}")
                                        st.pyplot(fig1)  

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
                                        ax3.pie(values_proportion_away, labels=labels_proportion_away, autopct='%1.2f%%', startangle=90, colors=["#2ecc71", "#95a5a6", "#e74c3c"])
                                        ax3.set_title(f"Proportion des résultats à l'Extérieur - {selected_team_away}")
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
                                    
                                    # Graphiques pour l'équipe selected_team_home
                                    # 1ère ligne : 1er but inscrit
                                    if df_home.iloc[0, :3].sum() > 0:  # Vérifier que les valeurs ne sont pas toutes nulles
                                        axes[0].pie(df_home.iloc[0, :3], labels=["1er but inscrit", "Aucun but", "1er but encaissé"],
                                                    autopct='%1.2f%%', startangle=90, colors=["#2ecc71", "#95a5a6", "#e74c3c"])
                                        axes[0].set_title(f"{selected_team_home} - 1er but inscrit")

                                    # 2ème ligne : Résultats après 1er but inscrit
                                    if df_home.iloc[0, 3:6].sum() > 0:  # Vérifier que les valeurs ne sont pas toutes nulles
                                        axes[1].pie(df_home.iloc[0, 3:6], labels=["Victoire", "Nul", "Défaite"],
                                                    autopct='%1.2f%%', startangle=90, colors=["#2ecc71", "#f1c40f", "#e74c3c"])
                                        axes[1].set_title(f"{selected_team_home} - Résultats après 1er but inscrit")
                                    
                                    # 3ème ligne : Résultats après 1er but encaissé
                                    if df_home.iloc[0, 6:].sum() > 0:  # Vérifier que les valeurs ne sont pas toutes nulles
                                        axes[2].pie(df_home.iloc[0, 6:], labels=["Victoire", "Nul", "Défaite"],
                                                    autopct='%1.2f%%', startangle=90, colors=["#2ecc71", "#f1c40f", "#e74c3c"])
                                        axes[2].set_title(f"{selected_team_home} - Résultats après 1er but encaissé")
                                    else:
                                        # Si aucune donnée à afficher, masquer la colonne correspondante
                                        axes[0].axis('off')  # Masque l'axe du graphique
                                        axes[1].axis('off')  # Masque l'axe du graphique
                                        axes[2].axis('off')  # Masque l'axe du graphique

                                    plt.tight_layout()  # Ajuste l'affichage pour éviter les chevauchements
                                    st.pyplot(fig) # On affiche la figure

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

                                        # Labels pour les diagrammes
                                        labels_proportion = ["Victoire", "Match Nul", "Défaite"]
                                        labels_proportion_home = ["Victoire à domicile", "Match Nul", "Défaite à domicile"]

                                        # Première ligne : Diagramme circulaire général
                                        with st.container():
                                            col1 = st.columns(1)  
                                            with col1[0]:
                                                fig1, ax1 = plt.subplots(figsize=(3, 3))
                                                wedges, texts, autotexts = ax1.pie(
                                                    values_proportion, 
                                                    labels=labels_proportion, 
                                                    autopct='%1.2f%%', 
                                                    startangle=90, 
                                                    colors=["#2ecc71", "#95a5a6", "#e74c3c"],
                                                    textprops={'fontsize': 6}
                                                )
                                                
                                                # Réduction manuelle de la taille des labels et pourcentages si nécessaire
                                                for text in texts:
                                                    text.set_fontsize(6)
                                                for autotext in autotexts:
                                                    autotext.set_fontsize(6)

                                                # Titre avec une taille plus petite
                                                ax1.set_title(
                                                    f"Proportion des résultats de {selected_team_home} contre {selected_team_away} (tous matchs confondus)", 
                                                    fontsize=6
                                                )
                                                st.pyplot(fig1) # On affiche la figure

                                        # Deuxième ligne : Résultats à domicile + Jauge
                                        if total_home != 0: # Si le nombre de buts est nulle, on n'affiche pas les graphiques associés

                                            with st.container():
                                                col2, col3 = st.columns(2)

                                                with col2:
                                                    fig2, ax2 = plt.subplots(figsize=(7, 7))
                                                    ax2.pie(values_proportion_home, labels=["Victoire à domicile", "Match Nul", "Défaite à domicile"], autopct='%1.2f%%', startangle=90, colors=["#2ecc71", "#95a5a6", "#e74c3c"])
                                                    ax2.set_title(f"Proportion des résultats à Domicile de {selected_team_home} contre {selected_team_away}")
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