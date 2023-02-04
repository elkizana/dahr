
setInterval(updateTimes, 1000)

function updateTimes() {   

$.getJSON('/Times', {
  lat : "36.805069" ,  //event.latLng.lat(),
  lng : "3.041835"  ,  //event.latLng.lng(), 
  //date : moment.utc().local().format('YYYY-MM-DD HH:mm:ss'),
  date : moment.utc().format('YYYY-MM-DD HH:mm:ss'),
  elevation : "35" , //document.getElementsByName("elevation")[0].value,
  horizon : 0  //document.getElementsByName("horizon_selection")[0].value ,
}, function(pythonResponse) {
    let percent =  pythonResponse["percent"]
       console.log( moment( pythonResponse["last_third"] ).utc().format('YYYY-MM-DD HH:mm:ss') )

       $("#panel").html(    moment().format("YYYY/M/D h:mm:ss")    + "<br>" );
       $("#panel").append(  "الفجر" + " : "  + moment( pythonResponse["fadjr"] ).utc().format('HH:mm:ss')  +  "<br>"    )  
       $("#panel").append(  " الطلوع" + " : "  + moment( pythonResponse["sunrise"] ).utc().format('HH:mm:ss') +  "<br>"    )  
       $("#panel").append(  "نصف النهار" + " : "  + moment( pythonResponse["noon"] ).utc().format('HH:mm:ss')  +  "<br>"    )  
       $("#panel").append(  "العصر" + " : "  + moment( pythonResponse["asr"] ).utc().format('HH:mm:ss')  +  "<br>"    )  

       $("#panel").append(  "المغرب" + " : "  + moment( pythonResponse["maghreb"] ).utc().format('HH:mm:ss') +  "<br>"    )  

       $("#panel").append(  "العشاء" + ":"  + moment( pythonResponse["icha"] ).utc().format('HH:mm:ss') +  "<br>"    )  
       $("#panel").append(  "نصف الليل" + " : "  + moment( pythonResponse["half_night"] ).utc().format('HH:mm:ss')  +  "<br>"    )  
       $("#panel").append(  "الثلث الآخر" + " : "  + moment( pythonResponse["last_third"] ).utc().format('HH:mm:ss')  +  "<br>"    )  

       pythonResponse["shadow"] != 0 ? $("#panel").append(  "الظل" + " : "  +  pythonResponse["shadow"]  +  "<br>"    )   :  null    
       $("#panel").append(  "بقي" + " : "  + pythonResponse["remaining"]  +  "<br>"    )  
       
       $("#sunset_time").html(moment( pythonResponse["sunset"] ).utc().format('HH:mm:ss'))
       $("#icha_time").html(moment( pythonResponse["icha"] ).utc().format('HH:mm:ss'))

       $("#half_night_time").html(moment( pythonResponse["half_night"] ).utc().format('HH:mm:ss'))
       $("#last_third_time").html(moment( pythonResponse["last_third"] ).utc().format('HH:mm:ss'))

       $("#fadjr_time").html(moment( pythonResponse["fadjr"] ).utc().format('HH:mm:ss'))
       $("#sunrise_time").html(moment( pythonResponse["sunrise"] ).utc().format('HH:mm:ss'))

      $("#noon_time").html(moment( pythonResponse["noon"] ).utc().format('HH:mm:ss'))
      $("#asr_time").html(moment( pythonResponse["asr"] ).utc().format('HH:mm:ss'))


        
     
     /*    for( key in pythonResponse) {
        $("#panel").append(  key  + " : " + pythonResponse[key] + "<br>") 
        } 
 */
        let progressCircle = document.querySelector(".progress");
        let radius = progressCircle.r.baseVal.value;
        let circumference = radius * 2 * Math.PI;
        progressCircle.style.strokeDasharray = circumference;
        
        setProgress(percent ) 

        switch (pythonResponse["next_time"] )   { 
          case "icha" :
            $(".lines").removeClass("active")
            $("#sunset  , #icha").addClass("active")  
          break 
          case "half_night" :
            $(".lines").removeClass("active")
            $("#icha  , #half_night").addClass("active")  
          break 
          case "fadjr" :
            $(".lines").removeClass("active")
            $("#night_last_third , #sunrise  ").addClass("active")   
          break 
          case "sunrise" :
            $(".lines").removeClass("active")
            $("#fadjr  , #sunrise").addClass("active")  
          break 
          case "noon" :
            $(".lines").removeClass("active")
            /* $("#noon  , #asr").addClass("active")   */
          break 
          case "asr" :
            $(".lines").removeClass("active")
            $("#noon  , #asr").addClass("active")  
          break 
          case "sunset" :
            $(".lines").removeClass("active")
            $("#asr  , #sunset").addClass("active")  
          break 
          
          default : 
          console.log("nooonneee")

        }

        function setProgress(percent) {
            progressCircle.style.strokeDashoffset = circumference - (percent / 100) * circumference;
        }
             

}
        );

      }

updateTimes()




  