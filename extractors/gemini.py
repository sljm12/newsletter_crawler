from crawl4ai import CrawlResult
from google import genai

class GeminiContentExtractor:
    def __init__(self, client :genai.Client):
        self.client = client

    def extract_content(self, content :CrawlResult):
        prompt = """
        Please extract the main text from the article and ignore all other text and links.

        {content}

        """

        output = prompt.format(content=content.markdown)
        response = self.client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=output
        )
        return response.text
    