function initial(detect, log, stream, record, jalert){
    document.getElementById("detection").value = detect;
    document.getElementById("loglvl").value = log;
    document.getElementById("streaming").value = stream;
    document.getElementById("recording").value = record;
    document.getElementById("alerting").value = jalert;
}
function returnLive(){
    document.getElementById("fluximage").style.display = "block";
    document.getElementById("fluximage").src = "{{ url_for('video_feed') }}"
    location.reload();
}
function fvideo(event){
    const newsrc = event.src.substring(0,event.src.lastIndexOf("."))
    document.getElementById("fluxvideo").style.display = "block";
    document.getElementById("fluximage").style.display = "none";
    document.getElementById("fluxvideo").src = newsrc + ".avi";

}