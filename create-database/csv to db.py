import sqlite3
import csv
import tqdm
conn = sqlite3.connect('database1.db')
cur = conn.cursor()
with open('Term1.csv',encoding='utf-8') as f:
   reader = csv.reader(f)
   data = list(reader)

cur.execute('''CREATE TABLE C_dict (
   phon_the string,
   gian_the string,
   phien_am string,
   nghia string
   );''')

for row in data:
   cur.execute(f"INSERT INTO C_dict VALUES (?,?,?,?);",row)

conn.commit()
conn.close()