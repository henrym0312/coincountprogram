import csv
f = open("volunteers.csv", "r")
reader = csv.reader(f)
data = []
for row in reader:
    people.append(row)
for item in people:
    print(item)
