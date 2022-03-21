import sys, requests
import constants
import csv, json, sqlite3


class BallDontLieAPI:
    def __init__(self, base_url: str = "https://www.balldontlie.io/api/v1"):
        self.base_url = base_url

    def grouped_teams(self) -> None:
        response = requests.get(f"{self.base_url}/teams")
        if response.status_code != 200:
            raise Exception(f"API request result: {response.status_code}\n{constants.errors[response.status_code]}")
        data = response.json()
        teams = data['data']
        while (data['meta']['next_page']):
            response = requests.get(f"{self.base_url}/teams?page={data['meta']['next_page']}")
            if response.status_code != 200:
                raise Exception(f"API request result: {response.status_code}\n{constants.errors[response.status_code]}")
            data = response.json()
            teams.extend(data['data'])
        grouped_by_division = {}
        for team in teams:
            if team['division'] in grouped_by_division:
                grouped_by_division[team['division']].append(team)
            else:
                grouped_by_division[team['division']] = [team]
        for division in sorted(grouped_by_division):
            print(division)
            for team in grouped_by_division[division]:
                print(f"\t{team['full_name']} ({team['abbreviation']})")

    def players_stats(self, name: str) -> None:
        response = requests.get(f"{self.base_url}/players?search={name.capitalize()}")
        if response.status_code != 200:
            raise Exception(f"API request result: {response.status_code}\n{constants.errors[response.status_code]}")
        data = response.json()
        players = data['data']

        tallest = [0, ""]
        heaviest = [0, ""]
        for player in players:
            if player['height_feet'] != None and player['height_inches'] != None:
                height_meters = (player['height_feet'] * 0.3048) + (player['height_inches'] * 0.0254)
                if height_meters > tallest[0]:
                    tallest[0], tallest[1] = height_meters, f"{player['first_name']} {player['last_name']}"
            if player['weight_pounds'] != None and player['weight_pounds'] > heaviest[0]:
                heaviest[0], heaviest[1] = player['weight_pounds'], f"{player['first_name']} {player['last_name']}"

        if tallest[0] != 0:
            print(f"The tallest player: {tallest[1]} {tallest[0]:.2f} meters")
        else:
            print(f"The tallest player: Not Found")

        if heaviest[0] != 0:
            print(f"The heaviest player: {heaviest[1]} {heaviest[0] / 2.2046:.2f} kilograms")
        else:
            print(f"The heaviest player: Not Found")

    def teams_stats(self, season: int, output: str = "stdout") -> None:
        # Extracting the teams
        response = requests.get(f"{self.base_url}/teams")
        if response.status_code != 200:
            raise Exception(f"API request result: {response.status_code}\n{constants.errors[response.status_code]}")
        teams = response.json()['data']

        teams_data = {f"{team['full_name']} ({team['abbreviation']})": {"won_games_as_home_team": 0,
                                                                        "won_games_as_visitor_team": 0,
                                                                        "lost_games_as_home_team": 0,
                                                                        "lost_games_as_visitor_team": 0} for team in teams}
        for team in teams:
            response = requests.get(f"{self.base_url}/games?seasons[]={season}&team_ids[]={team['id']}")
            if response.status_code != 200:
                raise Exception(f"API request result: {response.status_code}\n{constants.errors[response.status_code]}")
            data = response.json()['data']
            for game in data:
                team_status = "home_team" if game['home_team']['id'] == team['id'] else "visitor_team"
                if game[f"{team_status}_score"] > game[
                    'home_team_score' if team_status == 'visitor_team' else 'visitor_team_score']:
                    teams_data[f"{team['full_name']} ({team['abbreviation']})"][f"won_games_as_{team_status}"] += 1
                elif game[f"{team_status}_score"] < game[
                    'home_team_score' if team_status == 'visitor_team' else 'visitor_team_score']:
                    teams_data[f"{team['full_name']} ({team['abbreviation']})"][f"lost_games_as_{team_status}"] += 1

        if output == "stdout":
            for key, values in teams_data.items():
                print(key)
                for statistic in values:
                    print(f"\t{statistic.replace('_', ' ')}: {values[statistic]}")
        elif output == "csv":
            filename = f"teams_stats_{season}.csv"
            colnames = ["Team name", "Won games as home team", "Won games as visitor team",
                        "Lost games as home team", "Lost games as visitor team"]
            rows = [[key, list(value.values())[0], list(value.values())[1],
                     list(value.values())[2], list(value.values())[3]] for key, value in teams_data.items()]
            with open(filename, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=";")
                csv_writer.writerow(colnames)
                csv_writer.writerows(rows)
        elif output == "json":
            filename = f"teams_stats_{season}.json"
            teams_data = [{"team_name": key, "won_games_as_home_team": list(value.values())[0],
                           "won_games_as_visitor_team": list(value.values())[1],
                           "lost_games_as_home_team": list(value.values())[2],
                           "lost_games_as_visitor_team": list(value.values())[3]} for key, value in teams_data.items()]
            with open(filename, 'w') as json_file:
                json.dump(teams_data, json_file, indent=4)
        elif output == "sqlite":
            filename = "teams_stats.db"
            with sqlite3.connect(filename) as connection:
                cursor = connection.cursor()
                table_creation_query = """CREATE TABLE teams_stats(team_name VARCHAR(255), 
                won_games_as_home_team SMALLINT, won_games_as_visitor_team SMALLINT, 
                lost_games_as_home_team SMALLINT, lost_games_as_visitor_team SMALLINT);"""
                cursor.execute(table_creation_query)
                for key, value in teams_data.items():
                    teams_data_insertion_query = """INSERT INTO teams_stats (team_name, won_games_as_home_team,
                    won_games_as_visitor_team, lost_games_as_home_team, lost_games_as_visitor_team) VALUES (?, ?, ?, ?, ?)"""
                    cursor.execute(teams_data_insertion_query, (
                    key, list(value.values())[0], list(value.values())[1], list(value.values())[2],
                    list(value.values())[3]))
                connection.commit()


if __name__ == "__main__":
    api = BallDontLieAPI()
    try:
        if sys.argv[1] == "grouped-teams":
            api.grouped_teams()
        elif sys.argv[1] == "players-stats":
            api.players_stats(sys.argv[3])
        elif sys.argv[1] == "teams-stats":
            if len(sys.argv) == 4:
                api.teams_stats(int(sys.argv[3]))
            elif len(sys.argv) == 6:
                api.teams_stats(int(sys.argv[3]), sys.argv[5])
        else:
            print('Invalid usage, please use the syntax:')
            print("python main.py grouped-teams")
            print("python main.py players-stats --name <name>")
            print("python main.py teams-stats --season <season> [--output <stdout/csv/json/sqlite>]")
    except IndexError:
        print("Not enough parameters provided. Try to execute the program from the command line.")