import sys
import csv
from scrayping import Scrayping

args = sys.argv
next_index = int(args[1])

c = -1
with open('../data/URL_list.tsv' ) as f:
    reader = csv.reader(f, delimiter=",")
    for raw in reader:
        if not raw == []:
            for url in raw:
                c += 1
                if c >= next_index:
                    print("URL index", end=":")
                    print(c)
                    print(url)
                    Scrayping.scrayping(url)