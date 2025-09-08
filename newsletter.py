import writer
from pprint import pprint
from pathlib import Path
from google import genai
import datetime
from dotenv import load_dotenv
import os

prompt = """
Imagine you are an editor that is tasked with reading {topic} related articles and summarize them as part of a daily newsletter for people who work in tech  to read. You are allowed to remove articles that are  or not related to {topic}. Please use your best judgement to do so. Please also categories similar articles together and put a category at the top.

The format of the newletter should be in the following format:
1. Title 
2. A brief summary roughly a paragraph size.

PLease output in markdown format. Make the article title link to the url of the article.

Below are a list of articles with the following tags

<Article> = The article number

<Title> = The title of the article

<URL> = The URL of the article

<Text> = The text of the article
"""

if __name__ == "__main__":
    load_dotenv()
    topic = "AI"
    print("Connecting to Postgres")
    writer = writer.PostgresWriter(os.getenv("db_conn"))
    print("Connection established")
    rows = writer.retrive(topic,"2025-09-07 00:00:00","2025-09-09 00:00:00")
    output = ""
    
    for r in rows:
        print(r)
        #text = Path("./extracts/"+str(r[0])+".md").read_text("utf8")
        output += "<Article> "+str(r[0])+"</Article>\n" 
        output += "<Title> "+r[1]+"</Title>\n"
        output += "<URL> "+r[2]+"</URL>\n"
        output += "<Text>\n"+r[5]+"\n</Text>\n"

    date_str = datetime.date.today().strftime("%Y-%m-%d")
    Path("./newsletter/newsletter_prompt_"+date_str+".txt").write_text(prompt +"\n\n" + output, "utf8")        
    #pprint(rows)
    
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=prompt.format(topic=topic) +"\n\n" + output)    

    filename = date_str + "-"+topic+"-newsletter.md"
    outputfile = Path(filename).write_text(response.text, "utf8")
    
