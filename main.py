import requests
import json
import sqlite3

key = '716459b7c7-e5bd56a727-rbh793'

From = input("შეიყვანეთ სასურველი ვალუტა, რომელიც გადაგყავთ სხვაში (გაითვალისწინეთ, შეიყვაეთ მსგავსად GEL) : ")
To = input("შეიყვანეთ სასურველი ვალუტა, რომელშიც გადაგყავთ სხვა (გაითვალისწინეთ, შეიყვაეთ მსგავსად GEL) : ")

url = f"https://api.fastforex.io/fetch-one?from={From}&to={To}&api_key=716459b7c7-e5bd56a727-rbh793"
headers = {"Accept": "application/json"}
response = requests.get(url, headers=headers)
print(response.text)
if response.status_code == 200:
    print (f"წარმატებით მოხერხდა დაკავშირება სტატუს კოდია - {response.status_code} ")
print(response.headers['Content-Type'])

res = response.json()
with open("data.json", "w") as file:
    json.dump(res, file, indent=4)

r = res['result']
val = r[f'{To}']
date = res['updated']
print(val)

conn = sqlite3.connect("my_database.sqlite")
cursor = conn.cursor()
# cursor.execute('''CREATE TABLE currency
#                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 Currency_name VARCHAR(50),
#                 To_Currency_name VARCHAR(100),
#                 result FLOAT,
#                 updated_date DATE );''')

cursor.execute('INSERT INTO currency (Currency_name, To_Currency_name, result, updated_date) VALUES (?, ?, ?, ?)', (From, To, val, date))
conn.commit()

conn.close()
