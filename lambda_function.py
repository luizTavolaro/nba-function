import json
import requests
from datetime import datetime

def lambda_handler(event, context):
    url = "http://ec2-54-158-72-226.compute-1.amazonaws.com:30000/times"
    response = requests.get(url)
    data = response.json()

    teams_total = len(data)
    teams_by_city = {}
    oldest_team = None
    oldest_team_date = None
    for team in data:
        city = team['cidade']
        if city not in teams_by_city:
            teams_by_city[city] = 0
        teams_by_city[city] += 1
        if oldest_team_date is None or datetime.strptime(team['dataFundacao'], '%a, %d %b %Y %H:%M:%S %Z') < oldest_team_date:
            oldest_team = team['nome']
            oldest_team_date = datetime.strptime(team['dataFundacao'], '%a, %d %b %Y %H:%M:%S %Z')
    
    oldest_team_city = team['cidade']
    oldest_team_date = team['dataFundacao']
    city_with_most_teams = max(teams_by_city, key=teams_by_city.get)
    city_with_most_teams_count = teams_by_city[city_with_most_teams]
    response = {
        "total_times": teams_total,
        "cidade_com_mais_times": {
            "cidade": city_with_most_teams,
            "quantidade": city_with_most_teams_count
        },
        "time_mais_antigo": {
            "nome": oldest_team,
            "dataFundacao": oldest_team_date,
            "cidade": oldest_team_city
        }
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps(
            response
        )
    }
