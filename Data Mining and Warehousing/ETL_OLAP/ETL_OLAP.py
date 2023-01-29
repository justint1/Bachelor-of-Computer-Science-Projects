import csv
import itertools
#reading in csv and transfering to rows array
csv_file = open("Car_Sales_Data_Set.csv")
csvreader = csv.reader(csv_file)
header = next(csvreader)
rows = []
for row in csvreader:
    rows.append(row)
csv_file.close()

#sorting list by country
rows.sort(key=lambda row: (row[0]))
file = open('Car_Sales_Data_Set_First_Sorting.csv', 'a+')
with file:#writing new sorted list to csv  
    write = csv.writer(file)
    write.writerows(rows)

#sorting list by country then year
rows.sort(key=lambda row: (row[0], row[1]))
file = open('Car_Sales_Data_Set_Second_Sorting.csv', 'a+')
with file:#writing new sorted list to csv
    write = csv.writer(file)
    write.writerows(rows)

#sorting list by country then year then quarter
rows.sort(key=lambda row: (row[0], row[1], row[2]))
file = open('Car_Sales_Data_Set_Third_Sorting.csv', 'a+')
with file:#writing new sorted list to csv
    write = csv.writer(file)
    write.writerows(rows)

print("OLAP Query's")
print("1. ()")
print("2. (Country)")
print("3. (Time_Year)")
print("4. (Time_Quarter-Time_Year)")
print("5. (Car_Manufacturer)")
print("6. (Country, Time_Year)")
print("7. (Country, Time_Quarter-Time_Year)")
print("8. (Country, Car_Manufacturer)")
print("9. (Time_Year, Car_Manufacturer)")
print("10.(Time_Quarter-Time_Year, Car_Manufacturer)")
print("11.(Country, Time_Year, Car_Manufacturer)")
print("12.(Country, Time_Quarter-Time_Year, Car_Manufacturer)\n")
command = input("Please Select an OLAP query by entering its corresponding number")
if (command == "1"):
    #Printing each record
    # Key and group code found from:
    # https://www.geeksforgeeks.org/itertools-groupby-in-python/
    rows.sort(key=lambda row: (row[0], row[1], row[2], row[3]))
    itr = itertools.groupby(rows, lambda x: (x[0], x[1], x[2], x[3]))
    for key, group in itr:
        kAndg = {key: list(group)}
        tempL = list(kAndg.values())
        lSum = 0
        for i in range(len(tempL[0])):
            lSum = lSum + int(tempL[0][i][4])
        print(key[0] + '-' + key[1] + "-" + key[2] + "-" + key[3] + "\t" + str(lSum))
if (command == "2"):
    #Printing by Country
    #Key and group code found from:
    #https://www.geeksforgeeks.org/itertools-groupby-in-python/
    itr = itertools.groupby(rows, lambda x: x[0])
    for key, group in itr:
        kAndg = {key: list(group)}
        tempL = list(kAndg.values())  # extracting list from kAndg values
        lSum = 0
        for i in range(len(tempL[0])):  # Adding together sum of total car sales in list
            lSum = lSum + int(tempL[0][i][4])  # accessing # of car sales value
        print(key + "\t" + str(lSum))

if(command == "3"):
    # Time-Year
    rows.sort(key=lambda row: (row[1]))
    itr = itertools.groupby(rows, lambda x: (x[1]))
    for key, group in itr:
        kAndg = {key: list(group)}
        tempL = list(kAndg.values())  # extracting list from kAndg values
        lSum = 0
        for i in range(len(tempL[0])):  # Adding together sum of total car sales in list
            lSum = lSum + int(tempL[0][i][4])  # accessing # of car sales value
        print(key + "\t" + str(lSum))
if(command == "4"):
    # Time_YEar-Time_Quarter
    rows.sort(key=lambda row: (row[1], row[2]))
    itr = itertools.groupby(rows, lambda x: (x[1], x[2]))
    for key, group in itr:
        kAndg = {key: list(group)}
        tempL = list(kAndg.values())  # extracting list from kAndg values
        lSum = 0
        for i in range(len(tempL[0])):  # Adding together sum of total car sales in list
            lSum = lSum + int(tempL[0][i][4])  # accessing # of car sales value
        print(key[0] + '-' + key[1] + "\t" + str(lSum))
if(command == "5"):
    # Car Manufacturer
    rows.sort(key=lambda row: (row[3]))
    itr = itertools.groupby(rows, lambda x: (x[3]))
    for key, group in itr:
        kAndg = {key: list(group)}
        tempL = list(kAndg.values())  # extracting list from kAndg values
        lSum = 0
        for i in range(len(tempL[0])):  # Adding together sum of total car sales in list
            lSum = lSum + int(tempL[0][i][4])  # accessing # of car sales value
        print(key + "\t" + str(lSum))
if(command == "6"):
    # Country-Time_Year
    rows.sort(key=lambda row: (row[0], row[1]))
    itr = itertools.groupby(rows, lambda x: (x[0], x[1]))
    for key, group in itr:
        kAndg = {key: list(group)}
        tempL = list(kAndg.values()) # extracting list from kAndg values
        lSum = 0
        for i in range(len(tempL[0])):  # Adding together sum of total car sales in list
            lSum = lSum + int(tempL[0][i][4])  # accessing # of car sales value
        print(key[0] + '-' + key[1] + "\t" + str(lSum))
if(command == "7"):
    # Country-Time_year-Time_Quarter
    rows.sort(key=lambda row: (row[0], row[1], row[2]))
    itr = itertools.groupby(rows, lambda x: (x[0], x[1], x[2]))
    for key, group in itr:
        kAndg = {key: list(group)}
        tempL = list(kAndg.values())  # extracting list from kAndg values
        lSum = 0
        for i in range(len(tempL[0])):  # Adding together sum of total car sales in list
            lSum = lSum + int(tempL[0][i][4])  # accessing # of car sales value
        print(key[0] + '-' + key[1] + '-' + key[2] + "\t" + str(lSum))
if(command == "8"):
    # Country-Car_Manufacturer
    rows.sort(key=lambda row: (row[0], row[3]))
    itr = itertools.groupby(rows, lambda x: (x[0], x[3]))
    for key, group in itr:
        kAndg = {key: list(group)}
        tempL = list(kAndg.values()) # extracting list from kAndg values
        lSum = 0
        for i in range(len(tempL[0])):  # Adding together sum of total car sales in list
            lSum = lSum + int(tempL[0][i][4])  # accessing # of car sales value
        print(key[0] + '-' + key[1] + "\t" + str(lSum))
if(command == "9"):
    # Time_Year-Car_Manufacturer
    rows.sort(key=lambda row: (row[1], row[3]))
    itr = itertools.groupby(rows, lambda x: (x[1], x[3]))
    for key, group in itr:
        kAndg = {key: list(group)}
        tempL = list(kAndg.values()) # extracting list from kAndg values
        lSum = 0
        for i in range(len(tempL[0])):  # Adding together sum of total car sales in list
            lSum = lSum + int(tempL[0][i][4])  # accessing # of car sales value
        print(key[0] + '-' + key[1] + "\t" + str(lSum))
if(command == "10"):
    # Time_Year-Time_Quarter-Car_Manufacturer
    rows.sort(key=lambda row: (row[1], row[2], row[3]))
    itr = itertools.groupby(rows, lambda x: (x[1], x[2], x[3]))
    for key, group in itr:
        kAndg = {key: list(group)}
        tempL = list(kAndg.values())# extracting list from kAndg values
        lSum = 0
        for i in range(len(tempL[0])):# Adding together sum of total car sales in list
            lSum = lSum + int(tempL[0][i][4])
        print(key[0] + '-' + key[1] + "-" + key[2] + "\t" + str(lSum))
if(command == "11"):
    # Country-Time_Year-Car_Manufacturer
    rows.sort(key=lambda row: (row[0], row[1], row[3]))
    itr = itertools.groupby(rows, lambda x: (x[0], x[1], x[3]))
    for key, group in itr:
        kAndg = {key: list(group)}
        tempL = list(kAndg.values())# extracting list from kAndg values
        lSum = 0
        for i in range(len(tempL[0])):# Adding together sum of total car sales in list
            lSum = lSum + int(tempL[0][i][4])
        print(key[0] + '-' + key[1] + "-" + key[2] + "\t" + str(lSum))
if(command == "12"):
    # Country-Time_Year-Time_Quarter-Car_Manufacturer
    rows.sort(key=lambda row: (row[0], row[1], row[2], row[3]))
    itr = itertools.groupby(rows, lambda x: (x[0], x[1], x[2], x[3]))
    for key, group in itr:
        kAndg = {key: list(group)}
        tempL = list(kAndg.values())# extracting list from kAndg values
        lSum = 0
        for i in range(len(tempL[0])):# Adding together sum of total car sales in list
            lSum = lSum + int(tempL[0][i][4])
        print(key[0] + '-' + key[1] + "-" + key[2] + "-" + key[3] + "\t" + str(lSum))