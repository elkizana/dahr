from flask import Flask
from flask import render_template
import datetime, ephem
from datetime import timedelta
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def Main():
    return render_template('index.html' )

myLocation = ephem.Observer()
myLocation18 = ephem.Observer()


@app.route('/Times')
def Times():
    lat, lng, date, elevation, horizon = request.args.get('lat'), request.args.get('lng'), request.args.get('date'), request.args.get('elevation'), request.args.get('horizon')
    
    myLocation.date , myLocation.lon , myLocation.lat , myLocation.elev  , myLocation.horizon = str(date) , lng ,  lat , int(elevation) , "0"  
    myLocation18.date , myLocation18.lon , myLocation18.lat , myLocation18.elev  , myLocation18.horizon = str(date) , lng ,  lat , int(elevation) , "-18"  
    now = datetime.datetime.now()   
    next_sunrise = ephem.localtime(myLocation.next_rising(ephem.Sun(), use_center=True) )
    prev_sunrise = ephem.localtime(myLocation.previous_rising(ephem.Sun(), use_center=True) )
    next_noon  = ephem.localtime( myLocation.next_transit(ephem.Sun() )   )
    prev_noon  = ephem.localtime( myLocation.previous_transit(ephem.Sun() )   )
    next_sunset = ephem.localtime(myLocation.next_setting(ephem.Sun(), use_center=False)  )
    prev_sunset = ephem.localtime(myLocation.previous_setting( ephem.Sun(), use_center=False) )
    icha = ephem.localtime(myLocation18.next_setting(ephem.Sun(), use_center=False)  )
    
    half_night = next_sunrise - ( next_sunrise - next_sunset) /  2  
    
    fadjr  = ephem.localtime(myLocation18.next_rising(ephem.Sun(), use_center=False)  )

    whole_time = next_sunset.timestamp() - prev_sunset.timestamp()
    night_time = next_sunrise.timestamp() - prev_sunset.timestamp()
    day_time = next_sunset.timestamp() - prev_sunrise.timestamp()

    asr =  next_sunset - ((next_sunset - prev_sunrise )/ 4 )


    listOftimes = {"sunset" : next_sunset ,"half_night" : half_night , "icha" : icha , "fadjr" : fadjr , "sunrise" : next_sunrise  , "next_noon" : next_noon , "asr" : asr   }
    listOftimes =  dict(sorted(listOftimes.items(), key=lambda item: item[1]))   
    listOftimes = {k:v for k, v in listOftimes.items() if v > now}

    next_time = next(   iter(listOftimes)  )
    if  next_time == "icha" or next_time == "sunrise"  or next_time == "half_night" or next_time == "fadjr" :
        elapsed_night_time =  now.timestamp() - prev_sunset.timestamp()
        percent  = (elapsed_night_time / night_time ) * 50 
        return jsonify(next_sunrise=next_sunrise,next_noon=next_noon,asr=asr,next_sunset=next_sunset,next_icha=icha,half_night=half_night,fadjr=fadjr,percent=percent ,next_time=next_time,night=True  )    
    else :
        elapsed_day_time = now.timestamp() - prev_sunrise.timestamp()
        percent = (elapsed_day_time /  day_time) * 50 + 50 
        return jsonify(next_sunrise=next_sunrise,next_noon=next_noon,asr=asr,next_sunset=next_sunset,next_icha=icha,fadjr=fadjr,percent=percent ,next_time=next_time,day=True  )    

  
app.run(debug=True)



if __name__ == '__main__':
    app.run()




""" 
  if next_salat == "sunrise"  :
        elapsed_night =  now.timestamp() - prev_sunset.timestamp()
        night_degree =  (elapsed_night / night_time ) * 180 

        return jsonify(next_sunrise=next_sunrise,noon=noon,next_sunset=next_sunset,night_degree=night_degree ,next_salat=next_salat,night=True  )    
    else :
        elapased_day = now.timestamp() - prev_sunrise.timestamp()
        day_degree = (elapased_day /  day_time) * 180
        return jsonify(next_sunrise=next_sunrise,noon=noon,next_sunset=next_sunset,day_degree=day_degree ,next_salat=next_salat,day=True)    
     """