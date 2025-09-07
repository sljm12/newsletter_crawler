import asyncio
from crawl4ai import *
from pathlib import Path
from extractors.readability import ReadabilityContentExtractor


def set_crawler_config(url :str):    
    crawl_config=CrawlerRunConfig(delay_before_return_html=10)

    return crawl_config


async def web_crawl(url, content_extractor):
    browser_conf = BrowserConfig(headless=False)            
    
    crawl_config=CrawlerRunConfig(delay_before_return_html=10)

    async with AsyncWebCrawler(config=browser_conf) as crawler:
        result = await crawler.arun(
            url=url,
            config=crawl_config            
        )
        Path("crawler.output.text").write_text(result.markdown, "utf8")
        content = content_extractor.extract_content(result)
        
        return content

if __name__ == "__main__":
    
    #client = genai.Client()
    #content_extractor = GeminiContentExtractor(client)

    #openaiClient = OpenAI(base_url="http://localhost:11434/v1", api_key="sk-")
    #content_extractor = OpenAIContentExtractor(openaiClient)

    content_extractor=ReadabilityContentExtractor()

    result = asyncio.run(web_crawl('https://www.theregister.com/2025/08/21/fydeos_chromiumos_degoogled/?td=rt-3a'
                    , content_extractor))
    
    print(result)
    
