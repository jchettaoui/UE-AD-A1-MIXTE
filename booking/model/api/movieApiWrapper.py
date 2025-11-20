import requests

class MovieApiWrapper:

    def __init__(self, url_api: str):
        self._url_api : str = url_api

    def get_movie_by_id(self, movie_id: str):
        return requests.post(
            self._url_api+f"/graphql", 
            json={"query": "{movie_with_id(" +f"_id:\"{movie_id}\")"+"{title}}"}
        )