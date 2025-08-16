import csv
from csv import DictReader

filename =r'practice_10x50.csv'
with open(filename, "w", newline="") as file:
    reader = DictReader (file)
    print(reader)
    for row in reader :
        print(row)