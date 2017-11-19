import os
os.chdir('C:\\Studying\\myvenv\\etc\\DB_PJquery2')

with open('.\\US.txt', 'rt') as f:
    US_opener= f.readlines()
    for elmt in US_opener:
        elmt= elmt[:-3]
print(US_opener, '\n')
with open('.\\OHTER.txt', 'rt') as f2:
    OTHER_opener= f2.readlines()
    for elmt in OTHER_opener:
        elmt= elmt[:-3]

with open('compare.txt', 'wt') as f3:
    for i, u in enumerate(US_opener):
        if u not in OTHER_opener:
            print(i, u)
