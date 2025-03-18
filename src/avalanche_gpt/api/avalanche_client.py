import requests
from beartype import beartype


@beartype
class AvalancheClient:
    """

    Args:
        date (str):
        region (str):
        language (str):

    Returns:


    """

    def __init__(self, date: str, region: str, lang: str):
        self.date = date
        self.region = region
        self.region = lang
        self.base_url = f"https://static.avalanche.report/bulletins/{date}/{date}_{region}_{lang}_CAAMLv6.json"

    def fetch_bulletins(self) -> dict:
        response = requests.get(self.base_url)
        response.raise_for_status()
        return response.json()
