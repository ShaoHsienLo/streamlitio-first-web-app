import psycopg2
import pandas as pd

conn = psycopg2.connect(database="postgres", user="postgres",
                        password="postgres", host="192.168.1.125",
                        port=5432)
cur = conn.cursor()
query = "select * from public.vibration order by timestamp desc limit 10"
cur.execute(query)
result = pd.DataFrame(cur.fetchall())
result.columns = [col.name for col in cur.description]
print(result)
conn.commit()
conn.close()
