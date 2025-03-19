from typing import Iterator
from beartype import beartype
from avalanche_gpt.api.avalanche_client import AvalancheClient
from avalanche_gpt.response.response_generator import ResponseGenerator

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
        self.response_generator = ResponseGenerator()

    def get_bulletins(self):
        return self.bulletins

    def generate_report(self) -> Iterator[str]:
        """generate formatted avalanche report"""
        return self.response_generator.generate_report(self.bulletins)


def main():
    session = Session("2025-03-01", "EUREGIO", "en")

    # Get raw bulletins and print
    print("Raw bulletins:")
    print(session.get_bulletins())

    # Get generated report and print
    print("\nGenerated report:")
    try:
        for chunk in session.generate_report():
            print(chunk, end="", flush=True)
    except Exception as e:
        print(f"\n\nError occurred: {str(e)}")

    print("\n")


if __name__ == "__main__":
    main()
