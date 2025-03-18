from beartype import beartype
from avalanche_gpt.api.avalanche_client import AvalancheClient

import logging

logger = logging.getLogger(__name__)


@beartype
class Session:
    """
    A session object that fetches avalanche bulletins for a given date, region, and language."

    Args:
        date (str): The date of the bulletin in the format 'YYYY-MM-DD'.
        region (str): The region of the bulletin.
        lang (str): The language of the bulletin.
    """

    def __init__(self, date: str, region: str, lang: str):
        self.client = AvalancheClient(date, region, lang)
        self.bulletins = self.client.fetch_bulletins()

    def get_bulletins(self):
        return self.bulletins


def main():
    session = Session("2025-03-01", "EUREGIO", "en")
    bulletins = session.get_bulletins()
    print(bulletins)


if __name__ == "__main__":
    main()
