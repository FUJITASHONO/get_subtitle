import sys
import csv

args = sys.argv
next_index = args[0]

c=0
with open('../data/URL_list.tsv' ) as f:
    reader = csv.reader(f, delimiter=",")
    for raw in reader:
        if not raw == []:
            for url in raw:
                c+=1
                if not url == []:
                    if c>=next_index:
                        print("現在の位置は", end=",")
                        print(c)
                        scrayping(url)