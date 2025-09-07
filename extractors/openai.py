from crawl4ai import CrawlResult
from openai import OpenAI

class OpenAIContentExtractor:
    def __init__(self, client:OpenAI):
        self.client = client

    def extract_content(self, content :CrawlResult):
        prompt = """
        Please extract the main text from the article and ignore all other text and links.

        {content}

        """

        output = prompt.format(content=content.markdown)
        response = self.client.chat.completions.create(
            model="qwen3:8b",
            messages=[{"role": "user", "content": output}]
        )
        return response.choices[0].message.content