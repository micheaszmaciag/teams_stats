import sys, requests
import constants

class BallDontLieAPI:
    def __init__(self, base_url: str = "https://www.balldontlie.io/api/v1"):
        self.base_url = base_url

    def grouped_teams(self) -> None:
        response = requests.get(f"{self.base_url}/teams")
        if response.status_code != 200:
            raise Exception(f"API request result: {response.status_code}\n{constants.errors[response.status_code]}")
        data = response.json()
        teams = data['data']
        while(data['meta']['next_page']):
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
        # TODO - Check if the keys are available inside the dictionary
        # Try-Catch (KeyError Exception)
        for division in sorted(grouped_by_division):
            print(division)
            for team in grouped_by_division[division]:
                print(f"\t{team['full_name']} ({team['abbreviation']})")


    def players_height_weight(self) -> None:
        response = requests.get(f"{self.base_url}/players")
        if response.status_code != 200:
            raise Exception(f"API request result: {response.status_code}\n{constants.errors[response.status_code]}")
        data = response.json()
        teams = data['data']
        while(data['meta']['next_page']):
            response = requests.get(f"{self.base_url}/teams?page={data['meta']['next_page']}")
            if response.status_code != 200:
                raise Exception(f"API request result: {response.status_code}\n{constants.errors[response.status_code]}")
            data = response.json()
            teams.extend(data['data'])


if __name__ == "__main__":
    api = BallDontLieAPI()
    api.grouped_teams()