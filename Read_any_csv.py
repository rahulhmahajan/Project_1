import csv

filename = r'practice_10x50.csv'
with open(filename) as file:
   data = csv.DictReader(file)
   for row in data :
       print(row['Column8'])
       if "Rahul" in row['Column8'] :
           print (row['Column7'])


