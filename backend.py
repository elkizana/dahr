from flask import Flask
from flask import render_template
import datetime, ephem , math
from datetime import timedelta
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

myLocation = ephem.Observer()
myLocation18 = ephem.Observer()

@app.route('/')
def Main():
    return render_template('index.html' )

@app.route('/Times')
def Times():
    lat, lng, date, elevation = request.args.get('lat'), request.args.get('lng'), request.args.get('date'), request.args.get('elevation')
    
    myLocation.date , myLocation.lon , myLocation.lat , myLocation.elev  , myLocation.horizon = str(date) , lng ,  lat , int(elevation) , "0"  
    myLocation18.date , myLocation18.lon , myLocation18.lat , myLocation18.elev  , myLocation18.horizon = str(date) , lng ,  lat , int(elevation) , "-18"  
    now = datetime.datetime.now()  

    fadjr  = ephem.localtime(myLocation18.next_rising(ephem.Sun(), use_center=False)  )
    
    next_sunrise = ephem.localtime(myLocation.next_rising(ephem.Sun(), use_center=True) )
    prev_sunrise = ephem.localtime(myLocation.previous_rising(ephem.Sun(), use_center=True) )
    
    next_noon  = ephem.localtime( myLocation.next_transit(ephem.Sun() )   )
    prev_noon  = ephem.localtime( myLocation.previous_transit(ephem.Sun() )   )
    
    next_sunset = ephem.localtime(myLocation.next_setting(ephem.Sun(), use_center=True)  )
    prev_sunset = ephem.localtime(myLocation.previous_setting( ephem.Sun(), use_center=True) )
    
    
    
    whole_time = next_sunset.timestamp() - prev_sunset.timestamp()


    if ephem.Sun(myLocation).alt <  0 :
        day_time = next_sunset.timestamp() - next_sunrise.timestamp()
        night_time = next_sunrise.timestamp() - prev_sunset.timestamp()
        half_night = prev_sunset + (next_sunrise - prev_sunset) / 2 
        shadow = "لا ظل"

        #print("night")
    else :
        #print('day')
        day_time = next_sunset.timestamp() - prev_sunrise.timestamp()
        night_time = next_sunrise.timestamp() - next_sunset.timestamp()
        half_night = next_sunset + (next_sunrise - next_sunset) / 2 
        shadow = (1  / math.tan(ephem.Sun(myLocation).alt))  

    
    asr = datetime.datetime.fromtimestamp( next_sunset.timestamp() -  11.6861800697 / 50 * day_time)
    maghreb = ephem.localtime(myLocation.next_setting( ephem.Sun(), use_center=False) )
    icha = ephem.localtime(myLocation18.next_setting(ephem.Sun(), use_center=False)  )

    
    

    listOftimes = {"sunset" : next_sunset , "maghreb" : maghreb  , "icha" : icha , "half_night" : half_night , "fadjr" : fadjr , "sunrise" : next_sunrise  , "noon" : next_noon , "asr" : asr   }
    listOftimes =  dict(sorted(listOftimes.items(), key=lambda item: item[1]))   
    listOftimes = {k:v for k, v in listOftimes.items() if v > now}
    
    next_time = next(   iter(listOftimes)  )
    listOftimes["next_time"] = next_time
    listOftimes["shadow"] = shadow
    print(next_time)
    
    if  next_time == "icha" or next_time == "sunrise"  or next_time == "half_night" or next_time == "fadjr" :
        elapsed_night_time =  now.timestamp() - prev_sunset.timestamp()
        half_night = datetime.datetime.fromtimestamp( prev_sunset.timestamp() +  night_time / 2 )
        listOftimes["percent"]   = (elapsed_night_time / night_time ) * 50 
        return listOftimes
    else :
        elapsed_day_time = now.timestamp() - prev_sunrise.timestamp()
        listOftimes["percent"] = (elapsed_day_time /  day_time) * 50 + 50
        #print(listOftimes)
        return listOftimes 
       
  
app.run(debug=True)



if __name__ == '__main__':
    app.run()






"""
        shadow _ of asr 16/01 : :: 2.582816646707519
    icha ::  5.454546421705379
    nisf  :: 50.00
    fadjr :: 44.4439564315093
    last_third : 33.3333333333
     asr :::: 38.31381993034258 ::: 11.6861800697  :: 88.3138199303
     MAGHREB :::: 0.10901532014220014   ::: 0.21803063656961422
    
    """