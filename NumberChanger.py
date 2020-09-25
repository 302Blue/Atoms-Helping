# Things you need to change in this file (See TODO)

# 1) Go to the shutil.copyfile line, put in your file name for both on either side of the comma
# Leave the second as filename-charged to allow for a modified version w/o changing original

# 2) Also edit the first with open statement to match whatever your the first filename is in the shutil line

# 3) Now make a charge file consisting of only the charges for 1 molecule and edit the chargeFile name to match
# I did this by importing the data into excel then copying the charge column of 1 molecule into a txt file
# Whatever you name the charge file has to be the name in ChargesFile field that is being read

# 4) Check to see that your Atoms List is divisible by your Charges list with no remainder
# If they are not divisible the charges will get assigned incorrectly after maxing out the list length

# 5) Edit the last two with open statements to match what your modified data file name will be
# This should match the second filename in your shutil.copyfile line from the beginning

# First thing we do is create a copy of the original data in case somehow this code destroys
# something important I can't be blamed, and we can modify a version without danger
# TODO - 1) Edit this with your original data filename and what you want the final merged data file to be called
import shutil
shutil.copyfile('combine-pc4.data', 'combine-pc4-charged.data')

# TODO - 2) Edit this with your original data filename
lineCount = 0
with open('combine-pc4.data', 'r') as originalFile:
    atomData = []
    # Get line numbers to isolate applicable data later
    for line in originalFile:
        lineCount += 1
        if 'Atoms' in line:
            atomStart = lineCount
        if 'Bonds' in line:
            bondEnd = lineCount
        # Write each line to the data list, separating elements by spaces
        atomData.append(line.strip().split(' '))
    print("Atoms Line: " + str(atomStart))
    print("Bonds Line: " + str(bondEnd))
    # Delete all lines prior to atom data and all lines after atom data
    del atomData[bondEnd-2:len(atomData)]
    del atomData[0:atomStart+1]
    # Open new file and to write just atom data to
    infoFile = open('AtomInfo.txt', 'w')
    for line in atomData:
        for item in line:
            infoFile.write('%s ' % item)
        infoFile.write('\n')
    infoFile.close()
    originalFile.close()
    # print(atomData)
    print("Atom Section Separated Out")

atomFile = open('AtomInfo.txt', 'r')
atomList = []
# Split the atom info file into a list that can be more easily appended
# From here AtomInfo.txt has all the info regarding atoms positions and its where we'll add charge info
for line in atomFile:
    atomList.append(line.strip().split(' '))
atomFile.close()
# print(atomList)
print("Atom Information File Created")

# TODO - 3) Edit this with your Charges filename
# Making a list from the charges file
chargesFile = open('PC4Charges.txt', 'r')
chargesList = []
for line in chargesFile:
    chargesList.append(line.strip())
# print(chargesList)

# Checking length of both list
# TODO - 4) Atom list length should be divisible to a whole number (no remainder) by your Charge list length
print("Is your Atom List divisible by your Charges List?")
print("Length of Atom List: " + str(len(atomList)))
print("Length of Charge List: " + str(len(chargesList)))
if (len(atomList)) % (len(chargesList)) != 0:
    print("It is not, please double check and adjust Charge list accordingly")
    quit()
else:
    print("They are divisible! You're doing an amazing job!")

# Here we take the AtomList and insert the applicable Charge
for count, element in enumerate(atomList, 0):
    insertPlace = count % len(chargesList)
    element.insert(3, chargesList[insertPlace].strip('[]'))
# print(atomList)

# Write combined list atom and charge list to a new file
with open('AtomCharges.data', 'w') as chargesFile:
    for line in atomList:
        for item in line:
            chargesFile.write('%s ' % item)
        chargesFile.write('\n')
    chargesFile.close()
print("Atom & Charges File Created")


# TODO - 5) Edit both these with what you want your merged data filename to be (match the second name from up top)
# Attempt to merge old data and new data into a final file
with open('combine-pc4-charged.data', 'r') as rFinalFile:
    tempData = []
    iterator = 1
    # Read all original data out into an array
    for line in rFinalFile:
        tempData.append(line.strip().split(' '))
    for listItem in atomList:
        # Insert new data alongside the the old data
        tempData[iterator + atomStart].insert(3, listItem[3])
        iterator += 1
    rFinalFile.close()
    print("Merging Old Data w/ New Data...")
    # Rewrite entire final file from updated array
    with open('combine-pc4-charged.data', 'w') as wFinalFile:
        for line in tempData:
            for element in line:
                wFinalFile.write('%s ' % element)
            wFinalFile.write('\n')
    wFinalFile.close()
    print("Final Combined Data File Created \n")
    print("Have an awesome day, you deserve it!")