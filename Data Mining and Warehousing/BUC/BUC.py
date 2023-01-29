import csv
#Reading in Product Sales data set and storing values in rows
csv_file = open("Product_Sales_Data_Set.csv")
csvreader = csv.reader(csv_file)
header = next(csvreader)
rows = []
for row in csvreader:
    rows.append(row)
csv_file.close()

#Initializing values used for computation corresponding to the given data set
items = ["Computer", "Camera", "Phone", "Printer"]
locations = ["Toronto", "Vancouver", "New York", "Chicago"]
years = [2017, 2018]
cardinality = [4,4,2,4]
dc = [[32,32,32,32],[8,8,8,8],[4,4],[1,1,1,1]]
numDims = 4

#arrays used to store values for different cuboids
itemList = []
itemLocList = []
itemLocYearList = []

#Getting minimum support from user
min_sup = int(input("Please enter the minimum support for iceberg cubes:"))

#Used to add up sales units in inputted array
def aggregate(inputs):
    sum = 0
    for i in range(0, len(inputs)):
        sum += int(inputs[i][4])
    return sum

#Bottom Up Cube Computation
def BUC(inputs, dim):
    d = dim
    for d in range(d, numDims):#Outlerloop, deals with calculating each dimension
        cos = cardinality[d]
        k = 0
        for j in range(0, cos):#InnerLoop, deals with calculating cubes within each dimension
            c = dc[d][j]
            salesUnits = aggregate(inputs[k:(k+c)])
            if salesUnits >= min_sup:
                appendToCuboid(salesUnits, d, j)
                if d+1 < numDims:#Recursive function
                    BUC(inputs[k:(k+c)], d+1)
            else:
                appendToCuboid("", d, j)
            k += c

#Used in BUC to generate cuboids
def appendToCuboid(stat, dim, feature):
    if(dim == 0):
        itemList.append(stat)
    if (dim == 1):
        itemLocList.append(stat)
    if (dim == 2):
        itemLocYearList.append(stat)

#WRITES RESULTS TO TEXT FILE
def writeCuboids(vals, vals2, vals3):
    file = open('Iceberg-Cube-Results.txt', 'w')
    #PRINTING: ITEM
    file.write("(Item)\n")
    for i in range(0,len(items)):
        file.write('{:<15s} {:<10s}\n'.format(items[i], str(vals[i])))
    file.write("\n")

    # PRINTING: ITEM-LOCATION
    file.write("(Item, Location)\n")
    file.write('{:>23s} {:>12s} {:>9s} {:>9s}\n'.format(locations[0], locations[1], locations[2], locations[3]))
    j = 0
    for i in range(0, len(items)):
        file.write('{:<15s} {:<10s} {:<10s} {:<10s} {:<10s}\n'.format(items[i], str(vals2[j]), str(vals2[j + 1]), str(vals2[j + 2]), str(vals2[j + 3])))
        j = j + 4
    file.write("\n")

    # PRINTING: ITEM-LOCATION-YEAR
    # Printing 2017
    file.write("(Item, Location, Year)\n")
    file.write('Year={0}\n'.format(years[0]))
    file.write('{:>23s} {:>12s} {:>9s} {:>9s}\n'.format(locations[0], locations[1], locations[2], locations[3]))
    j = 0
    for i in range(0, len(items)):
        file.write('{:<15s} {:<10s} {:<10s} {:<10s} {:<10s}\n'.format(items[i], str(vals3[j]), str(vals3[j + 2]), str(vals3[j + 4]), str(vals3[j + 6])))
        j = j + 10
    file.write("\n")
    # Printing 2018
    file.write('Year={0}\n'.format(years[1]))
    file.write('{:>23s} {:>12s} {:>9s} {:>9s}\n'.format(locations[0], locations[1], locations[2], locations[3]))
    j = 1
    for i in range(0, len(items)):
        file.write('{:<15s} {:<10s} {:<10s} {:<10s} {:<10s}\n'.format(items[i], str(vals3[j]), str(vals3[j + 2]), str(vals3[j + 4]), str(vals3[j + 6])))
        j = j + 10


#PRINTS RESULTS TO CONSOLE(DISREGARD, ONLY USED FOR TESTING)
def printCuboids(vals, vals2, vals3):
    #PRINTING: ITEM
    print("(Item)")
    for i in range(0,len(vals)):
        print('{:<15s} {:<10s}'.format(items[i], str(vals[i])))
    print("\n")

    #PRINTING: ITEM-LOCATION
    print("(Item, Location)")
    print('{:>23s} {:>12s} {:>9s} {:>9s}'.format(locations[0], locations[1], locations[2], locations[3]))
    j = 0
    for i in range(0,len(items)):
        print('{:<15s} {:<10s} {:<10s} {:<10s} {:<10s}'.format(items[i], str(vals2[j]), str(vals2[j+1]), str(vals2[j+2]), str(vals2[j+3])))
        j = j+4
    print("\n")

    #PRINTING: ITEM-LOCATION-YEAR
    #Printing 2017
    print("(Item, Location, Year)")
    print("Year=", years[0])
    print('{:>23s} {:>12s} {:>9s} {:>9s}'.format(locations[0], locations[1], locations[2], locations[3]))
    j = 0
    for i in range(0, len(items)):
        print('{:<15s} {:<10s} {:<10s} {:<10s} {:<10s}'.format(items[i], str(vals3[j]), str(vals3[j + 2]), str(vals3[j + 4]), str(vals3[j + 6])))
        j = j + 10
    print("\n")
    #Printing 2018
    print("Year=", years[1])
    print('{:>23s} {:>12s} {:>9s} {:>9s}'.format(locations[0], locations[1], locations[2], locations[3]))
    j = 1
    for i in range(0, len(items)):
        print('{:<15s} {:<10s} {:<10s} {:<10s} {:<10s}'.format(items[i], str(vals3[j]), str(vals3[j + 2]), str(vals3[j + 4]), str(vals3[j + 6])))
        j = j + 10

#Running bottom up computation then writing results for (item), (item,location), and (item,location,year) to "Iceberg-Cube-Results.txt"
BUC(rows, 0)
writeCuboids(itemList, itemLocList, itemLocYearList)


