#Three-PIP Image Printing Helper
#Purpose of this tool:
#This helper is meant to help you print 4"x6" images on letter (8.5"x11") paper.
#This exists as a standard output feature of the photo printing wizard in Windows XP,
#but does not exist on anything newer, nor does it make an appearance on other platforms.
#No other photo printing software currently provided as a courtesy supports this ability;
#At best, they print two pictures on one sheet of letter (or larger) paper. This wastes
#more paper than I am comfortable with. Hence the birth of this tool!

#usage:
# For now, it only directly supports files of the .JPG or .jpg files. (For case-sensitive systems,
# the script will scan for both. For systems which ignore case, the script will do a quick check
# to avoid duplicates).
#Place the script (this file) into the folder with all your images, and run. If you want multiple
# copies of an image, the tool will ask you how many copies you want. Duplicates will NOT be printed
# on the same sheet; rather, the tool will do one of each image per sheet but will duplicate
# the sheets.
#To run: run like a normal Python script. The images will be placed in the same folder, as will a
# log. One of the first things the software will do is try to create a log file. If it cannot
# create a log file, check your folder permissions & storage space.
# Once the script is done, print the new images to have your copies!

#REQUIREMENTS: Python and a valid installation of PIL or Pillow (Python Imaging Library successor)
#!!!DEPENDING ON THE SYSTEM, PILLOW MAY REQUIRE INSTALLATION OF EXTERNAL LIBRARIES FOR PROCESSING!!
# Target Python version: 2.7.10, with potential bolt-on support for Python 3.4.
# Target OS: Windows 8.1 and OS X 10.10. Compatibility with Windows 7, 8, & 10 as well as versions
# of OS X from 10.6 to 10.11 is highly likely, so long as Python is installed correctly.
# The version of Pillow used to run this tool is listed below.

#ORIGINAL BUILD DATE
# 11 August 2015, with progressive updates throughout the following month.
# Tweaked for presentation & uploaded originally on 8 Oct 2015

#Python extensions installed during development (only Pillow should be required):
# altgraph (0.12)
# macholib (1.7)
# modulegraph (0.12.1)
# pexpect (3.1)
# Pillow (2.9.0)
# pip (7.1.0)
# py2app (0.9)
# setuptools (15.2)
# virtualenv (13.1.0)


import glob
import time
import math
from PIL import Image

desiredLetterWidth = 6*850
desiredLetterHeight = 6 * 1100
singlePicturePortraitWidth = int(40*desiredLetterWidth/85)
singlePicturePortraitHeight = int(60*desiredLetterHeight/110)
print("Target resolution: " + str(desiredLetterWidth) + "*" + str(desiredLetterHeight))

#left,upper,right,lower
imBoxUpperLeft = (10,10)
imBoxUpperRight = (20+singlePicturePortraitWidth,10)
imBoxLowerMid = (10,10+singlePicturePortraitHeight+10)

#rotates CCW by 90 degrees. returns rotated image.
def rotateImage90Deg(imageToRotate):
    return imageToRotate.rotate(90)

#determine if a picture's orientation is portrait. If False, is square or landscape. Else true.
def pictureIsPortrait(imageToAnalyze):
    width,height = imageToAnalyze.size
    if(width > height):
        return False

#resize a picture for use in lower landscape slot
#use AFTER the picture is in the correct orientation
def resizeForLandscape(imageToFix):
    width,height = imageToFix.size
    applicableRatio = min((float(singlePicturePortraitHeight)/float(width)), (float(singlePicturePortraitWidth)/float(height)))
    return imageToFix.resize((int(applicableRatio*width),int(applicableRatio*height)))
    
#resize a picture for use in the upper "portrait" slots
#use AFTER the picture is in the correct orientation
def resizeForPortrait(imageToFix):
    (widthM,heightM) = imageToFix.size
    applicableRatio = min(float(singlePicturePortraitWidth)/float(widthM), float(singlePicturePortraitHeight)/float(heightM))
    return imageToFix.resize((int(applicableRatio*widthM),int(applicableRatio*heightM)))

#prepares pictures for use in either of the upper two "portrait" slots
def analyzeAndFixUpper(imageToFix):
    if(not pictureIsPortrait(imageToFix)):
        imageToFix = rotateImage90Deg(imageToFix)
    return resizeForPortrait(imageToFix)

#prepares pictures for use in the lower "landscape" slot
def analyzeAndFixLower(imageToFix):
    if(pictureIsPortrait(imageToFix)):
        imageToFix = rotateImage90Deg(imageToFix)
    return resizeForLandscape(imageToFix)
    
def pasteIntoImage(background,imageToPaste,position):
    if(position == "upperleft"):
        background.paste(imageToPaste,imBoxUpperLeft)
    elif(position == "upperright"):
        background.paste(imageToPaste,imBoxUpperRight)
    elif(position == "lower"):
        background.paste(imageToPaste,imBoxLowerMid)
    else:
        print("cannot place; invalid position defined")

def main():
    localtime = time.localtime(time.time())
    friendlyTime = str(localtime.tm_year) + "-" + str(localtime.tm_mon) + "-" + str(localtime.tm_mday) + "-" + str(localtime.tm_hour) + "-" + str(localtime.tm_min) + "-" + str(localtime.tm_sec)
    logFile = None
    try:
        logFile = open(str("log"+friendlyTime+".txt"),'w')
    except IOError:
        print("No logging. Program may not succeed. (Do you have permission to write here?)")
    fileNamesIn = glob.glob("*.jpg")
    fileNamesIn.extend(glob.glob("*.JPG"))
    copiesOfEach = 0
    copiesOfEach = int(raw_input("How many copies of each would you like to use? (1 or more): "))
    print("You entered " + str(copiesOfEach))
    fileNames = []
    for x in range(0,copiesOfEach):
        fileNames.extend(fileNamesIn)
    print("lenfileNamesIn and lenfileNames" + str(len(fileNamesIn)) +"::"+ str(len(fileNames)))
    print("Num of copies: "+str(len(fileNames)/len(fileNamesIn))+".")
    if len(fileNames) < 2:
        print("not enough pictures found. exiting...")
    else:
        trimmedFileCount = len(fileNames) - (len(fileNames) % 3)
        for x in range(0,trimmedFileCount/3):
            try:
                filesIn = str((fileNames[(3*x)],fileNames[(3*x)+1],fileNames[(3*x)+2]))
                print(filesIn)
                if logFile != None: logFile.write(filesIn + "\n")
                background = Image.new("RGB", (desiredLetterWidth, desiredLetterHeight), "white")
                image1 = Image.open(fileNames[(3*x)])
                image2 = Image.open(fileNames[(3*x)+1])
                image3 = Image.open(fileNames[(3*x)+2])
                pasteIntoImage(background, analyzeAndFixUpper(image1), "upperleft")
                pasteIntoImage(background, analyzeAndFixUpper(image2), "upperright")
                pasteIntoImage(background, analyzeAndFixLower(image3), "lower")
                outfileName = "4x6toLetter"+friendlyTime+"{:0>2d}".format(x+1)+".jpg"
                print("__cluster saved to... " + outfileName)
                if logFile != None: logFile.write(outfileName + "\n")
                background.save(outfileName)
            except IOError:
                pass
        if(len(fileNames)%3 == 0):
            print("No files missed!")
            if logFile != None: logFile.write("No files missed!\n")
        elif((len(fileNames)-2)%3 == 0):
            print("Two files missed; putting these files into one final collage:")
            if logFile != None: logFile.write("Two files missed; putting these files into one final collage:\n")
            finalFilesIn = str(fileNames[len(fileNames)-2])+", "+str(fileNames[len(fileNames)-1])
            if logFile != None: logFile.write(finalFilesIn+"\n")
            try:
                background = Image.new("RGB", (desiredLetterWidth, desiredLetterHeight), "white")
                image1 = Image.open(fileNames[len(fileNames)-2])
                image2 = Image.open(fileNames[len(fileNames)-1])
                pasteIntoImage(background, analyzeAndFixUpper(image1), "upperleft")
                pasteIntoImage(background, analyzeAndFixUpper(image2), "upperright")
                outfileName = "4x6toLetter"+friendlyTime+"{:0>2d}".format(0)+".jpg"
                print("__cluster saved to... " + outfileName)
                if logFile != None: logFile.write(outfileName + "\n")
                background.save(outfileName)
            except IOError:
                pass
        else:
            print("One file missed; putting it onto one final collage:")
            if logFile != None: logFile.write("One file missed; putting it onto one final collage:"+"\n")
            print(str(fileNames[len(fileNames)-1]))
            if logFile != None: logFile.write(str(fileNames[len(fileNames)-1])+"\n")
            try:
                background = Image.new("RGB", (desiredLetterWidth, desiredLetterHeight), "white")
                image1 = Image.open(fileNames[len(fileNames)-1])
                pasteIntoImage(background, analyzeAndFixLower(image1), "lower")
                outfileName = "4x6toLetter"+friendlyTime+"{:0>2d}".format(0)+".jpg"
                print("__cluster saved to... " + outfileName)
                if logFile != None: logFile.write(outfileName + "\n")
                background.save(outfileName)
            except IOError:
                pass
        
        if logFile != None:
            try:
                print("Saving list of successfully processed files to logfile.")
                logFile.write("\n\n Files processed: \n")
                for file in fileNames:
                    logFile.write(file + " [*] ")
                logFile.close()
            except IOError:
                pass
        print("Collage creation complete!")
    
if __name__ == "__main__":
    main()
