
"""

  ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  +                                                                                                                      +   
  +  Weather Comparison Project for the Astro Pi Competition                                                             +
  +                                                                                                                      +
  +  This has been written by Nicole Ashworth for the Astro Pi competition, 2015.                                        +
  +  This program is designed to compare the average weather of England with the Interntional Space Station.             +
  +  The average weather file is from Heathrow airport of the year 2014.                                                 +
  +                                                                                                                      +
  +  Originally, the program was going to take the temperature and humidity from the Astro Pi sensors                    +
  +  but the board got hot and the sensor picked up the heat of the board                                                +
  +  and the humidity was not included in the file we found of average weather.                                          +
  +  It was going to give the number of rainy days missed, but there is no specific date of takeoff so it was not done.  +
  +                                                                                                                      +
  +  Author : Nicole Ashworth                                                                                            +
  +  Date   : 24/05/2015                                                                                                 +
  +                                                                                                                      +
  ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  
"""


#import everything needed
import csv                      #this is to read the delimited file
import datetime                 #this is to use the correct date in the comparison from the file to ISS
from astro_pi import AstroPi    #this is to be able to use the sensors and board on the Astro Pi
from time import sleep, time    #this is to be able to make the code wait when it is needed to
from random import randint      #this is to be able to generate a random greeting/goodbye from the list


#value for looping through text file
find_match = 0 #this is used when looping through the file so that it stops looking when a match is found


#columns in text file
dayColumn = 1 #the column number of the day column
tempColumn = 2 #the column number of the temperature column
rainColumn = 6 #the column number of the rainfall column
cloudColumn = 4 #the column number of the cloud cover column


#Arrays to read data into
dayArr = [] #the array to put the days into
avTempArr = [] #the array to put the temperatures into
avRainArr = [] #the array to put the rainfall data into
avCloudArr = [] #the array to put the cloud cover data into


#initiate AstroPi
ap = AstroPi()


#filenames
iconFileName = ""
sunPng= "sun.png" #this is the sunny weather icon
cloudPng = "cloud.png" #this is the cloudy weather icon
sunCloudPng = "sunncloud.png" #this is the sunny/cloudy weather icon
lightRainPng = "light rain.png" #this is the light rain weather icon
heavyRainPng = "heavy rain.png" #this is the heavy rain weather icon
pngPath = "./" #this is the path to the icons relative to this script


#weather range values
valueSun = 3 #less than 3 hours cloud therefore sunny
valueCloudSun = 5 #between valueSun and valueCloudSun then cloudy/sunny
NoRain = 1 #less than 1 then no rain
LightRain = 10 # more than this is heavy rain otherwise light rain


#message arrays
goodbyes = ['Bye bye!', 'Have a great day!', 'See you soon!', 'Goodbye Tim!'] #the list of goodbye messages that can be chosen
greetings = ['Hi Tim!', 'How are you, Tim?', 'Howdy Tim!', 'Hello Tim!', 'Hey there Tim!'] #the list of greetings that can be chosen


#choose random message
def pickMessage(messages):
    num_messages = len(messages)
    num_picked = randint(0, num_messages - 1)
    message_picked = messages[num_picked]
    return message_picked   


#Greet Tim
ap.show_message(pickMessage(greetings)) #display a random greeting


#set up date/time
now = datetime.datetime.now() #the current date
thisday = now.strftime("%m-%d") #the current month and day


#take stats from station
StationTemp = 24 #We would get from sensor but Pi board gets hot so not accurate


#sort day and temperature into array
day = []
avTemp = []


#open file and read in the values for each column
with open('./heathrowWeather2014.tsv') as csvfile:
    csvReader = csv.reader(csvfile, delimiter="\t")
    for row in csvReader:
        dayArr.append(row[dayColumn])
        avTempArr.append(row[tempColumn])
        avRainArr.append(row[rainColumn])
        avCloudArr.append(row[rainColumn])
        

#read data
for chosen in dayArr:
    if chosen == thisday: #if the date in the row matches the current month and day
        avTemp = round(float(avTempArr[find_match]),1)
        avRain = round(float(avRainArr[find_match]),1)
        avCloud = round(float(avCloudArr[find_match]), 1)
        break
    find_match = find_match + 1 #add one so it checks the next row 
    

#print temp data
tempDiff = round(StationTemp - avTemp,1)
ap.show_message("The likely UK temp is %sC" % avTemp)
if tempDiff < 0:
    ap.show_message("ISS is %sC colder" % tempDiff,text_colour=[0, 0, 255]) #display the difference in blue if ISS is colder
else:
    ap.show_message("ISS is %sC warmer" % tempDiff,text_colour=[255, 0, 0]) #display the difference in red if ISS is warmer
ap.clear()


#compare the values and set the icon 
if avRain < NoRain: #if there is no rain
    if avCloud < valueSun: #if it is sunny
        iconFileName = sunPng
    elif valueSun >= avCloudArr < valueCloudSun: #if it is cloudy
        iconFileName = cloudPng
    else:   #otherwise it is sunny/cloudy
        iconFileName = suncloudPng
elif avRain <= LightRain: #if there is light rain
    iconFileName = lightRainPng
else:       #otherwise it is heavy rain
    iconFileName = heavyRainPng
    

iconFileName= pngPath + iconFileName #add the correct icon file name onto the path to the icons folder


#display end icon
ap.show_message("Likely weather") #display the words 'Likely weather'
ap.load_image(iconFileName) #display the icon image 
sleep(2) #keep displaying the image for 2 seconds


#say goodbye
ap.show_message(pickMessage(goodbyes)) #display a random goodbye message
