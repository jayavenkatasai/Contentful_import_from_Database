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
cursor.execute('select QUESTION_ID, SEQUENCE, VALUE, TEXT, ACTIVE from [rebootdb].[LIST_TBL_QUESTIONNAIRE_ANSWER_backup]')

result = cursor.fetchall()

with open('subopt.csv', mode='w', newline='') as csv_file:
    fieldnames = ['QUESTION_ID', 'SEQUENCE','Value', 'Text', 'Active']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for row in result:
        writer.writerow({'QUESTION_ID': row[0],'SEQUENCE': row[1], 'Value': row[2], 'Text': row[3],'Active':row[4]})

client = Client('CFPAT-ORh4DkMa8FVRRg_jItmcRmIrzUXbFI2Iy8ieMptHNXk')
 # space = client.spaces().find('xagxqhvplncs')
content_types = client.content_types('nmga2v5if8yc','dev').all()

content_type = next((ct for ct in content_types if ct.name == 'Sub_Activities_Options'), None)
# print(content_type)
entries = []

with open('subopt.csv', mode='r') as csv_file:
     reader = csv.DictReader(csv_file)
     for row in reader:
         entry = content_type.entries().create()
         entry.questionId = int(row['QUESTION_ID'])
         entry.sequence = int(row['SEQUENCE'])
         entry.value1 =str(row['Value'])
         entry.text1 = str(row['Text'])
         entry.active = bool(row['Active'])
         entry.save()

         entries.append(entry)

