- [daysSpentAt](#daysspentat)
    - [Introduction](#introduction)
    - [Make it work](#make-it-work)
    - [Short tutorial to download Google Location History](#short-tutorial-to-download-google-location-history)
# daysSpentAt
## Introduction
Want to know when and how much time per day you spent on a location? Try this simple python parser of Google routes or timeline location takeout.json `Location History.json` (whatever is called now).

For example if you want to know how much time you spend sitting at your office desk at work per day, this is the simplest tool to get a csv file to get some statistics out of it.

*This script parses my 10.117.690... that's 10 million lines json (of 2 years data) in 6 seconds so it's not something you wanna do by hand or import directly in Excel...*

The `output.csv` has the following header:

``Year,Month,Day,EarliestTime,LatestTime,TotalSeconds,Hours,Minutes,Seconds``

After running this script you'll get the `TotalSeconds` accumulated for each day that Google marked a `Still` activity inside the location circle read as a command line input. (Meaning you have to provide a (lat,long) and distance, to make it work)

Also `EarliestTime` and `LatestTime` are humanly formatted (hh:mm:ss) to get a hang of when you started and stopped being there. Same for `Hours,Minutes,Seconds` that is the human traslation of `TotalSeconds`. Finally `Year,Month,Day` are integers to make it easy for pivot table programs without messing with timestamps.

## Make it work
0. You'll need python3
1. Place this script on your PC, download or clone:

`git clone https://github.com/fdobad/daysSpentAt`

2. Download your Google location history json and put it next to the script. *It's **very likely** you activated the location history setting when installing or using any app, like googlemaps... Detailed instructions at the bottom of this [page](#short-tutorial-to-download-google-location-history).*
3. Basic run example:

`python timeSpentAt.py -l -33.8068463,-70.0247826 -d 0.25`

*That's all folks! The default uses `-i Location History.json` and `-o output.csv`*

Or get basic help: 

`python timeSpentAt.py -h`

TODO better help...

TODO use a pandas dataframe to plot things and get kpi's

## Short tutorial to download Google Location History
TODO insert images
1. Go to googlemaps, log in
2. Select the (hamburguer) Menu icon, left of the search bar
3. Scroll to 'Your timeline', select
4. On the timeline map view, on the bottom right corner, select the (cog) configure icon
5. Select 'Download a copy of all your data'
6. On the 'Select data to include' make sure you're just selecting 'Location History':
 
        6.a. Select 'SELECT NONE' button
        6.b. Activate 'Location History' switch 
        6.c. Select 'NEXT' button
7. Select 'CREATE ARCHIVE'
8. Follow the directions and put the extracted file probably named 'Location History.json' on the same folder as this script.