function initial(detect, log, stream, record, jalert){
    document.getElementById("detection").value = detect;
    document.getElementById("loglvl").value = log;
    document.getElementById("streaming").value = stream;
    document.getElementById("recording").value = record;
    document.getElementById("alerting").value = jalert;
}

function image(event){
    document.getElementById("fluxvideo").style.display = "none";
    document.getElementById("fluximage").style.display = "block";
    document.getElementById("fluximage").src = event.src;

}
function returnLive(){
    document.getElementById("fluximage").style.display = "block";
    document.getElementById("fluximage").src = "{{ url_for('video_feed') }}"
    location.reload();
}
function fvideo(event){
    document.getElementById("fluxvideo").style.display = "block";
    document.getElementById("fluximage").style.display = "none";
    document.getElementById("fluxvideo").src = event.src;

}