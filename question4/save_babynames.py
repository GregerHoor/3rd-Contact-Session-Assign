import re
import os

import psycopg
from psycopg.types.json import Jsonb
from psycopg.rows import dict_row

from dotenv import load_dotenv

html = None

# Please adopt use of path as reciding in your file manager.
path_to_html_file = 'C:/Users/USER/3rd Contact Session Assign/question4/baby2008.html'

with open(path_to_html_file, 'r', encoding="utf-8") as file:
    html = file.read()
    
items = re.findall(r'<tr align="right"><td>(\d+)</td><td>(.*?)</td><td>(.*?)</td>\n</tr>', html)

items_dict = [
    {
        'rank':i[0],
        'male_name':i[1],
        'female_name':i[2],
    }
    for i in items
]

# Please adopt use of your postgres db private dets
load_dotenv(r"C:\Users\USER\PostgreSQL.env")

conn = psycopg.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
)
cur = conn.cursor(row_factory=dict_row)
        
cur.execute("""
    CREATE TABLE IF NOT EXISTS babyname_2008 (
        rank INT UNIQUE,
        male_name VARCHAR(25) NOT NULL,
        female_name VARCHAR(255) NOT NULL
    );
""")

for i in items_dict:
    cur.execute("INSERT INTO babyname_2008 (rank, male_name, female_name) VALUES (%s, %s, %s) ON CONFLICT (rank) DO NOTHING", (i.get('rank'), i.get('male_name'), i.get('female_name')))
    
cur.execute("SELECT * FROM babyname_2008")

all_names = cur.fetchall()
print(all_names)

conn.commit()
cur.close()
conn.close()