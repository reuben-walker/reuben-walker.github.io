# Program:    placesWorld_RW.py
# Programmer: Reuben Walker
# Date:       November 17 2023
# Purpose:    To determine the total populations of user-selected places
#             around the world, and generate a report of the total 
#             populations in each quadrant of the world. 
#             Additionally, identify the most and least populated
#             places and give provide their names, quadrants, and populations.


#NOTE: User will select features using QGIS's selection tool. This program
#      assumes that the PlacesOfTheWorld shapefile is already loaded and selected.

# import libraries
import math
import os

#getNSHemi function definition
def getNSHemi(yLat):
    if yLat < 0:
        NSHemi = 'South'
    if yLat > 0:
        NSHemi = 'North'
    if yLat == 0:
        NSHemi = 'Equator'
    return NSHemi

# getEWHemi function definition
def getEWHemi(xLong):
    if xLong < 0:
        EWHemi = 'western'
    if xLong > 0:
        EWHemi = 'eastern'
    if xLong == 0:
        EWHemi = 'Prime Meridian'
    return EWHemi

# main function definition
def main(NWcount,NEcount,SWcount,SEcount,NWpop,NEpop,SWpop,SEpop,maxPop,minPop):
    
    # make PlacesOfTheWorld the working layer
    layer = iface.activeLayer()
    
    # select all points if none are selected
    if layer.selectedFeatureCount() == 0:
        layer.selectAll()
        
    selection = layer.selectedFeatures()
    
    # this is a loop to handle filename entry.
    reply = 65536
    while reply == 65536:
        # prompt user to enter filename
        qid = QInputDialog()
        title = "Create report"
        label = "Please enter the name for the report text file:"
        mode = QLineEdit.Normal
        default = "worldplacesreport.txt"
        userFileName, ok = QInputDialog.getText(qid,title,label,mode,default)
        
        # exit program if user selects "cancel"
        if ok == False:
            return
        
        # add a '.txt' extension to the filename if the user didn't enter one and set the file path
        if userFileName[-4:].upper() != ".TXT":
            userFileName = userFileName + ".txt"
        filePath = r'C:\temp' + '\\' + userFileName
        
        # if the file already exists, ask user if they want to overwrite it.
        # if the user selects "no", variable "reply" will get set to 65536, 
        # which restarts the while-loop and prompts the user to 
        # try a different file name
        if  ok == True and os.path.isfile(filePath):
            reply = QMessageBox.question(iface.mainWindow(), 'Warning','File with name "{}" already exists. Do you want to overwrite it?'.format(userFileName), QMessageBox.Yes, QMessageBox.No)
        else:
            reply = 0
        
        
    # loop through the features, extracting XY coordinates and population info
    for feature in selection:
        
        # passing XY coordinates to getEWHemi and getNSHemi
        geom = feature.geometry()
        xCoord = geom.asPoint().x()
        EW_hemi = getEWHemi(xCoord)
        yCoord = geom.asPoint().y()
        NS_hemi = getNSHemi(yCoord)
        
        # adding features & population numbers to the appropriate quadrant category
        if NS_hemi =='North' and EW_hemi =='western':
            NWcount +=1
            NWpop.append(feature['pop_max'])
            quadrant = 'Northwestern'
            
        elif NS_hemi =='North' and EW_hemi =='eastern':
            NEcount +=1
            NEpop.append(feature['pop_max'])
            quadrant = 'Northeastern'
            
        elif NS_hemi =='South' and EW_hemi =='western':
            SWcount +=1
            SWpop.append(feature['pop_max'])
            quadrant = 'Southwestern'
            
        elif NS_hemi =='South' and EW_hemi =='eastern':
            SEcount +=1
            SEpop.append(feature['pop_max'])
            quadrant = 'Southeastern'
            
        else:
            break
            quadrant = 'No Quadrant Found'
        
        # checking if the population of the current feature is the highest or lowest so far, and extracting its information if it is
        if feature['pop_max'] > maxPop:
            maxPopName = feature['nameascii']
            maxPop = feature['pop_max']
            maxPopQuad = quadrant
            
        if feature['pop_max'] < minPop:
            minPopName = feature['nameascii']
            minPop = feature['pop_max']
            minPopQuad = quadrant
    
    # getting population totals for each quadrant
    NWpop_total = sum(NWpop)
    NEpop_total = sum(NEpop)
    SWpop_total = sum(SWpop)
    SEpop_total = sum(SEpop)
    
    # writing to the output file
    with  open(filePath,'w') as outfile:
        print('Report of Select World Places',file=outfile)
        print('='*85,file=outfile)
        print('{} northeastern places have a total population of {}'.format(len(NEpop),NEpop_total),file=outfile)
        print('{} northwestern places have a total population of {}'.format(len(NWpop),NWpop_total),file=outfile)
        print('{} southeastern places have a total population of {}'.format(len(SEpop),SEpop_total),file=outfile)
        print('{} southwestern places have a total population of {}'.format(len(SWpop),SWpop_total),file=outfile)
        print('='*85,file=outfile)
        print('The {} place of {} has the highest population of {}'.format(maxPopQuad,maxPopName,maxPop),file=outfile)
        print('The {} place of {} has the lowest population of {}'.format(minPopQuad,minPopName,minPop),file=outfile)
        outfile.close()
    
    print("Output file successfully saved to " + filePath)

# calling main function
main(0,0,0,0,[],[],[],[],0,math.inf)