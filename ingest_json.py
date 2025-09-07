"""
Ingest JSON files into Postgres database
"""
import json
from pprint import pprint
import codecs
from writer import PostgresWriter    
from model import FeedItem
from pathlib import Path
import psycopg
from dotenv import load_dotenv
import os

def write_file(filepath, writer):
    with codecs.open(filepath,'r','utf8') as f:
        data =json.load(f)
        category = Path(filepath).name.split(".")[0]

        dates = list(data["AggregateMap"].keys())
        #dates.sort(reverse=True)
        #print(dates[0])
        for d in dates:
            print("Processing date:", d, "for category:", category)
            ingested=0
            failed=0
            duplicates=0
            items = data["AggregateMap"][d]
            for i in items:
                f = FeedItem(i["url"],i["date"],i["title"],i["content"],category)
                try:
                    writer.insert_feed(f)
                    writer.conn.commit()                    
                    ingested += 1
                except (psycopg.errors.UniqueViolation) as e:
                    #print("Duplicate entry for URL:", f.url)                  
                    duplicates += 1
                    writer.conn.rollback()
                except psycopg.errors.InFailedSqlTransaction as e:
                    #print("Transaction failed for URL:", f.url, "Error:", e)
                    failed += 1
                    writer.conn.rollback()
            print(f"Date: {d}, Category: {category}, Ingested: {ingested}, Failed: {failed}, Duplicates: {duplicates}")

if __name__ == "__main__":
    load_dotenv()

    writer = PostgresWriter(os.getenv("db_conn"))
    
    d = Path("os.getenv('json_data')")
    
    files = d.glob("*.json")
    print(files)
    for f in files:
        print(f)
        write_file(f ,writer)    
    '''
    write_file(d / "Chess.json", writer)
    '''
