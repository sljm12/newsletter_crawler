import psycopg
from model import FeedItem
from pprint import pprint
from dotenv import load_dotenv
import os

class PostgresWriter:
    def __init__(self,connection_str):
        self.conn=psycopg.connect(connection_str)
    
    def insert_feed(self, feedItem :FeedItem):
        with self.conn.cursor() as cur:
            cur.execute('Insert into public."FeedItem" (title, url, content, date, category) values (%s,%s,%s,%s,%s)',
                        (feedItem.title, feedItem.url, feedItem.content, feedItem.date, feedItem.category))
                        
    def update_webcontent(self, id, content):
        with self.conn.cursor() as cur:
            cur.execute('update public."FeedItem" SET webcontent=%s where id = %s;',
                        (content, id))
            self.conn.commit()
    
    def retrive(self, category, startdate, enddate):
        with self.conn.cursor() as cur:
            cur.execute('select * from public."FeedItem" where category = %s and date >= %s AND date < %s;',
                        (category, startdate, enddate))
            return cur.fetchall()
        
    def retrive_categories(self, categories :list, startdate, enddate, has_webcontent=False):
        with self.conn.cursor() as cur:
            if has_webcontent:
                cur.execute('select * from public."FeedItem" where category = ANY(%s) and date >= %s AND date < %s and webcontent is not null;',
                            (categories, startdate, enddate))
            else:
                cur.execute('select * from public."FeedItem" where category = ANY(%s) and date >= %s AND date < %s and webcontent is null;',
                        (categories, startdate, enddate))
            return cur.fetchall()
    

if __name__ == "__main__":
    load_dotenv()
    print("Connecting")
    writer = PostgresWriter(os.getenv("db_conn"))
    rows = writer.retrive_categories(['AI', 'Software'], "2025-08-01 00:00:00", "2025-08-31 23:59:59", has_webcontent=True)
    pprint(rows)
    print("Done")