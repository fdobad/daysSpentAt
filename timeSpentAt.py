import sys,getopt,code
from json import loads
from datetime import timedelta,datetime
from dateutil import tz
from math import radians, cos, sin, asin, sqrt
from timeit import default_timer as timer
def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km

def timeSpentAt(location,distance,inputjson,output,verbose):
    
    fr=open(inputjson,'r')
    thejson=loads(fr.read())
    jsonsize=len(thejson['locations'])
    
    fw=open(output,'w')
    fw.write('Year,Month,Day,EarliestTime,LatestTime,TotalSeconds,Hours,Minutes,Seconds\n')
    
    stillIndexes=[]
    cumdur=timedelta(0,0,0)
    latest=None
    boolSetLatest=True
    for i in range(jsonsize):
        try:
            if thejson['locations'][i]['activity'][0]['activity'][0]['type'] == 'STILL' and \
                haversine(*location,thejson['locations'][i]['latitudeE7']/10000000,thejson['locations'][i]['longitudeE7']/10000000)<=distance:

                stillIndexes.append(i)
    
                if len(stillIndexes)>1:
                    a=datetime.fromtimestamp(float(thejson['locations'][stillIndexes[-1]]['activity'][0]['timestampMs'])/1000)
                    b=datetime.fromtimestamp(float(thejson['locations'][stillIndexes[-2]]['activity'][0]['timestampMs'])/1000)
                    if a.day != b.day:
                        mm,ss=divmod(cumdur.days * 86400 + cumdur.seconds, 60)
                        hh,mm=divmod(mm,60)
                        if verbose: print('Still found: {!s},{!s},{!s},{!s},{!s},{!s},{!s},{!s},{!s}\n'.format( \
                                b.year,b.month,b.day,b.time(),latest.time(),cumdur.seconds,hh,mm,ss))
                        #code.InteractiveConsole(locals=locals()).interact()
                        fw.write('{!s},{!s},{!s},{!s},{!s},{!s},{!s},{!s},{!s}\n'.format( \
                                b.year,b.month,b.day,b.time(),latest.time(),cumdur.seconds,hh,mm,ss))
                        cumdur=timedelta(0,0,0)
                        boolSetLatest=True
                    else:
                        cumdur+=b-a
                        if boolSetLatest:
                            latest=a
                            boolSetLatest=False
        except KeyError: 
            pass
    
    fr.close()
    fw.close()

#def statistics(output):
#   TODO great statistics and plots
#    df=read_csv(output, delimiter=',')
#    print(df.describe())
#    pandas_profiling.ProfileReport(df)
#    code.InteractiveConsole(locals=locals()).interact()

def usage():
    print('Hello there! more docs at https://github.com/fdobad/daysSpentAt\n\
Options:\n\
    -v or --verbose to print each time a day is registered\n\
    -l or --location Location must be a two floats separated by ",", example -l -33.8068463,-70.0247826\n\
    -d or --distance must be a float in meters, defining the circle around the location -l 0.25 \n\
    -i or --input is the json to read, defaults to "Location History.json" \n\
    -o or --output is the csv to write, defaults to "output.csv" \n\
Please feel free to change line 20 of this script from 6371 to 3959 to use freedom units...')
    sys.exit(2)

def main():
    start = timer()
    print("timer init")
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:l:d:o:v", ["help", "input=", "location=", "distance=", "output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        print('wtf')
        sys.exit(2)
    # place your default values here
    inputjson = 'Location History.json' 
    output = 'output.csv'
    location = (-33.4275076,-70.6172828)#(-33.8068463,-70.0247826) #
    distance = 0.25
    verbose=False
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-i", "--input"):
            inputjson = a
        elif o in ("-l", "--location"):
            if a.index(',')!=-1:
                location=tuple(map(float,a.split(',')))
            else:
                print('Location must be a two floats separated by ",", example -l -33.8068463,-70.0247826')
                usage()
                sys.exit()
        elif o in ("-d", "--distance"):
            try:
                distance = float(a)
            except ValueError:
                print('Distances must be a float (in meters), using default '+default)
                usage()
                sys.exit()

        elif o in ("-o", "--output"):
            output = a
        else:
            assert False, "unhandled option"
    print('Using these parameters: ',location,distance,inputjson,output,verbose)
    timeSpentAt(location,distance,inputjson,output,verbose )
    #statistics(output)
    print('timer: that took %s seconds'%(timer() - start))

if __name__ == "__main__":
    main()
