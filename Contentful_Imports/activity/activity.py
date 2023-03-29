import csv
import pyodbc
from contentful_management import Client

# Database Connection
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=server_name;'
    'DATABASE=database_name;'
    'UID=user_id;'
    'PWD=Password;'
)
#Selecting Required fields from database
cursor = conn.cursor()
cursor.execute("SELECT id,title, module, [order],caption,time,link,QUESTION_ID FROM [rebootdb].[activity_Backup]")
result = cursor.fetchall()
#Dumping Database data to csv file
with open('activity.csv', mode='w', newline='') as csv_file:
    fieldnames = ['Activity_ID','Title', 'Module', 'Order','caption','time','Video_link','Content or Question Id']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    writer.writeheader()
    for row in result:
        writer.writerow({'Activity_ID': row[0], 'Title': row[1], 'Module': row[2],'Order':row[3],'caption': row[4], 'time': row[5], 'Video_link':row[6], 'Content or Question Id': row[7]})
#Accessing Contentful using "Contentful_management_token" by creating a client
client = Client('CFPAT-ORh4DkMa8FVRRg_jItmcRmIrzUXbFI2Iy8ieMptHNXk') #acess token

content_types = client.content_types('nmga2v5if8yc','dev').all() #('space_id','Environment_id')
#Selecting required content_model (ct.name == 'content_model')
content_type = next((ct for ct in content_types if ct.name == 'Activities'), None)
entries = []

with open('activity.csv', mode='r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        entry = content_type.entries().create() #Creating entry
        entry.activityId = int(row['Activity_ID']) #Importing csv data into specified fields
        entry.title = str(row['Title'])
        entry.module =int(row['Module'])
        entry.order = int(row['Order'])
        entry.caption = str(row['caption'])
        entry.time =int(row['time'])
        entry.videolink = str(row['Video_link'])
        if row['Content or Question Id'] != '':
           entry.questionId = int(row['Content or Question Id'])
        entry.save() # Saves entries in a draft mode
        #to publish entries directly use "entrty.publish()"
        entries.append(entry)

