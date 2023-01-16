
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
     //console.log( pythonResponse["next_time"] )

       $("#panel").html( moment.utc().local().format(' YYYY-MM-DD HH:mm:ss') + "<br>" );
     
      for( key in pythonResponse) {
        $("#panel").append(  key  + " : " + pythonResponse[key] + "<br>") 
        }

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
            $("#night_last_third , #fajr  ").addClass("active")   
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




  