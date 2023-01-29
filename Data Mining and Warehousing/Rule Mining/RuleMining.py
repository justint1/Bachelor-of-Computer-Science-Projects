import csv

#Reading in Product Sales data set and storing values in rows
csv_file = open("Play_Tennis_Data_Set.csv")
csvreader = csv.reader(csv_file)
header = next(csvreader)
rows = []
for row in csvreader:
    rows.append(row)
csv_file.close()
N = len(rows)#represents the length of the data set and is used for support and condidence calculations

#retreiving support and confidence values from user(in range 0.0 - 1.0)
min_sup = float(input("Please enter a minimum support threshold:"))
min_conf = float(input("Please enter a minimum confidence threshold:"))

#genFreqItemSet(input, header): Used to generate the 1st frequent itemSet which consists of each attribute and its number of occurences
def genFreqItemSet(input, header):
    itemCount = {}
    for items in input:#Accessing each tuple in input
        for item in items:#Accessing each item in each tuple
            if item not in itemCount:#if new item generate its position and start count
                itemCount[item] = 1
            else:#if items been seen add to count
                itemCount[item] = itemCount[item] + 1

    #Generating a new itemset with only items above minimum support
    newItemCount = {}
    for item, count in itemCount.items():
        if count >= min_sup*N:
            newItemCount[item] = count
    return newItemCount

#genCk(Lk, rows, f): used to generate the kth set of candidate item sets by distributing attributes
def genCk(Lk, rows):
    Ck = []
    #Loops through list of itemSets, combines them and stores them in a new candidate set, ignores tuples that are the same or the same thign in a different order
    for itemset in Lk:
        for itemset2 in Lk:
            if itemset2 > itemset:#insures that there are no identical sets
                Ck.append((itemset, itemset2))
    return Ck
#genLk(Ck, input): Used to generate the kth set of frequent item sets by counting the number of occurences of each item set in each row of daat provided
def genLk(Ck, input):
    itemCount = {}
    #retreiving each candidate item set and calculating calculating its frequency in data set
    for itemset in Ck:
        for rows in input:
            if set(itemset).issubset(set(rows)):#if all items in current candidate subset is in current row of original data
                if itemset not in itemCount:#if this is a new itemset add it to new item count at 1, if not increase count by 1
                    itemCount[itemset] = 1
                else:
                    itemCount[itemset] = itemCount[itemset] + 1
    #Generating a new itemset with only items above minimum support
    newItemCount = {}
    for item, count in itemCount.items():
        if count >= min_sup*N:
            newItemCount[item] = count
    return newItemCount

#makeRuleName(tempI): takes in an item name and returns that item with along with the cateogry its from
def makeRuleName(tempI):
    if((tempI == 'FALSE') | (tempI == "TRUE")):
        name = "Windy=" + tempI
        return name
    if((tempI == 'P') | (tempI == "N")):
        name = "PlayTennis=" + tempI
        return name
    if ((tempI == 'sunny') | (tempI == "overcast") | (tempI == 'rain')):
        name = "Outlook=" + tempI
        return name
    if ((tempI == 'hot') | (tempI == "mild") | (tempI == 'cool')):
        name = "Temperature=" + tempI
        return name
    if ((tempI == 'high') | (tempI == "normal")):
        name = "Humidity=" + tempI
        return name

#printRules(freqItems, candidateItems): takes in initial item frequency dictionary and a candidate item dictionary and prints the rules assocaited with the candidate items
def printRules(freqItems, candidateItems):
    n = len(candidateItems)
    ruleCount = 1
    file = open('Rules.txt', 'w')
    file.write("1. User Input\n")
    file.write("Support={}\n".format(min_sup))
    file.write("Confidence={}\n\n".format(min_conf))
    file.write("2. Rules\n")
    for i in range(0, n):#Loops through each frequent item set to generate rules from the set
        tempItem = candidateItems.popitem()
        for j in range(0,len(tempItem)):#loops through each item in a candidate set to generate rules for each item
            tempConf = round(tempItem[1] / freqItems.get(tempItem[0][j]), 2)#Calculating condfidence/support for given item in candidate set
            tempSupport = round(tempItem[1] / N, 2)
            #converting item names to include the category they are from
            i1 =makeRuleName(tempItem[0][0])
            i2 = makeRuleName(tempItem[0][1])
            #Only need to check that item satisfys minimum confidence as it wouldnt make it this far if it didnt satisfy support
            if(tempConf >= min_conf):
                if(j == 0):
                    file.write("Rule #{}: {{{}}}=>{{{}}}\n".format(ruleCount, i1, i2))
                    file.write("(Support={}, Confidence={})\n\n".format(tempSupport, tempConf))
                    ruleCount += 1
                if (j == 1):
                    file.write("Rule #{}: {{{}}}=>{{{}}}\n".format(ruleCount, i2, i1))
                    file.write("(Support={}, Confidence={})\n\n".format(tempSupport, tempConf))
                    ruleCount += 1


#apriori(rows, header) main fucntion used to execute the apriori algorithm
def apriori(rows, header):
    Lk = genFreqItemSet(rows, header)
    results = {}
    while(len(Lk) != 0):#loop used to generate frequent item sets until the set is empty and the loop is broken
        Ck = genCk(Lk, rows)
        Lk = genLk(Ck, rows)
        results.update(Lk)
    #last frequent item set is used along with the first frequent item set to generate and print all association rules
    printRules(genFreqItemSet(rows, header), results)


apriori(rows, header)