# Import des librairies
import json
import time
import numpy as  np
import pandas as pd
from bs4 import BeautifulSoup
from pydantic import BaseModel
from typing import List, Optional
from selenium import webdriver
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import psycopg2
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, date
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm

# Charger le fichier .env
load_dotenv()

# Connection à la base de données Supabase
def connect_to_supabase():
    project_url = os.getenv("PROJECT_URL")
    api_key = os.getenv("API_KEY")
    
    if not api_key:
        raise ValueError("La clé API de Supabase est manquante !")
    
    try:
        supabase = create_client(project_url, api_key)
        print("✅ Connexion réussie à Supabase !")
        return supabase
    except Exception as e:
        print(f"❌ Erreur de connexion à Supabase : {e}")
        return None

# Connection à la base de données via Postgres
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DBNAME"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST"),
            port=os.getenv("PORT")
        )
        print("✅ Connexion réussie à la base de données !")
        return conn
    except psycopg2.OperationalError as e:
        print(f"❌ Erreur de connexion : {e}")
        return None

# Définition de la classe Season
class Season(BaseModel):
    id_season: int
    season_name: str
    id_competition: int
    link_url: str

# Création d'une fonction pour insérer des données sur notre projet Supabase
def insert_seasons(seasons_df, supabase):
    seasons = [Season(**x).dict() for x in seasons_df.to_dict(orient='records')]
    execution = supabase.table('season').upsert(seasons).execute()

# Création d'une classe pour les informations sur les équipes
class Team(BaseModel):
    id_team: int
    team_name: str

# Création d'une fonction pour insérer les informations des équipes dans la base de données
def insert_teams(teams_df, supabase):
    teams = [Team(**x).dict() for x in teams_df.to_dict(orient='records')]
    supabase.table('team').upsert(teams).execute()
    print(f"✅ {len(teams)} équipes insérées dans Supabase.")

# Création d'une classe pour les matchs
class Match(BaseModel):
    id_match: int
    id_season: int
    id_home_team: int
    id_away_team: int
    match_date: date
    link_url: str

# Fonction pour insérer les matches dans la base de données
def insert_matches(matches_df, supabase):
    matches = [Match(**x).dict() for x in matches_df.to_dict(orient='records')]
    for match in matches:
        if isinstance(match['match_date'], date):
            match['match_date'] = match['match_date'].strftime('%Y-%m-%d')
    supabase.table('info_match').upsert(matches).execute()

# Définition de la classe Goal
class Goal(BaseModel):
    id_match: int
    score_home: int
    score_away: int
    result: int
    home_0_15: int
    away_0_15: int
    home_16_30: int
    away_16_30: int
    home_31_45: int
    away_31_45: int
    home_46_60: int
    away_46_60: int
    home_61_75: int
    away_61_75: int
    home_76_90: int
    away_76_90: int
    squad_1st_goal : int

# Création d'une fonction pour insérer des données sur notre projet Supabase
def insert_goals(goals, supabase):
    goals = [
        Goal(**x).model_dump()
        for x in goals.to_dict(orient='records')
    ]
    execution = supabase.table('info_goal').upsert(goals).execute()

def scrape_and_store_seasons():
    """Scrape les saisons de SofaScore et les stocke dans Supabase."""
    
    # 🔹 Connexion à la base PostgreSQL et Supabase
    conn = connect_to_db()
    if not conn:
        return

    supabase = connect_to_supabase()
    if not supabase:
        return

    cursor = conn.cursor()

    # 🔹 Récupérer les compétitions
    cursor.execute("SELECT id_competition, link_url FROM competition;")
    records = cursor.fetchall()

    # 🔹 Récupérer les saisons déjà enregistrées
    cursor.execute("SELECT id_season FROM season;")
    season_already_records = {row[0] for row in cursor.fetchall()}  # Conversion en set d'entiers

    # 🔹 Initialiser Selenium
    driver = webdriver.Chrome()
    seasons = []

    try:
        for id_competition, relative_url in records:
            if id_competition in [335, 339, 13330]:  # Compétitions à ignorer
                continue

            url_season_french = 'https://www.sofascore.com' + relative_url
            driver.get(url_season_french)
            time.sleep(5)

            # 🔹 Gérer la bannière des cookies
            try:
                cookies_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "fc-cta-consent"))
                )
                cookies_button.click()
            except:
                pass

            targeted_seasons = ["24/25", "23/24", "22/23", "21/22", "2024/25"]
            season_found = False

            for season in targeted_seasons:
                try:
                    dropdown_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "DropdownButton"))
                    )
                    dropdown_button.click()
                    time.sleep(1)

                    dropdown_options = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, "DropdownItem"))
                    )

                    for option in dropdown_options:
                        if option.text.strip() == season:
                            ActionChains(driver).move_to_element(option).click(option).perform()
                            time.sleep(3)

                            WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CLASS_NAME, "DropdownButton"))
                            )

                            current_url = driver.current_url
                            parts = current_url.split('/')
                            id_season = int(parts[-1].split('#id:')[-1])         
                            competition_name = " ".join(parts[-2].split('-')).title()
                            season_name = f"{competition_name} {season}"

                            if id_season in season_already_records:
                                continue 

                            season_obj = Season(
                                id_season=id_season,
                                season_name=season_name,
                                id_competition=id_competition,
                                link_url=current_url
                            )
                            seasons.append(season_obj)

                            season_found = True
                            break
                except:
                    continue

            if not season_found:
                continue

        # 🔹 Insérer les saisons dans Supabase
        if seasons:
            seasons_df = pd.DataFrame([seas.model_dump() for seas in seasons])
            insert_seasons(seasons_df, supabase)
        else:
            print("Aucune nouvelle saison à insérer.")

    finally:
        driver.quit()
        conn.close()

# Fonction pour récupérer les informations sur les matchs
def scrape_and_store_matches():
    conn = connect_to_db()
    if not conn:
        return
    supabase = connect_to_supabase()
    if not supabase:
        return
    
    cursor = conn.cursor()
    cursor.execute("SELECT id_season, link_url FROM season;")
    info_seasons = cursor.fetchall()
    
    cursor.execute("SELECT id_match FROM info_goal;")
    existing_matches = {row[0] for row in cursor.fetchall()}
    
    cursor.execute("""
        SELECT DISTINCT s.id_season FROM season s 
        JOIN info_match im ON s.id_season = im.id_season 
        WHERE s.season_name NOT LIKE '%24/25%' 
        AND s.season_name NOT LIKE '%2024/25%';
    """)
    past_seasons = {row[0] for row in cursor.fetchall()}
    
    driver = webdriver.Chrome()
    matches, teams = [], []
    
    def handle_cookies():
        try:
            cookies_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "fc-cta-consent"))
            )
            cookies_button.click()
        except:
            pass

    def extract_matches(id_season, url):
        driver.get(url)
        time.sleep(5)
        handle_cookies()
        
        while True:
            try:
                html_content = driver.page_source
                soup = BeautifulSoup(html_content, 'html.parser')
                
                for link in soup.find_all('a', {"data-testid": "event_cell"}):
                    href = link.get('href')
                    id_match = int(link.get('data-id'))
                    if id_match in existing_matches:
                        continue
                    
                    date_element = link.find('bdi', {'class': 'Text kcRyBI'})
                    match_date = None
                    if date_element:
                        try:
                            match_date = datetime.strptime(date_element.text.strip().split()[0], "%d/%m/%y").strftime("%Y-%m-%d")
                        except:
                            continue
                    
                    home_team = link.find('div', {'data-testid': 'left_team'})
                    away_team = link.find('div', {'data-testid': 'right_team'})
                    
                    id_home_team = int(home_team.find('img')['src'].split('/')[-3])
                    id_away_team = int(away_team.find('img')['src'].split('/')[-3])
                    
                    team_home_name = home_team.find('bdi').text.strip()
                    team_away_name = away_team.find('bdi').text.strip()
                    
                    matches.append({
                        'id_match': id_match,
                        'id_season': id_season,
                        'id_home_team': id_home_team,
                        'id_away_team': id_away_team,
                        'match_date': match_date,
                        'link_url': href
                    })
                    teams.append({'id_team': id_home_team, 'team_name': team_home_name})
                    teams.append({'id_team': id_away_team, 'team_name': team_away_name})
                
                prev_button = driver.find_element(By.XPATH, 
                    "//div[contains(@class, 'Box Flex')]/button[contains(@class, 'Button') and contains(@style, 'visible')][1]"
                )
                if prev_button:
                    prev_button.click()
                    time.sleep(3)
                else:
                    break
            except:
                break
    
    for id_season, url in info_seasons:
        if id_season in past_seasons:
            continue
        extract_matches(id_season, url)
    
    if matches:
        insert_matches(pd.DataFrame(matches).drop_duplicates(subset=['id_match']), supabase)
    if teams:
        insert_teams(pd.DataFrame(teams).drop_duplicates(subset=['id_team']), supabase)
    
    driver.quit()
    conn.close()
    print("✅ Extraction et stockage des matchs terminés !")

# Fonction pour récupérer les informations sur les buts
def scrape_and_store_goals():
    conn = connect_to_db()
    if not conn:
        return
    supabase = connect_to_supabase()
    if not supabase:
        return

    # On effectue la requête pour obtenir les liens url des matchs
    cursor = conn.cursor()
    cursor.execute("""
            SELECT id_match, link_url, id_season FROM info_match;
    """)

    info_matchs = cursor.fetchall()

    # On effectue la requête pour obtenir les saisons des matchs
    cursor.execute("""
            SELECT DISTINCT s.id_season, s.season_name
    FROM Season s
    JOIN info_match im ON s.id_season = im.id_season;

    """)

    info_matchs_season = cursor.fetchall()

    # On effectue la requête pour obtenir les identifiants des matchs dejà dans la base
    cursor.execute("SELECT id_match FROM info_goal;")
    info_matchs_goal = {row[0] for row in cursor.fetchall()}  # Conversion en set d'entiers

    # On effectue la requête pour obtenir les identifiants des matchs dejà dans la base
    cursor.execute("SELECT DISTINCT s.id_season FROM season s JOIN info_match im ON s.id_season = im.id_season WHERE s.season_name NOT LIKE '%24/25%' AND s.season_name NOT LIKE '%2024/25%';")
    not_current_season_and_already_stored = {row[0] for row in cursor.fetchall()}  # Conversion en set d'entiers

    # Initialisation du WebDriver
    def init_webdriver():
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Mode headless
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        prefs = {
            "profile.managed_default_content_settings.images": 2,  # Bloque les images
            "profile.managed_default_content_settings.javascript": 1,  # Active uniquement le JS essentiel
        }
        chrome_options.add_experimental_option("prefs", prefs)
        return webdriver.Chrome(options=chrome_options)

    def handle_cookies_banner(driver):
        try:
            cookies_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "fc-cta-consent"))
            )
            cookies_button.click()
            print("Bannière de cookies fermée.")
        except Exception:
            pass  # Ignorer si aucune bannière n'est présente


    def fetch_match_data(id_match):
        try:
            response = os.popen(
                f'curl -H "Host: api.sofascore.com" -H "Accept: */*" '
                f'-H "User-Agent: curl/8.1.2" https://api.sofascore.com/api/v1/event/{id_match}/incidents'
            ).read()
            return json.loads(response)['incidents']
        except Exception as e:
            print(f"Erreur lors de la récupération des incidents pour {id_match} : {e}")
            return []

    def extract_match_scores(incidents):
        infos_score_match = pd.DataFrame(incidents)[pd.DataFrame(incidents)['text'] == 'FT']
        score_home = infos_score_match['homeScore'].values[0] if not infos_score_match.empty else None
        score_away = infos_score_match['awayScore'].values[0] if not infos_score_match.empty else None
        
        # Vérification et conversion
        score_home = int(score_home) if score_home is not None else 0
        score_away = int(score_away) if score_away is not None else 0

        return score_home, score_away

    def calculate_result(score_home, score_away):
        if score_home == score_away:
            return 0  # Match nul
        return 1 if score_home > score_away else 2  # Victoire domicile ou extérieur

    def calculate_time_intervals(incidents, match_goal_df):
        """
        Calcule le nombre de buts par intervalles de temps et met à jour le DataFrame match_goal_df.
        """
        time_intervals = [(0, 15), (16, 30), (31, 45), (46, 60), (61, 75), (76, 90)]
        incidents_df = pd.DataFrame(incidents)
        goals = incidents_df[incidents_df['incidentType'] == 'goal']

        # Initialisation des colonnes à 0 par défaut
        for start, end in time_intervals:
            match_goal_df[f'home_{start}_{end}'] = 0
            match_goal_df[f'away_{start}_{end}'] = 0

        if goals.empty:
            # Aucun but, retourner directement
            return match_goal_df

        # Si des buts existent, vérifier les intervalles
        for start, end in time_intervals:
            home_goals = goals[
                (goals['time'] >= start) &
                (goals['time'] <= end) &
                (goals['isHome'] == True)
            ]
            away_goals = goals[
                (goals['time'] >= start) &
                (goals['time'] <= end) &
                (goals['isHome'] == False)
            ]


            match_goal_df[f'home_{start}_{end}'] = len(home_goals)
            match_goal_df[f'away_{start}_{end}'] = len(away_goals)

        return match_goal_df

    def calculate_first_goal(goals, match_goal_df):
        if goals.empty:
            match_goal_df['squad_1st_goal'] = 0
        else:
            first_goal = goals.sort_values(by='time').iloc[0]
            match_goal_df['squad_1st_goal'] = 1 if first_goal['isHome'] else 2

        return match_goal_df

    def process_match(info_match, driver):
        id_match, relative_url, id_season = info_match
        url_match = f'https://www.sofascore.com{relative_url}'
        
        id_match = int(id_match)
        
        try:
            driver.get(url_match)
        except TimeoutException:
            print(f"Timeout lors du chargement de la page : {url_match}")
            
            # Optionnel : Limite de tentatives pour éviter une boucle infinie
            max_retries = 3
            for i in range(max_retries):
                try:
                    driver.quit()
                    driver = init_webdriver()
                    driver.get(url_match)
                    print(f"Tentative {i+1}/{max_retries} réussie.")
                    break  # Sortir de la boucle si succès
                except TimeoutException:
                    print(f"Tentative {i+1}/{max_retries} échouée.")
            else:
                print("Échec après plusieurs tentatives. Abandon.")

        handle_cookies_banner(driver)

        incidents = fetch_match_data(id_match)
        if not incidents:
            return None

        score_home, score_away = extract_match_scores(incidents)
        result = calculate_result(score_home, score_away)

        match_goal_df = pd.DataFrame({'id_match': [id_match], 'score_home': [score_home], 'score_away': [score_away], 'result': [result], 'id_season': [id_season]})
        match_goal_df = calculate_time_intervals(incidents, match_goal_df)
        
        goals = pd.DataFrame(incidents)[pd.DataFrame(incidents)['incidentType'] == 'goal']
        match_goal_df = calculate_first_goal(goals, match_goal_df)
        
        return match_goal_df

    # Fonction principale avec réinitialisation du WebDriver
    def extract_goals(info_matchs, info_matchs_season, supabase, info_matchs_goal, not_current_season_and_already_stored, reset_interval=10):

        # Ajouter une étape pour ignorer les matchs des saisons déjà enregistrées et terminées
        filtered_matches = [match for match in info_matchs if match[2] not in not_current_season_and_already_stored]

        filtered_matches = [match for match in filtered_matches if match[0] not in info_matchs_goal]

        print(f"Nombre de matchs à traiter après filtrage : {len(filtered_matches)}")

        if not filtered_matches:
            print("Aucun match à traiter pour les saisons sélectionnées.")
            return  # Arrêter l'exécution si aucun match n'est à traiter

        matchs = []
        driver = init_webdriver()    

        try:
            # Utilisation de tqdm pour afficher la progression
            for i, info_match in enumerate(tqdm(filtered_matches, desc="Traitement des matchs", unit="match")):
                # Réinitialiser le WebDriver périodiquement
                if i > 0 and i % reset_interval == 0:
                    driver.quit()
                    driver = init_webdriver()

                try:
                    # Traiter un match individuel
                    match_goal_df = process_match(info_match, driver)
                    if match_goal_df is not None:
                        matchs.append(match_goal_df)
                except Exception as e:
                    print(f"Erreur lors du traitement du match {info_match[0]} : {e}")
                    continue  # Continuer avec le prochain match en cas d'erreur
        finally:
            # S'assurer que le WebDriver est fermé même en cas d'erreur
            driver.quit()

        # Combiner toutes les données collectées
        if matchs:
            all_matches_df = pd.concat(matchs, ignore_index=True)
            print("Insertion des informations de buts pour tous les matchs...")
            insert_goals(all_matches_df, supabase)
        else:
            print("Aucune donnée à insérer.")

    extract_goals(info_matchs, info_matchs_season, supabase, info_matchs_goal,not_current_season_and_already_stored)

# Éxécuter la fonction
if __name__ == "__main__":
    scrape_and_store_seasons()
    scrape_and_store_matches()
    scrape_and_store_goals()