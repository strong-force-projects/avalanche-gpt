import os
import json
from typing import Iterator
from openai import OpenAI
from dotenv import load_dotenv
from beartype import beartype

load_dotenv(override=True)


@beartype
class ResponseGenerator:
    """Generates natural language avalanche reports from CAAMLv6 data using LLMs."""

    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.0):
        """
        Args:
            model (str): OpenAI model name
            temperature(float): Creativity control (0.0 = strict factual)
        """
        self.model = model
        self.temperature = temperature
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

        # print(self.api_key)

    def generate_report(self, bulletins: dict) -> Iterator[str]:
        """Generate avalanche report from bulletin data."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self._build_messages(bulletins),
                temperature=self.temperature,
                stream=True,
            )

            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            raise RuntimeError(f"Report generation failed: {str(e)}") from e

    def _build_messages(self, bulletins: dict) -> list[dict]:
        """Construct the prompt messages from the LLM."""
        return [
            {
                "role": "system",
                "content": "You are a professional avalanche forecaster.",
            },
            {"role": "user", "content": self._build_prompt(bulletins)},
        ]

    def _build_prompt(self, bulletins: dict) -> str:
        """Construct the detailed prompt template."""
        return f"""
            You are an expert avalanche forecaster. Based solely on the avalanche bulletin data provided below,
            generate a comprehensive and accurate avalanche report. DO NOT include any information that is not present in the bulletin data.
            For every piece of information, append a source reference that includes the bulletin ID and the publication time. \n\n
            The report should include:\n
            1. A summary of avalanche activity with highlights and detailed comments.\n
            2. Details on snowpack structure, including critical observations.\n"
            3. A list of avalanche problems with danger ratings.\n
            4. Any travel advisories or warnings.\n\n
            Format the report using bullet points or sections, and for each fact, add a citation like [Source: Bulletin ID <ID>, Published at <Time>].\n\n
            Bulletin data (in JSON format):\n
            {json.dumps(bulletins, indent=2)}\n\n
            Remember: Use ONLY the provided bulletin data and do not add any extra details or assumptions.
        """
