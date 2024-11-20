import csv

file = open("C:/Users/svenp/Documents/EPFL/CMT/Projet/LéXPLORE Temperature Chain.csv", newline = '')
csvReader = csv.reader(file, delimiter = ',')
for row in csvReader:
    sum = 0.0
    count = 0
    for mesure in row[2:]:
        sum += float(mesure)
        count += 1
    if count != 0:
        mean = sum/count
        #print(mean)
    else:
        print(f"lack of row nb.{row} makes count = 0")