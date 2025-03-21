import requests
from beartype import beartype


@beartype
class AvalancheClient:
    """Client for fetching avalanche bulletins from avalanche.report API.

    This class handles the retrieval and basic parsing of avalanche bulletin data
    in CAAMLv6 format from the static avalanche.report service.

    Args:
        date (str): Date of the bulletin in 'YYYY-MM-DD' format
        region (str): Region code for the desired avalanche bulletin (e.g., 'EUREGIO')
        lang (str): Language code for the bulletin content (e.g., 'en', 'de')
    """

    def __init__(self, date: str, region: str, lang: str):
        """Initializes the avalanche client with specified parameters.

        Args:
            date (str): Date string in 'YYYY-MM-DD' format
            region (str): Target region code for avalanche data
            lang (str): Desired language for bulletin content
        """
        self.date = date
        self.region = region
        self.lang = lang
        self.base_url = f"https://static.avalanche.report/bulletins/{date}/{date}_{region}_{lang}_CAAMLv6.json"

    def fetch_bulletins(self) -> dict:
        """Fetches avalanche bulletins from the configured API endpoint.

        Retrieves the full bulletin data in CAAMLv6 JSON format from the
        avalanche.report service.

        Returns:
            dict: Parsed JSON response containing avalanche bulletins
        """
        response = requests.get(self.base_url)
        response.raise_for_status()
        return response.json()
