
import csv
import pyodbc
from contentful_management import Client

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-HME0A24;'
    'DATABASE=GAR;'
    'UID=venkat;'
    'PWD=Password@123;'
)
cursor = conn.cursor()
cursor.execute("SELECT title, module, [order] FROM [rebootdb].[activity]")
result = cursor.fetchall()

with open('output_file.csv', mode='w', newline='') as csv_file:
    fieldnames = ['title', 'module', 'order']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for row in result:
        writer.writerow({'title': row[0], 'module': row[1], 'order': row[2]})

client = Client('CFPAT-MvI0nqvJs4lPgezGfg9WT057Q9xqE8uyMj8yX7qX-cY')
# space = client.spaces().find('xagxqhvplncs')
content_types = client.content_types('xagxqhvplncs','master').all()

content_type = next((ct for ct in content_types if ct.name == 'Activity'), None)
# print(content_type)
entries = []

with open('output_file.csv', mode='r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        entry = content_type.entries().create()
        entry.title = str(row['title'])
        entry.module =int(row['module'])
        entry.order = int(row['order'])

        entry.save()
       
        entries.append(entry)
print(entries)
