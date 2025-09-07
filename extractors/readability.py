from crawl4ai import CrawlResult
from readabilipy import simple_json_from_html_string
from html_to_markdown import convert_to_markdown

class ReadabilityContentExtractor:
    def extract_content(self, content :CrawlResult):
        try:
            article = simple_json_from_html_string(content.fit_html)
            return convert_to_markdown(article['content'])
        except Exception as e:
            print("Readability extraction failed:", e)
            return ""