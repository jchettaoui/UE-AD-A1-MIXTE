import requests


class UserApiWrapper:

    def __init__(self, api_url: str):
        self.api_url : str = api_url

    def is_user_an_administrator(self, userid) -> bool:
        if userid is None:
            return False
        result = requests.get(self.api_url+f"/users/{userid}/admin")
        if result.status_code != 200:
            return False
        return result.json()["admin"]
