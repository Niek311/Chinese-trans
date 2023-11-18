import sqlite3
import csv
import os
from tqdm import tqdm

path=os.path.abspath('create-database\cedict_1_0_ts_utf-8_mdbg.csv')
conn = sqlite3.connect('database.db')
cur = conn.cursor()
with open(path,encoding='utf-8-sig') as f:
   reader = csv.reader(f)
   data = list(reader)

cur.execute('''CREATE TABLE C_dict (
   phon_the string,
   gian_the string,
   phien_am string,
   nghia string
   );''')

for row in tqdm(data):
   cur.execute(f"INSERT INTO C_dict VALUES (?,?,?,?);",row)

conn.commit()
conn.close()