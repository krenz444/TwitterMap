__author__ = 'erkrenz'
import csv

with open('/tmp/data5.txt', 'w') as file:
    reader = csv.reader(file, delimiter='|')
    for line in reader:
        print line
