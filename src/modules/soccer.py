import requests
from src.utils.html import create_table
from datetime import datetime, timedelta
import pytz

def get_fixtures(league_id, season, api_key):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    start_date = datetime.now().strftime("%Y-%m-%d")
    end_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    pst = pytz.timezone('US/Pacific')

    querystring = {
        "league": league_id,
        "season": season,
        "from": start_date,
        "to": end_date
    }

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()
        fixtures = data.get("response", [])
        if len(fixtures) == 0:
            print(f"There are no fixtures scheduled for today.")
            return ""
        else:
            fixtures_list = []
            for fixture in fixtures:
                home_team = fixture["teams"]["home"]["name"]
                away_team = fixture["teams"]["away"]["name"]
                utc_start_time = datetime.strptime(fixture["fixture"]["date"], "%Y-%m-%dT%H:%M:%S%z")
                pst_start_time = utc_start_time.astimezone(pst)
                start_time_str = pst_start_time.strftime("%m/%d/%Y %I:%M %p %Z")
                fixture_data = {'Home Team': home_team, 'Away Team': away_team, 'Start Time': start_time_str}
                fixtures_list.append(fixture_data)
            fixtures_table = create_table(fixtures_list)
            return fixtures_table
    else:
        print(f"Error retrieving fixtures: {response.status_code} - {response.text}")
        return ""
