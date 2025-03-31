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

# Fonction pour récupérer les statistiques de moyenne de buts par match pour une équipe donnée regroupé par saison (au moins 5 matchs dans cette saison pour être comptabilisé)
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

# Fonction pour récupérer les information de buts inscrits par une équipe, regroupé par saison (au moins 5 matchs dans cette saison pour être comptabilisé)
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

# Fonction pour récupérer les information de buts concédés pour une équipe donnée, regroupé par saison
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

# Fonction pour récupérer la fréquence des scores d'une équipe pour une saison donnée (au moins 5 matchs dans cette saison pour être comptabilisé)
def get_frequent_score(team_name, season_name):
    try:
        # Appel de la fonction RPC avec le paramètre de l'équipe et de la saison
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

# Fonction sur les informations de la saison à domicile et à l'extérieur pour chaque équipe d'une saison donnée (au moins 5 matchs dans cette saison pour être comptabilisé)
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

# Fonction personnalisée pour le formatage conditionnel
def format_value(x):
    if pd.isnull(x):
        return "0"
    elif x == int(x):
        return str(int(x))  # Affiche sans décimales si entier
    else:
        return f"{x:.2f}"   # Affiche avec 2 décimales sinon

# Fonction pour colorer la saison sélectionnée
def highlight_selected_season(row):
    return ['background-color: lightcoral' if row["Saison"] == selected_season else '' for _ in row]

# Fonction pour colorer l'équipe sélectionnée
def highlight_selected_squad(row):
    return ['background-color: lightcoral' if row["Équipe"] == selected_team else '' for _ in row]

st.title("📊 Analyse d'une Équipe") # Titre de l'application

if "selected_season" not in st.session_state or st.session_state.get("selected_season") == "Sélectionnez une saison":
    st.image("Image/banniere_equipe.jpg") # Utilisation de la 1er bannière en image

st.sidebar.header("🔍 Sélection de l'équipe") # Sélection de la compétition en sidebar
teams_available = get_teams()

# Boucle pour selectionner l'équipe de son choix présent dans la base de données
if teams_available:
    selected_team = st.sidebar.selectbox("Choisissez une équipe :", ["Sélectionnez une équipe"] + teams_available, index=0)
    
    if teams_available != "Sélectionnez une équipe":
        st.sidebar.header("🔍 Sélection de la saison") # Sélection de la saison en fonction de l'équipe choisie
        seasons_available = get_seasons(selected_team) # Récupération des données
        
        # Selection des saisons disponibles pour l'équipe de son choix (doit avoir au moins 5 matchs joué dans une saison pour être comptabilisé)
        if seasons_available:
            selected_season = st.sidebar.selectbox("Choisissez une saison :", ["Sélectionnez une saison"] + seasons_available, index=0)
            
            # Selection de la section de notre choix
            if selected_season != "Sélectionnez une saison":
                st.sidebar.header("📊 Sélectionnez une analyse")
                section = st.sidebar.radio("Sections", ["Statistiques générales", "1er but inscrit", "Distribution des buts", "Domicile / Extérieur", "Comparaison entre les saisons"])
                
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
                        df[numeric_columns] = df[numeric_columns].applymap(
                            lambda x: int(x) if pd.notnull(x) and x == int(x) else (round(x, 2) if pd.notnull(x) else 0)
                        )
                        
                        # Trier par le nombre de buts inscrits
                        df = df.sort_values(by=["Nbr. buts inscrits"], ascending=False)
                        
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
                        df[numeric_columns] = df[numeric_columns].applymap(
                            lambda x: int(x) if pd.notnull(x) and x == int(x) else (round(x, 2) if pd.notnull(x) else 0)
                        )
                        
                        # Trier par le nombre de buts concédés
                        df = df.sort_values(by=["Nbr. buts concédés"], ascending=False)
                        
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
                        
                        fig, axes = plt.subplots(3, 3, figsize=(18, 12)) # Création de la figure avec 3 lignes et 3 colonnes

                        # Proportion du 1er but
                        axes[0, 0].pie(
                            first_goal_team.iloc[0, :3], labels=["1er but inscrit", "Aucun but", "1er but encaissé"],
                            autopct='%1.2f%%', startangle=90, colors=["#2ecc71", "#95a5a6", "#e74c3c"]
                        )
                        axes[0, 0].set_title(f"Proportion du 1er but pour {selected_team} durant la {selected_season}")

                        # Résultats à domicile
                        axes[0, 1].pie(
                            first_goal_team.iloc[0, 3:6], labels=["Domicile / 1er but inscrit", "Domicile / Aucun but", "Domicile / 1er but encaissé"],
                            autopct='%1.2f%%', startangle=90, colors=["#2ecc71", "#95a5a6", "#e74c3c"]
                        )
                        axes[0, 1].set_title("Résultats à domicile")

                        # Résultats à l'extérieur
                        axes[0, 2].pie(
                            first_goal_team.iloc[0, 6:9], labels=["Extérieur / 1er but inscrit", "Extérieur / Aucun but", "Extérieur / 1er but encaissé"],
                            autopct='%1.2f%%', startangle=90, colors=["#2ecc71", "#95a5a6", "#e74c3c"]
                        )
                        axes[0, 2].set_title("Résultats à l'extérieur")

                        # --- 2ème ligne : 1er but inscrit ---
                        data_labels_inscrit = [
                            (first_goal_team.iloc[0, 9:12], "Proportion des résultats après 1er but inscrit"),
                            (first_goal_team.iloc[0, 12:15], "Résultats à domicile après 1er but inscrit"),
                            (first_goal_team.iloc[0, 15:18], "Résultats à l'extérieur après 1er but inscrit"),
                        ]

                        for ax, (values, title) in zip(axes[1], data_labels_inscrit):
                            ax.pie(values, labels=["Victoire", "Match nul", "Défaite"], autopct='%1.2f%%', startangle=90, colors=["#2ecc71", "#95a5a6", "#e74c3c"])
                            ax.set_title(title)

                        # --- 3ème ligne : 1er but encaissé ---
                        data_labels_encaissé = [
                            (first_goal_team.iloc[0, 18:21], "Proportion des résultats après 1er but encaissé"),
                            (first_goal_team.iloc[0, 21:24], "Résultats à domicile après 1er but encaissé"),
                            (first_goal_team.iloc[0, 24:27], "Résultats à l'extérieur après 1er but encaissé"),
                        ]

                        for ax, (values, title) in zip(axes[2], data_labels_encaissé):
                            ax.pie(values, labels=["Victoire", "Match nul", "Défaite"], autopct='%1.2f%%', startangle=90, colors=["#2ecc71", "#95a5a6", "#e74c3c"])
                            ax.set_title(title)

                        st.pyplot(fig) # Affichage des graphiques dans Streamlit

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

                            col1, col2 = st.columns(2) # Création des colonnes Streamlit à Domicile

                            # Création du diagramme circulaire
                            with col1:
                                fig1, ax1 = plt.subplots(figsize=(7, 7))  
                                ax1.pie(values_proportion_home, labels=labels_proportion_home, autopct='%1.2f%%', startangle=90, colors=["#2ecc71", "#95a5a6", "#e74c3c"])
                                ax1.set_title("Proportion des résultats à Domicile")
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
                                    title={"text": "Avantage du terrain à Domicile (en %)"},
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
                                ax3.set_title("Proportion des résultats à l'Extérieur")
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
                            
                            style_rank_away_data = (
                                rank_away_data.style
                                .format({col: format_value for col in rank_away_data.columns[1:]})  # Correction ici aussi
                                .apply(highlight_selected_squad, axis=1)
                                .set_properties(**{"text-align": "center"})
                            )
                            
                            st.subheader(f"Classement à l'extérieur pour la saison de {selected_season}")
                            st.dataframe(style_rank_away_data)

                elif section == "Comparaison entre les saisons":

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
                        df[numeric_columns] = df[numeric_columns].applymap(
                            lambda x: int(x) if pd.notnull(x) and x == int(x) else (round(x, 2) if pd.notnull(x) else 0)
                        )
                        
                        df = df.sort_values(by=numeric_columns.tolist(), ascending=False) # Trier le tableau
                        
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

                        for col in df_adv_home_away_team.columns:
                            if col not in ["Équipe", "Saison", "Type"]:
                                # Utilisation de .loc pour des assignations sûres
                                df_adv_home_away_team.loc[:, col] = pd.to_numeric(df_adv_home_away_team[col], errors='coerce')

                        # Récupération des valeurs selon le facteur Domicile/Extérieur avec copie explicite
                        data_home = df_adv_home_away_team[df_adv_home_away_team["Type"] == "Home"].copy()
                        data_away = df_adv_home_away_team[df_adv_home_away_team["Type"] == "Away"].copy()

                        # Retrait des colonnes inutiles
                        data_home = data_home.drop(columns=["Équipe", "Type"])
                        data_away = data_away.drop(columns=["Équipe", "Type"])

                        if not data_home.empty:
                            # Utilisation de .loc pour l'assignation conditionnelle
                            data_home.loc[:, ["Victoire (en %)", "Match Nul (en %)", "Défaite (en %)"]] = (
                                data_home[["Victoire (en %)", "Match Nul (en %)", "Défaite (en %)"]].div(data_home["Matches joués"], axis=0)
                            ) * 100

                            data_home = data_home.sort_values(by=["Points"], ascending=False)
                            style_data_home = (
                                data_home.style
                                .format({col: format_value for col in data_home.columns[1:]})
                                .apply(highlight_selected_season, axis=1)
                                .set_properties(**{"text-align": "center"})
                            )
                            st.subheader(f"⚽ Informations sur les performances à domicile de {selected_team} (toutes saisons)")
                            st.dataframe(style_data_home)

                        if not data_away.empty:
                            # Utilisation de .loc pour l'assignation conditionnelle
                            data_away.loc[:, ["Victoire (en %)", "Match Nul (en %)", "Défaite (en %)"]] = (
                                data_away[["Victoire (en %)", "Match Nul (en %)", "Défaite (en %)"]].div(data_away["Matches joués"], axis=0)
                            ) * 100

                            data_away = data_away.sort_values(by=["Points"], ascending=False)
                            style_data_away = (
                                data_away.style
                                .format({col: format_value for col in data_away.columns[1:]})
                                .apply(highlight_selected_season, axis=1)
                                .set_properties(**{"text-align": "center"})
                            )
                            st.subheader(f"⚽ Informations sur les performances à l'extérieur de {selected_team} (toutes saisons)")
                            st.dataframe(style_data_away)