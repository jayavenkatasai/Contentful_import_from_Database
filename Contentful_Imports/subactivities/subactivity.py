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
cursor.execute('''SELECT b.id, a.QUESTION_TITLE, a.DETAIL_TEXT, a.QUESTION, a.QUESTION_ID, a.QUESTION_TYPE, a.SEQUENCE, a.CONTENT_TYPE 
                  FROM  [rebootdb].[LIST_TBL_QUESTIONNAIRE_Backup] a
join [rebootdb].[activity_Backup] b
on a.QUESTION_ID = b.QUESTION_ID
''')
result = cursor.fetchall()
with open('subactivity.csv', mode='w', newline='') as csv_file:
    fieldnames = ['Activity_ID', 'Header','Subhead', 'Content Under Subhead', 'Content or Question Id','question_type','sequence','ContentType']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for row in result:
        writer.writerow({'Activity_ID': row[0],'Header': row[1], 'Subhead': row[2], 'Content Under Subhead': row[3],'Content or Question Id':row[4],'question_type': row[5], 'sequence': row[6], 'ContentType':row[7]})
client = Client('CFPAT-ORh4DkMa8FVRRg_jItmcRmIrzUXbFI2Iy8ieMptHNXk')
 # space = client.spaces().find('xagxqhvplncs')
content_types = client.content_types('nmga2v5if8yc','dev').all()
content_type = next((ct for ct in content_types if ct.name == 'SubActivities'), None)
# print(content_type)
entries = []
with open('subactivity.csv', mode='r') as csv_file:
     reader = csv.DictReader(csv_file)
     for row in reader:
         entry = content_type.entries().create()
         entry.activityId = int(row['Activity_ID'])
         entry.questionTitle = str(row['Header'])
         entry.Detail =str(row['Subhead'])
         entry.questionary = str(row['Content Under Subhead'])
         entry.questionType =str(row['question_type'])
         entry.sequence = int(row['sequence'])
         entry.contentType = str(row['ContentType'])
         
         entry.questionId = float(row['Content or Question Id'])
         entry.save()

         entries.append(entry)
# print(entries)
