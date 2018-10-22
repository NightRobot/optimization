import csv
from pprint import pprint
group = []
with open('../../data/redundancylist.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        # print(', '.join(row))
        group.append(row)
    print(group)
# pprint(data)

