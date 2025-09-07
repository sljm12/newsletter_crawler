'''
Crawler STOMP Client
This script connects to a STOMP message broker, listens for messages on a specified queue, 
and processes each message by performing a web crawl based on the URL provided in the message.
It saves the results of the crawl to a markdown file named after the ID from the message.
'''
import time
import sys
from pathlib import Path
import stomp
import asyncio
from crawler import web_crawl
from writer import PostgresWriter
from crawler import ReadabilityContentExtractor
from dotenv import load_dotenv
import os

class MyListener(stomp.ConnectionListener):
    def __init__(self, writer, conn, content_extractor=None):
        self.writer = writer        
        self.content_extractor = content_extractor
        self.conn = conn

    def on_error(self, frame):
        print('received an error "%s"' % frame.body)

    def on_message(self, frame):
        print('received a message "%s"' % frame.body)
        id,url = frame.body.split(",")
        filename =id+".md"
        p = Path("./extracts/"+filename)
        if p.exists():
            print("File already exists, skipping:", filename)
            return
        else:
            result = asyncio.run(web_crawl(url, self.content_extractor))        
            if result is not None:
                p.write_text(result, "utf8")
                writer.update_webcontent(id, result)
                print("Done "+filename)
            else:
                print("No content extracted for:", id)
        self.conn.ack(frame.headers['message-id'], frame.headers['subscription'])
        

if __name__ == "__main__":
    load_dotenv()
    writer = PostgresWriter(os.getenv("db_conn"))
    # Connect to the STOMP broker

    #client = genai.Client()
    #content_extractor = GeminiContentExtractor(client)
    content_extractor=ReadabilityContentExtractor()

    conn = stomp.Connection([(os.getenv("stomp_conn_host"), os.getenv("stomp_conn_port"))], heartbeats=(5000,0))
    listener = MyListener(writer, conn, content_extractor)    
    conn.set_listener('', listener)
    conn.connect(os.getenv("stomp_user"),os.getenv("stomp_pw"),wait=True)
    conn.subscribe(destination='/queue/test', 
                   id="1", 
                   ack='client-individual',
                   headers={
                        #'activemq.subscriptionName': '1',
                        'persistent': 'true'
                    })
    print("Ready")

    while True:
        time.sleep(1)
